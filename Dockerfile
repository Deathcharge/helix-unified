# Helix Collective v16.8 - Backend Dockerfile (Helix Hub Production Release)
# CACHE BUSTER: Using exact Python version to force complete rebuild
FROM python:3.11.10-slim

WORKDIR /app

# Install system dependencies for Grok's analytics libraries (scikit-learn, tensorflow, prophet)
RUN apt-get update && apt-get install -y \
    gcc g++ curl \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements-backend.txt requirements.txt

# CRITICAL FIX: Install pycryptodome FIRST
RUN pip install --no-cache-dir pycryptodome

# Install mega.py WITHOUT dependencies (prevents pycrypto installation)
RUN pip install --no-cache-dir --no-deps mega.py

# Verify Cryptodome installation (pycryptodome imports as 'Crypto', not 'Cryptodome')
RUN python3 -c "import Crypto; print('✅ Cryptodome installed:', Crypto.__version__)"
RUN python3 -c "from Crypto.Cipher import AES; print('✅ AES import works')"

# Install lightweight dependencies first (reduces memory pressure)
RUN pip install --no-cache-dir \
    fastapi==0.115.6 \
    uvicorn[standard]==0.34.0 \
    python-dotenv==1.0.1 \
    jinja2==3.1.6 \
    aiofiles==23.2.1 \
    sse-starlette==2.2.1 \
    websockets==13.0

# Install API clients and utilities
RUN pip install --no-cache-dir \
    httpx==0.28.0 \
    aiohttp==3.12.14 \
    requests==2.32.4 \
    pyyaml==6.0.1 \
    toml==0.10.2 \
    python-multipart==0.0.18 \
    pydantic==2.10.3 \
    python-dateutil==2.8.2 \
    pytz==2024.1

# Install Discord and integrations
RUN pip install --no-cache-dir \
    discord.py==2.3.2 \
    anthropic==0.39.0 \
    notion-client==2.5.0

# Install monitoring and media
RUN pip install --no-cache-dir \
    sentry-sdk[fastapi]==2.19.0 \
    pydub==0.25.1 \
    Pillow==10.4.0 \
    loguru==0.7.2

# Install heavy ML dependencies LAST (one at a time to reduce memory spikes)
RUN pip install --no-cache-dir numpy==1.26.4
RUN pip install --no-cache-dir pandas==2.2.3
RUN pip install --no-cache-dir scikit-learn
RUN pip install --no-cache-dir cmdstanpy==1.2.2
RUN pip install --no-cache-dir prophet

# Install visualization libraries
RUN pip install --no-cache-dir \
    streamlit==1.40.0 \
    plotly==5.18.0

# CACHE BUSTER: Force rebuild from this point (v16.8 - 2025-11-07)
ARG REBUILD_TRIGGER=v16.8-20251107
ENV REBUILD_TRIGGER=${REBUILD_TRIGGER}

# Copy application code for v15.2 structure (MERGED: MemeSync + Main)
COPY backend ./backend
COPY bot ./bot
COPY dashboard ./dashboard
COPY grok ./grok
COPY Shadow ./Shadow
COPY scripts ./scripts
COPY templates ./templates
COPY config ./config
COPY content ./content
COPY .streamlit ./.streamlit

# Copy root-level sync modules (CRITICAL: bot imports these!)
# Note: crai_dataset.json is optional - enhanced_kavach.py handles missing file gracefully
COPY mega_sync.py .
COPY mega_sync2.py .
COPY sync.py .
COPY fix_crypto_imports.py .

# Copy discovery manifest for external AI agents (v16.7)
COPY helix-manifest.json .

# Copy configuration file (CRITICAL: required by backend/config_manager.py)
COPY helix_config.toml .

# MemeSync artifacts integrated into bot/discord_bot_manus.py

# Create runtime directories (app will use these)
RUN mkdir -p Helix/state Helix/commands Helix/ethics Shadow/manus_archive/visual_outputs Shadow/manus_archive/audio_outputs Shadow/manus_archive/cloud_mock

# Create default UCF state file
RUN echo '{"harmony":0.355,"resilience":0.82,"prana":0.67,"drishti":0.73,"klesha":0.24,"zoom":1.0}' > Helix/state/ucf_state.json

# Create default heartbeat file
RUN echo '{"timestamp":"2025-10-22T00:00:00Z","status":"initialized","phase":3}' > Helix/state/heartbeat.json

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/backend:/app/grok:/app/bot:/app/dashboard

# Expose port (Railway will override with $PORT)
EXPOSE 8000

# Copy deployment script (in repo root)
COPY deploy_v15.3.sh .

# Make executable
RUN chmod +x deploy_v15.3.sh

# HYBRID DEPLOYMENT: Support both FastAPI backend AND Streamlit dashboard
# Railway can choose which to run via environment variable
# Default: FastAPI backend (for API endpoints)
# Set HELIX_MODE=streamlit to run Streamlit instead
CMD ["bash", "-c", "if [ \"$HELIX_MODE\" = \"streamlit\" ]; then bash deploy_v15.3.sh; else python backend/main.py; fi"]
