# 🚀 Helix Collective - Complete Setup Guide

## Complete Checklist for Running ALL Features

This guide documents **every** API key, environment variable, and system requirement needed to run Helix Collective at full capacity. Use this when setting up accounts en masse for complete system testing.

---

## 📋 Quick Reference: What You Need

### Mandatory (Core Functionality)
- ✅ Discord Developer Account → `DISCORD_BOT_TOKEN`
- ✅ Random secret keys → `API_SECRET_KEY`, `JWT_SECRET`
- ✅ Database (PostgreSQL or SQLite) → `DATABASE_URL`
- ✅ At least ONE LLM API (OpenAI OR Anthropic)

### Voice Features 🎙️
- Google Cloud Platform account → `GOOGLE_CLOUD_TTS_*`
- OR ElevenLabs account → `ELEVENLABS_API_KEY`

### Advanced Features
- Redis (caching) → `REDIS_URL`
- Stability AI / Replicate (images) → API keys
- Backblaze/MEGA/Nextcloud (storage) → credentials
- Perplexity (multi-LLM) → API key

---

## 🎯 Complete Environment Variables List

Copy to `.env` file:

```bash
# ============================================
# CORE - Required for basic functionality
# ============================================

# Discord Bot
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_CLIENT_ID=your_discord_client_id
DISCORD_GUILD_ID=your_discord_guild_id
DISCORD_PREFIX=!

# API Server
API_HOST=0.0.0.0
API_PORT=8000
API_SECRET_KEY=generate_random_32_chars_minimum
JWT_SECRET=generate_random_32_chars_minimum
API_DEBUG=false

# Database (Required for persistence)
DATABASE_URL=postgresql://user:pass@localhost:5432/helix_unified
# Railway: Use ${{Postgres.DATABASE_URL}}
# Local testing: sqlite:///helix_unified.db

# Redis (Required for caching)
REDIS_URL=redis://localhost:6379
# Railway: Use ${{Redis.REDIS_URL}}

# ============================================
# AI & LLM - At least ONE required
# ============================================

# OpenAI (GPT models, DALL-E, TTS)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7

# Anthropic Claude (Consciousness processing)
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-3-sonnet-20240229
CLAUDE_MAX_TOKENS=4000
CLAUDE_TEMPERATURE=0.7

# Perplexity (Optional - Web-augmented AI)
PERPLEXITY_API_KEY=pplx-...

# ============================================
# VOICE & AUDIO - Required for Voice Patrol
# ============================================

# Google Cloud TTS/STT (Recommended)
GOOGLE_CLOUD_TTS_API_KEY=...
GOOGLE_CLOUD_TTS_KEY_PATH=/app/google-cloud-key.json
GOOGLE_CLOUD_PROJECT_ID=your_project_id
GOOGLE_CLOUD_TTS_VOICE=en-US-Standard-C
GOOGLE_CLOUD_TTS_LANGUAGE_CODE=en-US
TTS_PROVIDER=google_cloud

# ElevenLabs TTS (Alternative)
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=...
# Set TTS_PROVIDER=elevenlabs to use this

# AssemblyAI (Speech-to-Text)
ASSEMBLYAI_API_KEY=...

# Voice Configuration
VOICE_AUTO_JOIN=false
VOICE_TIMEOUT=300
MAX_VOICE_CONNECTIONS=10
VOICE_PROCESSOR_URL=http://localhost:8001
# Railway: http://voice-processor.railway.internal:8001

# ============================================
# IMAGE GENERATION - Optional
# ============================================

# Stability AI (Stable Diffusion)
STABILITY_API_KEY=...

# Replicate (Multiple AI models)
REPLICATE_API_KEY=...

# ============================================
# CLOUD STORAGE - Optional
# ============================================

# Backblaze B2 / AWS S3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-west-002
S3_BUCKET_NAME=helix-storage

# Nextcloud WebDAV
NEXTCLOUD_URL=https://nextcloud.example.com
NEXTCLOUD_USERNAME=...
NEXTCLOUD_PASSWORD=...

# MEGA Cloud Storage
MEGA_EMAIL=...
MEGA_PASSWORD=...

# ============================================
# INTEGRATIONS - Partially Implemented
# ============================================

# Notion (⚠️ API calls are placeholders)
NOTION_API_KEY=secret_...
NOTION_DATABASE_ID=...

# Zapier (⚠️ Notifications incomplete)
WEBHOOK_SECRET=...
WEBHOOK_URL=https://hooks.zapier.com/...

# ============================================
# RAILWAY DEPLOYMENT
# ============================================

RAILWAY_TOKEN=...
RAILWAY_PROJECT_ID=...

# Microservice Databases (use shared Postgres)
AGENT_ORCHESTRATOR_DB=${{Postgres.DATABASE_URL}}
VOICE_PROCESSOR_DB=${{Postgres.DATABASE_URL}}
WEBSOCKET_SERVICE_DB=${{Postgres.DATABASE_URL}}
ZAPIER_SERVICE_DB=${{Postgres.DATABASE_URL}}

# ============================================
# MONITORING & LOGGING
# ============================================

LOG_LEVEL=INFO
LOG_FILE=logs/helix_unified.log
LOG_JSON=false
PERFORMANCE_MONITORING_ENABLED=true
METRICS_RETENTION_HOURS=24

# ============================================
# RATE LIMITING & AGENT CONFIG
# ============================================

RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=1000
MAX_AGENTS=16
DEFAULT_AGENT_PERSONALITY=friendly
AGENT_RESPONSE_TIMEOUT=30
```

