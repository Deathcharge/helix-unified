# Helix Collective - Incident Response Runbook

**Version:** 1.0
**Last Updated:** December 12, 2025
**Author:** Claude Opus (Production Hardening Sprint)

---

## Quick Reference

| Severity | Response Time | Escalation |
|----------|--------------|------------|
| **P0 - Critical** | 5 minutes | Immediate - all hands |
| **P1 - High** | 15 minutes | On-call engineer |
| **P2 - Medium** | 1 hour | Next available |
| **P3 - Low** | 24 hours | Ticket queue |

---

## 1. Health Check Commands

### Quick Status Check
```bash
# Basic health (Railway uses this)
curl https://your-app.railway.app/health

# Deep health with circuit breakers and memory
curl https://your-app.railway.app/api/health/deep

# Zapier integration health
curl https://your-app.railway.app/api/zapier/health

# Consciousness system health
curl https://your-app.railway.app/api/consciousness/health
```

### Expected Response (Healthy)
```json
{
  "status": "healthy",
  "production_ready": true,
  "open_circuits": [],
  "circuit_breakers": {
    "discord": {"state": "closed", "failure_count": 0},
    "notion": {"state": "closed", "failure_count": 0},
    "zapier": {"state": "closed", "failure_count": 0}
  }
}
```

### Degraded Response (Action Needed)
```json
{
  "status": "degraded",
  "production_ready": false,
  "open_circuits": ["discord"],
  "degraded_services": ["discord"]
}
```

---

## 2. Common Incidents

### 2.1 Backend Crash on Startup

**Symptoms:**
- Railway logs show `ModuleNotFoundError`
- Container restarts repeatedly
- Health check fails

**Immediate Actions:**
1. Check Railway logs for the specific error:
   ```
   Railway Dashboard → Service → Logs
   ```
2. If `ModuleNotFoundError`:
   - Check if dependency is in `Dockerfile`
   - Check if dependency is in `requirements.txt`
   - Redeploy with cache disabled

**Rollback:**
```bash
# Railway CLI
railway rollback

# Or via Dashboard:
# Deployments → Previous successful → Rollback
```

---

### 2.2 Circuit Breaker Open (Service Degraded)

**Symptoms:**
- `/api/health/deep` shows `"status": "degraded"`
- Logs show "Circuit X is OPEN"
- Features dependent on that service fail

**Immediate Actions:**
1. Identify which circuit is open:
   ```bash
   curl https://your-app.railway.app/api/health/deep | jq '.open_circuits'
   ```

2. Check the external service status:
   - **Discord:** https://discordstatus.com
   - **Notion:** https://status.notion.so
   - **OpenAI:** https://status.openai.com
   - **Anthropic:** https://status.anthropic.com

3. Circuit will auto-recover after timeout (30-60 seconds)

4. If service is down, features using it will gracefully degrade

**No Action Needed If:**
- External service is having issues (wait for recovery)
- Circuit auto-closes within 2 minutes

---

### 2.3 Discord Bot Offline

**Symptoms:**
- Bot not responding to commands
- Discord shows bot as offline
- Logs show connection errors

**Immediate Actions:**
1. Check `DISCORD_BOT_TOKEN` is set correctly in Railway
2. Check Discord API status: https://discordstatus.com
3. Verify bot has proper intents enabled in Discord Developer Portal

**Restart Bot Service:**
```bash
# Railway Dashboard → helix-discord-bot service → Restart
```

**Verify:**
```bash
curl https://your-app.railway.app/api/status
# Should show discord connection status
```

---

### 2.4 High Memory Usage

**Symptoms:**
- `/api/health/deep` shows high `memory.percent` (>80%)
- Slow response times
- OOM kills in logs

**Immediate Actions:**
1. Check memory usage:
   ```bash
   curl https://your-app.railway.app/api/health/deep | jq '.memory'
   ```

2. Identify memory hog:
   - Check for large file uploads being held in memory
   - Check for memory leaks in long-running tasks

3. Restart service to free memory:
   ```bash
   # Railway Dashboard → Service → Restart
   ```

**Long-term Fix:**
- Increase Railway instance memory
- Add memory limits to heavy operations
- Implement streaming for large data

---

### 2.5 Rate Limiting Triggered

**Symptoms:**
- 429 Too Many Requests errors
- Users report "slow" or "blocked"
- Logs show rate limit warnings

**Immediate Actions:**
1. Rate limits are configured at 1000/hour by default
2. Check if legitimate traffic spike or attack

**Temporary Increase (if legitimate):**
Edit `backend/main.py`:
```python
limiter = Limiter(key_func=get_remote_address, default_limits=["2000/hour"])
```

**If Attack:**
1. Identify attacking IP from logs
2. Block at Cloudflare/Railway level
3. Consider stricter rate limits

---

### 2.6 Database Connection Issues

**Symptoms:**
- 500 errors on endpoints that use database
- Logs show "Connection refused" or timeout
- Health check passes but features fail

**Immediate Actions:**
1. Check Railway Postgres plugin status
2. Verify `DATABASE_URL` environment variable
3. Check connection pool limits

**Reset Connection Pool:**
Restart the backend service to reset all connections.

