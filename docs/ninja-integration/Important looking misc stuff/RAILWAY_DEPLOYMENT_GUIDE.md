# Railway Deployment Guide - Service-Specific Environment Variables

## Overview
This guide maps environment variables to specific Railway services for optimal deployment architecture.

## 🏗️ Recommended Railway Service Architecture

### Service 1: Discord Bot (Main Application)
**Service Name**: `helix-discord-bot`  
**Entry Point**: `enhanced_agent_bot.py`  
**Purpose**: Main Discord bot with AI agents

### Service 2: FastAPI Backend
**Service Name**: `helix-api-backend`  
**Entry Point**: `main.py`  
**Purpose**: REST API for metrics, webhooks, and management

### Service 3: Database (Optional)
**Service Name**: `helix-database`  
**Type**: PostgreSQL or Railway's built-in database
**Purpose**: Persistent data storage

## 📋 Environment Variables by Service

### 🤖 Service 1: Discord Bot (`helix-discord-bot`)

#### Core Discord Configuration
```env
# Required - Discord Bot
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_CLIENT_ID=your_discord_client_id
DISCORD_GUILD_ID=your_primary_guild_id
DISCORD_PREFIX=!

# Bot Configuration
BOT_ID=helix_unified_bot
BOT_NAME=Helix Unified Bot
BOT_PERSONALITY=friendly
```

#### AI & LLM Configuration
```env
# Anthropic Claude (Required for AI responses)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
CLAUDE_MODEL=claude-3-sonnet-20240229
CLAUDE_MAX_TOKENS=4000
CLAUDE_TEMPERATURE=0.7

# OpenAI (Optional - for image generation and Whisper)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7
```

#### TTS Configuration (Choose at least one)
```env
# Google Cloud TTS (Recommended)
GOOGLE_CLOUD_TTS_API_KEY=your_google_cloud_tts_api_key_here
GOOGLE_CLOUD_TTS_KEY_PATH=/app/google-cloud-key.json
GOOGLE_CLOUD_PROJECT_ID=your_project_id
GOOGLE_CLOUD_TTS_VOICE=en-US-Standard-C
GOOGLE_CLOUD_TTS_LANGUAGE_CODE=en-US
TTS_PROVIDER=google_cloud

# ElevenLabs TTS (Alternative)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=your_voice_id_here

# AWS Polly TTS (Alternative)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
```

#### Image Generation (Optional)
```env
# Stability AI (Stable Diffusion)
STABILITY_API_KEY=your_stability_ai_api_key_here

# Replicate (Multiple models)
REPLICATE_API_KEY=your_replicate_api_key_here
```

#### Voice Transcription (Optional)
```env
# AssemblyAI
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
```

#### Logging & Monitoring
```env
LOG_LEVEL=INFO
LOG_FILE=logs/helix_unified.log
LOG_JSON=false
```

#### Performance Settings
```env
PERFORMANCE_MONITORING_ENABLED=true
METRICS_RETENTION_HOURS=24
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=1000
```

#### Agent Configuration
```env
MAX_AGENTS=16
DEFAULT_AGENT_PERSONALITY=friendly
AGENT_RESPONSE_TIMEOUT=30
```

#### Voice Configuration
```env
VOICE_AUTO_JOIN=false
VOICE_TIMEOUT=300
MAX_VOICE_CONNECTIONS=10
```

---

### 🌐 Service 2: FastAPI Backend (`helix-api-backend`)

#### API Configuration
```env
# API Server
API_HOST=0.0.0.0
API_PORT=8000
API_SECRET_KEY=your_secret_key_here
API_DEBUG=false

# CORS Settings
CORS_ORIGINS=["https://yourdomain.com"]
```

#### Database Configuration
```env
# Database URL (use Railway's DATABASE_URL if using their PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database
# Or for SQLite in development
# DATABASE_URL=sqlite:///helix_unified.db
```

#### Webhook Configuration
```env
WEBHOOK_SECRET=your_webhook_secret_here
WEBHOOK_URL=your_webhook_url_here
```

#### Monitoring & Metrics
```env
PERFORMANCE_MONITORING_ENABLED=true
METRICS_RETENTION_HOURS=24
LOG_LEVEL=INFO
LOG_FILE=logs/api.log
```

#### Rate Limiting
```env
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=1000
```

---

### 🗄️ Service 3: Database (If using Railway PostgreSQL)

Railway will automatically provide:
```env
DATABASE_URL=postgresql://...
PGHOST=...
PGPORT=...
PGUSER=...
PGPASSWORD=...
PGDATABASE=...
```

**Note**: These are automatically injected by Railway when you add a PostgreSQL database.

---

## 🔗 Shared Variables (Optional)

If you want to share variables across services, create a **Shared Variables** group in Railway:

### Shared Group: `helix-shared`
```env
# Logging
LOG_LEVEL=INFO
LOG_JSON=false

# Performance
PERFORMANCE_MONITORING_ENABLED=true
METRICS_RETENTION_HOURS=24

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=1000
```

Then reference this group in both services.

---

## 📊 Variable Priority Matrix

