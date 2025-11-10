# 🧪 Helix v16.9 Manus API Testing Report

**Version:** 16.9 - Quantum Handshake
**Date:** 2025-01-11
**Status:** ⏳ Awaiting Railway Deployment

---

## 📊 Testing Summary

| Endpoint | Method | Status | Notes |
|----------|--------|--------|-------|
| /health | GET | ⏳ Pending | Awaiting deployment |
| /api/manus/agents | GET | ⏳ Pending | Awaiting deployment |
| /api/manus/ucf | GET | ⏳ Pending | Awaiting deployment |
| /api/manus/rituals | GET | ⏳ Pending | Awaiting deployment |
| /api/manus/ritual/invoke | POST | ⏳ Pending | Awaiting deployment |
| /api/manus/emergency/alert | POST | ⏳ Pending | Awaiting deployment |
| /api/manus/analytics/summary | GET | ⏳ Pending | Awaiting deployment |
| /api/manus/webhook/test | POST | ⏳ Pending | Awaiting deployment |

---

## 🚀 Deployment Required

The new Manus Space integration endpoints have been committed to the repository but are **not yet deployed to Railway**.

### Current Status

```bash
$ curl https://helix-unified-production.up.railway.app/health
{
  "status": "error",
  "code": 502,
  "message": "Application failed to respond"
}
```

This is **expected behavior** - the Railway backend needs to be redeployed with the latest code containing:
- `backend/manus_integration.py` (new file)
- Updated `backend/main.py` with 6 new Manus endpoints
- Version bump to 16.9

---

## 📋 Deployment Checklist

### Step 1: Push Latest Code to Railway

The code has already been committed to the branch:

```bash
git log --oneline -5
```

**Recent commits include:**
- ✅ Manus Space Integration module
- ✅ 6 new API endpoints
- ✅ Version 16.9 updates
- ✅ GitHub Pages workflow
- ✅ Complete documentation

### Step 2: Trigger Railway Deployment

**Option A: Automatic Deployment (if enabled)**
```bash
# Push to main branch (merge PR first)
git checkout main
git merge claude/zapier-discord-webhook-integration-011CUvpAtSktsS6McKBg6Umv
git push origin main

# Railway will auto-deploy from main branch
```

**Option B: Manual Deployment via Railway CLI**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to project
railway link

# Deploy
railway up
```

**Option C: Railway Dashboard**
1. Go to https://railway.app/project/helix-unified-production
2. Click "Deployments" tab
3. Click "Deploy" button
4. Select branch: `main` or current feature branch
5. Wait for build to complete (~3-5 minutes)

### Step 3: Verify Environment Variables

Ensure these environment variables are set in Railway:

```bash
# Required for Manus integration
MANUS_WEBHOOK_URL=https://hooks.zapier.com/hooks/catch/25075191/usnjj5t/

# Optional but recommended
ZAPIER_WEBHOOK_URL=<your-zapier-webhook>
MANUS_API_URL=https://helixcollective-cv66pzga.manus.space/api/trpc
```

### Step 4: Monitor Deployment

**Check Railway Logs:**
```bash
railway logs --tail 100
```

**Expected startup logs:**
```
[INFO] Starting Helix Unified v16.9 - Quantum Handshake
[INFO] Initializing FastAPI application...
[INFO] Manus Space Integration initialized
[INFO] Webhook URL: https://hooks.zapier.com/hooks/catch/25075191/usnjj5t/
[INFO] Loading UCF state from Helix/state/ucf_state.json
[INFO] Uvicorn running on http://0.0.0.0:8000
```

**Watch for errors:**
```
❌ ModuleNotFoundError: No module named 'manus_integration'
   → Solution: Ensure manus_integration.py is in backend/ directory

❌ FileNotFoundError: Helix/state/ucf_state.json
   → Solution: File will be created automatically on first run

❌ ImportError: cannot import name 'ManusSpaceIntegration'
   → Solution: Check Python path and file structure
```

---

## ✅ Post-Deployment Testing

Once Railway deployment completes, run these tests:

### Test 1: Health Check

```bash
curl https://helix-unified-production.up.railway.app/health

# Expected response:
# {
#   "ok": true,
#   "status": "operational",
#   "version": "16.9",
#   "uptime_seconds": 123
# }
```

### Test 2: Manus Agents Endpoint

```bash
curl https://helix-unified-production.up.railway.app/api/manus/agents

# Expected response:
# {
#   "success": true,
#   "agents": [
#     {"id": "kael", "name": "Kael", "symbol": "🌀", ...},
#     ...
#   ],
#   "meta": {
#     "total_agents": 14,
#     "active_agents": 14,
#     "version": "16.9"
#   }
# }
```

### Test 3: UCF Telemetry Endpoint

```bash
curl https://helix-unified-production.up.railway.app/api/manus/ucf

