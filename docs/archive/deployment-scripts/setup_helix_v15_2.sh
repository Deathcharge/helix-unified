#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# 🌀  Helix Collective v15.2 – Manus + Claude Unified Setup
# ─────────────────────────────────────────────────────────────
set -e

echo "🌌 Initializing Helix v15.2 Environment..."

# 1️⃣  Create required directories
echo "📁 Creating directory structure..."
mkdir -p backend/services backend/agents
mkdir -p Helix/state Helix/commands Helix/ethics
mkdir -p Shadow/manus_archive/visual_outputs
mkdir -p frontend scripts

# 2️⃣  Verify core files exist
echo "🔍 Verifying core modules..."
if [ ! -f "backend/helix_storage_adapter_async.py" ]; then
    echo "⚠️  Warning: backend/helix_storage_adapter_async.py not found"
    echo "   This file should already exist from the Ω-Bridge installation"
fi

if [ ! -f "backend/samsara_bridge.py" ]; then
    echo "⚠️  Warning: backend/samsara_bridge.py not found"
    echo "   This file should already exist from the Ω-Bridge installation"
fi

# 3️⃣  Generate example .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env template..."
    cat > .env <<'EOF'
# ─── Discord & Core ────────────────────────
DISCORD_TOKEN=your_discord_token_here
DISCORD_GUILD_ID=your_guild_id_here
DISCORD_STATUS_CHANNEL_ID=your_status_channel_id
DISCORD_TELEMETRY_CHANNEL_ID=your_telemetry_channel_id
STORAGE_CHANNEL_ID=your_storage_channel_id
ARCHITECT_ID=your_user_id

# ─── Storage ───────────────────────────────
HELIX_STORAGE_MODE=local
# For Nextcloud:
# HELIX_STORAGE_MODE=nextcloud
# NEXTCLOUD_URL=https://your.nextcloud.server/remote.php/dav/files/user/
# NEXTCLOUD_USER=username
# NEXTCLOUD_PASS=app_password

# For MEGA:
# HELIX_STORAGE_MODE=mega
# MEGA_API_KEY=your_mega_token

# ─── API/Deployment ────────────────────────
HELIX_URL=http://localhost:8000
PORT=8000
PYTHONUNBUFFERED=1
LOG_LEVEL=INFO

# ─── Helix Configuration ───────────────────
HELIX_VERSION=15.2
HELIX_CODENAME=Manus + Claude Autonomy Pack
HELIX_PHASE=15
ENABLE_KAVACH_SCAN=True

# ─── Optional: Notion Integration ─────────
# NOTION_API_KEY=secret_xxxxx
# NOTION_SYSTEM_STATE_DB=database_id
# NOTION_AGENT_REGISTRY_DB=database_id
# NOTION_EVENT_LOG_DB=database_id
# NOTION_CONTEXT_DB=database_id
EOF
    echo "✅ Created .env template"
else
    echo "ℹ️  .env already exists - skipping"
fi

# 4️⃣  Install dependencies
echo "📦 Checking dependencies..."
if command -v pip &> /dev/null; then
    if [ -f "requirements.txt" ]; then
        echo "📦 Installing Python dependencies..."
        pip install -r requirements.txt
    else
        echo "📦 Installing core dependencies..."
        pip install fastapi uvicorn aiohttp aiofiles discord.py python-dotenv \
                   pillow numpy scipy redis asyncpg sqlalchemy \
                   streamlit plotly pandas pyyaml python-multipart
    fi
else
    echo "⚠️  pip not found - please install Python dependencies manually"
fi

# 5️⃣  Create initial UCF state if it doesn't exist
if [ ! -f "Helix/state/ucf_state.json" ]; then
    echo "🌀 Creating initial UCF state..."
    cat > Helix/state/ucf_state.json <<'EOF'
{
  "harmony": 0.355,
  "resilience": 1.1191,
  "prana": 0.5175,
  "drishti": 0.5023,
  "klesha": 0.010,
  "zoom": 1.0228,
  "timestamp": "2025-10-23T00:00:00Z"
}
EOF
    echo "✅ Created initial UCF state"
fi

# 6️⃣  Optional: Create export archive
if command -v zip &> /dev/null; then
    ZIPNAME="Helix_v15.2_ManusClaude_$(date +%Y%m%d_%H%M%S).zip"
    echo "📦 Creating deployment archive: $ZIPNAME"
    zip -r "$ZIPNAME" \
        backend/ \
        Helix/ \
        Shadow/ \
        frontend/ \
        scripts/ \
        requirements.txt \
        Dockerfile \
        docker-compose.yml \
        railway.toml \
        README.md \
        CHANGELOG.md \
        .env.example \
        setup_helix_v15_2.sh \
        -x "*.pyc" "__pycache__/*" "*.log" ".git/*" ".env"
    echo "✅ Created archive: $ZIPNAME"
fi

# 7️⃣  Summary
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "🎯  Helix v15.2 Setup Complete!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "✅ Directory structure created"
echo "✅ Configuration template ready (.env)"
echo "✅ Dependencies installed"
echo "✅ UCF state initialized"
echo ""
echo "📋 Next Steps:"
echo "   1. Edit .env with your Discord token and configuration"
echo "   2. Run locally:   python backend/main.py"
echo "   3. Test Discord:  Invite bot and try !status"
echo "   4. Deploy:        git push to Railway/Render"
echo ""
echo "🌐 Endpoints (when running):"
echo "   • API:         http://localhost:8000"
echo "   • Docs:        http://localhost:8000/docs"
echo "   • Health:      http://localhost:8000/health"
echo "   • Storage:     http://localhost:8000/storage/status"
echo "   • Visualize:   http://localhost:8000/visualize/ritual"
echo ""
echo "💬 Discord Commands:"
echo "   • !status          - System status"
echo "   • !ritual 108      - Execute Z-88 ritual"
echo "   • !storage status  - Storage telemetry"
echo "   • !storage sync    - Force cloud upload"
echo "   • !storage clean   - Prune old archives"
echo ""
echo "🦑 Tat Tvam Asi 🙏"
echo "═══════════════════════════════════════════════════════════"
