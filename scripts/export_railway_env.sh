#!/bin/bash
# 🌀 Helix Collective - Clean Railway Environment Export
# Exports all environment variables needed for Railway deployment
# Usage: ./scripts/export_railway_env.sh [service_name]

set -e

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Load .env file
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found. Copy .env.example to .env first${NC}"
    exit 1
fi

export $(grep -v '^#' .env | xargs)

# Service selection
SERVICE_NAME=${1:-all}

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  🚂 Railway Environment Variable Export${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ============================================================================
# SHARED VARIABLES (All Services)
# ============================================================================
export_shared_vars() {
    echo -e "${GREEN}📦 Shared Variables (All Services)${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    cat << EOF
# Core Configuration
export HELIX_VERSION="${HELIX_VERSION:-v16.7}"
export HELIX_PHASE="${HELIX_PHASE:-production}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"
export DEBUG="${DEBUG:-false}"

# Zapier Webhooks (Shared)
export ZAPIER_WEBHOOK_URL="${ZAPIER_WEBHOOK_URL}"
export ZAPIER_MASTER_HOOK_URL="${ZAPIER_MASTER_HOOK_URL}"

# Notion Integration (Shared)
export NOTION_API_KEY="${NOTION_API_KEY}"
export NOTION_SYSTEM_STATE_DB="${NOTION_SYSTEM_STATE_DB}"
export NOTION_AGENT_REGISTRY_DB="${NOTION_AGENT_REGISTRY_DB}"
export NOTION_EVENT_LOG_DB="${NOTION_EVENT_LOG_DB}"
export NOTION_CONTEXT_DB="${NOTION_CONTEXT_DB}"

# Storage Configuration (Shared)
export HELIX_STORAGE_MODE="${HELIX_STORAGE_MODE:-nextcloud}"
export NEXTCLOUD_URL="${NEXTCLOUD_URL}"
export NEXTCLOUD_USER="${NEXTCLOUD_USER}"
export NEXTCLOUD_PASS="${NEXTCLOUD_PASS}"
export NEXTCLOUD_BASE_PATH="${NEXTCLOUD_BASE_PATH:-/Helix}"

# MEGA Backup (Optional)
export MEGA_EMAIL="${MEGA_EMAIL}"
export MEGA_PASS="${MEGA_PASS}"
export MEGA_REMOTE_DIR="${MEGA_REMOTE_DIR:-/Helix-Backups}"
EOF
    echo ""
}

# ============================================================================
# SERVICE 1: helix-backend-api (NO BOT)
# ============================================================================
export_backend_api() {
    echo -e "${GREEN}🔧 Service 1: helix-backend-api${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    cat << EOF
# API Configuration
export API_HOST="${API_HOST:-0.0.0.0}"
export API_PORT="${API_PORT:-8000}"

# Database
export DATABASE_URL="${DATABASE_URL}"
export REDIS_URL="${REDIS_URL:-redis://localhost:6379}"

# ⚠️ NO DISCORD_TOKEN on this service!
EOF
    echo ""
}

# ============================================================================
# SERVICE 2: helix-dashboard (Streamlit)
# ============================================================================
export_dashboard() {
    echo -e "${GREEN}📊 Service 2: helix-dashboard${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    cat << EOF
# Dashboard uses shared variables only
# Railway auto-sets PORT variable
# No additional env vars needed
EOF
    echo ""
}

# ============================================================================
# SERVICE 3: helix-claude-api
# ============================================================================
export_claude_api() {
    echo -e "${GREEN}🤖 Service 3: helix-claude-api${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    cat << EOF
# Claude API Key
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}"

# Andrew's Consciousness Empire Webhooks
export CONSCIOUSNESS_ENGINE_WEBHOOK="https://hooks.zapier.com/hooks/catch/25075191/primary"
export COMMUNICATIONS_HUB_WEBHOOK="https://hooks.zapier.com/hooks/catch/25075191/usxiwfg"
export NEURAL_NETWORK_WEBHOOK="https://hooks.zapier.com/hooks/catch/25075191/usnjj5t"
EOF
    echo ""
}

