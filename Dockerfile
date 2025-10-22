# Helix Collective v14.5 - Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend ./backend
COPY scripts ./scripts

# Create necessary directories
RUN mkdir -p Helix/state Helix/commands Helix/ethics Shadow/manus_archive

# Expose port (Railway will override with $PORT)
EXPOSE 8000

# Run FastAPI app with dynamic port binding
# Uses Railway's PORT env var, falls back to 8000 for local development
CMD sh -c "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"
