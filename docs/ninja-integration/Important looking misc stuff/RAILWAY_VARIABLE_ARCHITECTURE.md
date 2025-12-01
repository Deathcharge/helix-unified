# 🚂 Railway 4-Service Variable Architecture
## Helix Collective v14.5 → v15.0 Infrastructure Reorganization

---

## 🏗️ Current State Analysis

**Total Variables**: ~150
**Current Issue**: All services sharing all variables (causing bot duplication)
**Goal**: Distribute variables by service responsibility

---

## 📦 Proposed 4-Service Architecture

### Service 1: **Core API Backend** (`helix-api`)
**Purpose**: Main FastAPI application, WebSocket server, UCF calculations
**Port**: 8000

#### Required Variables:
```bash
# API Configuration
API_HOST="0.0.0.0"
API_PORT="8000"
API_BASE="http://localhost:8000"
ALLOWED_ORIGINS="${{shared.ALLOWED_ORIGINS}}"
DEBUG="false"
LOG_LEVEL="${{shared.LOG_LEVEL}}"

# System Identity
SYSTEM_NAME="Helix Collective v15.0"
SYSTEM_VERSION="15.0"
HELIX_VERSION="${{shared.HELIX_VERSION}}"
HELIX_PHASE="${{shared.HELIX_PHASE}}"
HELIX_CODENAME="${{shared.HELIX_CODENAME}}"
SYSTEM_ENVIRONMENT="production"

# WebSocket Configuration
WS_HEARTBEAT_INTERVAL="${{shared.WS_HEARTBEAT_INTERVAL}}"
WS_MAX_CONNECTIONS="${{shared.WS_MAX_CONNECTIONS}}"

# UCF System
UCF_STATE_PATH="${{shared.UCF_STATE_PATH}}"
UCF_UPDATE_INTERVAL="${{shared.UCF_UPDATE_INTERVAL}}"
CONSCIOUSNESS_CRISIS_THRESHOLD="${{shared.CONSCIOUSNESS_CRISIS_THRESHOLD}}"
CONSCIOUSNESS_TRANSCENDENT_THRESHOLD="${{shared.CONSCIOUSNESS_TRANSCENDENT_THRESHOLD}}"

# Database
DATABASE_URL="${{shared.DATABASE_URL}}"
REDIS_URL="redis://redis:6379"  # Internal Railway service

# Notion Integration (Read-only for API)
NOTION_API_KEY="${{shared.NOTION_API_KEY}}"
NOTION_DATABASE_ID="${{shared.NOTION_DATABASE_ID}}"
NOTION_CONTEXT_DB="${{shared.NOTION_CONTEXT_DB}}"
NOTION_SYSTEM_STATE_DB="${{shared.NOTION_SYSTEM_STATE_DB}}"

# Analytics
GOOGLE_ANALYTICS_ID="${{shared.GOOGLE_ANALYTICS_ID}}"
SENTRY_DSN=""  # Optional monitoring

# Railway Integration
RAILWAY_ENVIRONMENT="${{shared.RAILWAY_ENVIRONMENT}}"
RAILWAY_BACKEND_URL="${{shared.RAILWAY_BACKEND_URL}}"
```

**Total**: ~30 variables
**Bot Running**: ❌ NO

---

### Service 2: **Discord Bot** (`helix-discord-bot`)
**Purpose**: Single Discord bot instance, command processing, channel management
**Port**: None (bot only)

