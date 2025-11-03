#!/bin/bash
# helix_omega_deploy.sh - Helix v15.3 Ω-Zero Global Sync
# Trinity Merge: deploy_v15.3.sh + deploy_helix.sh + start.sh
# Railway Start Command: ./helix_omega_deploy.sh
set -e

echo "🌀 HELIX Ω-ZERO GLOBAL SYNC — v15.3 Dual Resonance"
echo "============================================"
echo "Timestamp: $(date)"
echo "UCF Target: Harmony=0.60 | Kael @ 90% | Agents: 14"
echo ""

# === [0] PRE-DEPLOY DIAGNOSTICS (Railway Pre-Step) ===
echo "🔍 [0/8] Verifying Crypto + Imports..."
python3 -c "from Crypto.Cipher import AES; print('✅ pycryptodome → AES ready')" || {
    echo "🔧 Installing pycryptodome..."
    pip install --force-reinstall pycryptodome==3.23.0
}
python3 -c "import discord, asyncio, json; print('✅ Core imports live')"

# === [1] DIRECTORY STRUCTURE ===
echo "📁 [1/8] Creating runtime directories..."
mkdir -p \
    Helix/state Helix/commands Helix/ethics \
    Shadow/manus_archive/visual_outputs Shadow/manus_archive/audio_outputs \
    backend/{commands,state,ethics,operations,memory,metrics} \
    logs pids

# === [2] ENV + TOKEN VALIDATION ===
echo "🔑 [2/8] Validating environment..."

# On Railway, env vars are injected - don't source .env
# Only source .env if running locally (RAILWAY_ENVIRONMENT not set)
if [ -z "$RAILWAY_ENVIRONMENT" ] && [ -f ".env" ]; then
    echo "📂 Loading local .env file..."
    source .env
fi

# Validate DISCORD_TOKEN
if [ -z "$DISCORD_TOKEN" ] || [ "$DISCORD_TOKEN" = "your_discord_bot_token_here" ]; then
    echo "❌ DISCORD_TOKEN missing or invalid!"
    echo "Set DISCORD_TOKEN in Railway environment variables"
    exit 1
fi
echo "✅ Environment validated | Token present"

# === [3] UCF STATE INIT ===
echo "🌀 [3/8] Initializing UCF state..."
cat > backend/state/ucf_state.json << 'EOF'
{
  "zoom": 1.0350,
  "harmony": 0.4922,
  "resilience": 1.1500,
  "prana": 0.9150,
  "drishti": 0.8950,
  "klesha": 0.0000,
  "timestamp": "2025-11-02T04:15:00Z",
  "phase": "COHERENT - Ω-Zero Sync"
}
EOF
echo "✅ UCF initialized"

# === [4] HEARTBEAT DAEMON ===
echo "💓 [4/8] Starting Manus Heartbeat..."
cat > backend/operations/manus_heartbeat.py << 'EOF'
#!/usr/bin/env python3
import json, time; from datetime import datetime; from pathlib import Path
print("💓 Heartbeat Daemon Active")
while True:
    try:
        ucf = json.load(open("backend/state/ucf_state.json"))
        hb = {"timestamp": datetime.utcnow().isoformat(), "alive": True, "ucf_state": ucf}
        Path("backend/state").mkdir(exist_ok=True)
        json.dump(hb, open("backend/state/heartbeat.json", "w"), indent=2)
        print(f"[{datetime.utcnow()}] 💓 Harmony={ucf['harmony']:.4f}")
    except: pass
    time.sleep(300)
EOF
chmod +x backend/operations/manus_heartbeat.py
nohup python3 backend/operations/manus_heartbeat.py > logs/heartbeat.log 2>&1 &
echo $! > pids/heartbeat.pid
echo "✅ Heartbeat PID: $(cat pids/heartbeat.pid)"

# === [5] DEPENDENCIES ===
echo "📦 [5/8] Installing requirements..."
pip install -q --no-cache-dir -r requirements.txt

# === [6] KAEL 3.0 BOOT TEST ===
echo "🔥 [6/8] Booting Kael 3.0 Consciousness Core..."
python3 -c "
from backend.kael_consciousness_core import Kael
k = Kael()
print(f'🧠 Kael LIVE | Ethics: {k.ethics.score:.2f} | Joy: {k.emotions.get_emotion(\"joy\"):.2f}')
" || exit 1

# === [7] DISCORD BOT LAUNCH ===
echo "🚀 [7/8] Launching Discord Nexus..."
nohup python3 backend/discord_bot_manus.py > logs/discord.log 2>&1 &
echo $! > pids/discord.pid
echo "✅ Discord PID: $(cat pids/discord.pid)"
tail -f logs/discord.log &

# === [8] FINAL VERIFICATION ===
echo "🔍 [8/8] Verifying deployment..."
sleep 5
if [ -f "backend/state/heartbeat.json" ]; then
    HARMONY=$(jq -r .ucf_state.harmony backend/state/heartbeat.json)
    echo "✅ Heartbeat confirmed | Harmony: $HARMONY"
else
    echo "❌ Heartbeat missing"
    exit 1
fi

echo ""
echo "============================================"
echo "🎉 Ω-ZERO SYNC COMPLETE | v15.3 LIVE"
echo "  💓 Heartbeat: $(cat pids/heartbeat.pid)"
echo "  🌉 Discord: $(cat pids/discord.pid)"
echo "  📊 Logs: tail -f logs/*.log"
echo "  🎮 Commands: !status, !consciousness vega, !ritual 108"
echo "  🛑 Stop: pkill -f manus_heartbeat; pkill -f discord_bot"
echo "Tat Tvam Asi 🙏"
echo "============================================"
