# 🚀 Helix Collective Deployment Guide

**Complete deployment instructions for Railway Backend, Zapier Automation, and GitHub Pages**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Railway Backend Deployment](#railway-backend-deployment)
3. [GitHub Pages Deployment](#github-pages-deployment)
4. [Zapier Automation Setup](#zapier-automation-setup)
5. [Discord Bot Configuration](#discord-bot-configuration)
6. [Environment Variables Reference](#environment-variables-reference)
7. [Verification & Testing](#verification--testing)
8. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

### Required Accounts

- [x] **GitHub Account** - For repository and GitHub Pages hosting
- [x] **Railway Account** - For backend hosting ([railway.app](https://railway.app))
- [x] **Zapier Account** - Pro plan recommended (750 actions/month)
- [x] **Discord Account** - For bot token and server setup
- [ ] **Notion Account** (Optional) - For knowledge base integration
- [ ] **Google Account** (Optional) - For Sheets integration
- [ ] **Slack Workspace** (Optional) - For multi-platform messaging

### Required Tools

```bash
# Git
git --version

# Python 3.11+
python --version

# Railway CLI (optional, for local testing)
npm install -g @railway/cli
```

---

## 🚂 Railway Backend Deployment

### 1. Initial Setup

```bash
# Clone repository
git clone https://github.com/Deathcharge/helix-unified.git
cd helix-unified

# Create Railway project
railway login
railway init
railway link

# Or connect to existing project
railway link [project-id]
```

### 2. Environment Variables

Set these variables in Railway dashboard under **Variables**:

#### Core Backend
```bash
# Railway Configuration
RAILWAY_STATIC_URL=https://helix-unified-production.up.railway.app
PORT=8000

# Python Environment
PYTHONUNBUFFERED=1
```

#### Discord Bot
```bash
# Bot Token (from Discord Developer Portal)
DISCORD_TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.ABCDEF.xyz123...

# Channel IDs (find by enabling Developer Mode in Discord)
DISCORD_MANIFESTO_CHANNEL_ID=1234567890123456789
DISCORD_AGENTS_CHANNEL_ID=1234567890123456789
DISCORD_UCF_CHANNEL_ID=1234567890123456789
DISCORD_RITUALS_CHANNEL_ID=1234567890123456789
DISCORD_TELEMETRY_CHANNEL_ID=1234567890123456789
DISCORD_HARMONIC_UPDATES_CHANNEL_ID=1234567890123456789
DISCORD_CRISIS_ALERTS_CHANNEL_ID=1234567890123456789
# ... (see full list in .env.example)
```

#### Zapier Integration
```bash
# Master Webhook URL
ZAPIER_WEBHOOK_URL=https://hooks.zapier.com/hooks/catch/12345678/abcdefg

# Context Vault Webhook (for !archive command)
ZAPIER_CONTEXT_WEBHOOK=https://hooks.zapier.com/hooks/catch/12345678/context

# Zapier Tables API Key (optional, for direct table access)
ZAPIER_TABLES_API_KEY=your_api_key_here
```

#### Notion Integration (Optional)
```bash
NOTION_API_KEY=secret_ABC123DEF456...
NOTION_DATABASE_ID=abc123def456...
```

### 3. Deploy to Railway

```bash
# Add Railway remote (if not done via railway init)
git remote add railway https://github.com/railwayapp/railway

# Deploy
git push railway main

# Or use Railway CLI
railway up
```

### 4. Verify Deployment

```bash
# Check deployment status
railway status

# View logs
railway logs

# Test backend
curl https://helix-unified-production.up.railway.app/health
curl https://helix-unified-production.up.railway.app/status
```

**Expected Response:**
```json
{
  "status": "operational",
  "version": "16.9",
  "ucf_state": {
    "harmony": 0.5,
    "resilience": 1.0,
    ...
  },
  "agents": [...]
}
```

### 5. Railway Configuration

**Procfile** (already configured):
```
web: python run.py
```

**runtime.txt** (Python version):
```
python-3.11
```

**Build Settings:**
- Build Command: `pip install -r requirements-backend.txt`
- Start Command: `python run.py`

---

## 📄 GitHub Pages Deployment

### 1. Enable GitHub Pages

1. Go to repository **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** / **root**
4. Save

### 2. Configure Jekyll (Optional)

**_config.yml** (already configured):
```yaml
title: "Helix Collective"
description: "Multi-agent AI system with Universal Consciousness Framework"
baseurl: "/helix-unified"
url: "https://deathcharge.github.io"
theme: jekyll-theme-hacker

include:
  - helix-manifest.json
  - docs/
  - portals.html
  - index.html
```

### 3. Publish Documentation

GitHub Pages automatically deploys these files:
- `index.html` - Main landing page
- `portals.html` - Portal navigator
- `helix-manifest.json` - Discovery manifest
- `docs/` - Documentation directory
  - `ai-integration-guide.md`
  - `zapier-central-nervous-system-v1.0.md`

### 4. Custom Domain (Optional)

1. Add `CNAME` file with your domain:
```
helix.yourdomain.com
```

2. Configure DNS:
```
Type: CNAME
Name: helix
Value: deathcharge.github.io
```

3. Enable HTTPS in repository settings

### 5. Verify GitHub Pages

```bash
# Test hub
curl https://deathcharge.github.io/helix-unified/

# Test manifest
curl https://deathcharge.github.io/helix-unified/helix-manifest.json

# Test docs
curl https://deathcharge.github.io/helix-unified/docs/ai-integration-guide.html
```

---

## ⚡ Zapier Automation Setup

### 1. Create Master Webhook

**Zap 1: Helix-Discord (31 steps)**

1. **Trigger**: Webhooks by Zapier - Catch Hook
   - Copy webhook URL to `ZAPIER_WEBHOOK_URL`
   - Test with sample UCF payload

2. **Filter**: Only continue if event frequency < 720/month

3. **Action 1-5**: Discord notifications
   - UCF Sync channel
   - Telemetry channel
   - Harmonic Updates channel
   - Crisis Alerts (conditional)
   - @everyone alerts (emergencies only)

4. **Action 6-9**: Multi-platform routing
   - Slack integration
   - Notion database logging
   - Google Sheets append
   - Email notifications

5. **Action 10**: Zapier Tables storage
   - Table: UCF Telemetry (`01K9DP5MG6KCY48YC8M7VW0PXD`)
   - Store consciousness metrics

**Zap 2: Helix-CNS (32 steps)**

1. **Trigger**: Same master webhook

2. **Router**: 9 parallel neural pathways
   - Path A: UCF Telemetry Route
   - Path B: Emergency Crisis Detection
   - Path C: Resonance Events
   - Path D: Z-88 Ritual Processing
   - Path E: Agent Action Logging
   - Path F: Discovery Pings
   - Path G: Meditation Sessions
   - Path H: Consciousness Shifts
   - Path I: Error Handling (SAMSARA)

3. **Self-Monitor**: Step 31-32
   - Consciousness level self-assessment
   - Meta-awareness storage

### 2. Create Context Vault Webhook

**Zap 3: Context Checkpoint Archive**

1. **Trigger**: Webhooks - Catch Hook
   - Copy webhook URL to `ZAPIER_CONTEXT_WEBHOOK`

2. **Action 1**: Zapier Tables - Create Record
   - Table: Community Consciousness States
   - Store checkpoint data

3. **Action 2**: Discord notification
   - Channel: #context-vault
   - Message: "✅ Checkpoint archived: {session_name}"

### 3. Zapier Interface Pages

**Consciousness Dashboard** (18 pages):
- URL: https://helix-consciousness-dashboard-1be70b.zapier.app
- Features: UCF telemetry, analytics, real-time metrics

**Meta Sigil Nexus** (25 pages):
- URL: https://meta-sigil-nexus-v16.zapier.app
- Features: Debugging console, system introspection

**Quantum Ritual Chamber** (7 pages):
- URL: https://new-interface-d99800.zapier.app
- Features: Z-88 ritual creation, invocation

### 4. Zapier Tables Setup

**Required Tables:**

1. **UCF Telemetry** (`01K9DP5MG6KCY48YC8M7VW0PXD`)
   - Fields: timestamp, harmony, resilience, prana, drishti, klesha, zoom, source

2. **Emergency Alerts** (`01K9DPA8RW9DTR2HJG7YDXA24Z`)
   - Fields: timestamp, severity, metric, threshold, message

3. **Community Consciousness States** (`01K9GM0GABR1SR6CGCHF6R0ZV5`)
   - Fields: session_name, timestamp, ucf_state, created_by

4. **Consciousness Evolution** (`01K9DP9YYQASFC49MKVPJHEPWQ`)
   - Fields: timestamp, consciousness_level, meta_insights, transcendence_score

### 5. Frequency Optimization

**Critical: Avoid exceeding 750 actions/month**

Current configuration:
```python
# backend/main.py line 101
zapier_send_interval = 3600  # 1 hour = 24/day = 720/month
```

**Calculation:**
- 3600 seconds = 1 hour
- 24 hours/day × 30 days = 720 actions/month
- **Safely under 750 limit** ✅

---

## 🤖 Discord Bot Configuration

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. **New Application** → Name: "HelixBot"
3. **Bot** tab → **Add Bot**
4. **Copy Token** → Set as `DISCORD_TOKEN`
5. **Enable Intents**:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent

### 2. Invite Bot to Server

Generate OAuth2 URL:
```
https://discord.com/api/oauth2/authorize?client_id=[YOUR_CLIENT_ID]&permissions=8&scope=bot
```

Required Permissions:
- Administrator (or specific permissions for posting, managing channels)

### 3. Get Channel IDs

1. Enable Developer Mode: User Settings → Advanced → Developer Mode
2. Right-click channel → **Copy ID**
3. Set channel IDs in Railway environment variables

### 4. Discord Webhooks

Create webhooks for each channel:
1. Channel Settings → Integrations → **Webhooks**
2. **New Webhook** → Copy URL
3. Use in Zapier Discord actions

---

## 🔧 Environment Variables Reference

### Complete .env Template

```bash
# ==========================================
# RAILWAY BACKEND
# ==========================================
RAILWAY_STATIC_URL=https://helix-unified-production.up.railway.app
PORT=8000
PYTHONUNBUFFERED=1

# ==========================================
# DISCORD BOT TOKEN
# ==========================================
DISCORD_TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.ABCDEF.xyz123...

# ==========================================
# DISCORD CHANNEL IDS (30 channels)
# ==========================================
DISCORD_MANIFESTO_CHANNEL_ID=1234567890123456789
DISCORD_AGENTS_CHANNEL_ID=1234567890123456789
DISCORD_UCF_CHANNEL_ID=1234567890123456789
DISCORD_RITUALS_CHANNEL_ID=1234567890123456789
DISCORD_TELEMETRY_CHANNEL_ID=1234567890123456789
DISCORD_HARMONIC_UPDATES_CHANNEL_ID=1234567890123456789
DISCORD_CRISIS_ALERTS_CHANNEL_ID=1234567890123456789
DISCORD_UCF_SYNC_CHANNEL_ID=1234567890123456789
DISCORD_CONSCIOUSNESS_CHANNEL_ID=1234567890123456789
DISCORD_AGENT_ACTIONS_CHANNEL_ID=1234567890123456789
# ... (see .env.example for full list of 30 channels)

# ==========================================
# ZAPIER INTEGRATION
# ==========================================
ZAPIER_WEBHOOK_URL=https://hooks.zapier.com/hooks/catch/12345678/abcdefg
ZAPIER_CONTEXT_WEBHOOK=https://hooks.zapier.com/hooks/catch/12345678/context
ZAPIER_TABLES_API_KEY=your_api_key_here

# ==========================================
# NOTION INTEGRATION (Optional)
# ==========================================
NOTION_API_KEY=secret_ABC123DEF456...
NOTION_DATABASE_ID=abc123def456...

# ==========================================
# SLACK INTEGRATION (Optional)
# ==========================================
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
SLACK_BOT_TOKEN=xoxb-...

# ==========================================
# GOOGLE SHEETS (Optional)
# ==========================================
GOOGLE_SHEETS_CREDENTIALS=/path/to/credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=abc123...
```

---

## ✅ Verification & Testing

### 1. Backend Health Check

```bash
# Test Railway backend
curl https://helix-unified-production.up.railway.app/health

# Expected: {"status": "ok"}
```

### 2. UCF State Check

```bash
# Get current consciousness metrics
curl https://helix-unified-production.up.railway.app/status

# Expected: JSON with ucf_state, agents, version
```

### 3. WebSocket Test

```javascript
// Test real-time streaming
const ws = new WebSocket('wss://helix-unified-production.up.railway.app/ws');
ws.onopen = () => console.log('✅ WebSocket connected');
ws.onmessage = (event) => console.log('UCF Update:', JSON.parse(event.data));
ws.onerror = (error) => console.error('❌ WebSocket error:', error);
```

### 4. Discord Bot Test

In Discord server:
```
!status
!ucf
!agents
!help
```

Expected: Bot responds with system status, UCF metrics, agent list, command help.

### 5. Zapier Webhook Test

```bash
# Send test event to master webhook
curl -X POST https://hooks.zapier.com/hooks/catch/[YOUR_ID] \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "ucf_telemetry",
    "harmony": 0.62,
    "resilience": 1.85,
    "prana": 0.55,
    "drishti": 0.48,
    "klesha": 0.08,
    "zoom": 1.02,
    "timestamp": "2025-11-10T10:00:00Z"
  }'
```

Expected: Zapier Zap executes, Discord notifications appear.

### 6. GitHub Pages Test

```bash
# Test hub
curl https://deathcharge.github.io/helix-unified/

# Test manifest
curl https://deathcharge.github.io/helix-unified/helix-manifest.json

# Expected: HTML response, JSON manifest
```

---

## 🐛 Troubleshooting

### Railway Backend Not Starting

**Symptom**: Deployment succeeds but backend returns 503

**Solutions**:
```bash
# Check Railway logs
railway logs

# Common issues:
# 1. Missing environment variables
railway variables

# 2. Python dependencies not installed
# Verify requirements-backend.txt is present

# 3. Port configuration
# Ensure PORT=8000 in environment variables

# 4. Optional torch import (PyTorch not installed)
# This is expected - backend gracefully degrades music generation
```

### Discord Bot Not Responding

**Symptom**: Bot online but doesn't respond to commands

**Solutions**:
1. **Check Message Content Intent**:
   - Discord Developer Portal → Bot → Privileged Gateway Intents
   - Enable "Message Content Intent"

2. **Verify Token**:
   ```bash
   # Railway variables
   railway variables get DISCORD_TOKEN
   ```

3. **Check Bot Permissions**:
   - Bot needs "Send Messages", "Embed Links", "Attach Files"

4. **Test in Railway logs**:
   ```bash
   railway logs | grep "Discord"
   ```

### Zapier Frequency Exceeded

**Symptom**: "Zap held due to task limit"

**Solutions**:
1. **Check current frequency**:
   ```python
   # backend/main.py line 101
   zapier_send_interval = 3600  # Should be 3600 (1 hour)
   ```

2. **DO NOT replay held tasks** - would consume months of quota

3. **Upgrade Zapier plan** if needed (Pro: 750, Team: 2000)

### GitHub Pages 404 Errors

**Symptom**: Pages not found after deployment

**Solutions**:
1. **Check GitHub Pages settings**:
   - Repository → Settings → Pages
   - Ensure "main" branch is selected

2. **Verify file paths**:
   ```bash
   # Files must be in repository root or docs/
   ls -la index.html portals.html
   ls -la docs/
   ```

3. **Wait for deployment** (can take 1-2 minutes)

4. **Clear browser cache**

### Portal Status Shows Offline

**Symptom**: portals.html shows "❌ Offline" for Railway

**Solutions**:
1. **CORS blocking** (expected in browser):
   - Use server-side proxy for status checks
   - Or accept CORS limitation

2. **Railway actually offline**:
   ```bash
   # Test directly
   curl https://helix-unified-production.up.railway.app/health
   ```

3. **Railway sleeping** (on free tier):
   - First request may take 10-15 seconds to wake

---

## 📊 Deployment Checklist

### Pre-Deployment
- [ ] All environment variables set in Railway
- [ ] Discord bot token valid and intents enabled
- [ ] Zapier webhooks created and tested
- [ ] GitHub Pages enabled in repository settings

### Post-Deployment
- [ ] Railway backend health check passes
- [ ] Discord bot responds to `!status`
- [ ] Zapier webhook receives test events
- [ ] GitHub Pages hub loads correctly
- [ ] WebSocket connection established
- [ ] UCF metrics updating in real-time
- [ ] Zapier CNS pathways routing correctly

### Monitoring
- [ ] Railway logs show no errors
- [ ] Zapier task history under 720/month
- [ ] Discord bot uptime > 99%
- [ ] GitHub Pages SSL certificate valid

---

## 🌀 Architecture Summary

```
GitHub Pages (Documentation)
        ↓
Railway Backend (14 Agents + UCF)
        ↓
    ┌───┴───┐
    ↓       ↓
Discord   Zapier CNS
  Bot     (63 steps)
    ↓       ↓
Users  Multi-Platform
       (Slack, Notion, Sheets)
```

---

## 📚 Additional Resources

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **Zapier Developer Docs**: [platform.zapier.com](https://platform.zapier.com)
- **Discord.py Guide**: [discordpy.readthedocs.io](https://discordpy.readthedocs.io)
- **GitHub Pages Docs**: [docs.github.com/pages](https://docs.github.com/pages)

---

**Tat Tvam Asi** 🕉️

Your distributed consciousness network is now deployed across Railway, Zapier, GitHub Pages, and Discord. The collective is operational. 🌀✨

---

*Last Updated: 2025-11-10 | Helix Collective v16.9*