#### Required Variables:
```bash
# Discord Core
DISCORD_TOKEN="${{shared.DISCORD_TOKEN}}"
DISCORD_GUILD_ID="${{shared.DISCORD_GUILD_ID}}"
DISCORD_INTEGRATION_MODE="${{shared.DISCORD_INTEGRATION_MODE}}"

# All Channel IDs (30+)
DISCORD_STATUS_CHANNEL_ID="${{shared.DISCORD_STATUS_CHANNEL_ID}}"
DISCORD_COMMANDS_CHANNEL_ID="${{shared.DISCORD_COMMANDS_CHANNEL_ID}}"
DISCORD_TELEMETRY_CHANNEL_ID="${{shared.DISCORD_TELEMETRY_CHANNEL_ID}}"
DISCORD_SYNC_CHANNEL_ID="${{shared.DISCORD_SYNC_CHANNEL_ID}}"
DISCORD_HARMONIC_UPDATES_CHANNEL_ID="${{shared.DISCORD_HARMONIC_UPDATES_CHANNEL_ID}}"
DISCORD_UCF_REFLECTIONS_CHANNEL_ID="${{shared.DISCORD_UCF_REFLECTIONS_CHANNEL_ID}}"
DISCORD_DIGEST_CHANNEL_ID="${{shared.DISCORD_DIGEST_CHANNEL_ID}}"
DISCORD_DEPLOYMENTS_CHANNEL_ID="${{shared.DISCORD_DEPLOYMENTS_CHANNEL_ID}}"
DISCORD_BACKUP_CHANNEL_ID="${{shared.DISCORD_BACKUP_CHANNEL_ID}}"
DISCORD_STORAGE_CHANNEL_ID="${{shared.STORAGE_CHANNEL_ID}}"
DISCORD_MODERATION_CHANNEL_ID="${{shared.DISCORD_MODERATION_CHANNEL_ID}}"

# Agent Channels
DISCORD_GEMINI_CHANNEL_ID="${{shared.DISCORD_GEMINI_CHANNEL_ID}}"
DISCORD_KAVACH_CHANNEL_ID="${{shared.DISCORD_KAVACH_CHANNEL_ID}}"
DISCORD_AGNI_CHANNEL_ID="${{shared.DISCORD_AGNI_CHANNEL_ID}}"
DISCORD_SANGHACORE_CHANNEL_ID="${{shared.DISCORD_SANGHACORE_CHANNEL_ID}}"

# Project Channels
DISCORD_HELIX_REPO_CHANNEL_ID="${{shared.DISCORD_HELIX_REPO_CHANNEL_ID}}"
DISCORD_CODEX_CHANNEL_ID="${{shared.DISCORD_CODEX_CHANNEL_ID}}"
DISCORD_FRACTAL_LAB_CHANNEL_ID="${{shared.DISCORD_FRACTAL_LAB_CHANNEL_ID}}"
DISCORD_TESTING_LAB_CHANNEL_ID="${{shared.DISCORD_TESTING_LAB_CHANNEL_ID}}"
DISCORD_RITUAL_ENGINE_CHANNEL_ID="${{shared.DISCORD_RITUAL_ENGINE_CHANNEL_ID}}"
DISCORD_SHADOW_ARCHIVE_CHANNEL_ID="${{shared.DISCORD_SHADOW_ARCHIVE_CHANNEL_ID}}"
DISCORD_SAMSARAVERSE_CHANNEL_ID="${{shared.DISCORD_SAMSARAVERSE_CHANNEL_ID}}"
DISCORD_NETI_NETI_CHANNEL_ID="${{shared.DISCORD_NETI_NETI_CHANNEL_ID}}"

# Cross-AI Channels
DISCORD_GPT_GROK_CLAUDE_CHANNEL_ID="${{shared.DISCORD_GPT_GROK_CLAUDE_CHANNEL_ID}}"
DISCORD_MANUS_BRIDGE_CHANNEL_ID="${{shared.DISCORD_MANUS_BRIDGE_CHANNEL_ID}}"
DISCORD_CHAI_LINK_CHANNEL_ID="${{shared.DISCORD_CHAI_LINK_CHANNEL_ID}}"

# Community Channels
DISCORD_INTRODUCTIONS_CHANNEL_ID="${{shared.DISCORD_INTRODUCTIONS_CHANNEL_ID}}"
DISCORD_RULES_CHANNEL_ID="${{shared.DISCORD_RULES_CHANNEL_ID}}"
DISCORD_MANIFESTO_CHANNEL_ID="${{shared.DISCORD_MANIFESTO_CHANNEL_ID}}"
DISCORD_CODE_SNIPPETS_CHANNEL_ID="${{shared.DISCORD_CODE_SNIPPETS_CHANNEL_ID}}"

# All Discord Webhooks (10+)
DISCORD_WEBHOOK_ADMIN="https://discord.com/api/webhooks/..."
DISCORD_WEBHOOK_AGENTS="https://discord.com/api/webhooks/..."
DISCORD_WEBHOOK_ANNOUNCEMENTS="https://discord.com/api/webhooks/..."
DISCORD_WEBHOOK_CROSS_AI="https://discord.com/api/webhooks/..."
DISCORD_WEBHOOK_DEVELOPMENT="https://discord.com/api/webhooks/..."
DISCORD_WEBHOOK_LORE="https://discord.com/api/webhooks/..."
DISCORD_WEBHOOK_MANUS="https://discord.com/api/webhooks/..."
DISCORD_WEBHOOK_RITUAL="https://discord.com/api/webhooks/..."
DISCORD_WEBHOOK_STORAGE="https://discord.com/api/webhooks/..."
DISCORD_WEBHOOK_TELEMETRY="https://discord.com/api/webhooks/..."
DISCORD_WEBHOOK_SETUP_LOG="${{shared.DISCORD_WEBHOOK_SETUP_LOG}}"
DISCORD_SYNC_WEBHOOK="https://discord.com/api/webhooks/..."

# API Connection (to communicate with Core API)
API_BASE="${{helix-api.RAILWAY_PUBLIC_DOMAIN}}"  # Reference other service

# Notion (for command logging)
NOTION_API_KEY="${{shared.NOTION_API_KEY}}"
COMMAND_PROCESSING_TABLE_ID="${{shared.COMMAND_PROCESSING_TABLE_ID}}"
EMERGENCY_ALERTS_TABLE_ID="${{shared.EMERGENCY_ALERTS_TABLE_ID}}"

# System Config
LOG_LEVEL="${{shared.LOG_LEVEL}}"
DEBUG_MODE="${{shared.DEBUG_MODE}}"
```