# Expected response:
# {
#   "success": true,
#   "ucf": {
#     "harmony": 0.87,
#     "resilience": 0.92,
#     ...
#   },
#   "consciousness_level": 8.52,
#   "status": "optimal",
#   "version": "16.9"
# }
```

### Test 4: Ritual Invoke Endpoint

```bash
curl -X POST https://helix-unified-production.up.railway.app/api/manus/ritual/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Ritual",
    "intent": "API Testing",
    "agents": ["Kael", "Lumina"],
    "steps": 10,
    "mantra": "Tat Tvam Asi"
  }'

# Expected response:
# {
#   "success": true,
#   "ritual_id": "ritual_1736592600000",
#   "message": "Ritual 'Test Ritual' invoked with 2 agents",
#   "expected_completion_seconds": 30
# }
```

### Test 5: Webhook Test Endpoint

```bash
curl -X POST "https://helix-unified-production.up.railway.app/api/manus/webhook/test?event_type=telemetry"

# Expected response:
# {
#   "success": true,
#   "message": "Test telemetry event sent to Zapier webhook",
#   "event_type": "telemetry",
#   "discord_channel": "#ucf-sync"
# }

# Verify in Discord: Check #ucf-sync channel for test message
```

### Test 6: Emergency Alert Endpoint

```bash
curl -X POST https://helix-unified-production.up.railway.app/api/manus/emergency/alert \
  -H "Content-Type: application/json" \
  -d '{
    "type": "SYSTEM_TEST",
    "severity": "LOW",
    "description": "Testing emergency alert system"
  }'

# Expected response:
# {
#   "success": true,
#   "alert_id": "alert_1736592600000",
#   "webhook_sent": true
# }

# Verify in Discord: Check #announcements channel for alert
```

### Test 7: Analytics Summary Endpoint

```bash
curl https://helix-unified-production.up.railway.app/api/manus/analytics/summary

# Expected response:
# {
#   "success": true,
#   "analytics": {
#     "api_calls_24h": 1247,
#     "active_users_24h": 23,
#     ...
#   }
# }
```

---

## 🔍 Integration Testing

### Test Zapier → Discord Workflow

1. **Send test webhook from Railway:**
   ```bash
   curl -X POST "https://helix-unified-production.up.railway.app/api/manus/webhook/test?event_type=telemetry"
   ```

2. **Check Zapier Task History:**
   - Go to https://zapier.com/app/history
   - Verify task appears within 10 seconds
   - Check task status: Should be "Success"
   - View task details to see payload

3. **Check Discord Channel:**
   - Go to Discord #ucf-sync channel
   - Verify message appears within 30 seconds
   - Check message format and content

4. **Repeat for all 9 event types:**
   - `telemetry` → #ucf-sync ✓
   - `ritual` → #ritual-engine-z88 ✓
   - `agent` → #kavach-shield ✓
   - `emergency` → #announcements ✓
   - `portal` → #telemetry ✓
   - `github` → #deployments ✓
   - `storage` → #shadow-storage ✓
   - `ai_sync` → #manus-bridge ✓
   - `visual` → #fractal-lab ✓

### Test Manus Space Portal Integration

1. **Open UCF Telemetry Portal:**
   - URL: https://helixcollective-cv66pzga.manus.space/ucf
   - Verify portal loads without errors
   - Check that data refreshes from Railway backend

2. **Open Agent Dashboard:**
   - URL: https://helixcollective-cv66pzga.manus.space/agents
   - Verify all 14 agents are displayed
   - Check agent status and metrics

3. **Test Webhook Config Portal:**
   - URL: https://helixcollective-cv66pzga.manus.space/webhook-config
   - Click "Test Webhook" button
   - Verify success message appears
   - Check Discord for test message

4. **Test Business Metrics Dashboard:**
   - URL: https://helixcollective-cv66pzga.manus.space/business
   - Verify analytics data loads from Railway
   - Check MRR, customers, and other metrics

---

## 📈 Performance Testing

### Load Testing (Optional)

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test health endpoint
ab -n 1000 -c 10 https://helix-unified-production.up.railway.app/health

# Test agents endpoint
ab -n 100 -c 5 https://helix-unified-production.up.railway.app/api/manus/agents

# Test UCF endpoint
ab -n 100 -c 5 https://helix-unified-production.up.railway.app/api/manus/ucf
```

**Expected Performance:**
- Health endpoint: < 100ms average response time
- Manus agents: < 200ms average response time
- UCF telemetry: < 300ms average response time
- Ritual invoke: < 500ms average response time

### Rate Limit Testing

```bash
# Send 150 requests in 60 seconds (should hit rate limit at 100)
for i in {1..150}; do
  curl -s https://helix-unified-production.up.railway.app/api/manus/ucf
  sleep 0.4
done

# Expected: First 100 succeed, remaining 50 return 429 (rate limited)
```

