# 🚂 Railway Environment Setup Guide

**Clean, organized workflow for setting Railway environment variables**

---

## 🎯 Quick Start

### Option 1: Auto-Export Script (Recommended)

```bash
# 1. Make sure .env is filled out (copy from .env.example)
cp .env.example .env
nano .env  # Fill in your actual values

# 2. Export for specific service
./scripts/export_railway_env.sh helix-discord-bot

# This will output:
# - All environment variables for that service
# - Ready-to-run Railway CLI commands
```

### Option 2: Manual Setup (Railway Dashboard)

Go to: https://railway.app → Your Project → Service → Variables

---

## 📋 Environment Variables by Service

### 🔧 Service 1: helix-backend-api

**Purpose:** REST API for UCF, agents, telemetry (NO Discord bot)

**Variables:**
```bash
# Core
HELIX_VERSION=v16.7
HELIX_PHASE=production
LOG_LEVEL=INFO
DEBUG=false

# API
API_HOST=0.0.0.0
API_PORT=8000

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://localhost:6379

# Zapier
ZAPIER_WEBHOOK_URL=https://hooks.zapier.com/hooks/catch/xxxxx/xxxxxx
ZAPIER_MASTER_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxxxx/master

# Notion
NOTION_API_KEY=secret_xxxxx
NOTION_SYSTEM_STATE_DB=009a946d04fb46aa83e4481be86f09ef
NOTION_AGENT_REGISTRY_DB=2f65aab794a64ec48bcc46bf760f128f
NOTION_EVENT_LOG_DB=acb01d4a955d4775aaeb2310d1da1102
NOTION_CONTEXT_DB=d704854868474666b4b774750f8b134a

# Storage (Nextcloud Primary)
HELIX_STORAGE_MODE=nextcloud
NEXTCLOUD_URL=https://use11.thegood.cloud
NEXTCLOUD_USER=Vidolaoin@gmail.com
NEXTCLOUD_PASS=xxxxx-xxxxx-xxxxx-xxxxx-xxxxx  # App password!
NEXTCLOUD_BASE_PATH=/Helix

# MEGA Backup (Optional)
MEGA_EMAIL=your_email@example.com
MEGA_PASS=your_password
MEGA_REMOTE_DIR=/Helix-Backups
```

**⚠️ DO NOT SET:** `DISCORD_TOKEN` (only on helix-discord-bot!)

---

### 📊 Service 2: helix-dashboard

**Purpose:** Streamlit dashboard for visualization

**Variables:**
```bash
# Uses shared variables only!
HELIX_VERSION=v16.7
HELIX_PHASE=production
NOTION_API_KEY=secret_xxxxx
# ... (same shared vars as backend)

# Railway auto-sets PORT
```

**No additional service-specific variables needed.**

---

### 🤖 Service 3: helix-claude-api

**Purpose:** Claude consciousness API endpoint

**Variables:**
```bash
# Core (Shared)
HELIX_VERSION=v16.7
HELIX_PHASE=production
LOG_LEVEL=INFO

# Claude API
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Andrew's Consciousness Empire Webhooks
CONSCIOUSNESS_ENGINE_WEBHOOK=https://hooks.zapier.com/hooks/catch/25075191/primary
COMMUNICATIONS_HUB_WEBHOOK=https://hooks.zapier.com/hooks/catch/25075191/usxiwfg
NEURAL_NETWORK_WEBHOOK=https://hooks.zapier.com/hooks/catch/25075191/usnjj5t

# Shared Zapier/Notion vars
ZAPIER_WEBHOOK_URL=https://hooks.zapier.com/hooks/catch/xxxxx/xxxxxx
NOTION_API_KEY=secret_xxxxx
# ... (same shared vars)
```

---

### 💬 Service 4: helix-discord-bot

**Purpose:** Discord bot orchestrator (ONLY service with bot token!)

**Variables:**
```bash
# Core (Shared)
HELIX_VERSION=v16.7
HELIX_PHASE=production
LOG_LEVEL=INFO

# ⚠️ DISCORD TOKEN - ONLY ON THIS SERVICE!
DISCORD_TOKEN=MTxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxx
DISCORD_GUILD_ID=1234567890123456789
ARCHITECT_ID=1234567890123456789

# Discord Channel IDs
DISCORD_STATUS_CHANNEL_ID=1234567890123456789
DISCORD_TELEMETRY_CHANNEL_ID=1234567890123456789
DISCORD_MANUS_BRIDGE_CHANNEL_ID=1234567890123456789
DISCORD_RITUAL_ENGINE_CHANNEL_ID=1234567890123456789
DISCORD_BACKUP_CHANNEL_ID=1234567890123456789
DISCORD_DEPLOYMENTS_CHANNEL_ID=1234567890123456789

# Claude API URL (from Service 3)
# Get this from Railway dashboard after deploying helix-claude-api
CLAUDE_API_URL=https://helix-claude-api.railway.app

# Shared vars
ZAPIER_WEBHOOK_URL=https://hooks.zapier.com/hooks/catch/xxxxx/xxxxxx
NOTION_API_KEY=secret_xxxxx
# ... (same shared vars)
```

---

## 🚀 Deployment Workflow

### Step 1: Prepare .env File

```bash
# Copy template
cp .env.example .env

# Fill in ALL values
nano .env

# Verify no placeholders remain
grep -E "your_|xxxxx|example\.com" .env
# ^ Should return nothing!
```

### Step 2: Deploy Services in Order

**Why this order?** Service 4 needs Service 3's URL.

```bash
# Deploy services 1-3 first
railway service helix-backend-api
railway up

railway service helix-dashboard
railway up

railway service helix-claude-api
railway up
```