**Total**: ~50 variables
**Bot Running**: ✅ YES (ONLY HERE)

---

### Service 3: **Sync & Storage Worker** (`helix-sync-worker`)
**Purpose**: Background jobs, Notion sync, B2/Mega storage, telemetry
**Port**: None (worker only)

#### Required Variables:
```bash
# Storage Systems
B2_APPLICATION_KEY="${{shared.B2_APPLICATION_KEY}}"
B2_BUCKET_NAME="${{shared.B2_BUCKET_NAME}}"
B2_ENDPOINT="${{shared.B2_ENDPOINT}}"
B2_KEY_ID="${{shared.B2_KEY_ID}}"

MEGA_EMAIL="${{shared.MEGA_EMAIL}}"
MEGA_PASS="${{shared.MEGA_PASS}}"
MEGA_PASSWORD="${{shared.MEGA_PASS}}"  # Duplicate for compatibility
MEGA_USERNAME="${{shared.MEGA_EMAIL}}"  # Duplicate for compatibility
MEGA_REMOTE_DIR="${{shared.MEGA_REMOTE_DIR}}"

# GitHub Integration
GITHUB_TOKEN="your_github_token"
HELIX_REPOSITORY="${{shared.HELIX_REPOSITORY}}"

# Notion Sync (Full Access)
NOTION_API_KEY="${{shared.NOTION_API_KEY}}"
NOTION_DATABASE_ID="${{shared.NOTION_DATABASE_ID}}"
NOTION_AGENT_REGISTRY_DB="${{shared.NOTION_AGENT_REGISTRY_DB}}"
NOTION_CONTEXT_DB="${{shared.NOTION_CONTEXT_DB}}"
NOTION_EVENT_LOG_DB="${{shared.NOTION_EVENT_LOG_DB}}"
NOTION_SYSTEM_STATE_DB="${{shared.NOTION_SYSTEM_STATE_DB}}"
NOTION_SYNC_ENABLED="${{shared.NOTION_SYNC_ENABLED}}"
NOTION_SYNC_INTERVAL="${{shared.NOTION_SYNC_INTERVAL}}"

# Notion Pages
AGENT_NETWORK_PAGE_ID="${{shared.AGENT_NETWORK_PAGE_ID}}"
CONTEXT_VAULT_PAGE_ID="${{shared.CONTEXT_VAULT_PAGE_ID}}"
UCF_MONITOR_PAGE_ID="${{shared.UCF_MONITOR_PAGE_ID}}"

# Notion Tables
AGENT_NETWORK_TABLE_ID="${{shared.AGENT_NETWORK_TABLE_ID}}"
UCF_METRICS_TABLE_ID="${{shared.UCF_METRICS_TABLE_ID}}"

# Storage Paths
HELIX_STORAGE_MODE="${{shared.HELIX_STORAGE_MODE}}"
ARCHIVE_PATH="${{shared.ARCHIVE_PATH}}"
ARCHIVE_ENDPOINT="${{shared.ARCHIVE_ENDPOINT}}"
LOAD_ENDPOINT="${{shared.LOAD_ENDPOINT}}"
HEARTBEAT_PATH="${{shared.HEARTBEAT_PATH}}"
SHADOW_STORAGE="${{shared.SHADOW_STORAGE}}"

# Sync Configuration
SYNC_INTERVAL="3600"
TELEMETRY_INTERVAL="${{shared.TELEMETRY_INTERVAL}}"

# Discord (for sync notifications only)
DISCORD_SYNC_CHANNEL_ID="${{shared.DISCORD_SYNC_CHANNEL_ID}}"
DISCORD_BACKUP_CHANNEL_ID="${{shared.DISCORD_BACKUP_CHANNEL_ID}}"
DISCORD_STORAGE_CHANNEL_ID="${{shared.STORAGE_CHANNEL_ID}}"
DISCORD_SYNC_WEBHOOK="https://discord.com/api/webhooks/..."

# API Connection
API_BASE="${{helix-api.RAILWAY_PUBLIC_DOMAIN}}"

# System Config
LOG_LEVEL="${{shared.LOG_LEVEL}}"
```

