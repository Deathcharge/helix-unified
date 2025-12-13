#!/bin/bash
# Voice Patrol Setup Script
# Installs FFmpeg and verifies voice patrol dependencies

set -e

echo "🎙️ Helix Voice Patrol Setup"
echo "================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
else
    OS="unknown"
fi

echo "📋 Detected OS: $OS"
echo ""

# Install FFmpeg
echo "📦 Installing FFmpeg..."
if [ "$OS" == "linux" ]; then
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y ffmpeg
    elif command -v yum &> /dev/null; then
        sudo yum install -y ffmpeg
    else
        echo "❌ Unable to install FFmpeg automatically."
        echo "Please install FFmpeg manually."
        exit 1
    fi
elif [ "$OS" == "mac" ]; then
    if command -v brew &> /dev/null; then
        brew install ffmpeg
    else
        echo "❌ Homebrew not found. Please install from https://brew.sh"
        exit 1
    fi
fi

# Verify FFmpeg installation
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg installed:"
    ffmpeg -version | head -n 1
else
    echo "❌ FFmpeg installation failed"
    exit 1
fi

echo ""
echo "🐍 Checking Python dependencies..."

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Not in a virtual environment"
    echo "Consider running: python -m venv venv && source venv/bin/activate"
fi

# Install Python dependencies
echo "📦 Installing voice patrol dependencies..."
pip install -q aiohttp discord.py pydub

# Check for Google Cloud credentials
echo ""
echo "🔑 Checking Google Cloud credentials..."
if [ -z "$GOOGLE_CLOUD_TTS_API_KEY" ] && [ -z "$GOOGLE_CLOUD_TTS_KEY_PATH" ]; then
    echo "⚠️  Warning: Google Cloud TTS credentials not found"
    echo "Set one of these environment variables:"
    echo "  - GOOGLE_CLOUD_TTS_API_KEY"
    echo "  - GOOGLE_CLOUD_TTS_KEY_PATH"
else
    echo "✅ Google Cloud credentials found"
fi

# Check for voice processor URL
echo ""
echo "🌐 Checking voice processor service..."
if [ -z "$VOICE_PROCESSOR_URL" ]; then
    echo "⚠️  Warning: VOICE_PROCESSOR_URL not set"
    echo "Using default: http://localhost:8001"
    export VOICE_PROCESSOR_URL="http://localhost:8001"
else
    echo "✅ Voice processor URL: $VOICE_PROCESSOR_URL"
fi

# Test voice processor health
echo ""
echo "🏥 Testing voice processor service..."
if curl -f -s "$VOICE_PROCESSOR_URL/health" > /dev/null; then
    echo "✅ Voice processor service is healthy"
else
    echo "⚠️  Voice processor service not responding"
    echo "Make sure to start it with:"
    echo "  cd backend/voice_processor"
    echo "  uvicorn main:app --port 8001"
fi

# Create cache directory
echo ""
echo "📁 Creating TTS cache directory..."
mkdir -p /tmp/helix_tts_cache
echo "✅ Cache directory created: /tmp/helix_tts_cache"

# Summary
echo ""
echo "================================"
echo "✅ Voice Patrol Setup Complete!"
echo "================================"
echo ""
echo "📝 Next steps:"
echo "  1. Start voice processor: cd backend/voice_processor && uvicorn main:app --port 8001"
echo "  2. Start Discord bot: python discord-bot/main.py"
echo "  3. Join a voice channel and run: !voice-join sentinel"
echo ""
echo "📚 Documentation: docs/VOICE_PATROL_GUIDE.md"
echo ""
