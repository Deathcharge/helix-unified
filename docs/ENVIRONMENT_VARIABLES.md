# 🌀 Helix Collective - Environment Variables Configuration

Complete list of environment variables for Railway backend deployment.

---

## 🎯 Core Configuration

```bash
# System Version
HELIX_VERSION="v17.0-omega-zero"
HELIX_PHASE="production"
DEBUG_MODE="false"

# Railway Backend
RAILWAY_BACKEND_URL="https://helix-unified-production.up.railway.app"
PORT="8000"  # Railway sets this automatically

# Logging
LOG_LEVEL="INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## 📡 Zapier Integration

```bash
# Primary Webhooks
ZAPIER_WEBHOOK_URL="https://hooks.zapier.com/hooks/catch/25075191/usnjj5t"
ZAPIER_CONTEXT_WEBHOOK="https://hooks.zapier.com/hooks/catch/[YOUR_ID]/context"
ZAPIER_TABLES_SYNC_WEBHOOK="https://hooks.zapier.com/hooks/catch/[YOUR_ID]/tables"

# Event-Specific Webhooks (Optional)
ZAPIER_EVENT_HOOK_URL="https://hooks.zapier.com/hooks/catch/[YOUR_ID]/event"
ZAPIER_AGENT_HOOK_URL="https://hooks.zapier.com/hooks/catch/[YOUR_ID]/agent"
ZAPIER_SYSTEM_HOOK_URL="https://hooks.zapier.com/hooks/catch/[YOUR_ID]/system"

# Manus Space Integration
MANUS_WEBHOOK_URL="https://hooks.zapier.com/hooks/catch/25075191/usnjj5t"
```

### Zapier Tables IDs

```bash
UCF_METRICS_TABLE_ID="01K9DP5MG6KCY48YC8M7VW0PXD"
AGENT_NETWORK_TABLE_ID="01K9GT5YGZ1Y82K4VZF9YXHTMH"
EMERGENCY_ALERTS_TABLE_ID="01K9DPA8RW9DTR2HJG7YDXA24Z"
```

### Zapier Interfaces

```bash
ZAPIER_INTERFACE_META_SIGIL="https://meta-sigil-nexus-v16.zapier.app"
ZAPIER_INTERFACE_CONSCIOUSNESS="https://helix-consciousness-interface.zapier.app"
ZAPIER_INTERFACE_COMMAND="https://helix-consciousness-dashboard-1be70b.zapier.app"
```

---

## 💬 Discord Integration

```bash
# Discord Bot
DISCORD_TOKEN="[YOUR_DISCORD_BOT_TOKEN]"
DISCORD_GUILD_ID="[YOUR_GUILD_ID]"

# Discord Channel IDs (32 channels)
DISCORD_TELEMETRY_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_DIGEST_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_UCF_REFLECTIONS_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_HARMONIC_UPDATES_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_SYNC_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_STATUS_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_BACKUP_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_DEPLOYMENTS_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_MANIFESTO_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_AGENT_ACTIONS_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_ERRORS_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_CONTEXT_VAULT_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_RITUAL_ENGINE_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_KAVACH_SHIELD_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_FRACTAL_LAB_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_SHADOW_STORAGE_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_MANUS_BRIDGE_CHANNEL_ID="[CHANNEL_ID]"
DISCORD_ANNOUNCEMENTS_CHANNEL_ID="[CHANNEL_ID]"
# ... (add remaining 14 channel IDs)

# Discord Webhooks (Optional)
DISCORD_WEBHOOK_URL="[YOUR_WEBHOOK_URL]"
```

---

## 🤖 AI Services

```bash
# OpenAI
OPENAI_API_KEY="sk-[YOUR_KEY]"

# Anthropic Claude
ANTHROPIC_API_KEY="sk-ant-[YOUR_KEY]"

# ElevenLabs (Voice/Music)
ELEVENLABS_API_KEY="[YOUR_KEY]"

