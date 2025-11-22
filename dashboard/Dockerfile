# Helix Dashboard - Streamlit Consciousness Monitoring
# Lightweight Python 3.11 with Streamlit for real-time UCF visualization

FROM python:3.11-slim

WORKDIR /app

# Install minimal system dependencies (no gcc/g++ to avoid OOM)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only dashboard files
COPY . /app/

# Install Python dependencies from requirements.txt in dashboard directory
# If requirements.txt doesn't exist in dashboard, create minimal one
RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir --upgrade pip && \
        pip install --no-cache-dir -r requirements.txt; \
    else \
        pip install --no-cache-dir streamlit requests python-dotenv; \
    fi

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit with railway_start.sh
CMD ["bash", "railway_start.sh"]