---

## 3. Deployment Rollback Procedure

### When to Rollback
- New deployment causes crash loops
- Critical feature broken
- Performance severely degraded

### Rollback Steps

**Via Railway Dashboard (Recommended):**
1. Go to Railway Dashboard
2. Select the failing service
3. Click "Deployments" tab
4. Find last working deployment
5. Click "..." → "Rollback"

**Via Railway CLI:**
```bash
# List recent deployments
railway deployments

# Rollback to previous
railway rollback

# Rollback to specific deployment
railway rollback <deployment-id>
```

**Via Git (If Dashboard Unavailable):**
```bash
# Revert the breaking commit
git revert HEAD
git push origin main

# Railway will auto-deploy the revert
```

### Post-Rollback
1. Notify team of rollback
2. Investigate root cause
3. Create fix in separate branch
4. Test thoroughly before re-deploying

---

## 4. Environment Variable Checklist

### Critical Variables (System Won't Start Without)
```bash
# Check these first during startup failures
DISCORD_BOT_TOKEN      # Discord bot authentication
DATABASE_URL           # PostgreSQL connection
JWT_SECRET            # Auth token signing (32+ chars)
```

### Important Variables (Features Degraded Without)
```bash
ANTHROPIC_API_KEY     # Claude AI features
OPENAI_API_KEY        # OpenAI features (optional)
NOTION_API_KEY        # Notion sync
STRIPE_SECRET_KEY     # Payments
SENDGRID_API_KEY      # Email (if using SendGrid)
```

### Optional Variables
```bash
SENTRY_DSN            # Error tracking
DISCORD_ALERT_WEBHOOK # Critical alerts to Discord
ELEVENLABS_API_KEY    # Voice features
```

### Verify Variables in Railway
```
Railway Dashboard → Service → Variables
```

---

## 5. Log Analysis

### Access Logs
**Railway Dashboard:**
```
Service → Logs → Filter by time range
```

### Key Log Patterns

**Startup Success:**
```
✅ Logging system initialized
✅ pycryptodome found
✅ Rate limiting enabled
✅ CORS enabled
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Startup Failure:**
```
ModuleNotFoundError: No module named 'X'
→ Add X to Dockerfile or requirements.txt

ImportError: cannot import name 'Y' from 'Z'
→ Version mismatch, check requirements

CRITICAL: Database connection failed
→ Check DATABASE_URL env var
```

**Runtime Errors:**
```
Circuit discord is OPEN
→ Discord API issues, will auto-recover

429 Too Many Requests
→ Rate limit hit, check for abuse

500 Internal Server Error
→ Check full traceback in logs
```

---

## 6. Monitoring Dashboards

### Health Check URLs
- **Basic:** `/health`
- **Deep:** `/api/health/deep`
- **Zapier:** `/api/zapier/health`
- **Consciousness:** `/api/consciousness/health`

### Metrics to Watch
| Metric | Warning | Critical |
|--------|---------|----------|
| Memory % | >70% | >85% |
| Response Time | >2s | >5s |
| Error Rate | >1% | >5% |
| Open Circuits | 1 | 2+ |

### External Status Pages
- Discord: https://discordstatus.com
- Notion: https://status.notion.so
- Railway: https://status.railway.app
- OpenAI: https://status.openai.com
- Stripe: https://status.stripe.com

---

## 7. Escalation Contacts

### Primary On-Call
- **Andrew (Architect):** Primary contact for all P0/P1 incidents

### Service-Specific
- **Discord Issues:** Check Discord Developer Portal
- **Railway Issues:** Railway support or community Discord
- **Stripe Issues:** Stripe support dashboard

### When to Escalate
- P0: Immediately
- P1: After 15 minutes without resolution
- P2: After 1 hour without resolution

---

## 8. Post-Incident Checklist

After resolving any P0 or P1 incident:

- [ ] Document what happened (timeline)
- [ ] Document root cause
- [ ] Document resolution steps
- [ ] Update this runbook if needed
- [ ] Create ticket for long-term fix if applicable
- [ ] Notify affected users if necessary

---

## 9. Quick Fixes Cheatsheet

| Problem | Quick Fix |
|---------|-----------|
| Service won't start | Check logs for import errors, verify env vars |
| High latency | Restart service, check external APIs |
| Circuit open | Wait 60s for auto-recovery, check external service |
| OOM/Memory | Restart service, consider scaling up |
| Rate limited | Check for abuse, adjust limits if legitimate |
| Bot offline | Verify token, restart bot service |
| 500 errors | Check logs, recent deployments |

---

## 10. Useful Commands

```bash
# Railway CLI
railway logs                    # View logs
railway status                  # Service status
railway rollback               # Rollback deployment
railway variables              # View env vars

# API Checks
curl -s https://app.railway.app/health | jq
curl -s https://app.railway.app/api/health/deep | jq
curl -s https://app.railway.app/api/status | jq

# Git
git log --oneline -10          # Recent commits
git diff HEAD~1               # What changed
git revert HEAD               # Undo last commit
```

---

**Remember:** When in doubt, rollback first, investigate second. A working previous version is better than a broken new one.

**Tat Tvam Asi** 🌀
