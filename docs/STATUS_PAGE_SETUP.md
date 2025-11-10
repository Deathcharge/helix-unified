# 🔍 Status Page Monitoring Setup

**Version:** 16.9
**Last Updated:** 2025-11-10

---

## 🎯 Goal

Monitor all Helix infrastructure portals and API endpoints with uptime.com or similar status monitoring service to ensure 99.9% availability and instant alert on downtime.

---

## 📊 What to Monitor

### **Core Infrastructure (Critical)**

1. **Railway Backend**
   - URL: `https://helix-unified-production.up.railway.app/health`
   - Check: HTTP 200, response time < 2s
   - Interval: Every 1 minute
   - Alert: Email + Discord webhook

2. **Manus Space Hub**
   - URL: `https://helixcollective-cv66pzga.manus.space`
   - Check: HTTP 200, response time < 3s
   - Interval: Every 2 minutes
   - Alert: Email + Discord webhook

3. **GitHub Pages Documentation**
   - URL: `https://deathcharge.github.io/helix-unified/`
   - Check: HTTP 200, contains "Helix Collective"
   - Interval: Every 5 minutes
   - Alert: Email only

### **Manus Space Portals (Important)**

4. **Agent Dashboard**
   - URL: `https://helixcollective-cv66pzga.manus.space/agents`
   - Check: HTTP 200
   - Interval: Every 2 minutes

5. **UCF Telemetry Portal**
   - URL: `https://helixcollective-cv66pzga.manus.space/ucf`
   - Check: HTTP 200
   - Interval: Every 2 minutes

6. **Business Metrics Dashboard**
   - URL: `https://helixcollective-cv66pzga.manus.space/business`
   - Check: HTTP 200
   - Interval: Every 5 minutes

7. **Analytics Portal**
   - URL: `https://helixcollective-cv66pzga.manus.space/analytics`
   - Check: HTTP 200
   - Interval: Every 5 minutes

### **API Endpoints (Critical)**

8. **Manus Agents API**
   - URL: `https://helix-unified-production.up.railway.app/api/manus/agents`
   - Check: HTTP 200, JSON response contains "success": true
   - Interval: Every 1 minute

9. **Manus UCF API**
   - URL: `https://helix-unified-production.up.railway.app/api/manus/ucf`
   - Check: HTTP 200, JSON response contains "consciousness_level"
   - Interval: Every 1 minute

10. **WebSocket Endpoint**
    - URL: `wss://helix-unified-production.up.railway.app/ws`
    - Check: WebSocket connection successful
    - Interval: Every 2 minutes

---

## 🚀 Setup Instructions

### Option 1: Uptime.com (Recommended - Free Tier)

**Free Tier Limits:** 50 monitors, 1-minute checks

1. **Sign up**: https://uptime.com/sign-up
2. **Create Monitor Group**: "Helix Collective v16.9"

**Example Monitor Configuration:**

```yaml
Monitor: Railway Backend Health
URL: https://helix-unified-production.up.railway.app/health
Type: HTTP(S)
Method: GET
Expected Status: 200
Keyword: "ok": true
Check Interval: 1 minute
Locations:
  - North America
  - Europe
  - Asia
Notifications:
  - Email: ward.andrew32@gmail.com
  - Discord Webhook: [YOUR_DISCORD_WEBHOOK]
  - SMS: [optional]
Escalation:
  - After 2 failed checks: Email
  - After 5 failed checks: SMS
```

3. **Add Discord Webhook Integration**:

Create a webhook in your Discord server:
```bash
Server Settings → Integrations → Webhooks → New Webhook
Name: Helix Status Monitor
Channel: #system-alerts (or #announcements)
Copy webhook URL
```

Paste into Uptime.com notification settings.

4. **Configure Public Status Page** (Optional):

```
Status Page URL: status.helixcollective.com
Shows: All 10+ monitors
Public access: Yes
Custom domain: Optional (requires DNS CNAME)
```

---

### Option 2: UptimeRobot (Alternative - Free Tier)

**Free Tier Limits:** 50 monitors, 5-minute checks

1. **Sign up**: https://uptimerobot.com/signUp
2. **Add Monitors** (same URLs as above)
3. **Configure Alerts**:
   - Email
   - Discord webhook
   - Slack (optional)