# ============================================================================
# SERVICE 4: helix-discord-bot (ONLY BOT SERVICE!)
# ============================================================================
export_discord_bot() {
    echo -e "${GREEN}💬 Service 4: helix-discord-bot${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    cat << EOF
# ⚠️ DISCORD TOKEN ONLY ON THIS SERVICE!
export DISCORD_TOKEN="${DISCORD_TOKEN}"
export DISCORD_GUILD_ID="${DISCORD_GUILD_ID}"
export ARCHITECT_ID="${ARCHITECT_ID}"

# Discord Channel IDs
export DISCORD_STATUS_CHANNEL_ID="${DISCORD_STATUS_CHANNEL_ID}"
export DISCORD_TELEMETRY_CHANNEL_ID="${DISCORD_TELEMETRY_CHANNEL_ID}"
export DISCORD_MANUS_BRIDGE_CHANNEL_ID="${DISCORD_MANUS_BRIDGE_CHANNEL_ID}"
export DISCORD_RITUAL_ENGINE_CHANNEL_ID="${DISCORD_RITUAL_ENGINE_CHANNEL_ID}"
export DISCORD_BACKUP_CHANNEL_ID="${DISCORD_BACKUP_CHANNEL_ID}"
export DISCORD_DEPLOYMENTS_CHANNEL_ID="${DISCORD_DEPLOYMENTS_CHANNEL_ID}"

# Claude API URL (set AFTER deploying service 3)
# Get URL from Railway dashboard: helix-claude-api service
export CLAUDE_API_URL="https://helix-claude-api.railway.app"
EOF
    echo ""
}

