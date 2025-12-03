#!/bin/bash
#
# Railway Setup Script
# ====================
# Automatically configures Railway project with all required services
#
# Prerequisites:
# - Railway CLI installed (curl -fsSL https://railway.app/install.sh | sh)
# - Railway account logged in (railway login)
#

set -e

echo "🚂 Helix Unified - Railway Auto-Setup"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo -e "${RED}❌ Railway CLI not found${NC}"
    echo "Install: curl -fsSL https://railway.app/install.sh | sh"
    exit 1
fi

echo -e "${GREEN}✓ Railway CLI found${NC}"

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo -e "${RED}❌ Not logged in to Railway${NC}"
    echo "Run: railway login"
    exit 1
fi

echo -e "${GREEN}✓ Logged in to Railway${NC}"
echo ""

# Create new project or link existing
read -p "Create new Railway project? (y/N): " create_new
if [[ "$create_new" =~ ^[Yy]$ ]]; then
    echo "Creating new Railway project..."
    railway init
else
    echo "Using existing Railway project..."
    railway link
fi

echo ""
echo "📦 Adding PostgreSQL database..."
railway add --plugin postgresql || echo "PostgreSQL already added"

echo ""
echo "📦 Adding Redis cache..."
railway add --plugin redis || echo "Redis already added"

echo ""
echo "🔑 Setting up environment variables..."
echo ""
echo "Please provide the following API keys (or press Enter to skip):"
echo ""

# Collect API keys
read -p "ANTHROPIC_API_KEY: " anthropic_key
read -p "OPENAI_API_KEY: " openai_key
read -p "STRIPE_SECRET_KEY: " stripe_key
read -p "STRIPE_PUBLISHABLE_KEY: " stripe_pub_key
read -p "DISCORD_BOT_TOKEN: " discord_token

# Generate JWT secret
jwt_secret=$(openssl rand -hex 32)
echo ""
echo -e "${GREEN}✓ Generated JWT_SECRET${NC}"

# Set environment variables
echo ""
echo "Setting environment variables..."

[ -n "$anthropic_key" ] && railway variables set ANTHROPIC_API_KEY="$anthropic_key"
[ -n "$openai_key" ] && railway variables set OPENAI_API_KEY="$openai_key"
[ -n "$stripe_key" ] && railway variables set STRIPE_SECRET_KEY="$stripe_key"
[ -n "$stripe_pub_key" ] && railway variables set STRIPE_PUBLISHABLE_KEY="$stripe_pub_key"
[ -n "$discord_token" ] && railway variables set DISCORD_BOT_TOKEN="$discord_token"
railway variables set JWT_SECRET="$jwt_secret"

echo ""
echo -e "${GREEN}✓ Environment variables configured${NC}"

echo ""
echo "🚀 Deploying services..."
railway up

echo ""
echo "======================================"
echo -e "${GREEN}✅ Railway setup complete!${NC}"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Check deployment status: railway status"
echo "2. View logs: railway logs"
echo "3. Open dashboard: railway open"
echo "4. Get service URLs: railway domain"
echo ""
echo "Your Railway project is ready! 🎉"
