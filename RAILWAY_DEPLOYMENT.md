# 🚀 Railway Deployment Guide — Helix Collective v14.5

## Overview

This guide walks you through deploying the Helix Collective v14.5 to Railway with full Zapier integration, Discord bot, and real-time Notion logging.

---

## 📋 Prerequisites

1. **Railway Account** — Free or paid (https://railway.app)
2. **Railway CLI** — Installed and authenticated
3. **GitHub Repository** — `Deathcharge/helix-unified` cloned and ready
4. **Environment Variables** — All required values prepared
5. **Zapier Webhooks** — Three webhooks created and tested
6. **Discord Bot Token** — From Discord Developer Portal
7. **Notion API Key** — From Notion Settings

---

## 🔧 Step 1: Install Railway CLI

### 1.1 Install Railway

```bash
# Using npm
npm install -g @railway/cli

# Or using Homebrew (macOS)
brew install railway

# Verify installation
railway --version
```

### 1.2 Authenticate with Railway

```bash
# Login to Railway
railway login

# This opens a browser window for authentication
# Follow the prompts to connect your Railway account
```

### 1.3 Verify Authentication

```bash
# Check if you're logged in
railway whoami

# Expected output:
# You are logged in as: your-email@example.com
```

---

## 🎯 Step 2: Create Railway Project

### 2.1 Initialize Railway Project

```bash
# Navigate to helix-unified directory
cd /path/to/helix-unified

# Initialize Railway project
railway init

# Follow the prompts:
# - Project name: helix-collective-v14.5
# - Environment: production
```

### 2.2 Link to Existing Project (Optional)

If you already have a Railway project:

```bash
# Link to existing project
railway link

# Select your project from the list
```

### 2.3 Verify Project

```bash
# Check project status
railway status

# Expected output:
# Project: helix-collective-v14.5
# Environment: production
```

---

## 🗄️ Step 3: Add Services

### 3.1 Add PostgreSQL Database

```bash
# Add PostgreSQL service
railway add postgres

# This creates a PostgreSQL database in your Railway project
# Railway automatically sets DATABASE_URL environment variable
```

### 3.2 Add Redis Cache

```bash
# Add Redis service
railway add redis

# This creates a Redis instance
# Railway automatically sets REDIS_URL environment variable
```

### 3.3 Verify Services

```bash
# View all services
railway status

# Expected output:
# Services:
#   - postgres
#   - redis
#   - backend (your app)
```

---

## 🔐 Step 4: Configure Environment Variables

### 4.1 Set Discord Configuration

```bash
# Set Discord bot token
railway variables set DISCORD_TOKEN=your_discord_bot_token_here

# Set Discord guild ID
railway variables set DISCORD_GUILD_ID=your_guild_id_here

# Set Architect ID (your Discord user ID)
railway variables set ARCHITECT_ID=your_user_id_here
```

### 4.2 Set Zapier Webhooks

```bash
# Set Zapier Event Log webhook
railway variables set ZAPIER_EVENT_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxxxx/event

# Set Zapier Agent Registry webhook
railway variables set ZAPIER_AGENT_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxxxx/agent

# Set Zapier System State webhook
railway variables set ZAPIER_SYSTEM_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxxxx/system
```

### 4.3 Set Notion Configuration

```bash
# Set Notion API key
railway variables set NOTION_API_KEY=your_notion_api_key_here

# Set Notion database IDs
railway variables set NOTION_AGENT_REGISTRY_DB=009a946d04fb46aa83e4481be86f09ef
railway variables set NOTION_EVENT_LOG_DB=acb01d4a955d4775aaeb2310d1da1102
railway variables set NOTION_SYSTEM_STATE_DB=2f65aab794a64ec48bcc46bf760f128f
railway variables set NOTION_CONTEXT_DB=d704854868474666b4b774750f8b134a
```

### 4.4 Set Application Configuration

```bash
# Set environment
railway variables set ENVIRONMENT=production

# Set API configuration
railway variables set API_HOST=0.0.0.0
railway variables set API_PORT=8000

# Set logging level
railway variables set LOG_LEVEL=INFO
```

### 4.5 Verify Environment Variables

```bash
# View all environment variables
railway variables

# Expected output:
# DISCORD_TOKEN=***
# DISCORD_GUILD_ID=***
# ARCHITECT_ID=***
# ZAPIER_EVENT_HOOK_URL=https://hooks.zapier.com/...
# ZAPIER_AGENT_HOOK_URL=https://hooks.zapier.com/...
# ZAPIER_SYSTEM_HOOK_URL=https://hooks.zapier.com/...
# NOTION_API_KEY=***
# ... (and other variables)
```

---

## 🚀 Step 5: Deploy to Railway

### 5.1 Deploy Application

```bash
# Deploy to Railway
railway up

# This will:
# 1. Build the Docker image
# 2. Push to Railway
# 3. Deploy services
# 4. Start the application

# Expected output:
# Building image...
# Pushing image...
# Deploying...
# ✓ Deployment successful
```

### 5.2 Monitor Deployment

```bash
# View deployment logs
railway logs --follow

# This shows real-time logs from your application
# Look for:
# - "MANUS BOOTSTRAP — STARTUP"
# - "All Zapier webhooks configured"
# - "Startup event logged"
# - "MANUS BOOTSTRAP READY"
```

### 5.3 Get Deployment URL

```bash
# Open Railway dashboard
railway open

# Or get the URL directly
railway variables get RAILWAY_STATIC_URL

# Your app is now available at:
# https://your-app-name.up.railway.app
```

---

## ✅ Step 6: Verify Deployment

### 6.1 Test Health Endpoint

```bash
# Test health check
curl https://your-app-name.up.railway.app/health

# Expected response:
# {
#   "status": "healthy",
#   "version": "14.5",
#   "codename": "Quantum Handshake",
#   "timestamp": "2025-10-21T20:30:00.000000",
#   "zapier": {
#     "configured": true,
#     "event_hook": true,
#     "agent_hook": true,
#     "system_hook": true
#   },
#   "session": {
#     "open": true
#   }
# }
```

### 6.2 Test Zapier Webhooks

```bash
# Test all three webhooks
curl -X POST https://your-app-name.up.railway.app/test/zapier

# Expected response:
# {
#   "status": "all_passed",
#   "results": {
#     "event_log": true,
#     "agent_registry": true,
#     "system_state": true
#   },
#   "timestamp": "2025-10-21T20:30:00.000000"
# }
```

### 6.3 Test Discord Bot

```bash
# In your Discord server, run:
!manus status

# Expected response:
# 🤲 **Manus Status**
# Status: HARMONIC
# Harmony: 0.355
# Last Update: 2025-10-21T20:30:00Z
# Directives Queued: 0
```

### 6.4 Verify Notion Sync

1. Open your Notion workspace
2. Check **Event Log** database — should see startup event
3. Check **Agent Registry** — Manus should be listed as Active
4. Check **System State** — components should be tracked
5. Check **Context Snapshots** — session should be saved

---

## 📊 Step 7: Monitor Production

### 7.1 View Logs

```bash
# View recent logs
railway logs --follow

# View logs from specific time
railway logs --since 1h

# View logs from specific service
railway logs --follow --service backend
```

### 7.2 Check Metrics

```bash
# View CPU and memory usage
railway status

# Expected output:
# CPU: 5-10%
# Memory: 100-200MB
# Uptime: XXh XXm
```

### 7.3 Monitor Zapier Integration

```bash
# Check if webhooks are being called
# In Railway logs, look for:
# - "Zapier webhook successful"
# - "Event logged to Notion"
# - "Agent status updated"

# Or check Notion databases for recent entries
```

### 7.4 Set Up Alerts (Optional)

In Railway dashboard:
1. Go to **Settings** → **Alerts**
2. Create alerts for:
   - High CPU usage (> 80%)
   - High memory usage (> 500MB)
   - Deployment failures
   - Health check failures

---

## 🔄 Step 8: Update and Redeploy

### 8.1 Make Code Changes

```bash
# Edit code locally
vim backend/manus_bootstrap.py

# Commit changes
git add .
git commit -m "Update Manus bootstrap"
git push origin main
```

### 8.2 Redeploy to Railway

```bash
# Redeploy automatically
railway up

# Or manually trigger deployment
railway redeploy

# Monitor the deployment
railway logs --follow
```

### 8.3 Rollback if Needed

```bash
# View deployment history
railway deployments

# Rollback to previous deployment
railway rollback <deployment-id>
```

---

## 🛡️ Step 9: Production Best Practices

### 9.1 Environment Isolation

```bash
# Use separate environments for dev and prod
railway init --environment staging
railway init --environment production

# Switch between environments
railway env staging
railway env production
```

### 9.2 Backup Strategy

```bash
# PostgreSQL backups (automatic on Railway)
# Redis snapshots (automatic on Railway)

# Manual backup
railway run pg_dump > backup.sql
```

### 9.3 Security

- **Never commit secrets** to Git
- **Use Railway environment variables** for all secrets
- **Rotate API keys** regularly
- **Monitor logs** for suspicious activity
- **Use HTTPS** for all connections

### 9.4 Performance Optimization

```bash
# Monitor resource usage
railway status

# Increase resources if needed
# In Railway dashboard:
# Settings → Compute → Increase CPU/Memory

# Scale horizontally (multiple instances)
# In Railway dashboard:
# Settings → Replicas → Set to 2+
```

---

## 🚨 Troubleshooting

### Issue: Deployment Fails

```bash
# Check build logs
railway logs --follow

# Common causes:
# - Missing environment variables
# - Dependency installation failure
# - Port already in use

# Solution:
# 1. Check all environment variables are set
# 2. Verify requirements.txt
# 3. Check for port conflicts
```

### Issue: Discord Bot Offline

```bash
# Check bot logs
railway logs --follow | grep discord

# Verify token
railway variables get DISCORD_TOKEN

# Restart bot
railway restart
```

### Issue: Zapier Webhooks Failing

```bash
# Check webhook logs
railway logs --follow | grep zapier

# Verify webhook URLs
railway variables get ZAPIER_EVENT_HOOK_URL
railway variables get ZAPIER_AGENT_HOOK_URL
railway variables get ZAPIER_SYSTEM_HOOK_URL

# Test webhooks
curl -X POST https://your-app-name.up.railway.app/test/zapier
```

### Issue: Notion Sync Not Working

```bash
# Check Notion API key
railway variables get NOTION_API_KEY

# Verify database IDs
railway variables get NOTION_AGENT_REGISTRY_DB
railway variables get NOTION_EVENT_LOG_DB
railway variables get NOTION_SYSTEM_STATE_DB
railway variables get NOTION_CONTEXT_DB

# Test Notion connection
curl https://your-app-name.up.railway.app/api/config/zapier
```

### Issue: High Memory Usage

```bash
# Check memory usage
railway status

# Identify memory leaks
railway logs --follow | grep memory

# Restart application
railway restart

# Increase memory allocation
# In Railway dashboard: Settings → Compute → Increase Memory
```

---

## 📈 Monitoring Dashboard

Create a monitoring dashboard to track:

| Metric | Target | Warning | Critical |
| :--- | :--- | :--- | :--- |
| **Uptime** | 99.9% | < 99% | < 95% |
| **Response Time** | < 100ms | < 500ms | > 1000ms |
| **Error Rate** | 0% | < 1% | > 5% |
| **CPU Usage** | < 20% | < 50% | > 80% |
| **Memory Usage** | < 200MB | < 400MB | > 500MB |
| **Zapier Success Rate** | 100% | > 95% | < 90% |
| **Notion Sync Latency** | < 500ms | < 1000ms | > 2000ms |

---

## 📚 Additional Resources

- **Railway Documentation:** https://docs.railway.app
- **Discord.py Documentation:** https://discordpy.readthedocs.io
- **Notion API:** https://developers.notion.com
- **Zapier Documentation:** https://zapier.com/help

---

## 🎯 Deployment Checklist

Before going live:

- [ ] All environment variables set in Railway
- [ ] PostgreSQL database created and configured
- [ ] Redis cache created and configured
- [ ] Zapier webhooks created and tested
- [ ] Discord bot token verified
- [ ] Notion API key verified
- [ ] Health endpoint returns 200 OK
- [ ] Discord bot appears online
- [ ] Zapier webhooks functional
- [ ] Notion databases receiving updates
- [ ] Logs being generated correctly
- [ ] Monitoring alerts configured
- [ ] Backup strategy in place
- [ ] Team trained on procedures

---

## 🙏 Summary

Your Helix Collective v14.5 is now deployed to Railway with:

- ✅ FastAPI backend with Manus Bootstrap
- ✅ Discord bot integration
- ✅ Zapier webhooks for real-time Notion sync
- ✅ PostgreSQL database
- ✅ Redis cache
- ✅ Comprehensive logging
- ✅ Health monitoring
- ✅ Production-ready configuration

---

**🚀 Helix Collective v14.5 — Production Deployed**  
*Tat Tvam Asi* 🙏

**Deployment URL:** https://your-app-name.up.railway.app  
**Status:** Live and Operational  
**Next Steps:** Monitor logs and verify Notion sync