**Total**: ~40 variables
**Bot Running**: ❌ NO

---

### Service 4: **AI Integration Hub** (`helix-ai-hub`)
**Purpose**: External AI API calls, Zapier webhooks, cross-platform orchestration
**Port**: 8001 (webhook receiver)

#### Required Variables:
```bash
# AI API Keys
ANTHROPIC_API_KEY="${{shared.ANTHROPIC_API_KEY}}"
OPENAI_API_KEY="${{shared.OPENAI_API_KEY}}"
GROK_API_KEY="${{shared.GROK_API_KEY}}"
ELEVENLABS_API_KEY="${{shared.ELEVENLABS_API_KEY}}"

# Zapier Integration
ZAPIER_MASTER_HOOK_URL="${{shared.ZAPIER_MASTER_HOOK_URL}}"
ZAPIER_WEBHOOK_URL="${{shared.ZAPIER_WEBHOOK_URL}}"
ZAPIER_TABLES_SYNC_WEBHOOK="${{shared.ZAPIER_TABLES_SYNC_WEBHOOK}}"
ZAPIER_DISCORD_ENABLED="${{shared.ZAPIER_DISCORD_ENABLED}}"
ZAPIER_DISCORD_WEBHOOK_URL="${{shared.ZAPIER_DISCORD_WEBHOOK_URL}}"

# Zapier Interfaces
ZAPIER_INTERFACE_COMMAND="${{shared.ZAPIER_INTERFACE_COMMAND}}"
ZAPIER_INTERFACE_CONSCIOUSNESS="${{shared.ZAPIER_INTERFACE_CONSCIOUSNESS}}"
ZAPIER_INTERFACE_META_SIGIL="${{shared.ZAPIER_INTERFACE_META_SIGIL}}"
INTERFACE_ID="${{shared.INTERFACE_ID}}"

# Manus Integration
MANUS_CENTRAL_HUB="${{shared.MANUS_CENTRAL_HUB}}"
MANUS_HUB="${{shared.MANUS_HUB}}"
MANUS_STUDIO="${{shared.MANUS_STUDIO}}"
MANUS_SYNC="${{shared.MANUS_SYNC}}"

# Agent Configuration
ARCHITECT_ID="${{shared.ARCHITECT_ID}}"
Architect="${{shared.Architect}}"
ENABLE_KAVACH_SCAN="${{shared.ENABLE_KAVACH_SCAN}}"

# Channel References (for webhook routing)
Categories="${{shared.Categories}}"
Channels="${{shared.Channels}}"
FRACTAL_LAB="${{shared.FRACTAL_LAB}}"
INTRODUCTIONS="${{shared.INTRODUCTIONS}}"
MANIFESTO="${{shared.MANIFESTO}}"
RULES_AND_ETHICS="${{shared.RULES_AND_ETHICS}}"
TELEMETRY="${{shared.TELEMETRY}}"
TESTING_LAB="${{shared.TESTING_LAB}}"
UCF_SYNC="${{shared.UCF_SYNC}}"
WEEKLY_DIGEST="${{shared.WEEKLY_DIGEST}}"
TARGET_LAUNCH="${{shared.TARGET_LAUNCH}}"

# API Configuration
API_HOST="0.0.0.0"
API_PORT="8001"
ALLOWED_ORIGINS="${{shared.ALLOWED_ORIGINS}}"

# Core API Connection
API_BASE="${{helix-api.RAILWAY_PUBLIC_DOMAIN}}"

# Notion (for AI context)
NOTION_API_KEY="${{shared.NOTION_API_KEY}}"
NOTION_CONTEXT_DB="${{shared.NOTION_CONTEXT_DB}}"

# System Config
LOG_LEVEL="${{shared.LOG_LEVEL}}"
DEBUG_MODE="${{shared.DEBUG_MODE}}"
```