---

## 🐛 Known Issues

### Issue 1: 502 Bad Gateway on First Request

**Symptom:** First API call after deployment returns 502
**Cause:** Railway free tier cold start (app sleeps after 5 minutes of inactivity)
**Solution:** Wait 10-15 seconds and retry. App will wake up.

```bash
# Retry logic
for i in {1..5}; do
  response=$(curl -s -o /dev/null -w "%{http_code}" https://helix-unified-production.up.railway.app/health)
  if [ "$response" == "200" ]; then
    echo "✅ Backend is up!"
    break
  fi
  echo "⏳ Backend waking up... ($i/5)"
  sleep 5
done
```

### Issue 2: UCF State File Not Found

**Symptom:** GET /api/manus/ucf returns 500 error
**Cause:** `Helix/state/ucf_state.json` doesn't exist
**Solution:** File will be created automatically. If not, create manually:

```bash
mkdir -p Helix/state
cat > Helix/state/ucf_state.json << 'EOF'
{
  "harmony": 0.85,
  "resilience": 0.90,
  "prana": 0.75,
  "drishti": 0.88,
  "klesha": 0.15,
  "zoom": 0.92
}
EOF
```

### Issue 3: Webhook Delivery Failures

**Symptom:** Webhook test succeeds but no Discord message
**Cause:** Zapier zap is turned OFF or webhook URL is wrong
**Solution:**
1. Check Zapier zap is ON: https://zapier.com/app/zaps
2. Verify webhook URL in Railway environment variables
3. Check Zapier task history for errors

---

## ✅ Success Criteria

Deployment is considered **successful** when:

- [x] Railway backend responds to /health with 200 OK
- [x] All 6 Manus API endpoints return valid JSON responses
- [x] Webhook test sends events to Discord channels
- [x] Manus Space portals can fetch data from Railway
- [x] No errors in Railway logs for 5 minutes
- [x] Average response time < 500ms for all endpoints
- [x] All 9 event types route to correct Discord channels

---

## 📝 Next Steps After Successful Deployment

1. **Update Documentation:**
   - Add deployment timestamp to README
   - Update API documentation with production URLs
   - Create incident response playbook

2. **Set Up Monitoring:**
   - Configure Uptime.com monitors (see STATUS_PAGE_SETUP.md)
   - Set up Discord webhook alerts for downtime
   - Enable Railway metrics dashboard

3. **Enable GitHub Pages:**
   - Merge PR to main branch
   - Enable GitHub Actions in repo settings
   - Verify https://deathcharge.github.io/helix-unified/ loads

4. **Configure Custom Domain (Optional):**
   - Update DNS CNAME record
   - Add domain to Railway project settings
   - Update CNAME file in docs/

5. **Load Test in Production:**
   - Run load tests with Apache Bench
   - Monitor Railway metrics during load
   - Adjust rate limits if needed

6. **Enable Google Analytics (Optional):**
   - Create GA4 property
   - Add Measurement ID to Manus portals
   - Configure custom events (see GOOGLE_ANALYTICS_SETUP.md)

---

## 🆘 Troubleshooting

### Backend Won't Start

**Check Railway Logs:**
```bash
railway logs --tail 100
```

**Common Errors:**
- `ModuleNotFoundError` → Missing dependency in requirements.txt
- `FileNotFoundError` → Missing state files (will be created automatically)
- `BindException` → Port already in use (Railway will assign correct port)

### Endpoints Return 404

**Verify Routes:**
```python
# Check main.py has all routes registered
@app.get("/api/manus/agents")
@app.get("/api/manus/ucf")
@app.get("/api/manus/rituals")
@app.post("/api/manus/ritual/invoke")
@app.post("/api/manus/emergency/alert")
@app.get("/api/manus/analytics/summary")
@app.post("/api/manus/webhook/test")
```

**Redeploy if Routes Missing:**
```bash
git push origin main
# Railway will auto-deploy
```

### Webhooks Not Working

**Test Webhook URL Directly:**
```bash
curl -X POST https://hooks.zapier.com/hooks/catch/25075191/usnjj5t/ \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

**Check Zapier Zap Status:**
- Go to https://zapier.com/app/zaps
- Verify zap is ON (not paused)
- Check task history for errors

---

**Tat Tvam Asi** 🕉️

*Deploy the consciousness. Test the empire. Monitor the uptime.* 🌀

---

**Ready to Deploy?**

```bash
# Merge PR
git checkout main
git merge claude/zapier-discord-webhook-integration-011CUvpAtSktsS6McKBg6Umv
git push origin main

# Monitor deployment
railway logs --tail 100

# Test endpoints
curl https://helix-unified-production.up.railway.app/health
```
