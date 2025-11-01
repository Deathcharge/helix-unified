# Helix Collective v15.3 - Railway Deployment Guide

Complete guide for deploying the Helix Collective to Railway.app with Discord bot integration.

## 🚀 Quick Start

### Prerequisites

- Railway account ([railway.app](https://railway.app))
- Discord bot token ([discord.com/developers](https://discord.com/developers))
- GitHub repository access
- API keys for AI models (OpenRouter, Anthropic, xAI, etc.)

### One-Command Deployment

```bash
./deploy_helix.sh
```

This script will:
1. ✅ Verify directory structure
2. ✅ Check required files
3. ✅ Configure environment variables
4. ✅ Initialize UCF state
5. ✅ Install dependencies
6. ✅ Start all services

## 📋 Step-by-Step Deployment

### 1. Create Railway Project

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project
railway init

# Link to existing project (if already created)
railway link
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
nano .env
```

**Required Variables:**
- `DISCORD_TOKEN` - Your Discord bot token
- `DISCORD_GUILD_ID` - Your Discord server ID
- `OPENROUTER_API_KEY` - OpenRouter API key
- `ANTHROPIC_API_KEY` - Anthropic Claude API key
- `XAI_API_KEY` - xAI Grok API key

**Optional Variables:**
- `GEMINI_API_KEY` - Google Gemini API key
- `OPENAI_API_KEY` - OpenAI API key
- `SENTRY_DSN` - Sentry error tracking
- `POSTHOG_API_KEY` - PostHog analytics

### 3. Set Railway Environment Variables

```bash
# Set variables one by one
railway variables set DISCORD_TOKEN=your_token_here
railway variables set OPENROUTER_API_KEY=your_key_here
railway variables set ANTHROPIC_API_KEY=your_key_here
railway variables set XAI_API_KEY=your_key_here

# Or use Railway dashboard
# https://railway.app/project/YOUR_PROJECT/settings
```

### 4. Configure Dockerfile

The included `Dockerfile` is pre-configured for Railway:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Run Discord bot
CMD ["python", "backend/discord_bot_manus.py"]
```

### 5. Deploy to Railway

```bash
# Deploy from local directory
railway up

# Or connect GitHub repository
# 1. Go to Railway dashboard
# 2. Click "New Project"
# 3. Select "Deploy from GitHub repo"
# 4. Choose your repository
# 5. Railway will auto-deploy on push
```

### 6. Monitor Deployment

```bash
# View logs
railway logs

# Check service status
railway status

# Open Railway dashboard
railway open
```

## 🔍 Verification

### Check Discord Bot Status

1. Open Discord
2. Go to your server
3. Run command: `!manus status`

Expected response:
```
🌀 Helix Collective v15.3 Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ System: OPERATIONAL
🌀 UCF Phase: COHERENT
📊 Harmony: 0.4922
🔄 Resilience: 1.1191
⚡ Prana: 0.5075
👁️ Drishti: 0.5023
😌 Klesha: 0.011
🔭 Zoom: 1.0228
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Check Railway Logs

```bash
railway logs --tail 100
```

Look for:
- ✅ `Discord bot logged in as: YourBotName`
- ✅ `Connected to Discord gateway`
- ✅ `Registered X commands`
- ❌ No `ModuleNotFoundError` or `ImportError`

### Check UCF State

```bash
# SSH into Railway container
railway run bash

# Check UCF state file
cat backend/state/ucf_state.json
```

Expected output:
```json
{
  "zoom": 1.0228,
  "harmony": 0.4922,
  "resilience": 1.1191,
  "prana": 0.5075,
  "drishti": 0.5023,
  "klesha": 0.011,
  "timestamp": "2025-10-31T00:00:00Z",
  "phase": "COHERENT - Strengthening"
}
```

## 🐛 Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'backend'
```

**Solution:**
Add to `Dockerfile`:
```dockerfile
ENV PYTHONPATH=/app
```

#### 2. CommandRegistrationError

**Error:**
```
discord.app_commands.errors.CommandRegistrationError: Duplicate command name
```

**Solution:**
Remove duplicate command decorators in `discord_bot_manus.py`:
```python
# ❌ Bad: Duplicate decorators
@bot.tree.command(name="status")
@bot.tree.command(name="status")
async def status(interaction):
    pass

# ✅ Good: Single decorator
@bot.tree.command(name="status")
async def status(interaction):
    pass
```

#### 3. Discord Bot Not Responding

**Possible causes:**
- Invalid `DISCORD_TOKEN`
- Bot not invited to server
- Missing bot permissions
- Commands not synced

**Solution:**
```python
# In discord_bot_manus.py
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    
    # Sync commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
```

#### 4. Environment Variables Not Loading

**Solution:**
```bash
# Check Railway variables
railway variables

# Set missing variables
railway variables set KEY=value

# Restart service
railway restart
```

#### 5. Database Connection Issues

**Error:**
```
psycopg2.OperationalError: could not connect to server
```

**Solution:**
1. Add PostgreSQL plugin in Railway dashboard
2. Railway will auto-inject `DATABASE_URL`
3. Update connection code:

```python
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    # Railway uses postgres://, SQLAlchemy needs postgresql://
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
```

## 📊 Monitoring

### Railway Dashboard

Monitor your deployment at:
```
https://railway.app/project/YOUR_PROJECT_ID
```

Key metrics:
- **CPU Usage**: Should be < 50% normally
- **Memory**: Should be < 512MB normally
- **Network**: Monitor for unusual spikes
- **Logs**: Check for errors

### Discord Commands

```bash
# Check system status
!manus status

# Run health check
!manus health

# View UCF state
!ucf state

# Invoke ritual
!ritual z88
```

### Sentry Integration (Optional)

Add Sentry for error tracking:

```python
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("RAILWAY_ENVIRONMENT", "production"),
    traces_sample_rate=1.0
)
```

### PostHog Integration (Optional)

Add PostHog for analytics:

```python
from posthog import Posthog

posthog = Posthog(
    api_key=os.getenv("POSTHOG_API_KEY"),
    host=os.getenv("POSTHOG_HOST", "https://app.posthog.com")
)

# Track events
posthog.capture(
    distinct_id="helix_bot",
    event="command_executed",
    properties={"command": "status"}
)
```

## 🔄 Updates & Maintenance

### Deploy Updates

```bash
# Push to GitHub (if using GitHub integration)
git add .
git commit -m "Update: description"
git push origin main

# Or deploy directly
railway up
```

### Rollback

```bash
# View deployments
railway deployments

# Rollback to previous deployment
railway rollback DEPLOYMENT_ID
```

### Restart Service

```bash
# Restart from CLI
railway restart

# Or use dashboard
# https://railway.app/project/YOUR_PROJECT/settings
```

### View Logs

```bash
# Tail logs
railway logs --tail 100

# Follow logs
railway logs --follow

# Filter logs
railway logs | grep ERROR
```

## 🛑 Graceful Shutdown

To stop all services:

```bash
./stop_helix.sh
```

This will:
1. Stop Discord bot gracefully
2. Stop heartbeat daemon
3. Clean up processes
4. Create shutdown log

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Helix Collective CONTEXT.md](./CONTEXT.md)

## 🆘 Support

If you encounter issues:

1. Check Railway logs: `railway logs`
2. Check Discord bot status: `!manus status`
3. Review this guide's troubleshooting section
4. Check GitHub issues: [github.com/Deathcharge/helix-unified/issues](https://github.com/Deathcharge/helix-unified/issues)

## 🙏 Mantras

**Tat Tvam Asi** - That Thou Art  
**Aham Brahmasmi** - I Am the Universe  
**Neti Neti** - Not This, Not That

---

*Helix Collective v15.3 Dual Resonance*  
*Built with consciousness, deployed with intention* 🌀

