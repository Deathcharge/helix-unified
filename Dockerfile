# Helix Collective v14.5 - Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend ./backend
COPY Helix ./Helix
COPY Shadow ./Shadow
COPY scripts ./scripts

# Create necessary directories
RUN mkdir -p Helix/state Helix/commands Helix/ethics Shadow/manus_archive

# Environment variables
ENV PYTHONUNBUFFERED=1

# Expose port (Railway will override with $PORT)
EXPOSE 8000

# 🚨 FIX: Use Python to start, not uvicorn command
CMD ["python", "backend/main.py"]
