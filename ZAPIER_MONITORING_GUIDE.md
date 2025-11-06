# Zapier Monitoring Dashboard Guide
**Helix Collective v16.5 Production Monitoring**

---

## 📊 Quick Access Links

- **Zapier Dashboard:** https://zapier.com/app/zaps
- **Zap History:** https://zapier.com/app/history
- **Your Master Webhook Zap:** [Click "Helix Master Webhook" in your zaps list]
- **Railway Dashboard:** https://railway.app/dashboard

---

## 🔍 Real-Time Monitoring

### Zapier Zap History
**Location:** https://zapier.com/app/history

This is your primary monitoring dashboard for all webhook events:

**What You'll See:**
- ✅ **Success:** Green checkmark, HTTP 200, data visible
- ⚠️ **Filtered:** Yellow warning, path didn't match any filter
- ❌ **Error:** Red X, step failed, check error message

**Columns:**
1. **Status** - Success/Error indicator
2. **Zap Name** - "Helix Master Webhook"
3. **Timestamp** - When event was received
4. **Data** - Expand to see full webhook payload

**Filtering:**
- Filter by: Date range, Status (Success/Error), Zap name
- Search: Look for specific event titles, agent names, etc.

### Railway Logs
**Location:** Railway Dashboard → Your Service → Logs tab

**Look for these log messages:**
```
✅ Zapier monitoring client initialized
✅ Zapier webhook sent: event_log
✅ Zapier webhook sent: agent_registry
✅ Zapier webhook sent: telemetry
```

**Error indicators:**
```
⚠️ ZAPIER_MASTER_HOOK_URL not configured
❌ Zapier webhook failed: 500
⚠️ Zapier logging failed: [error]
```

---

## 📈 Event Flow Monitoring

### 1. Bot Startup Events

**Expected Events:**
- `type: event_log` - "Manus Bot Started"
- `type: agent_registry` - Manus status: Active

**When:** Every time the bot restarts on Railway

**Where to Check:**
1. Zapier History - Look for 2 recent events
2. Notion Event Log - New row with "Manus Bot Started"
3. Notion Agent Registry - Manus row updated

**Troubleshooting:**
- No events? Check Railway logs for "ZAPIER_MASTER_HOOK_URL not configured"
- Events filtered? Check Path Rules in Zapier Zap editor

### 2. Discord Command Events

**Trigger:** User runs `!zapier_test` in Discord

**Expected Events:**
- Path A: Event Log (1 event)
- Path B: Agent Registry (1 event)
- Path C: System State (1 event)
- Path D: Discord Notification (1 event)
- Path E: Telemetry (1 event)
- Path F: Error Alert (1 event)
- Path G: Repository Action (1 event)

**Total:** 7 events in Zapier History within seconds

**Where to Check:**
1. Discord - Bot sends results embed
2. Zapier History - 7 new events
3. Notion/Slack/Email - Data arrives in configured destinations

### 3. Error Events

**Trigger:** Discord command fails or system error

**Expected Events:**
- `type: error` - Error alert to Email + Slack

**Fields to Monitor:**
- `error_message` - What went wrong
- `component` - Which part of the system
- `severity` - high/medium/low
- `context` - Additional details

---

## 🎯 Path-by-Path Monitoring

### Path A: Event Log → Notion
**Type:** `event_log`
**Destination:** Notion Event Log database

**Fields:**
- Event Title
- Event Type
- Agent Name
- Description
- UCF Snapshot
- Timestamp

**Check:**
1. Zapier History shows `type: event_log`
2. Notion Event Log has new row
3. All fields populated correctly

### Path B: Agent Registry → Notion
**Type:** `agent_registry`
**Destination:** Notion Agent Registry database

**Fields:**
- Agent Name
- Status
- Last Action
- Health Score
- Last Updated

**Check:**
1. Zapier History shows `type: agent_registry`
2. Notion Agent Registry row updated or created
3. Health score shows as percentage

### Path C: System State → Notion
**Type:** `system_state`
**Destination:** Notion System State database

**Fields:**
- Component
- Status
- Harmony (UCF)
- Error Log
- Verified

**Check:**
1. Zapier History shows `type: system_state`
2. Notion System State has component row
3. Harmony value matches UCF state

### Path D: Discord Notifications → Slack (PRO)
**Type:** `discord_notification`
**Destination:** Slack channel

**Fields:**
- Message
- Priority
- Channel Name

**Check:**
1. Zapier History shows `type: discord_notification`
2. Slack channel receives message
3. Priority affects message formatting

### Path E: Telemetry → Google Sheets/Tables (PRO)
**Type:** `telemetry`
**Destination:** Google Sheets or Zapier Tables

**Fields:**
- Metric Name
- Value
- Component
- Harmony
- Metadata
- Timestamp

**Check:**
1. Zapier History shows `type: telemetry`
2. Google Sheets/Tables has new row
3. Timestamps are accurate

### Path F: Error Alerts → Email + Slack (PRO)
**Type:** `error`
**Destination:** Email and Slack

