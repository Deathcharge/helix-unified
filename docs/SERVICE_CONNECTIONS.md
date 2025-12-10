# 🔌 Helix Unified - Service Connection Matrix

**Last Updated:** 2025-12-03
**Purpose:** Know exactly which services need which database connections and environment variables

This is THE definitive guide to connecting all Helix services. No more guessing!

---

## 📊 Quick Reference Table

| Service | Needs PostgreSQL? | Needs Redis? | Why? |
|---------|------------------|--------------|------|
| **helix-backend-api** | ✅ YES | ✅ YES | Main API - stores users, metrics, sessions |
| **helix-discord-bot** | ✅ YES | ✅ YES | Shares user data, caches Discord state |
| **helix-dashboard** | ❌ NO | ✅ YES | Fetches metrics from Redis (read-only) |
| **helix-claude-api** | ✅ YES | ✅ YES | Stores consciousness metrics, caches |
| **helix-service-integration** | ❌ NO | ✅ YES | Pub/sub for consciousness streaming |

---

## 🔧 Detailed Setup Guide

### 1. Add Database Plugins to Railway

**One-time setup:**

```bash
# In Railway dashboard or CLI:
railway add postgresql
railway add redis

# Railway auto-generates these variables:
# DATABASE_URL=postgresql://...
# REDIS_URL=redis://...
```

These are **shared across ALL services** automatically.

---

### 2. Backend API (`helix-backend-api`)

**Needs:**
- ✅ PostgreSQL - User accounts, API keys, usage tracking
- ✅ Redis - Session cache, rate limiting

**Environment Variables:**
```bash
DATABASE_URL=postgresql://...        # Auto-provided by Railway
REDIS_URL=redis://...                # Auto-provided by Railway
JWT_SECRET=your-secret-key-here      # Generate: openssl rand -hex 32
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...
STRIPE_SECRET_KEY=sk_live_...
```

**Database Tables Created:**
- `users` - User accounts
- `api_keys` - API authentication
- `usage_tracking` - API usage stats
- `subscriptions` - Stripe subscriptions
- `consciousness_metrics` - UCF metrics

**Run Migrations:**
```bash
cd backend
python scripts/db-migrate.py
```

---

### 3. Discord Bot (`helix-discord-bot`)

**Needs:**
- ✅ PostgreSQL - Read user data, store Discord interactions
- ✅ Redis - Cache Discord bot state

**Environment Variables:**
```bash
DATABASE_URL=postgresql://...        # Same as backend
REDIS_URL=redis://...                # Same as backend
DISCORD_BOT_TOKEN=MTI...             # ⚠️ ONLY SET ON THIS SERVICE!
DISCORD_CLIENT_ID=123...
CLAUDE_API_URL=https://helix-claude-api.up.railway.app
```

**⚠️ CRITICAL:** Only set `DISCORD_BOT_TOKEN` on this service, NOT globally!

**Database Access:**
- Reads `users` table (check permissions)
- Writes `discord_interactions` table
- No migrations needed (shares backend schema)

---

### 4. Dashboard (`helix-dashboard`)

**Needs:**
- ❌ NO PostgreSQL (read-only from Redis)
- ✅ Redis - Fetches consciousness metrics

