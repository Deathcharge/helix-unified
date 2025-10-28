# Helix Collective v14.5 - Backend Dockerfile (FIXED for Railway)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt-get/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Create runtime directories (app will use these)
# The app creates these at startup, but we pre-create for safety
RUN mkdir -p Helix/state Helix/commands Helix/ethics Shadow/manus_archive

# Create default UCF state file
RUN echo '{"harmony":0.355,"resilience":0.82,"prana":0.67,"drishti":0.73,"klesha":0.24,"zoom":1.0}' > Helix/state/ucf_state.json

# Create default heartbeat file
RUN echo '{"timestamp":"2025-10-22T00:00:00Z","status":"initialized","phase":3}' > Helix/state/heartbeat.json

# Environment variables
ENV PYTHONUNBUFFERED=1

# Expose port (Railway will override with $PORT)
EXPOSE 8000

# Start application (using uvicorn directly for robustness)
# The main.py file uses os.getenv("PORT", 8000) to get the port, so we don't need to pass it here.
# CMD ["python", "backend/main.py"] is also correct as main.py calls uvicorn.run()
# I will stick to the original CMD since main.py handles the port logic correctly.
CMD ["python", "backend/main.py"]
