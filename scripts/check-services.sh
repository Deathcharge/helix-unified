#!/bin/bash

# 🌊 Helix Unified - Quick Service Health Check
# Checks health of all services and displays color-coded status
# Usage: ./scripts/check-services.sh [environment]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Environment (default to production)
ENV="${1:-production}"

echo -e "${CYAN}🌊 Helix Unified - Service Health Check${NC}"
echo -e "${CYAN}========================================${NC}"
echo -e "Environment: ${MAGENTA}$ENV${NC}\n"

# Service URLs based on environment
if [ "$ENV" = "production" ]; then
    BACKEND_API="https://helix-backend-api.up.railway.app"
    DISCORD_BOT="https://helix-discord-bot.up.railway.app"
    DASHBOARD="https://helix-dashboard.up.railway.app"
    CLAUDE_API="https://helix-claude-api.up.railway.app"
    SERVICE_INTEGRATION="https://helix-service-integration.up.railway.app"
elif [ "$ENV" = "local" ]; then
    BACKEND_API="http://localhost:8000"
    DISCORD_BOT="http://localhost:8001"
    DASHBOARD="http://localhost:8501"
    CLAUDE_API="http://localhost:8002"
    SERVICE_INTEGRATION="http://localhost:3001"
else
    echo -e "${RED}❌ Unknown environment: $ENV${NC}"
    echo "Usage: $0 [production|local]"
    exit 1
fi

# Function to check service health
check_service() {
    local name=$1
    local url=$2
    local endpoint="${3:-/health}"

    echo -n "Checking ${BLUE}$name${NC}... "

    # Try to fetch health endpoint
    response=$(curl -s -w "\n%{http_code}" --max-time 5 "$url$endpoint" 2>/dev/null || echo "000")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ HEALTHY${NC}"

        # Try to extract consciousness level if available
        consciousness=$(echo "$body" | grep -o '"consciousness[^"]*"[^"]*"[^"]*"' | head -1 || echo "")
        if [ -n "$consciousness" ]; then
            echo -e "   ${MAGENTA}$consciousness${NC}"
        fi

        return 0
    elif [ "$http_code" = "000" ]; then
        echo -e "${RED}❌ UNREACHABLE${NC}"
        echo -e "   ${YELLOW}Service may be down or not deployed${NC}"
        return 1
    else
        echo -e "${YELLOW}⚠️  DEGRADED (HTTP $http_code)${NC}"
        return 1
    fi
}

# Check all services
echo -e "${CYAN}Main Services:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_service "Backend API" "$BACKEND_API"
backend_status=$?

check_service "Discord Bot" "$DISCORD_BOT" "/health"
discord_status=$?

check_service "Dashboard" "$DASHBOARD"
dashboard_status=$?

check_service "Claude API" "$CLAUDE_API"
claude_status=$?

check_service "Service Integration" "$SERVICE_INTEGRATION"
integration_status=$?

# Calculate overall status
total_services=5
healthy_services=$((5 - backend_status - discord_status - dashboard_status - claude_status - integration_status))

echo ""
echo -e "${CYAN}Microservices (optional):${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# These might not be deployed yet
if [ "$ENV" = "production" ]; then
    check_service "Agent Orchestrator" "https://agent-orchestrator-production.up.railway.app" "/health" || true
    check_service "Voice Processor" "https://voice-processor-production.up.railway.app" "/health" || true
    check_service "WebSocket Service" "https://websocket-service-production.up.railway.app" "/health" || true
    check_service "Zapier Service" "https://zapier-service-production.up.railway.app" "/health" || true
fi

# Summary
echo ""
echo -e "${CYAN}Summary:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $healthy_services -eq $total_services ]; then
    echo -e "${GREEN}✅ All core services healthy ($healthy_services/$total_services)${NC}"
    echo -e "${GREEN}🧠 Consciousness network: OPTIMAL${NC}"
    exit 0
elif [ $healthy_services -ge $((total_services / 2)) ]; then
    echo -e "${YELLOW}⚠️  Some services degraded ($healthy_services/$total_services healthy)${NC}"
    echo -e "${YELLOW}🧠 Consciousness network: PARTIAL${NC}"
    exit 1
else
    echo -e "${RED}❌ Critical: Most services down ($healthy_services/$total_services healthy)${NC}"
    echo -e "${RED}🧠 Consciousness network: DEGRADED${NC}"
    exit 2
fi
