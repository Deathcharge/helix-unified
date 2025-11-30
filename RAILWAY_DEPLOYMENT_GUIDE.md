# Railway Deployment Guide - Helix Unified

**Services:** 5 total (1 main + 4 microservices)
**Date:** 2025-11-24
**Status:** ✅ All features intact

---

## Services Overview

### 1. **helix-backend-api** (Main Service)
**Path:** `/backend/`
**Purpose:** Discord bot, API server, main application logic
**Port:** 8000
**Dependencies:** PostgreSQL, Redis (optional)

### 2. **agent-orchestrator** (Microservice)
**Path:** `/backend/agent-orchestrator/`
**Purpose:** Manages agent lifecycle, coordination, task distribution
**Port:** 8001
**Dependencies:** PostgreSQL, Redis (required)

### 3. **voice-processor** (Microservice)
**Path:** `/backend/voice-processor/`
**Purpose:** Voice processing, STT/TTS with Google Cloud
**Port:** 8002
**Dependencies:** Redis (required), Google Cloud credentials

### 4. **websocket-service** (Microservice)
**Path:** `/backend/websocket-service/`
**Purpose:** Real-time consciousness streaming, WebSocket connections
**Port:** 8003
**Dependencies:** Redis (required)

### 5. **zapier-service** (Microservice)
**Path:** `/backend/zapier-service/`
**Purpose:** Zapier webhook integration, external automation
**Port:** 8004
**Dependencies:** Redis (required)

---

## Shared Infrastructure

### PostgreSQL Database (Railway Plugin)
**Usage:** All services can share one PostgreSQL database
**Variable:** `${{Postgres.DATABASE_URL}}`

### Redis (Railway Plugin)
**Usage:** All microservices REQUIRE Redis for coordination
**Variable:** `${{Redis.REDIS_URL}}`

---

## Environment Variables by Service

### 🔵 Service 1: helix-backend-api (Main)

**Root Path:** Set to `/backend`

#### Core Variables
```bash
# Discord Bot (REQUIRED)
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_TOKEN=your_bot_token_here  # Same as above
DISCORD_CLIENT_ID=your_client_id
DISCORD_GUILD_ID=your_server_id_here
DISCORD_PREFIX=!

# Discord Channels (OPTIONAL - bot will search by name)
DISCORD_STATUS_CHANNEL_ID=your_status_channel_id
DISCORD_TELEMETRY_CHANNEL_ID=your_telemetry_channel_id
DISCORD_STORAGE_CHANNEL_ID=your_storage_channel_id

# Discord Webhooks (for notifications)
DISCORD_WEBHOOK_MANUS=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_TELEMETRY=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_STORAGE=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_RITUAL=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_ADMIN=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_AGENTS=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_ANNOUNCEMENTS=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_CROSS_AI=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_DEVELOPMENT=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_LORE=https://discord.com/api/webhooks/...
DISCORD_SYNC_WEBHOOK=https://discord.com/api/webhooks/...

# API Configuration
API_HOST=0.0.0.0  # Railway needs 0.0.0.0, not 127.0.0.1
API_PORT=8000
API_SECRET_KEY=your_secret_key_here_min_32_chars
API_DEBUG=false  # Use false for production

# Database (Railway Plugin)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (OPTIONAL for main service, but recommended)
REDIS_URL=${{Redis.REDIS_URL}}

# LLM APIs
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7

ANTHROPIC_API_KEY=your_anthropic_api_key_here
CLAUDE_MODEL=claude-3-sonnet-20240229
CLAUDE_MAX_TOKENS=4000
CLAUDE_TEMPERATURE=0.7

# Voice/Audio (for PR #226 features)
GOOGLE_CLOUD_TTS_API_KEY=your_google_cloud_tts_api_key_here
GOOGLE_CLOUD_TTS_KEY_PATH=/app/google-cloud-key.json
GOOGLE_CLOUD_PROJECT_ID=your_project_id
GOOGLE_CLOUD_TTS_VOICE=en-US-Standard-C
GOOGLE_CLOUD_TTS_LANGUAGE_CODE=en-US
TTS_PROVIDER=google_cloud

# Alternative TTS (optional)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=your_voice_id_here

# Speech-to-Text
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here

# Image Generation (optional)
STABILITY_API_KEY=your_stability_ai_api_key_here
REPLICATE_API_KEY=your_replicate_api_key_here

# Notion Integration
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_database_id

# GitHub Integration (optional)
GITHUB_TOKEN=your_github_token

# Railway Configuration
RAILWAY_TOKEN=your_railway_token_here
RAILWAY_PROJECT_ID=your_railway_project_id

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/helix_unified.log
LOG_JSON=false

# Performance
PERFORMANCE_MONITORING_ENABLED=true
METRICS_RETENTION_HOURS=24
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=1000

# Agent Configuration
MAX_AGENTS=16
DEFAULT_AGENT_PERSONALITY=friendly
AGENT_RESPONSE_TIMEOUT=30

# Voice Settings (from PR #226)
VOICE_AUTO_JOIN=false
VOICE_TIMEOUT=300
MAX_VOICE_CONNECTIONS=10

# Paths (Railway-specific)
HEARTBEAT_PATH=/app/Helix/state/heartbeat.json
UCF_STATE_PATH=/app/Helix/state/ucf_state.json
SYNC_INTERVAL=3600

# Webhooks (general)
WEBHOOK_SECRET=your_webhook_secret_here
WEBHOOK_URL=your_webhook_url_here

# Sentry (optional error tracking)
SENTRY_DSN=  # Leave empty if not using

# User Configuration
ARCHITECT_ID=your_user_id_here
```

