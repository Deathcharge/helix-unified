#!/bin/bash

# 🌊 Helix Unified - Enhanced Deployment Automation
# One-command deployment with health checks, rollback, and monitoring
# Usage: ./scripts/deploy-helix.sh [production|staging] [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT="${1:-production}"
SKIP_TESTS="${SKIP_TESTS:-false}"
SKIP_BUILD="${SKIP_BUILD:-false}"
AUTO_ROLLBACK="${AUTO_ROLLBACK:-true}"
DEPLOY_TIMEOUT=300 # 5 minutes

echo -e "${CYAN}🌊 Helix Unified - Enhanced Deployment${NC}"
echo -e "${CYAN}======================================${NC}"
echo -e "Environment: ${MAGENTA}$ENVIRONMENT${NC}"
echo -e "Auto-rollback: ${MAGENTA}$AUTO_ROLLBACK${NC}\n"

# Function: Check prerequisites
check_prerequisites() {
    echo -e "${BLUE}📋 Checking prerequisites...${NC}"

    # Check Railway CLI
    if ! command -v railway &> /dev/null; then
        echo -e "${RED}❌ Railway CLI not found${NC}"
        echo "Install: curl -fsSL https://railway.app/install.sh | sh"
        exit 1
    fi

    # Check if logged in
    if ! railway whoami &> /dev/null; then
        echo -e "${RED}❌ Not logged in to Railway${NC}"
        echo "Run: railway login"
        exit 1
    fi

    # Check git status
    if [[ -n $(git status -s) ]]; then
        echo -e "${YELLOW}⚠️  Uncommitted changes detected${NC}"
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    echo -e "${GREEN}✅ Prerequisites OK${NC}\n"
}

# Function: Run tests
run_tests() {
    if [ "$SKIP_TESTS" = "true" ]; then
        echo -e "${YELLOW}⚠️  Skipping tests (SKIP_TESTS=true)${NC}\n"
        return 0
    fi

    echo -e "${BLUE}🧪 Running tests...${NC}"

    # Backend tests
    echo "  Backend tests..."
    if pytest tests/ -v --tb=short --timeout=30; then
        echo -e "${GREEN}  ✅ Backend tests passed${NC}"
    else
        echo -e "${RED}  ❌ Backend tests failed${NC}"
        return 1
    fi

    # Frontend tests (if package.json exists)
    if [ -f "frontend/package.json" ]; then
        echo "  Frontend tests..."
        cd frontend
        if npm test -- --watchAll=false --passWithNoTests; then
            echo -e "${GREEN}  ✅ Frontend tests passed${NC}"
        else
            echo -e "${RED}  ❌ Frontend tests failed${NC}"
            cd ..
            return 1
        fi
        cd ..
    fi

    echo -e "${GREEN}✅ All tests passed${NC}\n"
}

# Function: Build locally (optional)
build_locally() {
    if [ "$SKIP_BUILD" = "true" ]; then
        echo -e "${YELLOW}⚠️  Skipping local build${NC}\n"
        return 0
    fi

    echo -e "${BLUE}🔨 Building locally...${NC}"

    # Build frontend
    if [ -f "frontend/package.json" ]; then
        echo "  Building frontend..."
        cd frontend
        if npm run build; then
            echo -e "${GREEN}  ✅ Frontend build successful${NC}"
        else
            echo -e "${RED}  ❌ Frontend build failed${NC}"
            cd ..
            return 1
        fi
        cd ..
    fi

    echo -e "${GREEN}✅ Local build successful${NC}\n"
}

# Function: Deploy to Railway
deploy_to_railway() {
    echo -e "${BLUE}🚀 Deploying to Railway ($ENVIRONMENT)...${NC}"

    # Get current deployment ID for rollback
    PREVIOUS_DEPLOYMENT=$(railway deployments | head -n 2 | tail -n 1 | awk '{print $1}')
    echo -e "  Previous deployment: ${CYAN}$PREVIOUS_DEPLOYMENT${NC}"

    # Deploy
    echo -e "\n  Pushing code to Railway..."
    if railway up; then
        echo -e "${GREEN}  ✅ Code pushed successfully${NC}"
    else
        echo -e "${RED}  ❌ Railway push failed${NC}"
        return 1
    fi

    # Wait for deployment
    echo -e "\n  ${YELLOW}⏳ Waiting for deployment to complete...${NC}"
    local elapsed=0
    local status=""

    while [ $elapsed -lt $DEPLOY_TIMEOUT ]; do
        status=$(railway status --json 2>/dev/null | grep -o '"status":"[^"]*"' | cut -d'"' -f4 || echo "unknown")

        if [ "$status" = "ACTIVE" ]; then
            echo -e "${GREEN}  ✅ Deployment successful!${NC}"
            return 0
        elif [ "$status" = "FAILED" ]; then
            echo -e "${RED}  ❌ Deployment failed${NC}"
            return 1
        fi

        echo -ne "  Status: $status (${elapsed}s)...\r"
        sleep 5
        elapsed=$((elapsed + 5))
    done

    echo -e "${RED}  ❌ Deployment timed out after ${DEPLOY_TIMEOUT}s${NC}"
    return 1
}

