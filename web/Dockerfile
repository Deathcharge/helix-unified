# Helix Consciousness Empire - Docker Configuration
# For helixspiral.work deployment

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy consciousness engine
COPY ../consciousness ./consciousness

# Copy web application
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data

# Expose port
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/api/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "helix_spiral_api:app", "--host", "0.0.0.0", "--port", "8000"]