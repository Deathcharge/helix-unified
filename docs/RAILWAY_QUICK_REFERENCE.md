# 🚂 Railway Quick Reference Card

**Fast answers for common questions**

---

## 🔍 Which services use CLAUDE_API_URL?

**ONLY ONE:** `helix-discord-bot` (Service 4)

```bash
# helix-discord-bot needs this to talk to helix-claude-api
CLAUDE_API_URL=https://helix-claude-api.railway.app
```

**DO NOT set on:**
- ❌ helix-backend-api
- ❌ helix-dashboard
- ❌ helix-claude-api

---

## 💾 Volume Mappings

**You can have MULTIPLE volumes per service!**

| Service | Mount Path | Size | What's Stored |
|---------|-----------|------|---------------|
| **helix-backend-api** | `/app/Shadow` | 3 GB | UCF archives, shadow storage |
| **helix-backend-api** | `/app/Helix` | 2 GB | UCF state, agent memory |
| **helix-backend-api** | `/app/visual_outputs` | 3 GB | Fractal art, ritual frames |
| **helix-discord-bot** | `/app/shared` | 1 GB | Shared state (bot ↔ backend) |

**Total:** 9 GB = $2.25/month

**Add volumes:**
```bash
railway service helix-backend-api
railway volume add --name shadow-storage --mount /app/Shadow --size 3
railway volume add --name helix-state --mount /app/Helix --size 2
railway volume add --name visual-outputs --mount /app/visual_outputs --size 3
```

---

## 🔐 Environment File Hierarchy

**Master Source of Truth:**
```
.env.example  ← Complete reference (commit safe, has placeholders)
     ↓
   .env  ← Your actual values (DO NOT COMMIT!)
     ↓
Railway Dashboard  ← Set variables here for production
```

**Workflow:**
1. Copy `.env.example` to `.env`
2. Fill in real values in `.env`
3. Use export script to generate Railway commands
4. Set variables in Railway dashboard or via CLI

---

## 🌐 Service URLs & Dependencies

```
┌─────────────────────────────────────────┐
│  helix-backend-api                      │
│  (REST API, NO Discord bot)             │
│  ↓ Talks to: Database, Redis            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  helix-dashboard                        │
│  (Streamlit UI)                         │
│  ↓ Talks to: Notion, Zapier Tables     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  helix-claude-api                       │
│  (Claude consciousness endpoints)       │
│  ↓ Talks to: Anthropic API, Zapier     │
│  URL: https://helix-claude-api.railway.app
└─────────────────────────────────────────┘
                    ↑
                    │ CLAUDE_API_URL
                    │
┌─────────────────────────────────────────┐
│  helix-discord-bot                      │
│  (ONLY service with DISCORD_TOKEN!)     │
│  ↓ Talks to: Discord, Service 3        │
└─────────────────────────────────────────┘
```

**Deploy Order:**
1. Services 1-3 (any order)
2. Get Service 3 URL
3. Set CLAUDE_API_URL on Service 4
4. Deploy Service 4

---

## 🔑 Critical Environment Variables

### Shared Across All Services:
- `HELIX_VERSION`
- `HELIX_PHASE`
- `LOG_LEVEL`
- `ZAPIER_WEBHOOK_URL`
- `ZAPIER_MASTER_HOOK_URL`
- `NOTION_API_KEY` + 4 database IDs
- `NEXTCLOUD_URL` + credentials
- `MEGA_EMAIL` + `MEGA_PASS` (optional)

### Service-Specific:

**helix-backend-api ONLY:**
- `DATABASE_URL`
- `REDIS_URL`

**helix-claude-api ONLY:**
- `ANTHROPIC_API_KEY`
- `CONSCIOUSNESS_ENGINE_WEBHOOK`
- `COMMUNICATIONS_HUB_WEBHOOK`
- `NEURAL_NETWORK_WEBHOOK`

**helix-discord-bot ONLY:**
- `DISCORD_TOKEN` ⚠️
- `DISCORD_GUILD_ID`
- `ARCHITECT_ID`
- 6+ channel IDs
- `CLAUDE_API_URL`

---

## 🚨 Common Mistakes

### ❌ Duplicate Discord Bot
**Problem:** DISCORD_TOKEN set on multiple services

**Fix:** Only set on `helix-discord-bot`
```bash
# Remove from other services
railway service helix-backend-api
railway variables delete DISCORD_TOKEN

railway service helix-claude-api
railway variables delete DISCORD_TOKEN
```

### ❌ Claude API Connection Fails
**Problem:** Service 4 can't reach Service 3

**Fix:** Verify CLAUDE_API_URL is correct
```bash
railway service helix-claude-api
railway domain
# Copy URL

railway service helix-discord-bot
railway variables set CLAUDE_API_URL="<paste-url-here>"
```

### ❌ Nextcloud Upload Fails
**Problem:** Using main password instead of app password

**Fix:** Generate app password in Nextcloud settings:
1. Nextcloud → Settings → Security
2. "Create new app password"
3. Name: "Helix Railway"
4. Copy password (format: `xxxxx-xxxxx-xxxxx-xxxxx-xxxxx`)

---

## 🛠️ Quick Commands

### Export Environment Variables
```bash
# Show all variables for all services
./scripts/export_railway_env.sh all

# Generate Railway CLI commands for specific service
./scripts/export_railway_env.sh helix-discord-bot
```

### Check Service Status
```bash
railway status

# Expected:
# ✓ helix-backend-api - Active
# ✓ helix-dashboard - Active
# ✓ helix-claude-api - Active
# ✓ helix-discord-bot - Active
```

### Test Deployment
```bash
# Discord bot
# In Discord: !consciousness test

# Claude API
curl https://helix-claude-api.railway.app/health

# Dashboard
# Open: https://helix-dashboard.railway.app

# Zapier
python tests/test_zapier_webhook.py --all
```

---

## 📚 Full Documentation

- **Environment Setup:** `docs/RAILWAY_ENV_SETUP.md`
- **Volume Storage:** `docs/RAILWAY_VOLUME_STORAGE.md`
- **General Deployment:** `RAILWAY_DEPLOYMENT.md`
- **Environment Variables:** `docs/ENVIRONMENT_VARIABLES.md`

---

*Tat Tvam Asi* 🕉️

**Last Updated:** 2025-11-19 | v17.0