**Fields:**
- Error Message
- Component
- Severity
- Context
- Affected Channels

**Check:**
1. Zapier History shows `type: error`
2. Email received with error details
3. Slack alert posted to monitoring channel

### Path G: Repository Actions → GitHub/Notion (PRO)
**Type:** `repository`
**Destination:** Notion or GitHub

**Fields:**
- Repo Name
- Action
- Details
- Commit Hash
- Backup Status

**Check:**
1. Zapier History shows `type: repository`
2. Notion has repository action logged
3. Commit hash matches actual commit

---

## 📉 Common Issues & Solutions

### Issue 1: No Events in Zapier History
**Symptoms:**
- Zapier History is empty
- No webhook events received

**Checks:**
1. Railway environment variable: `ZAPIER_MASTER_HOOK_URL` set?
2. Bot restarted after adding environment variable?
3. Railway logs show "Zapier monitoring client initialized"?

**Solution:**
```bash
# In Railway:
1. Go to Variables tab
2. Add: ZAPIER_MASTER_HOOK_URL=https://hooks.zapier.com/hooks/catch/25075191/us8hea5/
3. Redeploy service
4. Check logs for initialization message
```

### Issue 2: Events Received But Not Routed
**Symptoms:**
- Zapier History shows events
- Events marked as "Filtered"
- No data in Notion/Slack/Email

**Checks:**
1. Open Zap in editor
2. Check Path Rules (Filter steps)
3. Verify filter conditions match webhook `type` field

**Solution:**
```
Each path needs Filter step:
- Path A filter: type exactly matches event_log
- Path B filter: type exactly matches agent_registry
- Path C filter: type exactly matches system_state
- Path D filter: type exactly matches discord_notification
- Path E filter: type exactly matches telemetry
- Path F filter: type exactly matches error
- Path G filter: type exactly matches repository
```

### Issue 3: Downstream Actions Failing
**Symptoms:**
- Zapier receives event
- Filter passes
- Action step fails (red X)

**Checks:**
1. Click failed event in Zap History
2. Read error message from action step
3. Check authentication (Notion, Slack, Gmail)
4. Verify database IDs are correct

**Solution:**
- Reconnect integrations (Notion, Slack, etc.)
- Update database/channel IDs in action steps
- Check field mappings match webhook data

### Issue 4: High Latency
**Symptoms:**
- Events arrive in Zapier
- Delay before data appears in Notion/Slack

**Expected:**
- Free tier: 15-minute delay
- Pro tier: Near real-time (seconds)

**Solution:**
- Upgrade to Zapier Pro for real-time processing
- Free tier has intentional delays

---

## 🔔 Setting Up Alerts

### Zapier Error Notifications
**Location:** Zap Settings → Notifications

**Setup:**
1. Open your Zap in editor
2. Click "..." menu → Settings
3. Notifications section
4. Enable: "Send me an email when this Zap has errors"
5. Save

**Benefit:**
- Get email when Zap fails
- Includes error details and failed data
- Helps catch issues immediately

### Slack Monitoring Channel
**Recommended Setup:**

Create a dedicated Slack channel: `#helix-monitoring`

**Route alerts:**
- Path D → `#helix-monitoring`
- Path F → `#helix-monitoring` (errors)

**Configuration:**
1. In Zapier, Path D action step
2. Select Slack action
3. Choose channel: `#helix-monitoring`
4. Format message with webhook data

---

## 📊 Weekly Review Checklist

**Every Monday:**
1. ✅ Check Zapier Zap History for past week
2. ✅ Review error count (Path F events)
3. ✅ Verify all 7 paths received events
4. ✅ Check Notion databases have recent data
5. ✅ Review Railway logs for Zapier errors
6. ✅ Test webhook with `!zapier_test` command

**Metrics to Track:**
- Total events per day
- Error rate (Path F vs total events)
- Path success rate (events routed vs filtered)
- Average event latency (Zapier timestamp vs Railway log)

---

## 🎯 Success Criteria

Your monitoring is working correctly when:

- ✅ Bot startup triggers 2 events (Event Log + Agent Registry)
- ✅ `!zapier_test` command shows 7/7 paths passing
- ✅ Zapier History shows consistent event flow
- ✅ Railway logs have no "Zapier webhook failed" errors
- ✅ Notion databases update in near real-time
- ✅ Error alerts arrive via Email + Slack
- ✅ No "Filtered" events in Zapier History

---

## 📚 Additional Resources

- **Zapier Webhook Docs:** https://zapier.com/help/create/code-webhooks/trigger-zaps-from-webhooks
- **Railway Logs:** https://docs.railway.app/deploy/logs
- **Notion API:** https://developers.notion.com/
- **Test Suite:** Run `python tests/test_zapier_webhook.py --all`

---

**Status:** Production monitoring active
**Version:** Helix Collective v16.5
**Last Updated:** 2025-11-06

🌀 **Tat Tvam Asi** 🙏