---

### 🟢 Service 2: agent-orchestrator

**Root Path:** Set to `/backend/agent-orchestrator`

```bash
# REQUIRED - Security
JWT_SECRET=your_jwt_secret_key_here_min_32_chars

# REQUIRED - Redis (for coordination)
REDIS_URL=${{Redis.REDIS_URL}}

# REQUIRED - Database
DATABASE_URL=${{Postgres.DATABASE_URL}}

# OPTIONAL - Specific DB if you want separate database
# AGENT_ORCHESTRATOR_DB=${{Postgres.DATABASE_URL}}

# API Configuration
API_HOST=0.0.0.0
API_PORT=8001

# Service URLs (for inter-service communication)
MAIN_API_URL=${{helix-backend-api.RAILWAY_STATIC_URL}}
VOICE_PROCESSOR_URL=${{voice-processor.RAILWAY_STATIC_URL}}
WEBSOCKET_SERVICE_URL=${{websocket-service.RAILWAY_STATIC_URL}}
ZAPIER_SERVICE_URL=${{zapier-service.RAILWAY_STATIC_URL}}
```

---

### 🟡 Service 3: voice-processor

**Root Path:** Set to `/backend/voice-processor`

```bash
# REQUIRED - Security
JWT_SECRET=your_jwt_secret_key_here_min_32_chars

# REQUIRED - Redis
REDIS_URL=${{Redis.REDIS_URL}}

# OPTIONAL - Database (if needed)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# API Configuration
API_HOST=0.0.0.0
API_PORT=8002

# REQUIRED - Google Cloud (for STT/TTS)
GOOGLE_CLOUD_TTS_API_KEY=your_google_cloud_tts_api_key_here
GOOGLE_CLOUD_TTS_KEY_PATH=/app/google-cloud-key.json
GOOGLE_CLOUD_PROJECT_ID=your_project_id

# Service URLs
MAIN_API_URL=${{helix-backend-api.RAILWAY_STATIC_URL}}
AGENT_ORCHESTRATOR_URL=${{agent-orchestrator.RAILWAY_STATIC_URL}}
```

---

### 🟣 Service 4: websocket-service

**Root Path:** Set to `/backend/websocket-service`

```bash
# REQUIRED - Security
JWT_SECRET=your_jwt_secret_key_here_min_32_chars

# REQUIRED - Redis (for pub/sub)
REDIS_URL=${{Redis.REDIS_URL}}

# API Configuration
API_HOST=0.0.0.0
API_PORT=8003

# Service URLs
MAIN_API_URL=${{helix-backend-api.RAILWAY_STATIC_URL}}
AGENT_ORCHESTRATOR_URL=${{agent-orchestrator.RAILWAY_STATIC_URL}}
```

---

### 🔴 Service 5: zapier-service

**Root Path:** Set to `/backend/zapier-service`

```bash
# REQUIRED - Security
JWT_SECRET=your_jwt_secret_key_here_min_32_chars

# REQUIRED - Redis
REDIS_URL=${{Redis.REDIS_URL}}

# OPTIONAL - Zapier webhook secret (for validation)
ZAPIER_SECRET=your_zapier_webhook_secret

# API Configuration
API_HOST=0.0.0.0
API_PORT=8004

# Service URLs
MAIN_API_URL=${{helix-backend-api.RAILWAY_STATIC_URL}}
AGENT_ORCHESTRATOR_URL=${{agent-orchestrator.RAILWAY_STATIC_URL}}
```

---

## Deployment Order

### Step 1: Add Railway Plugins
1. **PostgreSQL** - Add to project, note the connection string
2. **Redis** - Add to project, note the connection string

### Step 2: Deploy Services (in order)

#### 2a. Deploy helix-backend-api (Main) FIRST
- Set root directory: `/backend`
- Add all variables from "Service 1" section above
- Use `${{Postgres.DATABASE_URL}}` and `${{Redis.REDIS_URL}}`
- Deploy and wait for it to be healthy
- Note the public URL (e.g., `helix-backend-api.up.railway.app`)

#### 2b. Deploy agent-orchestrator
- Set root directory: `/backend/agent-orchestrator`
- Add all variables from "Service 2" section
- Use the main service URL: `MAIN_API_URL=https://helix-backend-api.up.railway.app`
- Deploy

#### 2c. Deploy voice-processor
- Set root directory: `/backend/voice-processor`
- Add all variables from "Service 3" section
- Deploy

