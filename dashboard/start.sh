#!/bin/bash
# Helix Dashboard Startup Script
# Sets up Python path to include parent directory for grok module access

# Set PYTHONPATH to include parent directory
export PYTHONPATH=/app:$PYTHONPATH

# Start Streamlit
streamlit run streamlit_app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --theme.base=dark \
    --theme.primaryColor=#8A2BE2