# Function: Health check
health_check() {
    echo -e "\n${BLUE}🏥 Running health checks...${NC}"

    local services=(
        "helix-backend-api"
        "helix-claude-api"
        "helix-dashboard"
        "helix-service-integration"
    )

    local failed_services=()

    for service in "${services[@]}"; do
        echo -n "  Checking $service..."

        # Get service URL from Railway
        service_url=$(railway service $service env | grep RAILWAY_STATIC_URL | cut -d'=' -f2 2>/dev/null || echo "")

        if [ -z "$service_url" ]; then
            echo -e " ${YELLOW}⚠️  URL not found${NC}"
            continue
        fi

        # Check health endpoint
        if curl -f -s --max-time 10 "https://$service_url/health" > /dev/null 2>&1; then
            echo -e " ${GREEN}✅${NC}"
        else
            echo -e " ${RED}❌${NC}"
            failed_services+=("$service")
        fi
    done

    if [ ${#failed_services[@]} -eq 0 ]; then
        echo -e "${GREEN}✅ All services healthy${NC}\n"
        return 0
    else
        echo -e "${RED}❌ Failed services: ${failed_services[*]}${NC}\n"
        return 1
    fi
}

# Function: Rollback
rollback() {
    local deployment_id=$1
    echo -e "${YELLOW}🔄 Rolling back to deployment: $deployment_id${NC}"

    if railway rollback "$deployment_id"; then
        echo -e "${GREEN}✅ Rollback successful${NC}"
        return 0
    else
        echo -e "${RED}❌ Rollback failed - manual intervention required${NC}"
        return 1
    fi
}

# Function: Show deployment info
show_deployment_info() {
    echo -e "\n${CYAN}📊 Deployment Information${NC}"
    echo -e "${CYAN}========================${NC}"

    # Get service URLs
    echo -e "\n${BLUE}Service URLs:${NC}"
    railway env | grep RAILWAY_STATIC_URL || echo "  (Run 'railway env' to see URLs)"

    # Show recent deployments
    echo -e "\n${BLUE}Recent Deployments:${NC}"
    railway deployments | head -n 6

    # Show logs tail
    echo -e "\n${BLUE}Recent Logs:${NC}"
    railway logs --lines 20

    echo -e "\n${GREEN}🎉 Deployment complete!${NC}"
    echo -e "Monitor: ${CYAN}railway logs --follow${NC}"
    echo -e "Status:  ${CYAN}railway status${NC}"
    echo -e "Rollback: ${CYAN}railway rollback${NC}\n"
}

# Main deployment flow
main() {
    # Step 1: Prerequisites
    check_prerequisites

    # Step 2: Run tests
    if ! run_tests; then
        echo -e "${RED}❌ Tests failed - deployment aborted${NC}"
        exit 1
    fi

    # Step 3: Build locally (optional)
    if ! build_locally; then
        echo -e "${RED}❌ Build failed - deployment aborted${NC}"
        exit 1
    fi

    # Step 4: Deploy
    if ! deploy_to_railway; then
        echo -e "${RED}❌ Deployment failed${NC}"

        if [ "$AUTO_ROLLBACK" = "true" ] && [ -n "$PREVIOUS_DEPLOYMENT" ]; then
            echo -e "${YELLOW}Auto-rollback enabled - reverting...${NC}"
            rollback "$PREVIOUS_DEPLOYMENT"
        fi

        exit 1
    fi

    # Step 5: Health check
    if ! health_check; then
        echo -e "${RED}❌ Health checks failed${NC}"

        if [ "$AUTO_ROLLBACK" = "true" ] && [ -n "$PREVIOUS_DEPLOYMENT" ]; then
            echo -e "${YELLOW}Auto-rollback enabled - reverting...${NC}"
            rollback "$PREVIOUS_DEPLOYMENT"
        else
            echo -e "${YELLOW}⚠️  Deployment is live but some services are unhealthy${NC}"
        fi

        exit 1
    fi

    # Step 6: Show info
    show_deployment_info
}

# Handle script options
case "${2:-}" in
    --skip-tests)
        SKIP_TESTS=true
        ;;
    --skip-build)
        SKIP_BUILD=true
        ;;
    --no-rollback)
        AUTO_ROLLBACK=false
        ;;
    --help|-h)
        echo "Usage: $0 [production|staging] [options]"
        echo ""
        echo "Options:"
        echo "  --skip-tests     Skip running tests"
        echo "  --skip-build     Skip local build"
        echo "  --no-rollback    Disable automatic rollback on failure"
        echo "  --help, -h       Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 production                    # Full deployment with tests"
        echo "  $0 production --skip-tests       # Deploy without tests"
        echo "  $0 staging --no-rollback         # Deploy to staging, no rollback"
        echo ""
        echo "Environment variables:"
        echo "  SKIP_TESTS=true       Skip tests"
        echo "  SKIP_BUILD=true       Skip build"
        echo "  AUTO_ROLLBACK=false   Disable rollback"
        exit 0
        ;;
esac

# Run main deployment
main