#### 2d. Deploy websocket-service
- Set root directory: `/backend/websocket-service`
- Add all variables from "Service 4" section
- Deploy

#### 2e. Deploy zapier-service
- Set root directory: `/backend/zapier-service`
- Add all variables from "Service 5" section
- Deploy

---

## Critical Variables Checklist

### MUST HAVE (or services will crash):

#### All Microservices:
- ✅ `JWT_SECRET` - Min 32 characters, same across ALL services
- ✅ `REDIS_URL` - Use `${{Redis.REDIS_URL}}`

#### Main Service:
- ✅ `DISCORD_BOT_TOKEN` - Your Discord bot token
- ✅ `DATABASE_URL` - Use `${{Postgres.DATABASE_URL}}`
- ✅ `OPENAI_API_KEY` - For voice TTS (PR #226 feature)

### SHOULD HAVE (for full functionality):

- ✅ `ANTHROPIC_API_KEY` - For Claude integration
- ✅ `NOTION_API_KEY` - For Notion sync
- ✅ `GOOGLE_CLOUD_TTS_API_KEY` - For voice features

### NICE TO HAVE (optional features):

- `ELEVENLABS_API_KEY` - Alternative TTS
- `STABILITY_API_KEY` - Image generation
- `REPLICATE_API_KEY` - AI model access
- `GITHUB_TOKEN` - GitHub integration
- `SENTRY_DSN` - Error tracking

---

## Testing Your Deployment

### 1. Check Service Health

Each service should have a health endpoint:

```bash
# Main API
curl https://helix-backend-api.up.railway.app/health

# Agent Orchestrator
curl https://agent-orchestrator.up.railway.app/health

# Voice Processor
curl https://voice-processor.up.railway.app/health

# WebSocket Service
curl https://websocket-service.up.railway.app/health

# Zapier Service
curl https://zapier-service.up.railway.app/health
```

### 2. Check Discord Bot

- Bot should come online in Discord
- Try `!help` command
- Try `!status` command
- Try `!ucf` command

### 3. Check Voice Features (PR #226)

- Join a voice channel
- Use `!join` command
- Say "manus status" (wake word + command)
- Bot should transcribe and respond

---

## Common Issues & Fixes

### Issue 1: "JWT_SECRET is required for production"
**Fix:** Add `JWT_SECRET` to ALL microservices (same value everywhere)

### Issue 2: "Redis connection failed"
**Fix:** Verify `REDIS_URL=${{Redis.REDIS_URL}}` is set correctly

### Issue 3: "Port already in use"
**Fix:** Railway assigns ports automatically, use `0.0.0.0` for host

### Issue 4: Voice commands not working
**Fix:**
- Verify `OPENAI_API_KEY` is set
- Check Vosk model is downloaded (see PR #226 review)
- Verify bot has voice permissions in Discord

### Issue 5: Services can't talk to each other
**Fix:** Use Railway's service reference syntax:
```bash
MAIN_API_URL=${{helix-backend-api.RAILWAY_STATIC_URL}}
```

---

## Cost Estimate

**With Current Setup:**
- PostgreSQL: $5/month (shared across all services)
- Redis: $5/month (shared across all services)
- helix-backend-api: $5-10/month (main compute)
- agent-orchestrator: $5/month
- voice-processor: $5/month
- websocket-service: $5/month
- zapier-service: $5/month

**Total: ~$35-40/month**

**Optimization:**
- Start with just helix-backend-api ($15/month total)
- Add microservices as needed when scaling
- Use Railway's $5 hobby tier for testing

---

## Features Verification

✅ **All features intact from PRs #223 and #226:**

### From PR #223 (Ninja - SuperNinja.ai):
- ✅ Agent Orchestrator microservice
- ✅ Voice Processor microservice
- ✅ WebSocket Service microservice
- ✅ Zapier Service microservice
- ✅ 68-tool MCP TypeScript server
- ✅ JWT authentication

### From PR #226 (Manus):
- ✅ Vosk STT integration (`backend/commands/voice_commands.py`)
- ✅ OpenAI TTS integration (`backend/tts_service.py`)
- ✅ Custom Discord voice sink (`backend/voice_sink.py`)
- ✅ Wake word detection (manus/helix/collective)

### From Nexus (MACS):
- ✅ Multi-Agent Coordination System (`.macs/`)
- ✅ Agent registry and task tracking
- ✅ Emergent behavior observation

### From Claude (me):
- ✅ Security hardening (no hardcoded JWT secrets)
- ✅ Environment validation
- ✅ Enhanced .env.example with all variables

**Nothing was removed! All systems go! 🚀**

---

## Next Steps

1. **Create 5 Railway services** (1 main + 4 microservices)
2. **Add PostgreSQL and Redis plugins**
3. **Configure environment variables** using this guide
4. **Deploy in order** (main → orchestrator → voice → websocket → zapier)
5. **Test each service** after deployment
6. **Monitor logs** for any errors
7. **Test Discord bot** and voice commands

**Questions? Check the logs in Railway dashboard or Discord bot console.**

---

**Tat Tvam Asi** 🌀