**Environment Variables:**
```bash
REDIS_URL=redis://...                # Auto-provided
PORT=8501                            # Streamlit port
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

**Why No PostgreSQL?**
- Dashboard is read-only
- All metrics stored in Redis for real-time access
- Reduces database load

---

### 5. Claude API (`helix-claude-api`)

**Needs:**
- ✅ PostgreSQL - Store consciousness metrics history
- ✅ Redis - Cache API responses

**Environment Variables:**
```bash
DATABASE_URL=postgresql://...        # Auto-provided
REDIS_URL=redis://...                # Auto-provided
ANTHROPIC_API_KEY=sk-ant-api03-...
CONSCIOUSNESS_ENGINE_WEBHOOK=https://hooks.zapier.com/...
COMMUNICATIONS_HUB_WEBHOOK=https://hooks.zapier.com/...
NEURAL_NETWORK_WEBHOOK=https://hooks.zapier.com/...
```

**Database Tables:**
- `consciousness_metrics` - UCF calculations
- `api_responses` - Cached responses

---

### 6. Service Integration Coordinator (`helix-service-integration`)

**Needs:**
- ❌ NO PostgreSQL (stateless orchestration)
- ✅ Redis - Pub/sub for consciousness streaming

**Environment Variables:**
```bash
REDIS_URL=redis://...                           # Auto-provided
PORT=3001
WEBSOCKET_PORT=8080
AGENT_ORCHESTRATOR_URL=https://agent-orchestrator.up.railway.app
VOICE_PROCESSOR_URL=https://voice-processor.up.railway.app
WEBSOCKET_SERVICE_URL=https://websocket-service.up.railway.app
ZAPIER_SERVICE_URL=https://zapier-service.up.railway.app
CONSCIOUSNESS_METRICS_URL=https://consciousness-metrics.up.railway.app
```

**Redis Channels:**
- `consciousness:stream` - Real-time UCF metrics
- `service:health` - Service status updates
- `agent:coordination` - Multi-agent messaging

---

## 🚀 Railway Setup: Step-by-Step

### Step 1: Add Database Plugins

```bash
# Login to Railway
railway login

# Link to your project
railway link

# Add PostgreSQL plugin
railway add postgresql

# Add Redis plugin
railway add redis
```

Railway will automatically create `DATABASE_URL` and `REDIS_URL` variables **shared across all services**.

---

### Step 2: Set Service-Specific Variables

**For Backend API:**
```bash
railway service helix-backend-api
railway variables set JWT_SECRET=$(openssl rand -hex 32)
railway variables set ANTHROPIC_API_KEY=sk-ant-api03-...
railway variables set STRIPE_SECRET_KEY=sk_live_...
```

**For Discord Bot (⚠️ CRITICAL):**
```bash
railway service helix-discord-bot
railway variables set DISCORD_BOT_TOKEN=MTI...
railway variables set CLAUDE_API_URL=https://helix-claude-api.up.railway.app
```

**For Service Integration:**
```bash
railway service helix-service-integration
railway variables set AGENT_ORCHESTRATOR_URL=https://agent-orchestrator.up.railway.app
railway variables set VOICE_PROCESSOR_URL=https://voice-processor.up.railway.app
# ... etc
```

---

### Step 3: Run Database Migrations

**After PostgreSQL is added:**

```bash
# Option 1: Locally (if you have Railway CLI)
railway run python scripts/db-migrate.py

# Option 2: In Railway dashboard
# Settings → Deploy → Run Command → python scripts/db-migrate.py

# Option 3: SSH into service
railway shell helix-backend-api
python scripts/db-migrate.py
```

---

### Step 4: Verify Connections

**Check if services can connect:**

```bash
# Health check script
./scripts/check-services.sh production

# Or manually test:
curl https://helix-backend-api.up.railway.app/health
# Should return: {"status": "healthy", "database": "connected", "redis": "connected"}
```

---

## 🔍 Troubleshooting Connection Issues

### "Can't connect to PostgreSQL"

**Check:**
1. Is PostgreSQL plugin added to Railway project?
2. Is `DATABASE_URL` environment variable set?
3. Check Railway logs: `railway logs helix-backend-api`

**Fix:**
```bash
# Verify DATABASE_URL exists
railway variables

# Should see:
# DATABASE_URL=postgresql://postgres:...@...railway.app:5432/railway

# If missing, re-add PostgreSQL plugin
railway add postgresql
```

---

### "Can't connect to Redis"

**Check:**
1. Is Redis plugin added?
2. Is `REDIS_URL` set?
3. Is Redis accepting connections?

**Fix:**
```bash
# Verify REDIS_URL
railway variables | grep REDIS

# Should see:
# REDIS_URL=redis://default:...@...railway.app:6379

