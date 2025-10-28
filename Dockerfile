# Helix Collective v15.2 - Backend Dockerfile (CONFLICT RESOLVED - MemeSync + Analytics)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Grok's analytics libraries (scikit-learn, tensorflow, prophet)
RUN apt-get update && apt-get install -y \
    gcc g++ curl \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# CRITICAL FIX: Install pycryptodome FIRST to avoid conflicts
RUN pip install --no-cache-dir pycryptodome

# Install Python dependencies (mega.py might try to install pycrypto)
RUN pip install --no-cache-dir -r requirements.txt

# FORCE: Remove any pycrypto that snuck in, reinstall pycryptodome
RUN pip uninstall -y pycrypto || true
RUN pip install --no-cache-dir --force-reinstall pycryptodome

# Verify installation (this will appear in build logs)
RUN python3 -c "import Cryptodome; print('✅ Cryptodome installed:', Cryptodome.__version__)"
RUN python3 -c "from Cryptodome.Cipher import AES; print('✅ AES import works')"

# Ensure prophet dependency
RUN pip install cmdstanpy==1.2.2

# Copy application code for v15.2 structure (MERGED: MemeSync + Main)
COPY backend ./backend
COPY bot ./bot
COPY dashboard ./dashboard
COPY grok ./grok
COPY Shadow ./Shadow
COPY scripts ./scripts

# Copy root-level sync modules (CRITICAL: bot imports these!)
COPY mega_sync.py .
COPY mega_sync2.py .
COPY sync.py .
COPY fix_crypto_imports.py .

# Copy MemeSync artifacts (from manus/memesync-v15.2 branch)
COPY test_discord_commands.py .

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

# HYBRID DEPLOYMENT: Support both FastAPI backend AND Streamlit dashboard
# Railway can choose which to run via environment variable
# Default: FastAPI backend (for API endpoints)
# Set HELIX_MODE=streamlit to run Streamlit instead
CMD ["bash", "-c", "if [ \"$HELIX_MODE\" = \"streamlit\" ]; then bash deploy_v15.3.sh; else python backend/main.py; fi"]
