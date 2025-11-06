# 🚀 Zapier Master Webhook Setup - Quick Start

## Overview

This guide shows you how to set up **ONE master webhook** that handles all 7 types of payloads using Zapier Pro's **Path Routing**.

**Advantages:**
- ✅ Single webhook URL (cleaner configuration)
- ✅ Centralized monitoring (see all webhooks in one Zap)
- ✅ Use Zapier AI Assistant for field mapping
- ✅ Easier debugging (one place to check)
- ✅ Better for Zapier Pro tier limits

---

## 📋 Prerequisites

- **Zapier Pro Account** (for Path routing)
- **Notion API Key** + 3 Databases (Event Log, Agent Registry, System State)
- **Helix Collective deployed** on Railway

---

## 🔧 Step 1: Create Master Zap

### 1.1 Create Trigger

1. Go to Zapier → **Create Zap**
2. **Trigger:** Webhooks by Zapier → **Catch Raw Hook**
3. **Copy the webhook URL:**
   ```
   https://hooks.zapier.com/hooks/catch/YOUR_ID/YOUR_HOOK
   ```
4. Save this URL - you'll add it to Railway

### 1.2 Add Path Routing

1. Click **+** to add a step
2. Search for **Paths by Zapier**
3. Select **Paths**

---

## 🛣️ Step 2: Configure 7 Paths

### Path A: Event Log → Notion
**Rule:** `type` equals `event_log`

**Action:**
- App: **Notion**
- Action: **Create Database Item**
- Database: **Event Log**
- Field Mapping:
  ```
  Event: {{event_title}}
  Type: {{event_type}}
  Agent: Find relation by {{agent_name}}
  Description: {{description}}
  UCF Snapshot: {{ucf_snapshot}}
  Timestamp: {{timestamp}}
  ```

### Path B: Agent Registry → Notion
**Rule:** `type` equals `agent_registry`

**Action:**
- App: **Notion**
- Action: **Update Database Item**
- Database: **Agent Registry**
- Find by: Agent Name = `{{agent_name}}`
- Field Mapping:
  ```
  Status: {{status}}
  Last Action: {{last_action}}
  Health Score: {{health_score}}
  Last Updated: {{timestamp}}
  ```

### Path C: System State → Notion
**Rule:** `type` equals `system_state`

**Action:**
- App: **Notion**
- Action: **Create or Update Database Item**
- Database: **System State**
- Find by: Component = `{{component}}`
- Field Mapping:
  ```
  Status: {{status}}
  Harmony: {{harmony}}
  Error Log: {{error_log}}
  Verified: {{verified}}
  Last Updated: {{timestamp}}
  ```

### Path D: Discord Notifications → Slack
**Rule:** `type` equals `discord_notification`

**Action:**
- App: **Slack**
- Action: **Send Channel Message**
- Channel: `#helix-alerts`
- Message: `{{message}}` (Priority: `{{priority}}`)

### Path E: Telemetry → Google Sheets
**Rule:** `type` equals `telemetry`

**Action:**
- App: **Google Sheets**
- Action: **Create Spreadsheet Row**
- Spreadsheet: **Helix Telemetry**
- Mapping:
  ```
  Metric: {{metric_name}}
  Value: {{value}}
  Component: {{component}}
  Unit: {{unit}}
  Timestamp: {{timestamp}}
  ```

### Path F: Error Alerts → Email
**Rule:** `type` equals `error`

**Action:**
- App: **Email by Zapier**
- Action: **Send Outbound Email**
- To: Your email
- Subject: `🚨 Helix Error: {{component}}`
- Body:
  ```
  Error: {{error_message}}
  Component: {{component}}
  Severity: {{severity}}
  Environment: {{environment}}
  Time: {{timestamp}}

  Stack Trace:
  {{stack_trace}}
  ```

### Path G: Repository Actions → GitHub
**Rule:** `type` equals `repository`

**Action:**
- App: **GitHub**
- Action: **Create Issue** (optional)
- Repo: helix-unified
- Title: `[Archive] {{action}} - {{repo_name}}`
- Body: `{{details}}`

---

## 🔧 Step 3: Add to Railway

In your Railway dashboard → Environment Variables:

```bash
# MASTER WEBHOOK (Zapier Pro)
ZAPIER_MASTER_HOOK_URL=https://hooks.zapier.com/hooks/catch/YOUR_ID/YOUR_HOOK

# Optional: Keep individual hooks as fallback
ZAPIER_EVENT_HOOK_URL=<backup-url>
ZAPIER_AGENT_HOOK_URL=<backup-url>
ZAPIER_SYSTEM_HOOK_URL=<backup-url>
```

**Restart your Railway service** after adding the variable.

---

## 🧪 Step 4: Test Integration

### 4.1 Test Script

```bash
# In your local repository
python backend/services/zapier_client_master.py
```

