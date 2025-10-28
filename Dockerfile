# Helix Collective v14.5 - Backend Dockerfile (FIXED)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Grok's analytics libraries (scikit-learn, tensorflow, prophet)
RUN apt-get update && apt-get install -y \
    gcc g++ curl \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install cmdstanpy==1.2.2  # Ensure prophet dependency

# Fix: Remove broken pycrypto, use pycryptodome
RUN pip uninstall -y pycrypto || true
RUN pip install pycryptodome

# Copy application code for v15.3 structure
COPY bot ./bot
COPY dashboard ./dashboard
COPY grok ./grok
COPY Shadow ./Shadow
COPY scripts ./scripts

# Create runtime directories (app will use these)
RUN mkdir -p Helix/state Helix/commands Helix/ethics Shadow/manus_archive/visual_outputs Shadow/manus_archive/audio_outputs Shadow/manus_archive/cloud_mock

# Create default UCF state file
RUN echo '{"harmony":0.355,"resilience":0.82,"prana":0.67,"drishti":0.73,"klesha":0.24,"zoom":1.0}' > Helix/state/ucf_state.json

# Create default heartbeat file
RUN echo '{"timestamp":"2025-10-22T00:00:00Z","status":"initialized","phase":3}' > Helix/state/heartbeat.json

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/backend:/app/grok:/app/bot:/app/dashboard:$PYTHONPATH

# Expose port (Railway will override with $PORT)
EXPOSE 8000

# Copy deployment script (in repo root)
COPY deploy_v15.3.sh .

# Make executable
RUN chmod +x deploy_v15.3.sh

# Start application (use deploy script for v15.3)
CMD ["bash", "deploy_v15.3.sh"]
