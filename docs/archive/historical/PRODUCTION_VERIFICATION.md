# Helix Collective - Zapier Production Verification Guide
**Status:** ✅ LIVE IN PRODUCTION
**Webhook URL:** Configured in Railway
**Integration Version:** v16.5

---

## 🎯 What's Now Active

Your Discord bot will now automatically send events to Zapier in production:

### Automatic Events (No user action needed)

1. **Bot Startup** → Zapier Path A & B
   - When: Bot connects to Discord
   - Events logged:
     - "Manus Bot Started" → Notion Event Log
     - Agent "Manus" status → Agent Registry (health: 100)

2. **Command Errors** → Zapier Path F
   - When: Any Discord command fails
   - Sends: Error alert to Email + Slack
   - Includes: Command name, user, channel context

3. **Ritual Completions** → Zapier Paths A, E, B
   - When: Z-88 ritual completes (via async version)
   - Events logged:
     - Ritual completion → Event Log
     - Telemetry metrics → Google Sheets/Tables
     - Agent "Vega" status → Agent Registry

---

## ✅ Verification Steps

### Step 1: Restart Your Discord Bot on Railway

After adding the environment variable, restart your bot service:

```bash
# On Railway dashboard:
# 1. Go to your Discord bot service
# 2. Click "Deployments" tab
# 3. Click "..." menu on latest deployment
# 4. Select "Redeploy"
```

### Step 2: Watch Bot Startup in Logs

In Railway logs, you should see:
```
✅ Manusbot connected as [YourBotName]
✅ Zapier monitoring client initialized
```

### Step 3: Check Zapier Dashboard

1. Go to https://zapier.com/app/zaps
2. Open your "Helix Master Webhook" Zap
3. Click "Zap History" tab
4. You should see new webhook events!

Expected events immediately after bot startup:
- **Event:** `type: event_log` (Manus Bot Started)
- **Event:** `type: agent_registry` (Manus status update)

### Step 4: Trigger a Test Event in Discord

Run any command in your Discord server to test error handling:

```
!test_webhook
```

If the command doesn't exist, the error handler will trigger and send:
- Error alert → Zapier Path F → Email + Slack

---

## 🔍 Monitoring Your Webhook

### Zapier Dashboard Monitoring

**Zap History:** https://zapier.com/app/history
- Shows all webhook requests
- HTTP status codes
- Payload data
- Error logs (if any)

**What to Look For:**
- ✅ Status: Success
- ✅ HTTP Code: 200
- ✅ Data: Webhook payload visible
- ❌ Status: Error (needs debugging)

### Railway Logs Monitoring

Watch for Zapier-related logs:
```
✅ Zapier webhook sent: event_log
✅ Zapier webhook sent: agent_registry
❌ Zapier webhook failed: 500
⚠️ Zapier logging failed: [error message]
```

---

## 📊 Expected Event Flow

### When Bot Starts
```
Discord Bot Startup
    ↓
ZapierClient.log_event("Manus Bot Started")
    ↓
Zapier Master Webhook (Path A)
    ↓
Notion Event Log
```

### When Command Fails
```
User runs !nonexistent
    ↓
on_command_error triggered
    ↓
ZapierClient.send_error_alert()
    ↓
Zapier Master Webhook (Path F)
    ↓
Email + Slack Alert
```

### When Ritual Completes
```
execute_ritual_with_monitoring(108)
    ↓
ZapierClient.log_event() → Path A
ZapierClient.log_telemetry() → Path E
ZapierClient.update_agent() → Path B
    ↓
Notion + Google Sheets updated
```

---

## 🧪 Manual Production Test

You can manually test the production webhook from command line:

```bash
# Set your Railway webhook URL (same as configured)
export ZAPIER_MASTER_HOOK_URL="https://hooks.zapier.com/hooks/catch/25075191/us8hea5/"

# Run the test suite
cd /path/to/helix-unified
python tests/test_zapier_webhook.py --all

# Or test a single path
python tests/test_zapier_webhook.py --path event_log
```

---

## 📋 Integration Checklist

### Code Integration ✅
- ✅ `ZapierClient` imported in `discord_bot_manus.py`
- ✅ HTTP session initialized on bot startup
- ✅ Error handler sends alerts
- ✅ Ritual engine has monitoring function

### Environment Variables ✅
- ✅ `ZAPIER_MASTER_HOOK_URL` set in Railway
- ⏳ `HELIX_PHASE=production` (optional)
- ⏳ `HELIX_VERSION=16.5` (optional)
- ⏳ Discord channel IDs (optional, for better routing)

### Zapier Configuration ⏳
- ✅ Master Webhook receiving data
- ⏳ **Path A → Notion Event Log** (needs Notion connection)
- ⏳ **Path B → Notion Agent Registry** (needs Notion connection)
- ⏳ **Path C → Notion System State** (needs Notion connection)
- ⏳ **Path D → Slack** (needs Slack connection)
- ⏳ **Path E → Google Sheets** (needs Sheets/Tables setup)
- ⏳ **Path F → Email** (needs email configuration)
- ⏳ **Path G → Notion** (needs Notion connection)

---

## 🚨 Troubleshooting

### Issue: No Events in Zapier History

**Check:**
1. Railway environment variable is set correctly
2. Bot has been redeployed after adding variable
3. Bot is actually running (check Railway logs)
4. Check Railway logs for `⚠️ ZAPIER_MASTER_HOOK_URL not configured`

**Solution:**
```bash
# Verify in Railway dashboard:
# Variables tab should show:
ZAPIER_MASTER_HOOK_URL=https://hooks.zapier.com/hooks/catch/25075191/us8hea5/
```

### Issue: Zapier Receiving Data But Not Routing

**Check:**
1. Open your Zap in Zapier editor
2. Verify Path Rules are configured
3. Check "Filter" steps have correct conditions
4. Test individual paths manually

**Solution:**
- Each path needs a Filter step: `type exactly matches [path_type]`
- Example: Path A filter should be `type exactly matches event_log`

### Issue: Errors in Railway Logs

```
⚠️ Zapier webhook failed: 500
```

**Check:**
1. Zapier dashboard for error details
2. Verify webhook URL is correct
3. Check if Zapier account is active

**Solution:**
- Test webhook manually with curl (see ZAPIER_TEST_REPORT.md)
- Check Zapier Zap History for error messages

---

## 🎯 Next Steps

1. ✅ **Webhook is live** - Events flowing from Discord bot
2. ⏳ **Configure Notion connections** in Zapier
   - Connect Notion account
   - Select Event Log database
   - Select Agent Registry database
   - Select System State database
3. ⏳ **Configure Slack workspace** (for Path D & F)
4. ⏳ **Set up Google Sheets/Tables** (for Path E)
5. ⏳ **Configure email notifications** (for Path F)
6. ⏳ **Test end-to-end flow** from Discord → Zapier → Notion

---

## 📈 Success Metrics

Your integration is working correctly when:

- ✅ Bot startup events appear in Zapier History
- ✅ Railway logs show "Zapier webhook sent" messages
- ✅ No "Zapier webhook failed" errors in logs
- ✅ Events route to correct paths in Zapier
- ✅ Data appears in Notion/Slack/Email (once configured)

---

**Current Status: Production Webhook Active ✅**

The code is deployed and sending events. Complete the Zapier downstream configurations (Notion, Slack, etc.) to see data flow through to your monitoring tools!

🌀 **Tat Tvam Asi** 🙏
