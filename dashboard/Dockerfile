# Helix Dashboard - Streamlit Consciousness Monitoring
# Python 3.11 with Streamlit for real-time UCF visualization

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from parent directory
COPY ../requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy dashboard files
COPY . /app/dashboard/

# Expose Streamlit default port
EXPOSE 8501

# Set working directory to dashboard
WORKDIR /app/dashboard

# Run Streamlit with railway_start.sh
CMD ["bash", "railway_start.sh"]