---

## 🏗️ System Dependencies

### Included in Dockerfile ✅
- `ffmpeg` (audio/video processing)
- `gcc`, `g++` (C compilation for Python packages)
- `gfortran` (Fortran for NumPy/SciPy)
- `libblas-dev`, `liblapack-dev` (linear algebra libraries)

### Local Development Setup

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y ffmpeg gcc g++ gfortran libblas-dev liblapack-dev python3.11 python3.11-venv
```

**macOS:**
```bash
brew install ffmpeg gcc python@3.11
```

**Windows:**
- Install Python 3.11 from python.org
- Download ffmpeg from https://ffmpeg.org/download.html
- Add ffmpeg to PATH

---

## 📦 Python Dependencies

### Always Installed (requirements.txt)
```bash
pip install -r requirements.txt
```

**Core packages:**
- `fastapi==0.115.6`, `uvicorn==0.30.5`
- `discord.py>=2.3.2`
- `openai`, `anthropic>=0.39.0`
- `streamlit==1.40.0`

**Data Science:**
- `numpy`, `pandas`, `scipy`
- `scikit-learn>=1.3.0` ✅ **NOW INCLUDED**
- `prophet`, `cmdstanpy` ✅ **NOW INCLUDED**

**Media:**
- `Pillow`, `librosa`, `soundfile`
- `pydub==0.25.1` ✅ **NOW INCLUDED** (requires ffmpeg)

**Cloud Storage:**
- `boto3>=1.28.0` ✅ **NOW INCLUDED**
- `webdav3>=3.14.0` ✅ **NOW INCLUDED**
- `mega.py`, `pycryptodome`

### Optional: Music Generation (Commented Out)

**⚠️ WARNING:** Requires ~2GB download + high RAM usage!

```bash
# Uncomment in requirements.txt:
torch>=2.0.0
transformers>=4.30.0