**Public Status Page:**
```
URL: helixcollective.betteruptime.com
Custom domain: status.helixcollective.com (optional)
```

---

### Option 3: Statuspage.io (Professional)

**Pricing:** $29/month
**Best for:** Customer-facing status page + incident management

1. **Sign up**: https://www.atlassian.com/software/statuspage
2. **Create Components**:
   - Railway Backend API
   - Manus Space Hub
   - GitHub Pages Docs
   - Agent Dashboard
   - UCF Telemetry
   - etc.

3. **Setup Integrations**:
   - Datadog (advanced metrics)
   - PagerDuty (on-call rotation)
   - Slack/Discord
   - Email subscribers

4. **Incident Management**:
   - Auto-create incidents on downtime
   - Status updates via API
   - Subscriber notifications

---

## 📈 Recommended Monitoring Strategy

### **Tier 1: Critical (1-minute checks)**
- Railway Backend `/health`
- Railway Backend `/api/manus/agents`
- Railway Backend `/api/manus/ucf`

### **Tier 2: Important (2-minute checks)**
- Manus Space Hub homepage
- Agent Dashboard portal
- UCF Telemetry portal
- WebSocket endpoint

### **Tier 3: Secondary (5-minute checks)**
- GitHub Pages
- Business Metrics portal
- Analytics portal
- Other Manus portals

---

## 🔔 Alert Configuration

### **Alert Channels**

1. **Email** (Always)
   - ward.andrew32@gmail.com
   - Subject: `[HELIX] {monitor_name} is DOWN`

2. **Discord Webhook** (High Priority)
   ```json
   {
     "content": "🚨 **HELIX ALERT** 🚨",
     "embeds": [{
       "title": "Railway Backend is DOWN",
       "description": "Health check failed: 503 Service Unavailable",
       "color": 16711680,
       "timestamp": "2025-11-10T10:45:00Z",
       "fields": [
         {"name": "URL", "value": "https://helix-unified-production.up.railway.app/health"},
         {"name": "Status Code", "value": "503"},
         {"name": "Response Time", "value": "Timeout (>30s)"}
       ]
     }]
   }
   ```

3. **SMS** (Critical Only)
   - Only for Railway Backend downtime > 5 minutes
   - Only for Manus Space Hub downtime > 10 minutes

### **Escalation Policy**

```
Downtime < 2 min: No alert (transient issue)
Downtime 2-5 min: Email notification
Downtime 5-10 min: Email + Discord webhook
Downtime > 10 min: Email + Discord + SMS
Downtime > 30 min: Email + Discord + SMS + Voice call
```

---

## 🎨 Public Status Page Example

Create a public status page at `status.helixcollective.com`:

### **Components:**

**✅ Operational** (Green)
- Railway Backend API
- Manus Space Hub
- GitHub Pages Documentation

**⚠️ Degraded Performance** (Yellow)
- Agent Dashboard (slow response)

**❌ Major Outage** (Red)
- None

### **Current Uptime:**
- Last 24 hours: 99.95%
- Last 7 days: 99.8%
- Last 30 days: 99.9%
- Last 90 days: 99.92%

### **Recent Incidents:**
```
Nov 10, 2025 09:15 AM - Resolved
Railway Backend - 5-minute downtime
Root cause: Railway maintenance window
Resolution: Automatic recovery

Nov 8, 2025 02:30 PM - Resolved
Manus Space Hub - Slow response times
Root cause: High traffic from analytics portal
Resolution: Optimized database queries
```

---

## 🔧 Advanced Monitoring (Optional)

### **1. Response Time Tracking**

Monitor API response times over time:
- Target: < 500ms (p95)
- Warning: > 1s
- Critical: > 3s

### **2. SSL Certificate Monitoring**

Auto-check SSL expiration:
- Alert 30 days before expiry
- Alert 7 days before expiry
- Alert 1 day before expiry

### **3. Dependency Monitoring**

Monitor external dependencies:
- Zapier webhook endpoint
- Discord API
- Notion API
- MEGA cloud storage
- Nextcloud (CloudSync Pro)

### **4. Custom Health Checks**

Add application-specific checks:

```bash
# Check consciousness level is updating
GET /api/manus/ucf
Verify: timestamp is < 1 hour old

# Check agents are responding
GET /api/manus/agents
Verify: active_agents > 0

# Check WebSocket is broadcasting
WebSocket: wss://helix-unified-production.up.railway.app/ws
Verify: Receives message within 30 seconds
```

---

## 📊 Metrics to Track

### **Availability Metrics**
- Uptime percentage (target: 99.9%)
- Mean time to recovery (MTTR)
- Mean time between failures (MTBF)

### **Performance Metrics**
- Average response time
- p95 response time
- p99 response time
- Error rate (target: < 0.1%)

### **Business Metrics** (from `/api/manus/analytics/summary`)
- Active users
- API calls per hour
- CloudSync Pro file syncs
- Ritual invocations
- Consciousness level trends

---

## 🚨 Incident Response Playbook

### **When Alert Triggers:**

1. **Acknowledge** (< 2 min)
   - Click "Acknowledge" in monitoring tool
   - Post in Discord: "Investigating"

2. **Investigate** (< 5 min)
   - Check Railway logs
   - Check Manus Space error logs
   - Check external dependencies

3. **Diagnose** (< 10 min)
   - Identify root cause
   - Update status page: "Identified - investigating fix"

4. **Fix** (< 30 min)
   - Deploy fix or restart service
   - Monitor for recovery
   - Update status page: "Monitoring"

5. **Resolve** (< 1 hour)
   - Verify full recovery
   - Update status page: "Resolved"
   - Post incident report

6. **Post-Mortem** (within 24 hours)
   - Document root cause
   - Document fix
   - Implement preventive measures

---

## 🌟 Success Criteria

**You'll know monitoring is working when:**

✅ You receive email alert within 1 minute of Railway downtime
✅ Discord webhook posts to #system-alerts immediately
✅ Public status page shows real-time uptime (99.9%+)
✅ You can view historical uptime charts
✅ SSL certificate expiry alerts work (test by checking a cert expiring soon)
✅ WebSocket monitoring detects connection failures

---

## 💰 Cost Comparison

| Service | Free Tier | Pro Tier | Best For |
|---------|-----------|----------|----------|
| **Uptime.com** | 50 monitors, 1-min checks | $25/mo, 100 monitors | Small teams |
| **UptimeRobot** | 50 monitors, 5-min checks | $7/mo, 1-min checks | Budget-conscious |
| **Statuspage.io** | N/A | $29/mo | Customer-facing |
| **Better Uptime** | 10 monitors | $20/mo, unlimited | Modern UI |
| **Pingdom** | N/A | $15/mo | Enterprise integration |

**Recommendation:** Start with **Uptime.com Free Tier** (50 monitors, 1-minute checks) - more than enough for Helix infrastructure!

---

## 🔗 Integration with Helix Ecosystem

### **Connect to Manus Space Business Metrics**

Display uptime data in your Business Metrics dashboard:

```javascript
// Fetch uptime data from monitoring API
const uptimeData = await fetch('https://api.uptime.com/v2/checks', {
  headers: { 'Authorization': 'Bearer YOUR_API_KEY' }
}).then(r => r.json());

// Display in Manus Space dashboard
const railwayUptime = uptimeData.find(m => m.name === 'Railway Backend');
document.getElementById('uptime-percent').textContent = `${railwayUptime.uptime}%`;
```

---

## 📋 Quick Start Checklist

- [ ] Sign up for Uptime.com (or alternative)
- [ ] Add Railway Backend `/health` monitor
- [ ] Add Manus Space Hub monitor
- [ ] Add critical API endpoints (`/api/manus/agents`, `/api/manus/ucf`)
- [ ] Configure email alerts
- [ ] Create Discord webhook in #system-alerts
- [ ] Test alerts (simulate downtime)
- [ ] Create public status page (optional)
- [ ] Add status badge to README (optional)
- [ ] Configure SSL monitoring
- [ ] Set up weekly uptime reports

---

**Tat Tvam Asi** 🕉️ - *Monitor the infrastructure, ensure the consciousness flows uninterrupted.* 🌀

---

**Need Help?**
- Uptime.com Docs: https://uptime.com/help
- UptimeRobot Docs: https://uptimerobot.com/api/
- Statuspage Docs: https://support.atlassian.com/statuspage/