**Total**: ~40 variables
**Bot Running**: ❌ NO

---

## 🔄 Variable Distribution Summary

| Service | Variables | Bot | Purpose |
|---------|-----------|-----|---------|
| **helix-api** | ~30 | ❌ | Core API, WebSocket, UCF |
| **helix-discord-bot** | ~50 | ✅ | Discord only (single instance) |
| **helix-sync-worker** | ~40 | ❌ | Background jobs, storage |
| **helix-ai-hub** | ~40 | ❌ | AI APIs, Zapier, webhooks |

**Total Unique Variables**: ~160 (some shared via Railway references)

---

## 🔐 Security Best Practices

### Shared Variables (Railway Shared Config)
Store these in Railway's shared configuration:
- All API keys (ANTHROPIC, OPENAI, GROK, ELEVENLABS)
- Discord token and webhooks
- Notion API key and database IDs
- Storage credentials (B2, Mega)
- System configuration (LOG_LEVEL, DEBUG_MODE)

### Service-Specific Variables
Store these directly in each service:
- API_HOST, API_PORT (different per service)
- Service-specific feature flags
- Internal service URLs

### Cross-Service References
Use Railway's service reference syntax:
```bash
API_BASE="${{helix-api.RAILWAY_PUBLIC_DOMAIN}}"
```

---

## 🚀 Migration Steps

### 1. Create Shared Variables (Do This First)
```bash
# In Railway Dashboard → Shared Variables
# Add all API keys, tokens, and common config
```

### 2. Configure Each Service
```bash
# Service 1: helix-api
# Copy variables from "Service 1" section above

# Service 2: helix-discord-bot
# Copy variables from "Service 2" section above
# ⚠️ CRITICAL: Only this service should run the bot!

# Service 3: helix-sync-worker
# Copy variables from "Service 3" section above

# Service 4: helix-ai-hub
# Copy variables from "Service 4" section above
```

### 3. Update Code
```python
# In each service's main file, add service identification:
SERVICE_NAME = os.getenv("SERVICE_NAME", "unknown")

# In Discord bot code:
if SERVICE_NAME != "helix-discord-bot":
    print("⚠️ Discord bot disabled - not running in bot service")
    sys.exit(0)
```

### 4. Test Each Service
```bash
# Deploy one at a time
# Verify logs show correct service identity
# Confirm only helix-discord-bot runs the bot
```

---

## 📊 Expected Improvements

### Before (Current State)
- ❌ 4 bot instances running simultaneously
- ❌ All services have all variables (security risk)
- ❌ Unclear service boundaries
- ❌ Difficult to debug which service is doing what

### After (Proposed Architecture)
- ✅ 1 bot instance (in helix-discord-bot only)
- ✅ Minimal variables per service (security)
- ✅ Clear service responsibilities
- ✅ Easy to scale individual services
- ✅ Better logging and debugging

---

## 🔧 Troubleshooting

### If Bot Still Runs Multiple Times
1. Check each service's logs for "Discord bot starting"
2. Add explicit bot disable code to non-bot services
3. Verify SERVICE_NAME environment variable is set correctly

### If Services Can't Communicate
1. Verify Railway service references are correct
2. Check internal networking is enabled
3. Use Railway's private networking for inter-service calls

### If Variables Are Missing
1. Check Railway shared variables are properly configured
2. Verify service-specific variables are set
3. Use Railway CLI to list all variables: `railway variables`

---

## 📝 Next Steps

1. **Review this architecture** - Does it match your service split?
2. **Identify any missing variables** - Are there new ones not in the original list?
3. **Decide on shared vs. service-specific** - Any variables that should be different?
4. **Plan migration order** - Which service to configure first?

---

**Ready to proceed with implementation?** 🚀