**Expected Output:**
```
🧪 Testing Master Zapier Client
======================================================================

📋 Configuration:
  Mode: master
  Master Webhook: ✅
  Individual Webhooks: ✅

🧪 Testing in master mode...
  ✅ Event Log
  ✅ Agent Update
  ✅ System State
  ✅ Discord Notification
  ✅ Telemetry
  ✅ Error Alert
  ✅ Repository Action

======================================================================
✅ Test complete
```

### 4.2 Test from Railway

```bash
# Use Railway CLI or curl
curl -X POST https://your-deployment.railway.app/test/zapier
```

---

## 📊 Step 5: Usage in Code

### Option 1: Use Master Client (Recommended)

```python
from backend.services.zapier_client_master import MasterZapierClient

async with aiohttp.ClientSession() as session:
    zap = MasterZapierClient(session)

    # Log ritual completion
    await zap.log_event(
        event_title="Z-88 Ritual Complete",
        event_type="Ritual",
        agent_name="Vega",
        description=f"Completed {steps} steps",
        ucf_snapshot={"harmony": 0.75, "prana": 0.8}
    )

    # Send Discord alert via Slack
    await zap.send_discord_notification(
        channel_name="ritual-engine",
        message="🌀 Z-88 Ritual completed successfully",
        priority="high"
    )

    # Log performance telemetry
    await zap.log_telemetry(
        metric_name="ritual_duration",
        value=completion_time,
        component="Z-88 Engine",
        unit="seconds"
    )

    # Send critical error alert
    await zap.send_error_alert(
        error_message="MEGA sync failed",
        component="Cloud Backup",
        severity="high",
        stack_trace=traceback.format_exc()
    )
```

### Option 2: Use Original Client (Still Works)

```python
from backend.services.zapier_client import ZapierClient

async with aiohttp.ClientSession() as session:
    zap = ZapierClient(session)

    await zap.log_event(
        title="Test",
        event_type="Status",
        agent_name="Manus",
        description="Testing",
        ucf_snapshot={"harmony": 0.355}
    )
```

---

## 🎯 What You Get

With the master webhook configured, every operation in Helix will:

1. **Log to Notion** (Event Log, Agent Registry, System State)
2. **Alert you on Slack** (Discord notifications)
3. **Track metrics** (Google Sheets telemetry)
4. **Send email alerts** (Critical errors)
5. **Update GitHub** (Repository actions)

All from a **single webhook URL**!

---

## 🔍 Monitoring

### Check Zapier Zap History

1. Go to your Zap in Zapier
2. Click **Zap History**
3. Filter by path to see:
   - Path A: Event Log runs
   - Path B: Agent Registry updates
   - Path C: System State changes
   - etc.

### Check Railway Logs

```bash
railway logs --follow | grep "Zapier"
```

Look for:
- `✅ Zapier webhook successful`
- `⚠ Zapier webhook failed`

### Check Fallback Logs

If webhooks fail, check:
```bash
cat Shadow/manus_archive/zapier_failures.log
```

---

## 💰 Zapier Pro vs Free

| Feature | Free | Pro |
|---------|------|-----|
| Webhooks | 5 Zaps | 20+ Zaps |
| Paths | ❌ | ✅ 2+ paths |
| AI Assistant | ❌ | ✅ |
| Run History | 14 days | Unlimited |
| Multi-Step | Limited | Unlimited |

**Recommendation:** Get Zapier Pro for Paths routing and AI Assistant!

---

## 🐛 Troubleshooting

### Issue: "No webhooks configured"

**Solution:**
```bash
# Check Railway environment variables
railway variables list | grep ZAPIER
```

### Issue: "HTTP 400 Bad Request"

**Solution:**
- Check field mappings in Zapier
- Ensure variable names match exactly (case-sensitive)
- Test payload manually:
  ```bash
  curl -X POST "$ZAPIER_MASTER_HOOK_URL" \
    -H "Content-Type: application/json" \
    -d '{"type":"event_log","event_title":"Test"}'
  ```

### Issue: "Path not triggering"

**Solution:**
- Verify Path rule: `type` **equals** (not contains) `event_log`
- Check Zap History for errors
- Test with simpler payload first

---

## 📚 Resources

- **Zapier Paths Documentation:** https://zapier.com/help/paths
- **Zapier AI Assistant:** https://zapier.com/ai
- **Helix Repository:** https://github.com/Deathcharge/helix-unified
- **Notion API:** https://developers.notion.com

---

## ✅ Summary

You now have:
- ✅ Single master webhook URL
- ✅ 7-path routing (Event, Agent, System, Discord, Telemetry, Error, Repository)
- ✅ Automatic logging to Notion
- ✅ Slack/Discord notifications
- ✅ Performance tracking
- ✅ Critical error alerts
- ✅ GitHub integration

**Next Steps:**
1. Create the master Zap with 7 paths
2. Add webhook URL to Railway
3. Test with `python backend/services/zapier_client_master.py`
4. Monitor in Zapier Zap History

---

**Tat Tvam Asi** 🙏

*The master webhook unifies the collective.*