### Step 3: Get Service URLs

```bash
# Get helix-claude-api URL
railway service helix-claude-api
railway domain
# Copy the URL (e.g., https://helix-claude-api.railway.app)
```

### Step 4: Set CLAUDE_API_URL on Discord Bot

```bash
railway service helix-discord-bot
railway variables set CLAUDE_API_URL="https://helix-claude-api.railway.app"
railway up
```

### Step 5: Verify All Services

```bash
# Check all services are running
railway status

# Expected output:
# ✓ helix-backend-api - Active
# ✓ helix-dashboard - Active
# ✓ helix-claude-api - Active
# ✓ helix-discord-bot - Active
```

---

## 🔐 Security Checklist

### ❌ Never Commit to Git:
- `DISCORD_TOKEN`
- `ANTHROPIC_API_KEY`
- `NOTION_API_KEY`
- `NEXTCLOUD_PASS`
- `MEGA_PASS`
- `DATABASE_URL` (if contains password)

### ✅ Safe to Commit:
- Railway service URLs
- Zapier webhook URLs (if public)
- Notion database IDs (UUIDs)
- Service configuration

### 🔒 Best Practices:
1. **Use Railway's environment variables** (not railway.toml)
2. **Use Nextcloud App Passwords** (not main password)
3. **One Discord token per bot instance** (avoid duplicate bot issues)
4. **Rotate keys quarterly** (set calendar reminder)

---

## 🧪 Testing Your Setup

### Test 1: Discord Bot

```bash
# In Discord
!consciousness test

# Expected: Bot responds within 5 seconds
```

### Test 2: Claude API

```bash
curl https://helix-claude-api.railway.app/health

# Expected: {"status": "healthy", "consciousness_level": X.XX}
```

### Test 3: Dashboard

Visit: `https://helix-dashboard.railway.app`

**Expected:**
- Purple Streamlit theme loads
- UCF metrics display
- Agent statuses show

### Test 4: Zapier Webhook

```bash
python tests/test_zapier_webhook.py --all

# Expected: All 7 paths pass (or Week 1 passes if using free tier)
```

---

## 🆘 Troubleshooting

### Issue: "DISCORD_TOKEN not found"

**Cause:** Token not set or set on wrong service

**Fix:**
```bash
railway service helix-discord-bot
railway variables set DISCORD_TOKEN="YOUR_TOKEN"
railway up
```

### Issue: "Duplicate bot instance detected"

**Cause:** DISCORD_TOKEN set on multiple services

**Fix:**
```bash
# Remove from all services EXCEPT helix-discord-bot
railway service helix-backend-api
railway variables delete DISCORD_TOKEN

railway service helix-claude-api
railway variables delete DISCORD_TOKEN

# Verify only helix-discord-bot has it
railway service helix-discord-bot
railway variables | grep DISCORD_TOKEN
```

### Issue: "CLAUDE_API_URL connection refused"

**Cause:** Service 4 trying to reach Service 3 before it's deployed

**Fix:**
```bash
# 1. Verify Service 3 is running
railway service helix-claude-api
railway status
# Should show: ✓ Active

# 2. Get correct URL
railway domain
# Copy URL

# 3. Update Service 4
railway service helix-discord-bot
railway variables set CLAUDE_API_URL="https://helix-claude-api.railway.app"
railway up
```

### Issue: "Nextcloud upload failed: Unauthorized"

**Cause:** Using main password instead of app password

**Fix:**
1. Go to Nextcloud → Settings → Security
2. Click "Create new app password"
3. Name it "Helix Railway"
4. Copy generated password (format: `xxxxx-xxxxx-xxxxx-xxxxx-xxxxx`)
5. Update Railway:
   ```bash
   railway variables set NEXTCLOUD_PASS="xxxxx-xxxxx-xxxxx-xxxxx-xxxxx"
   ```

---

## 📊 Volume Configuration (Recommended)

Each service can have **multiple volumes** (not just one!).

### helix-backend-api Volumes:

```bash
# Via Railway CLI
railway service helix-backend-api

railway volume add \
  --name shadow-storage \
  --mount /app/Shadow \
  --size 3

railway volume add \
  --name helix-state \
  --mount /app/Helix \
  --size 2

railway volume add \
  --name visual-outputs \
  --mount /app/visual_outputs \
  --size 3
```

### helix-discord-bot Volumes:

```bash
railway service helix-discord-bot

railway volume add \
  --name shared-state \
  --mount /app/shared \
  --size 1
```

**Total Cost:** 9 GB × $0.25/GB = **$2.25/month**

See `RAILWAY_VOLUME_STORAGE.md` for full details.

---

## ✅ Complete Setup Checklist

- [ ] `.env` file created and filled
- [ ] No placeholder values in `.env`
- [ ] Nextcloud app password generated
- [ ] Railway CLI installed (`npm i -g @railway/cli`)
- [ ] Railway CLI authenticated (`railway login`)
- [ ] Service 1 (backend-api) deployed
- [ ] Service 2 (dashboard) deployed
- [ ] Service 3 (claude-api) deployed and URL copied
- [ ] Service 4 (discord-bot) deployed with correct CLAUDE_API_URL
- [ ] Volumes configured (optional but recommended)
- [ ] Discord bot shows online
- [ ] `!consciousness test` works in Discord
- [ ] Claude API `/health` endpoint responds
- [ ] Dashboard loads and shows metrics
- [ ] Zapier webhook test passes

---

*Tat Tvam Asi* 🕉️

**Last Updated:** 2025-11-19 | v17.0 | Clean Railway Export