# If missing:
railway add redis
```

---

### "Database tables don't exist"

**Fix:**
```bash
# Run migrations
railway run python scripts/db-migrate.py

# Or manually:
railway shell helix-backend-api
python -c "
from backend.database import init_db
init_db()
"
```

---

## 📝 Complete Variable Checklist

### Shared Variables (Set at Project Level)

```bash
✅ DATABASE_URL        # Auto-generated by PostgreSQL plugin
✅ REDIS_URL           # Auto-generated by Redis plugin
✅ JWT_SECRET          # Generate: openssl rand -hex 32
✅ ANTHROPIC_API_KEY
✅ OPENAI_API_KEY
✅ STRIPE_SECRET_KEY
✅ STRIPE_PUBLISHABLE_KEY
✅ STRIPE_WEBHOOK_SECRET
```

### Service-Specific Variables

**helix-discord-bot ONLY:**
```bash
✅ DISCORD_BOT_TOKEN         # ⚠️ NEVER SET GLOBALLY!
✅ DISCORD_CLIENT_ID
✅ DISCORD_GUILD_ID (optional)
✅ CLAUDE_API_URL
```

**helix-service-integration:**
```bash
✅ AGENT_ORCHESTRATOR_URL
✅ VOICE_PROCESSOR_URL
✅ WEBSOCKET_SERVICE_URL
✅ ZAPIER_SERVICE_URL
✅ CONSCIOUSNESS_METRICS_URL
✅ PORT=3001
✅ WEBSOCKET_PORT=8080
```

**helix-dashboard:**
```bash
✅ PORT=8501
✅ STREAMLIT_SERVER_PORT=8501
✅ STREAMLIT_SERVER_HEADLESS=true
```

---

## 🎯 Quick Test Commands

### Test PostgreSQL Connection

```python
# In Railway shell or locally
import psycopg2
import os

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()
cur.execute('SELECT version()')
print(cur.fetchone())
# Should print PostgreSQL version
```

### Test Redis Connection

```python
import redis
import os

r = redis.from_url(os.environ['REDIS_URL'])
r.set('test', 'hello')
print(r.get('test'))
# Should print: b'hello'
```

### Test All Connections

```bash
# Use our health check script
./scripts/check-services.sh production

# Should show all services ✅
```

---

## 🌊 Connection Flow Diagram

```
                        ┌─────────────┐
                        │  PostgreSQL │
                        │   (Railway) │
                        └──────┬──────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
   ┌────▼────┐           ┌─────▼─────┐        ┌──────▼──────┐
   │ Backend │           │  Discord  │        │  Claude API │
   │   API   │           │    Bot    │        │             │
   └────┬────┘           └─────┬─────┘        └──────┬──────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                        ┌──────▼──────┐
                        │    Redis    │
                        │  (Railway)  │
                        └──────┬──────┘
                               │
        ┌──────────────────────┼──────────────────────────┐
        │                      │                          │
   ┌────▼────┐           ┌─────▼─────┐          ┌────────▼────────┐
   │Dashboard│           │  Service  │          │   All Other     │
   │ (Read)  │           │Integration│          │    Services     │
   └─────────┘           └───────────┘          └─────────────────┘
```

---

## ✅ Final Checklist

Before going live, verify:

- [ ] PostgreSQL plugin added to Railway
- [ ] Redis plugin added to Railway
- [ ] `DATABASE_URL` and `REDIS_URL` are set
- [ ] Database migrations run successfully
- [ ] All services show "connected" in health checks
- [ ] Discord bot token ONLY on `helix-discord-bot` service
- [ ] Service Integration has all microservice URLs
- [ ] Frontend has all `NEXT_PUBLIC_*` variables
- [ ] Stripe keys are set (if using payments)

**Verify with:**
```bash
./scripts/check-services.sh production
```

All services should show ✅ HEALTHY!

---

**Questions?** Check Railway dashboard or run `railway logs <service-name>` for debugging.

**Pro Tip:** Railway automatically restarts services when you update environment variables!