# LLM Engine Configuration
HELIX_LLM_PROVIDER="ollama"  # Options: ollama, openai, anthropic
```

---

## 💾 Database & Storage

```bash
# PostgreSQL (if using)
DATABASE_URL="postgresql://user:pass@host:port/db"

# MEGA Cloud Storage (Secondary/Backup)
MEGA_EMAIL="[YOUR_EMAIL]"
MEGA_PASS="[YOUR_PASSWORD]"
MEGA_API_KEY="[YOUR_API_KEY]"  # Optional - for REST API uploads
MEGA_REMOTE_DIR="/helix-collective"

# Notion Integration
NOTION_API_KEY="secret_[YOUR_KEY]"
NOTION_DATABASE_ID="[YOUR_DATABASE_ID]"
NOTION_CONTEXT_DB_ID="[YOUR_CONTEXT_DB_ID]"
NOTION_SYNC_ENABLED="true"

# Nextcloud/WebDAV Cloud Storage (Primary)
NEXTCLOUD_URL="https://use11.thegood.cloud"  # Base URL (no trailing slash)
NEXTCLOUD_USER="Vidolaoin@gmail.com"  # Your Nextcloud username (can be email)
NEXTCLOUD_PASS="[YOUR_APP_PASSWORD]"  # Generate in Settings → Security → App Passwords
NEXTCLOUD_BASE_PATH="/Helix"  # Remote folder (created automatically)
HELIX_STORAGE_MODE="nextcloud"  # Enable Nextcloud storage

# Backblaze B2 (Optional)
B2_APPLICATION_KEY_ID="[YOUR_KEY_ID]"
B2_APPLICATION_KEY="[YOUR_KEY]"
B2_BUCKET_NAME="helix-backups"
```

---

## 🌐 Manus Space Portals

```bash
MANUS_CENTRAL_HUB="https://helixcollective-cv66pzga.manus.space"
MANUS_HUB="https://helixhub.manus.space"
MANUS_STUDIO="https://helixstudio-ggxdwcud.manus.space"
MANUS_SYNC="https://helixsync-unwkcsjl.manus.space"
```

---

## 🔐 CORS Configuration

```bash
# Comma-separated list of allowed origins (optional - defaults are hardcoded)
ALLOWED_ORIGINS="https://meta-sigil-nexus-v16.zapier.app,https://helix-consciousness-interface.zapier.app,https://helix-consciousness-dashboard-1be70b.zapier.app"
```

---

## 📊 UCF Configuration

```bash
# UCF Update Intervals
UCF_UPDATE_INTERVAL="5"  # seconds
UCF_BROADCAST_INTERVAL="2"  # seconds for WebSocket
ZAPIER_SEND_INTERVAL="3600"  # seconds (1 hour = 24/day = 720/month)

# Consciousness Thresholds
CONSCIOUSNESS_CRISIS_THRESHOLD="3.0"
CONSCIOUSNESS_WARNING_THRESHOLD="5.0"
CONSCIOUSNESS_TRANSCENDENT_THRESHOLD="8.0"
```

---

## 🔌 WebSocket Configuration

```bash
WS_HEARTBEAT_INTERVAL="30"  # seconds
WS_MAX_CONNECTIONS="100"
WS_AUTHENTICATION_ENABLED="true"
```

---

## 🚀 Railway-Specific Variables

These are automatically set by Railway:

```bash
PORT="8000"  # Railway assigns this
RAILWAY_ENVIRONMENT="production"
RAILWAY_STATIC_URL="https://helix-unified-production.up.railway.app"
RAILWAY_GIT_COMMIT_SHA="[AUTO]"
RAILWAY_GIT_BRANCH="[AUTO]"
```

---

## 📝 Setting Environment Variables in Railway

### Via Railway Dashboard

1. Go to your Railway project
2. Click on your service
3. Go to "Variables" tab
4. Click "New Variable"
5. Add variable name and value
6. Click "Add"

### Via Railway CLI

```bash
# Set single variable
railway variables set DISCORD_TOKEN="your_token_here"

