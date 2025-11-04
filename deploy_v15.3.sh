#!/bin/bash
# deploy_v15.3.sh - Helix v15.3 Quantum Handshake
set -e

echo "--- Helix Collective v15.3 Deployment Initiated ---"

# 0. CRITICAL: Verify pycryptodome is installed
echo "0. Verifying Crypto dependencies..."
python3 -c "import Cryptodome; print('✅ Cryptodome version:', Cryptodome.__version__)" || {
    echo "❌ CRITICAL: pycryptodome not found! Installing now..."
    pip install --force-reinstall pycryptodome
}
python3 -c "from Cryptodome.Cipher import AES; print('✅ AES import successful')" || {
    echo "❌ CRITICAL: Cryptodome.Cipher.AES import failed!"
    exit 1
}

# 1. Create directories
echo "1. Creating runtime directories..."
mkdir -p Helix/state Helix/commands Helix/ethics Shadow/manus_archive/visual_outputs Shadow/manus_archive/audio_outputs

# 2. Start Discord Bot (only if RUN_BOT is not set to "false")
if [ "${RUN_BOT:-true}" != "false" ]; then
    echo "2. Starting Discord Bot (LIVE LOGS)..."
    # Use DISCORD_TOKEN (Railway variable name) or DISCORD_BOT_TOKEN as fallback
    TOKEN="${DISCORD_TOKEN:-$DISCORD_BOT_TOKEN}"
    if [ -z "$TOKEN" ]; then
        echo "WARNING: DISCORD_TOKEN is not set - skipping bot startup"
    else
        python3 bot/discord_bot_manus.py > bot_output.log 2>&1 &
        BOT_PID=$!
        echo "Bot started with PID: $BOT_PID"

        # Stream bot logs to Railway console
        tail -f bot_output.log &
        TAIL_PID=$!
    fi
else
    echo "2. Skipping Discord Bot (RUN_BOT=false)"
fi

# 3. Start Streamlit
echo "3. Starting Streamlit on port ${PORT:-8080}..."
streamlit run dashboard/streamlit_app.py \
    --server.port ${PORT:-8080} \
    --server.address 0.0.0.0 \
    --server.headless=true

# Cleanup on exit
if [ -n "$TAIL_PID" ]; then kill $TAIL_PID 2>/dev/null || true; fi
if [ -n "$BOT_PID" ]; then kill $BOT_PID 2>/dev/null || true; fi
echo "--- Deployment Complete ---"
