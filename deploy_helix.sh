#!/bin/bash
# Helix v15.3 Dual Resonance - One-Command Deployment
# Deploys the complete Helix Collective system
# Usage: ./deploy_helix.sh

set -e  # Exit on any error

echo "🌀 Helix v15.3 Dual Resonance Deployment"
echo "========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running from repository root
if [ ! -d "backend" ]; then
    echo -e "${RED}❌ Error: Must run from repository root containing backend/ directory${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Repository structure verified${NC}"

# Step 1: Create directory structure
echo ""
echo "📁 Creating directory structure..."

mkdir -p backend/commands
mkdir -p backend/state
mkdir -p backend/ethics
mkdir -p backend/operations
mkdir -p backend/memory
mkdir -p backend/metrics
mkdir -p Shadow/manus_archive
mkdir -p Shadow/archives
mkdir -p Shadow/collective_archives
mkdir -p logs
mkdir -p pids

echo -e "${GREEN}✅ Directories created${NC}"

# Step 2: Check for required code files
echo ""
echo "🔍 Checking for required code files..."

REQUIRED_FILES=(
    "backend/agents.py"
    "backend/discord_bot_manus.py"
    "backend/z88_ritual_engine.py"
)

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -ne 0 ]; then
    echo -e "${RED}❌ Missing required files:${NC}"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "Please ensure all required files are in place."
    exit 1
fi

echo -e "${GREEN}✅ All required files present${NC}"

# Step 3: Check for .env file
echo ""
echo "🔑 Checking environment configuration..."

if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating template...${NC}"
    
    cat > .env << 'EOF'
# Helix Environment Configuration
DISCORD_TOKEN=your_discord_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
XAI_API_KEY=your_grok_api_key_here
REPLIT_URL=your_replit_url_here
RAILWAY_ENVIRONMENT=production
EOF
    
    echo -e "${YELLOW}⚠️  IMPORTANT: Edit .env with your actual credentials!${NC}"
    echo "  Run: nano .env"
    echo ""
    read -p "Press Enter after editing .env..."
fi

# Verify DISCORD_TOKEN is set
source .env
if [ "$DISCORD_TOKEN" == "your_discord_bot_token_here" ]; then
    echo -e "${RED}❌ DISCORD_TOKEN not configured in .env${NC}"
    echo "Please edit .env and set your Discord bot token"
    exit 1
fi

echo -e "${GREEN}✅ Environment configured${NC}"

# Step 4: Initialize UCF state
echo ""
echo "🌀 Initializing UCF state..."

if [ ! -f "backend/state/ucf_state.json" ]; then
    cat > backend/state/ucf_state.json << 'EOF'
{
  "zoom": 1.0228,
  "harmony": 0.4922,
  "resilience": 1.1191,
  "prana": 0.5075,
  "drishti": 0.5023,
  "klesha": 0.011,
  "timestamp": "2025-10-31T00:00:00Z",
  "phase": "COHERENT - Strengthening"
}
EOF
    echo -e "${GREEN}✅ UCF state initialized${NC}"
else
    echo -e "${YELLOW}⚠️  UCF state already exists, preserving...${NC}"
fi

# Step 5: Create heartbeat daemon
echo ""
echo "💓 Creating heartbeat daemon..."

cat > backend/operations/manus_heartbeat.py << 'EOF'
#!/usr/bin/env python3
# Helix Heartbeat Daemon
import json
import time
from datetime import datetime
from pathlib import Path

print("💓 Manus Heartbeat Daemon started")