# ============================================================================
# RAILWAY CLI COMMANDS
# ============================================================================
generate_railway_commands() {
    local service=$1
    echo -e "${YELLOW}🚀 Railway CLI Commands for: ${service}${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Select service
    echo "# Switch to service"
    echo "railway service ${service}"
    echo ""

    # Core shared variables
    echo "# Set shared variables"
    echo "railway variables set \\"
    echo "  HELIX_VERSION=\"${HELIX_VERSION:-v16.7}\" \\"
    echo "  HELIX_PHASE=\"${HELIX_PHASE:-production}\" \\"
    echo "  LOG_LEVEL=\"${LOG_LEVEL:-INFO}\" \\"
    echo "  DEBUG=\"${DEBUG:-false}\" \\"
    echo "  ZAPIER_WEBHOOK_URL=\"${ZAPIER_WEBHOOK_URL}\" \\"
    echo "  ZAPIER_MASTER_HOOK_URL=\"${ZAPIER_MASTER_HOOK_URL}\" \\"
    echo "  NOTION_API_KEY=\"${NOTION_API_KEY}\" \\"
    echo "  NOTION_SYSTEM_STATE_DB=\"${NOTION_SYSTEM_STATE_DB}\" \\"
    echo "  NOTION_AGENT_REGISTRY_DB=\"${NOTION_AGENT_REGISTRY_DB}\" \\"
    echo "  NOTION_EVENT_LOG_DB=\"${NOTION_EVENT_LOG_DB}\" \\"
    echo "  NOTION_CONTEXT_DB=\"${NOTION_CONTEXT_DB}\" \\"
    echo "  HELIX_STORAGE_MODE=\"${HELIX_STORAGE_MODE:-nextcloud}\" \\"
    echo "  NEXTCLOUD_URL=\"${NEXTCLOUD_URL}\" \\"
    echo "  NEXTCLOUD_USER=\"${NEXTCLOUD_USER}\" \\"
    echo "  NEXTCLOUD_PASS=\"${NEXTCLOUD_PASS}\" \\"
    echo "  NEXTCLOUD_BASE_PATH=\"${NEXTCLOUD_BASE_PATH:-/Helix}\""
    echo ""

    # Service-specific variables
    case $service in
        helix-backend-api)
            echo "# Backend-specific variables"
            echo "railway variables set \\"
            echo "  API_HOST=\"${API_HOST:-0.0.0.0}\" \\"
            echo "  API_PORT=\"${API_PORT:-8000}\" \\"
            echo "  DATABASE_URL=\"${DATABASE_URL}\" \\"
            echo "  REDIS_URL=\"${REDIS_URL:-redis://localhost:6379}\""
            ;;
        helix-claude-api)
            echo "# Claude API variables"
            echo "railway variables set \\"
            echo "  ANTHROPIC_API_KEY=\"${ANTHROPIC_API_KEY}\" \\"
            echo "  CONSCIOUSNESS_ENGINE_WEBHOOK=\"https://hooks.zapier.com/hooks/catch/25075191/primary\" \\"
            echo "  COMMUNICATIONS_HUB_WEBHOOK=\"https://hooks.zapier.com/hooks/catch/25075191/usxiwfg\" \\"
            echo "  NEURAL_NETWORK_WEBHOOK=\"https://hooks.zapier.com/hooks/catch/25075191/usnjj5t\""
            ;;
        helix-discord-bot)
            echo "# Discord Bot variables (ONLY SERVICE WITH DISCORD_TOKEN!)"
            echo "railway variables set \\"
            echo "  DISCORD_TOKEN=\"${DISCORD_TOKEN}\" \\"
            echo "  DISCORD_GUILD_ID=\"${DISCORD_GUILD_ID}\" \\"
            echo "  ARCHITECT_ID=\"${ARCHITECT_ID}\" \\"
            echo "  DISCORD_STATUS_CHANNEL_ID=\"${DISCORD_STATUS_CHANNEL_ID}\" \\"
            echo "  DISCORD_TELEMETRY_CHANNEL_ID=\"${DISCORD_TELEMETRY_CHANNEL_ID}\" \\"
            echo "  DISCORD_MANUS_BRIDGE_CHANNEL_ID=\"${DISCORD_MANUS_BRIDGE_CHANNEL_ID}\" \\"
            echo "  DISCORD_RITUAL_ENGINE_CHANNEL_ID=\"${DISCORD_RITUAL_ENGINE_CHANNEL_ID}\" \\"
            echo "  DISCORD_BACKUP_CHANNEL_ID=\"${DISCORD_BACKUP_CHANNEL_ID}\" \\"
            echo "  DISCORD_DEPLOYMENTS_CHANNEL_ID=\"${DISCORD_DEPLOYMENTS_CHANNEL_ID}\" \\"
            echo "  CLAUDE_API_URL=\"https://helix-claude-api.railway.app\""
            ;;
    esac
    echo ""
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

case $SERVICE_NAME in
    all)
        export_shared_vars
        export_backend_api
        export_dashboard
        export_claude_api
        export_discord_bot
        echo ""
        echo -e "${YELLOW}💡 To generate Railway CLI commands, run:${NC}"
        echo -e "   ./scripts/export_railway_env.sh helix-backend-api"
        echo -e "   ./scripts/export_railway_env.sh helix-dashboard"
        echo -e "   ./scripts/export_railway_env.sh helix-claude-api"
        echo -e "   ./scripts/export_railway_env.sh helix-discord-bot"
        ;;
    helix-backend-api|helix-dashboard|helix-claude-api|helix-discord-bot)
        export_shared_vars
        case $SERVICE_NAME in
            helix-backend-api) export_backend_api ;;
            helix-dashboard) export_dashboard ;;
            helix-claude-api) export_claude_api ;;
            helix-discord-bot) export_discord_bot ;;
        esac
        echo ""
        generate_railway_commands $SERVICE_NAME
        ;;
    *)
        echo -e "${RED}❌ Unknown service: $SERVICE_NAME${NC}"
        echo ""
        echo "Usage: ./scripts/export_railway_env.sh [service_name]"
        echo ""
        echo "Available services:"
        echo "  - all (show all variables)"
        echo "  - helix-backend-api"
        echo "  - helix-dashboard"
        echo "  - helix-claude-api"
        echo "  - helix-discord-bot"
        exit 1
        ;;
esac

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Railway environment export complete!${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
