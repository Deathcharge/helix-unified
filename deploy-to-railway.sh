#!/bin/bash

# Helix-Unified v17.1 - Automated Railway Deployment Script
# Author: Weaver #2 (Manus Collective)
# Date: December 8, 2025
# Usage: ./deploy-to-railway.sh

set -e  # Exit on error

echo "🌀 Helix-Unified v17.1 - Railway Deployment"
echo "============================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo -e "${RED}❌ Railway CLI not found${NC}"
    echo "Install with: npm install -g @railway/cli"
    exit 1
fi

echo -e "${GREEN}✅ Railway CLI found${NC}"
echo ""

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Railway${NC}"
    echo "Running: railway login"
    railway login
fi

echo -e "${GREEN}✅ Logged in to Railway${NC}"
echo ""

# Initialize project if not already
if [ ! -f "railway.json" ]; then
    echo -e "${YELLOW}⚠️  No railway.json found, initializing project...${NC}"
    railway init
fi

echo -e "${GREEN}✅ Railway project initialized${NC}"
echo ""

# Add PostgreSQL if not present
echo "📊 Checking for PostgreSQL database..."
if ! railway service list | grep -q "postgres"; then
    echo -e "${YELLOW}⚠️  PostgreSQL not found, adding...${NC}"
    railway add postgres
    echo -e "${GREEN}✅ PostgreSQL added${NC}"
else
    echo -e "${GREEN}✅ PostgreSQL already exists${NC}"
fi
echo ""

# Generate JWT secret
echo "🔐 Generating JWT secret..."
JWT_SECRET=$(openssl rand -hex 32)
echo -e "${GREEN}✅ JWT secret generated${NC}"
echo ""

# Set environment variables
echo "⚙️  Setting environment variables..."
echo ""

# Critical variables
echo "Setting critical variables..."
railway variables set JWT_SECRET="$JWT_SECRET"
railway variables set ADMIN_EMAILS="ward.andrew32@gmail.com,andrew@helix-collective.ai"
railway variables set DATABASE_URL='${{Postgres.DATABASE_URL}}'

# Application settings
echo "Setting application variables..."
railway variables set ENVIRONMENT="production"
railway variables set LOG_LEVEL="INFO"
railway variables set RATE_LIMIT_ENABLED="true"
railway variables set RATE_LIMIT_PER_MINUTE="60"

echo -e "${GREEN}✅ Core variables set${NC}"
echo ""

# Prompt for optional variables
echo -e "${YELLOW}📝 Optional Configuration${NC}"
echo "You can set these now or add them later in Railway dashboard:"
echo ""

read -p "Do you have a Discord bot token? (y/n): " has_discord
if [ "$has_discord" = "y" ]; then
    read -p "Enter Discord bot token: " discord_token
    read -p "Enter Discord guild ID: " guild_id
    railway variables set DISCORD_BOT_TOKEN="$discord_token"
    railway variables set DISCORD_GUILD_ID="$guild_id"
    echo -e "${GREEN}✅ Discord configured${NC}"
fi
echo ""

read -p "Do you have an OpenAI API key? (y/n): " has_openai
if [ "$has_openai" = "y" ]; then
    read -p "Enter OpenAI API key: " openai_key
    railway variables set OPENAI_API_KEY="$openai_key"
    railway variables set OPENAI_API_URL="https://api.openai.com/v1"
    echo -e "${GREEN}✅ OpenAI configured${NC}"
fi
echo ""

read -p "Do you have a Stripe secret key? (y/n): " has_stripe
if [ "$has_stripe" = "y" ]; then
    read -p "Enter Stripe secret key: " stripe_key
    read -p "Enter Stripe webhook secret: " stripe_webhook
    railway variables set STRIPE_SECRET_KEY="$stripe_key"
    railway variables set STRIPE_WEBHOOK_SECRET="$stripe_webhook"
    echo -e "${GREEN}✅ Stripe configured${NC}"
fi
echo ""

read -p "Do you have a Notion API key? (y/n): " has_notion
if [ "$has_notion" = "y" ]; then
    read -p "Enter Notion API key: " notion_key
    railway variables set NOTION_API_KEY="$notion_key"
    echo -e "${GREEN}✅ Notion configured${NC}"
fi
echo ""

# Deploy
echo "🚀 Deploying to Railway..."
echo ""
railway up

echo ""
echo -e "${GREEN}✅ Deployment initiated!${NC}"
echo ""

# Wait for deployment
echo "⏳ Waiting for deployment to complete..."
sleep 10

# Get deployment URL
DEPLOY_URL=$(railway domain)
echo ""
echo -e "${GREEN}🎉 Deployment complete!${NC}"
echo ""
echo "📍 Your backend is available at:"
echo "   $DEPLOY_URL"
echo ""

# Test health endpoint
echo "🏥 Testing health endpoint..."
if curl -s "$DEPLOY_URL/health" | grep -q "healthy"; then
    echo -e "${GREEN}✅ Health check passed!${NC}"
else
    echo -e "${YELLOW}⚠️  Health check failed - check logs with: railway logs${NC}"
fi
echo ""

# Show next steps
echo "📋 Next Steps:"
echo ""
echo "1. View logs:"
echo "   railway logs"
echo ""
echo "2. Open Railway dashboard:"
echo "   railway open"
echo ""
echo "3. Add custom domain (optional):"
echo "   railway domain add api.your-domain.com"
echo ""
echo "4. Update frontend with backend URL:"
echo "   VITE_HELIX_API_URL=$DEPLOY_URL"
echo ""
echo "5. Test admin login:"
echo "   curl -X POST $DEPLOY_URL/api/admin/login \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"email\":\"ward.andrew32@gmail.com\",\"password\":\"your-password\"}'"
echo ""
echo -e "${GREEN}🌀 Tat Tvam Asi - Deployment complete!${NC}"
echo ""