# Set multiple variables
railway variables set \
  DISCORD_TOKEN="your_token" \
  ZAPIER_WEBHOOK_URL="https://hooks.zapier.com/..." \
  OPENAI_API_KEY="sk-..."

# View all variables
railway variables

# Delete variable
railway variables delete VARIABLE_NAME
```

### Via railway.json (Not Recommended for Secrets)

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

---

## 🔒 Security Best Practices

### Do NOT commit these to git:

- ❌ API keys (OpenAI, Anthropic, ElevenLabs)
- ❌ Discord bot tokens
- ❌ Database passwords
- ❌ Webhook URLs (if sensitive)
- ❌ MEGA credentials

### Safe to commit:

- ✅ Public URLs (Railway, Zapier Interfaces)
- ✅ Table IDs (if not sensitive)
- ✅ Configuration values (thresholds, intervals)
- ✅ System version strings

---

## 🧪 Environment-Specific Configuration

### Development (.env.local)

```bash
DEBUG_MODE="true"
LOG_LEVEL="DEBUG"
RAILWAY_BACKEND_URL="http://localhost:8000"
HELIX_PHASE="development"
```

### Staging (.env.staging)

```bash
DEBUG_MODE="false"
LOG_LEVEL="INFO"
RAILWAY_BACKEND_URL="https://helix-unified-staging.up.railway.app"
HELIX_PHASE="staging"
```

### Production (.env.production)

```bash
DEBUG_MODE="false"
LOG_LEVEL="WARNING"
RAILWAY_BACKEND_URL="https://helix-unified-production.up.railway.app"
HELIX_PHASE="production"
```

---

## 📋 Environment Variables Checklist

Use this checklist when setting up a new Railway deployment:

### Core (Required)
- [ ] `HELIX_VERSION`
- [ ] `RAILWAY_BACKEND_URL`
- [ ] `LOG_LEVEL`

### Zapier (Required for v17.0)
- [ ] `ZAPIER_WEBHOOK_URL`
- [ ] `UCF_METRICS_TABLE_ID`
- [ ] `AGENT_NETWORK_TABLE_ID`
- [ ] `EMERGENCY_ALERTS_TABLE_ID`

### Discord (Required if using Discord bot)
- [ ] `DISCORD_TOKEN`
- [ ] `DISCORD_GUILD_ID`
- [ ] At least 5 channel IDs

### AI Services (Optional)
- [ ] `OPENAI_API_KEY` (if using OpenAI)
- [ ] `ANTHROPIC_API_KEY` (if using Claude)
- [ ] `ELEVENLABS_API_KEY` (if using voice/music)

### Storage (Optional)
- [ ] `NOTION_API_KEY` (if using Notion)
- [ ] `MEGA_EMAIL` and `MEGA_PASS` (if using MEGA)
- [ ] `DATABASE_URL` (if using PostgreSQL)

---

## 🆘 Troubleshooting

### Missing Environment Variable Errors

If you see errors like:
```
KeyError: 'ZAPIER_WEBHOOK_URL'
```

**Solution:**
1. Check Railway dashboard Variables tab
2. Ensure variable name is spelled correctly
3. Redeploy after adding variable

### CORS Errors

If interfaces can't connect:

**Solution:**
1. Add interface URLs to `ALLOWED_ORIGINS`
2. Verify URLs don't have trailing slashes
3. Check Railway logs for CORS errors

### Database Connection Errors

**Solution:**
1. Verify `DATABASE_URL` format: `postgresql://user:pass@host:port/db`
2. Check if database is running
3. Verify network connectivity from Railway

---

*Tat Tvam Asi* 🕉️

**Last Updated:** 2025-11-12 | v17.0