| Variable | Discord Bot | API Backend | Database | Priority |
|----------|-------------|-------------|----------|----------|
| DISCORD_BOT_TOKEN | ✅ Required | ❌ | ❌ | Critical |
| ANTHROPIC_API_KEY | ✅ Required | ❌ | ❌ | Critical |
| OPENAI_API_KEY | ⚠️ Optional | ❌ | ❌ | Medium |
| GOOGLE_CLOUD_TTS_API_KEY | ⚠️ Optional | ❌ | ❌ | Medium |
| DATABASE_URL | ✅ Required | ✅ Required | ✅ Auto | Critical |
| API_SECRET_KEY | ❌ | ✅ Required | ❌ | Critical |
| WEBHOOK_SECRET | ⚠️ Optional | ✅ Required | ❌ | Medium |
| LOG_LEVEL | ✅ | ✅ | ❌ | Low |

**Legend:**
- ✅ Required: Service needs this to function
- ⚠️ Optional: Enables additional features
- ❌ Not needed: Service doesn't use this

---

## 🚀 Deployment Steps

### Step 1: Create Services in Railway

1. **Create Discord Bot Service**
   ```bash
   # In Railway dashboard
   New Service → GitHub Repo → Select helix-unified
   Service Name: helix-discord-bot
   Start Command: python enhanced_agent_bot.py
   ```

2. **Create API Backend Service**
   ```bash
   # In Railway dashboard
   New Service → GitHub Repo → Select helix-unified
   Service Name: helix-api-backend
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. **Add PostgreSQL Database** (Optional)
   ```bash
   # In Railway dashboard
   New → Database → PostgreSQL
   ```

### Step 2: Configure Environment Variables

#### For Discord Bot Service:
1. Go to `helix-discord-bot` service
2. Click "Variables" tab
3. Add all variables from "Service 1: Discord Bot" section above
4. Click "Deploy"

#### For API Backend Service:
1. Go to `helix-api-backend` service
2. Click "Variables" tab
3. Add all variables from "Service 2: FastAPI Backend" section above
4. Click "Deploy"

### Step 3: Configure Networking

1. **API Backend**: Enable public networking to get a URL
2. **Discord Bot**: No public networking needed (connects to Discord)
3. **Database**: Private networking only (accessed by services)

### Step 4: Deploy

1. Push code to GitHub
2. Railway will auto-deploy both services
3. Monitor logs for any errors
4. Test Discord bot functionality

---

## 🔧 Service-Specific Configuration Files

### Discord Bot Service (`railway.json`)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python enhanced_agent_bot.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### API Backend Service (`railway.api.json`)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## 🎯 Minimal Configuration (Quick Start)

If you want to get started quickly with minimal features:

### Discord Bot (Minimal)
```env
# Required only
DISCORD_BOT_TOKEN=your_token
ANTHROPIC_API_KEY=your_key
DATABASE_URL=sqlite:///helix_unified.db
LOG_LEVEL=INFO
```

### API Backend (Minimal)
```env
# Required only
API_SECRET_KEY=your_secret
DATABASE_URL=sqlite:///helix_unified.db
API_PORT=8000
LOG_LEVEL=INFO
```

---

## 🔐 Security Best Practices

### 1. Use Railway's Secret Variables
- Mark sensitive variables as "secret" in Railway
- Never commit secrets to GitHub
- Rotate keys regularly

### 2. Separate Environments
```
Production: helix-unified-prod
Staging: helix-unified-staging
Development: helix-unified-dev
```

### 3. Database Security
- Use Railway's private networking
- Enable SSL connections
- Regular backups

### 4. API Security
- Use strong API_SECRET_KEY
- Enable rate limiting
- Use HTTPS only

---

## 📈 Scaling Recommendations

### Small Server (<1000 users)
- **Discord Bot**: 1 instance, 512MB RAM
- **API Backend**: 1 instance, 256MB RAM
- **Database**: Shared PostgreSQL

### Medium Server (1000-10000 users)
- **Discord Bot**: 2 instances, 1GB RAM each
- **API Backend**: 2 instances, 512MB RAM each
- **Database**: Dedicated PostgreSQL

### Large Server (>10000 users)
- **Discord Bot**: 3+ instances, 2GB RAM each
- **API Backend**: 3+ instances, 1GB RAM each
- **Database**: High-performance PostgreSQL with replicas

---

## 🐛 Troubleshooting

### Discord Bot Won't Start
1. Check `DISCORD_BOT_TOKEN` is correct
2. Verify `ANTHROPIC_API_KEY` is valid
3. Check logs: `railway logs helix-discord-bot`

### API Backend Issues
1. Verify `DATABASE_URL` is correct
2. Check `API_SECRET_KEY` is set
3. Ensure port is correct: `$PORT` variable

### Database Connection Errors
1. Check `DATABASE_URL` format
2. Verify database service is running
3. Check private networking is enabled

### High Memory Usage
1. Reduce `MAX_AGENTS` value
2. Lower `METRICS_RETENTION_HOURS`
3. Disable unused features

---

## 📞 Support

For Railway-specific issues:
- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

For Helix Unified issues:
- Check logs in Railway dashboard
- Review SECURITY.md for security issues
- Check DEVELOPMENT_SETUP.md for setup help

---

## ✅ Deployment Checklist

Before deploying to production:

- [ ] All required environment variables set
- [ ] Database configured and accessible
- [ ] API keys validated and working
- [ ] Logs configured and accessible
- [ ] Rate limiting enabled
- [ ] Monitoring enabled
- [ ] Backup strategy in place
- [ ] Secrets properly secured
- [ ] Services can communicate
- [ ] Health checks passing

---

**Your Railway deployment is now configured for optimal performance and security! 🚀**