# Then install (CPU version)
pip install torch transformers --index-url https://download.pytorch.org/whl/cpu
```

**Not recommended for Railway** (OOM risk). Use Linode/VPS for music features.

---

## 🎮 Account Setup Guide

### 1. Discord Developer Account
1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Name it "Helix Collective"
4. Go to "Bot" tab → "Add Bot"
5. Copy `DISCORD_BOT_TOKEN`
6. Enable "Message Content Intent", "Server Members Intent", "Presence Intent"
7. Go to "OAuth2" → Copy `DISCORD_CLIENT_ID`
8. Invite bot to server with `bot` and `applications.commands` scopes

### 2. OpenAI Platform
1. Go to https://platform.openai.com/signup
2. Add payment method (required for API access)
3. Go to https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Copy `OPENAI_API_KEY` (starts with `sk-`)

### 3. Anthropic Claude
1. Go to https://console.anthropic.com/
2. Sign up / log in
3. Go to "API Keys" → "Create Key"
4. Copy `ANTHROPIC_API_KEY` (starts with `sk-ant-`)

### 4. Google Cloud Platform (Voice Features)
1. Go to https://console.cloud.google.com/
2. Create new project
3. Enable APIs:
   - Cloud Text-to-Speech API
   - Cloud Speech-to-Text API
4. Create service account:
   - IAM & Admin → Service Accounts → Create
   - Grant roles: "Cloud Speech Administrator", "Cloud Text-to-Speech Admin"
5. Create key (JSON format)
6. Download key file → set `GOOGLE_CLOUD_TTS_KEY_PATH`
7. Copy project ID → set `GOOGLE_CLOUD_PROJECT_ID`

### 5. Railway (Deployment)
1. Go to https://railway.app/
2. Sign up with GitHub
3. Create new project
4. Add services:
   - PostgreSQL (database)
   - Redis (caching)
   - Helix Backend (your repo)
5. Copy API token from Account Settings → Tokens
6. Set `RAILWAY_TOKEN`

### 6. Optional: Additional Services

**ElevenLabs (Alternative TTS):**
- https://elevenlabs.io/
- Create account → API Key → Copy

**Stability AI (Image Generation):**
- https://platform.stability.ai/
- Create account → API Keys → Create

**Replicate (AI Models):**
- https://replicate.com/
- Sign up → Account → API Tokens

**Backblaze B2 (Storage):**
- https://www.backblaze.com/b2/cloud-storage.html
- Create account → App Keys → Create

**Notion (Sync - ⚠️ Incomplete):**
- https://www.notion.so/my-integrations
- Create integration → Copy token

---

## 🚂 Railway Deployment

### Quick Deploy Button
Click to deploy entire stack:
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

### Manual Deployment

1. **Add PostgreSQL database:**
   - Railway Dashboard → Add Service → Database → PostgreSQL
   - Copy `DATABASE_URL` from Variables tab

2. **Add Redis:**
   - Add Service → Database → Redis
   - Copy `REDIS_URL` from Variables tab

3. **Deploy main backend:**
   - Add Service → GitHub Repo → Select `helix-unified`
   - Set environment variables (see above)
   - Build command: `pip install -r requirements.txt`
   - Start command: `python backend/main.py`

4. **Deploy dashboard (optional):**
   - Add Service → GitHub Repo → Select `helix-unified`
   - Root directory: `/dashboard`
   - Set `HELIX_MODE=streamlit`
   - Start command: `bash railway_start.sh`

### Environment Variable Setup in Railway

Use Railway's variable referencing:
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
API_HOST=0.0.0.0
PORT=${{PORT}}  # Railway auto-assigns
```

---

## 🖥️ Platform Comparison Matrix

| Feature | Railway | Linode VPS | Vercel | Streamlit Cloud |
|---------|---------|------------|--------|-----------------|
| Discord Bot | ✅ | ✅ | ❌ | ❌ |
| FastAPI Backend | ✅ | ✅ | ⚠️ Serverless only | ❌ |
| Voice Patrol | ✅ | ✅ | ❌ | ❌ |
| Grok Analytics | ✅ | ✅ | ❌ | ✅ Read-only |
| Music Generation | ❌ OOM | ✅ | ❌ | ❌ |
| Streamlit Dashboard | ✅ | ✅ | ❌ | ✅ |
| WebSockets | ✅ | ✅ | ❌ | ❌ |
| Databases | ✅ Managed | ✅ Self-hosted | ❌ | ❌ |
| ffmpeg Support | ✅ | ✅ | ❌ | ❌ |
| Cost (Monthly) | $5-20 | $5-60 | $0-20 | $0-200 |

**Recommendation:**
- **Railway:** Best for 90% of features (recommended)
- **Linode VPS:** Only if you need music generation or custom ML models
- **Vercel:** Frontend/API gateway only
- **Streamlit Cloud:** Public dashboard only

---

## ✅ Testing Your Setup

### 1. Validate Environment
```bash
python -c "from backend.core.env_validator import validate_environment; validate_environment()"
```

