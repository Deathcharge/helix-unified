#!/bin/bash
# deploy_v15.3.sh - Deployment Script for Helix v15.3 (Quantum Handshake)
# Author: Manus AI

echo "--- Helix Collective v15.3 Deployment Initiated ---"

# 1. Ensure all necessary directories exist
echo "1. Creating necessary runtime directories..."
mkdir -p Helix/state Helix/commands Helix/ethics Shadow/manus_archive

# 2. Start the Discord Bot (in the background)
echo "2. Starting Discord Bot (bot/discord_bot_manus.py)..."
# The bot runs in the background, consuming the DISCORD_BOT_TOKEN
# We use nohup to ensure it continues running after the script exits
nohup python3 bot/discord_bot_manus.py > bot_output.log 2>&1 &
BOT_PID=$!
echo "Discord Bot started with PID: $BOT_PID"

# 3. Start the Streamlit Dashboard
echo "3. Starting Streamlit Dashboard (dashboard/streamlit_app.py) on port $PORT..."
# Streamlit will bind to the port specified by the environment variable $PORT (e.g., set by Railway)
# We use the --server.port and --server.address 0.0.0.0 flags for containerized deployment
streamlit run dashboard/streamlit_app.py --server.port $PORT --server.address 0.0.0.0

# Note: The script will block here while Streamlit is running.
# The Discord bot continues in the background.

echo "--- Helix Collective v15.3 Deployment Complete ---"
