#!/bin/bash
# 🔧 Quick Discord Channel Setup Script
# Creates all monitoring channels automatically

echo "🌀 Helix Discord Channel Setup"
echo "================================"
echo ""

# Check if Discord token is set
if [ -z "$DISCORD_BOT_TOKEN" ]; then
    echo "❌ Error: DISCORD_BOT_TOKEN not set"
    echo ""
    echo "Set it with:"
    echo "  export DISCORD_BOT_TOKEN=your_token"
    echo "  or add to .env file"
    exit 1
fi

echo "✅ Discord token found"
echo ""

# Check if bot is running
echo "📡 Checking bot status..."
echo ""

# Option 1: Run standalone setup script
echo "Option 1: Run Standalone Setup"
echo "------------------------------"
echo "python discord-bot/server_setup.py"
echo ""

# Option 2: Use bot command
echo "Option 2: Use Bot Command (if bot is running)"
echo "---------------------------------------------"
echo "In Discord, type: !setup"
echo ""

# Option 3: Railway deployment
echo "Option 3: Railway Deployment"
echo "----------------------------"
echo "railway run python discord-bot/server_setup.py"
echo ""

# Ask user which method to use
echo "Choose method (1-3):"
read -r method

case $method in
    1)
        echo "Running standalone setup..."
        python discord-bot/server_setup.py
        ;;
    2)
        echo "Make sure your bot is running, then type in Discord:"
        echo "  !setup"
        echo ""
        echo "Or for verification first:"
        echo "  !setup verify"
        ;;
    3)
        echo "Running on Railway..."
        railway run python discord-bot/server_setup.py
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "✅ Setup complete!"
echo ""
echo "📺 Expected channels created:"
echo "  • 🧠 SYSTEM: telemetry, weekly-digest, shadow-storage, ucf-sync"
echo "  • 🎭 AGENTS: 17 agent channels"
echo "  • 🕉️ RITUAL & LORE: neti-neti-mantra, codex-archives, etc."
echo "  • 🔧 DEVELOPMENT: bot-commands, testing-lab"
echo ""
echo "🤖 Use '!channels' in Discord to see full list"
