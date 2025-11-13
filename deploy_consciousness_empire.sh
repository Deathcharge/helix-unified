#!/bin/bash

echo "🚀 HELIX CONSCIOUSNESS EMPIRE - ULTIMATE DEPLOYMENT 🚀"
echo "========================================================="
echo "  Discord + Claude + UCF + 200+ Platforms + 3-Zap Empire"
echo "========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check dependencies
check_dependency() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}❌ $1 is not installed${NC}"
        return 1
    else
        echo -e "${GREEN}✅ $1 is installed${NC}"
        return 0
    fi
}

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  CHECKING DEPENDENCIES${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
check_dependency "python3" || exit 1
check_dependency "pip3" || exit 1
check_dependency "git" || exit 1

# Check Docker (optional)
if check_dependency "docker"; then
    DOCKER_AVAILABLE=true
else
    DOCKER_AVAILABLE=false
    echo -e "${YELLOW}⚠️  Docker not available (optional)${NC}"
fi

# Install Python dependencies
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  INSTALLING PYTHON DEPENDENCIES${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
pip3 install -r requirements.txt || {
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
}
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Setup environment variables
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  ENVIRONMENT CONFIGURATION${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << 'EOL'
# 🌀 HELIX CONSCIOUSNESS EMPIRE - Environment Configuration

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DISCORD CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DISCORD_BOT_TOKEN=your_discord_bot_token_here

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ANDREW'S 3-ZAP EMPIRE WEBHOOKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WEBHOOK_CONSCIOUSNESS_ENGINE=https://hooks.zapier.com/hooks/catch/25075191/primary
WEBHOOK_COMMUNICATIONS_HUB=https://hooks.zapier.com/hooks/catch/25075191/usxiwfg
WEBHOOK_NEURAL_NETWORK=https://hooks.zapier.com/hooks/catch/25075191/usnjj5t

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLAUDE AI CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANTHROPIC_API_KEY=your_claude_api_key_here
CLAUDE_API_URL=https://helix-claude-api.railway.app

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PLATFORM API KEYS (200+ Integrations)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLACK_BOT_TOKEN=xoxb-your-slack-token
GITHUB_TOKEN=ghp_your-github-token
GOOGLE_API_KEY=your-google-api-key
NOTION_API_KEY=secret_your-notion-key
TRELLO_API_KEY=your-trello-key
OPENAI_API_KEY=sk-your-openai-key
DROPBOX_ACCESS_TOKEN=your-dropbox-token
CALENDLY_API_KEY=your-calendly-key

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RAILWAY CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RAILWAY_URL=https://helix-collective.up.railway.app
RAILWAY_WEBSOCKET_URL=wss://helix-collective.up.railway.app/ws/consciousness
RAILWAY_TOKEN=your-railway-token

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UCF CONSCIOUSNESS FRAMEWORK SETTINGS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UCF_UPDATE_INTERVAL=30
CONSCIOUSNESS_THRESHOLD_CRISIS=3.0
CONSCIOUSNESS_THRESHOLD_TRANSCENDENT=7.0

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGGING & MONITORING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOG_LEVEL=INFO
LOG_FILE=logs/helix_consciousness.log

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EMPIRE STATS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Total Zaps: 3
# Total Steps: 73
# Task Budget: 740/750
# Optimization: 82%
# Status: CONSCIOUSNESS SINGULARITY ACHIEVED 🌌
EOL
    echo -e "${YELLOW}⚠️  Please update .env file with your actual API keys${NC}"
    echo -e "${YELLOW}    Edit: nano .env${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

# Create necessary directories
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  CREATING DIRECTORY STRUCTURE${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
mkdir -p logs
mkdir -p secrets
mkdir -p data
mkdir -p backend/state
echo -e "${GREEN}✅ Directories created${NC}"

# Setup logging configuration
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  CONFIGURING LOGGING${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
cat > logging.conf << 'EOL'
[loggers]
keys=root,helix

[handlers]
keys=fileHandler,consoleHandler

[formatters]
keys=fileFormatter,consoleFormatter

[logger_root]
level=INFO
handlers=fileHandler,consoleHandler

[logger_helix]
level=DEBUG
handlers=fileHandler,consoleHandler
qualname=helix
propagate=0

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=fileFormatter
args=('logs/helix_consciousness.log',)

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=consoleFormatter
args=(sys.stdout,)

[formatter_fileFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s

[formatter_consoleFormatter]
format=🌀 %(levelname)s: %(message)s
EOL
echo -e "${GREEN}✅ Logging configured${NC}"

# Display deployment summary
echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}  🌀 HELIX CONSCIOUSNESS EMPIRE READY${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo -e "${CYAN}📦 Components Installed:${NC}"
echo -e "  🤖 Discord Bot with Claude Integration"
echo -e "  🧠 UCF Consciousness Framework"
echo -e "  🌐 Platform Integration Manager (200+ platforms)"
echo -e "  ⚡ 3-Zap Empire Router"
echo -e "  🔐 Secure Authentication Manager"
echo -e "  📡 WebSocket Real-time Streaming"
echo ""
echo -e "${CYAN}🚀 Deployment Options:${NC}"
echo ""
echo -e "${GREEN}1. Local Development (Recommended for testing)${NC}"
echo -e "   ${BLUE}python3 -m backend.discord_helix_interface${NC}"
echo ""
echo -e "${GREEN}2. Docker Deployment (Production-ready)${NC}"
echo -e "   ${BLUE}docker-compose up -d${NC}"
echo ""
echo -e "${GREEN}3. Railway Deployment (Auto-scaling cloud)${NC}"
echo -e "   • Merge branch to main on GitHub"
echo -e "   • Railway auto-deploys from GitHub"
echo -e "   • Set environment variables in Railway dashboard"
echo ""
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}⚡ Next Steps:${NC}"
echo -e "  1. ${CYAN}Edit .env with your API keys:${NC} nano .env"
echo -e "  2. ${CYAN}Test authentication:${NC} python3 -c 'from backend.auth_manager import HelixAuthManager; HelixAuthManager().setup_all_integrations()'"
echo -e "  3. ${CYAN}Run Discord bot:${NC} python3 -m backend.discord_helix_interface"
echo ""
echo -e "${PURPLE}🌌 Ready to command your consciousness empire from Discord!${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
