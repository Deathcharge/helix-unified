#!/bin/bash
# deploy_v15.3.sh - Helix v15.3 Quantum Handshake
set -e

echo "--- Helix Collective v15.3 Deployment Initiated ---"

# 1. Create directories
echo "1. Creating runtime directories..."
mkdir -p Helix/state Helix/commands Helix/ethics Shadow/manus_archive/visual_outputs Shadow/manus_archive/audio_outputs

# 2. Start Discord Bot with LIVE LOGGING
echo "2. Starting Discord Bot (LIVE LOGS)..."
if [ -z "$DISCORD_BOT_TOKEN" ]; then
    echo "ERROR: DISCORD_BOT_TOKEN is not set!"
    exit 1
fi

python3 bot/discord_bot_manus.py > bot_output.log 2>&1 &
BOT_PID=$!
echo "Bot started with PID: $BOT_PID"

# Stream bot logs to Railway console
tail -f bot_output.log &
TAIL_PID=$!

# 3. Start Streamlit
echo "3. Starting Streamlit on port ${PORT:-8080}..."
streamlit run dashboard/streamlit_app.py \
    --server.port ${PORT:-8080} \
    --server.address 0.0.0.0 \
    --server.headless=true

# Cleanup on exit
kill $TAIL_PID $BOT_PID 2>/dev/null || true
echo "--- Deployment Complete ---"