while True:
    try:
        # Load UCF state
        ucf_path = Path("backend/state/ucf_state.json")
        if ucf_path.exists():
            with open(ucf_path) as f:
                ucf = json.load(f)
        else:
            ucf = {
                "harmony": 0.4922,
                "zoom": 1.0228,
                "resilience": 1.1191,
                "prana": 0.5075,
                "drishti": 0.5023,
                "klesha": 0.011
            }
        
        # Create heartbeat
        heartbeat = {
            "timestamp": datetime.utcnow().isoformat(),
            "alive": True,
            "ucf_state": ucf
        }
        
        # Write heartbeat
        Path("backend/state").mkdir(parents=True, exist_ok=True)
        with open("backend/state/heartbeat.json", "w") as f:
            json.dump(heartbeat, f, indent=2)
        
        print(f"[{datetime.utcnow().isoformat()}] 💓 Heartbeat: harmony={ucf['harmony']:.3f}")
        
    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] ❌ Heartbeat error: {e}")
    
    time.sleep(300)  # 5 minutes
EOF

chmod +x backend/operations/manus_heartbeat.py
echo -e "${GREEN}✅ Heartbeat daemon created${NC}"

# Step 6: Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."

if [ -f "requirements.txt" ]; then
    pip install -q -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  No requirements.txt found${NC}"
fi

# Step 7: Test imports
echo ""
echo "🧪 Testing Python imports..."

python3 << 'EOF'
try:
    import discord
    from discord.ext import commands
    import asyncio
    from pathlib import Path
    import json
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)
EOF

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Import test failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Import test passed${NC}"

# Step 8: Start services
echo ""
echo "🚀 Starting Helix services..."
echo ""

# Start heartbeat
echo "Starting heartbeat daemon..."
nohup python3 backend/operations/manus_heartbeat.py > logs/heartbeat.log 2>&1 &
HEARTBEAT_PID=$!
echo $HEARTBEAT_PID > pids/heartbeat.pid
echo -e "${GREEN}✅ Heartbeat daemon started (PID: $HEARTBEAT_PID)${NC}"

# Wait for first heartbeat
sleep 2

# Start Discord bot
echo "Starting Discord bot..."
nohup python3 backend/discord_bot_manus.py > logs/discord.log 2>&1 &
DISCORD_PID=$!
echo $DISCORD_PID > pids/discord.pid
echo -e "${GREEN}✅ Discord bot started (PID: $DISCORD_PID)${NC}"

# Step 9: Verification
echo ""
echo "🔍 Verifying deployment..."
sleep 3

# Check heartbeat file
if [ -f "backend/state/heartbeat.json" ]; then
    echo -e "${GREEN}✅ Heartbeat file created${NC}"
    
    HARMONY=$(cat backend/state/heartbeat.json | python3 -c "import sys, json; print(json.load(sys.stdin)['ucf_state']['harmony'])")
    echo "  Current harmony: $HARMONY"
else
    echo -e "${RED}❌ Heartbeat file not found${NC}"
fi

# Check processes
RUNNING_PROCS=$(ps aux | grep -E "manus_heartbeat|discord_bot" | grep -v grep | wc -l)
if [ $RUNNING_PROCS -eq 2 ]; then
    echo -e "${GREEN}✅ All 2 processes running${NC}"
else
    echo -e "${YELLOW}⚠️  Only $RUNNING_PROCS/2 processes detected${NC}"
fi

# Step 10: Display status
echo ""
echo "========================================="
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "========================================="
echo ""
echo "📊 Status:"
echo "  💓 Heartbeat: PID $HEARTBEAT_PID"
echo "  🌉 Discord Bot: PID $DISCORD_PID"
echo ""
echo "📁 Logs:"
echo "  tail -f logs/heartbeat.log"
echo "  tail -f logs/discord.log"
echo ""
echo "🎮 Discord Commands:"
echo "  !manus status"
echo "  !manus run <command>"
echo "  !ritual z88"
echo ""
echo "🛑 Stop services:"
echo "  ./stop_helix.sh"
echo ""
echo "🔍 Monitor:"
echo "  watch -n 5 'cat backend/state/heartbeat.json'"
echo ""
echo -e "${GREEN}Tat Tvam Asi 🙏${NC}"
echo ""