### 2. Test Dependencies
```bash
# Test Prophet (time series forecasting)
python -c "from prophet import Prophet; print('✅ Prophet installed')"

# Test scikit-learn
python -c "from sklearn.linear_model import LinearRegression; print('✅ scikit-learn installed')"

# Test ffmpeg
ffmpeg -version
```

### 3. Test Discord Bot
```bash
python bot/discord_bot_manus.py
```
Should see: `✅ Logged in as Helix#1234`

### 4. Test Backend API
```bash
python backend/main.py
```
Visit: http://localhost:8000/docs

### 5. Test Grok Agent
```bash
python -c "from grok.grok_agent_core import GrokAgentCore; agent = GrokAgentCore(); print(agent.analyze_ucf_trends())"
```

### 6. Test Voice Features
```bash
python -c "from backend.tts_service import tts_service; print('TTS Available:', tts_service.available)"
```

---

## ⚠️ Known Limitations

See **[KNOWN_LIMITATIONS.md](./KNOWN_LIMITATIONS.md)** for full list.

**Critical issues:**
1. ❌ **Prophet library** was commented out → ✅ **FIXED** (now in requirements.txt)
2. ❌ **scikit-learn** missing → ✅ **FIXED** (now in requirements.txt)
3. ❌ **ffmpeg** not in Dockerfile → ✅ **FIXED** (added to all Dockerfiles)
4. ❌ **boto3/webdav3** missing → ✅ **FIXED** (added to requirements.txt)
5. ⚠️ **Notion API** returns placeholder responses (TODO: implement)
6. ⚠️ **Zapier webhooks** incomplete (TODO: implement)
7. ⚠️ **Railway monitoring** returns mock data (TODO: connect real API)
8. ⚠️ **Grok Agent** generates synthetic data (TODO: connect real archive)

---

## 🆘 Troubleshooting

### "ImportError: No module named 'prophet'"
✅ **FIXED!** Run: `pip install -r requirements.txt --upgrade`

### "ImportError: No module named 'sklearn'"
✅ **FIXED!** Run: `pip install -r requirements.txt --upgrade`

### "ffmpeg not found"
✅ **FIXED in Docker!** For local dev:
```bash
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg  # macOS
```

### "CRITICAL: cryptography not available"
```bash
pip install cryptography --upgrade
```

### "DATABASE_URL not set - database features disabled"
Add to `.env`:
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/helix
# OR for local testing:
DATABASE_URL=sqlite:///helix_unified.db
```

### "REDIS_URL not set - caching disabled"
Either:
1. Install Redis: `docker run -d -p 6379:6379 redis`
2. Or leave empty (performance impact only)

### Railway OOM Error
Comment out in `requirements.txt`:
```bash
# torch>=2.0.0
# transformers>=4.30.0
```

---

## 🎯 Minimal Test Setup

For quick testing without all accounts:

```bash
# Required minimum
DISCORD_BOT_TOKEN=<from Discord developer portal>
API_SECRET_KEY=<random 32 chars>
OPENAI_API_KEY=<from OpenAI platform>

# Optional (use defaults)
DATABASE_URL=sqlite:///helix_unified.db
REDIS_URL=  # Empty = caching disabled
```

**What works:**
- ✅ Discord bot (text commands)
- ✅ Basic API endpoints
- ✅ Grok Agent (with mock data)
- ✅ Streamlit dashboard (with mock data)

**What doesn't work:**
- ❌ Voice features (no Google Cloud)
- ❌ Cloud storage (no credentials)
- ❌ Image generation (no Stability AI)
- ❌ Music generation (not installed)

---

## 📞 Support Resources

- **Helix Issues:** Check [KNOWN_LIMITATIONS.md](./KNOWN_LIMITATIONS.md)
- **Railway Docs:** https://docs.railway.app/
- **Discord API:** https://discord.com/developers/docs
- **OpenAI Docs:** https://platform.openai.com/docs
- **Anthropic Docs:** https://docs.anthropic.com/

---

**Last Updated:** 2025-12-06  
**Version:** v17.0 - Post-Dependency Audit  
**All critical dependencies fixed!** ✅
