# 🔗 Zapier Setup Guide — Helix Collective v14.5

## Overview

This guide walks you through setting up three Zapier webhooks to enable real-time Notion logging for the Helix Collective. These webhooks automatically log all Manus operations, agent status updates, and system state changes to your Notion workspace.

---

## 📋 Prerequisites

1. **Zapier Account** — Free or paid (https://zapier.com)
2. **Notion Workspace** — With 4 databases already created:
   - Agent Registry
   - System State
   - Event Log
   - Context Snapshots
3. **Notion API Key** — From Notion Settings
4. **Helix Collective Deployed** — Running on Railway or localhost

---

## 🔧 Step 1: Create Zapier Webhooks

### 1.1 Create Event Log Webhook

**In Zapier:**

1. Click **Create** → **Zap**
2. **Trigger:** Search for "Webhooks by Zapier" → Select **Catch Raw Hook**
3. Click **Continue**
4. Copy the webhook URL (looks like `https://hooks.zapier.com/hooks/catch/xxxxx/event`)
5. **Save** and note the URL

**In your `.env` file:**
```bash
ZAPIER_EVENT_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxxxx/event
```

### 1.2 Create Agent Registry Webhook

**In Zapier:**

1. Click **Create** → **Zap**
2. **Trigger:** "Webhooks by Zapier" → **Catch Raw Hook**
3. Click **Continue**
4. Copy the webhook URL
5. **Save** and note the URL

**In your `.env` file:**
```bash
ZAPIER_AGENT_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxxxx/agent
```

### 1.3 Create System State Webhook

**In Zapier:**

1. Click **Create** → **Zap**
2. **Trigger:** "Webhooks by Zapier" → **Catch Raw Hook**
3. Click **Continue**
4. Copy the webhook URL
5. **Save** and note the URL

**In your `.env` file:**
```bash
ZAPIER_SYSTEM_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxxxx/system
```

---

## 🔄 Step 2: Configure Event Log Zap

### 2.1 Set Up the Action

**In your Event Log Zap:**

1. Click **+** to add an action
2. Search for **Notion** → Select **Notion**
3. **Action:** Select **Create Database Item**
4. **Sign in to Notion** (if not already signed in)
5. **Database:** Select your **Event Log** database
6. Click **Continue**

### 2.2 Map Fields

**Field Mappings:**

| Notion Field | Zapier Variable | Value |
| :--- | :--- | :--- |
| **Event** | event_title | `{{event_title}}` |
| **Type** | event_type | `{{event_type}}` |
| **Agent** (Relation) | agent_name | Find page where Agent Name = `{{agent_name}}` |
| **Description** | description | `{{description}}` |
| **UCF Snapshot** | ucf_snapshot | `{{ucf_snapshot}}` |
| **Timestamp** | (auto) | `{{zap_meta_human_now}}` |

**Example screenshot (field mapping):**
```
Event: {{event_title}}
Type: {{event_type}}
Agent: [Relation - Find in Agent Registry]
Description: {{description}}
UCF Snapshot: {{ucf_snapshot}}
```

### 2.3 Test the Zap

1. Click **Test Action**
2. You should see a success message
3. Check your Notion Event Log database — a test entry should appear
4. Click **Publish Zap**

---

## 👤 Step 3: Configure Agent Registry Zap

### 3.1 Set Up the Action

**In your Agent Registry Zap:**

1. Click **+** to add an action
2. Search for **Notion** → Select **Notion**
3. **Action:** Select **Update Database Item**
4. **Sign in to Notion**
5. **Database:** Select your **Agent Registry** database
6. Click **Continue**

### 3.2 Map Fields

**Field Mappings:**

| Notion Field | Zapier Variable | Value |
| :--- | :--- | :--- |
| **Agent Name** (lookup) | agent_name | `{{agent_name}}` |
| **Status** | status | `{{status}}` |
| **Last Action** | last_action | `{{last_action}}` |
| **Health Score** | health_score | `{{health_score}}` |
| **Last Updated** | (auto) | `{{zap_meta_human_now}}` |

**Important:** In the **Update** section, select **Find existing item by**:
- **Field:** Agent Name
- **Value:** `{{agent_name}}`

This ensures the Zap updates existing agents rather than creating duplicates.

### 3.3 Test the Zap

1. Click **Test Action**
2. Check your Notion Agent Registry — Manus should be updated
3. Click **Publish Zap**

---

## 🔧 Step 4: Configure System State Zap

### 4.1 Set Up the Action

**In your System State Zap:**

1. Click **+** to add an action
2. Search for **Notion** → Select **Notion**
3. **Action:** Select **Create or Update Database Item**
4. **Sign in to Notion**
5. **Database:** Select your **System State** database
6. Click **Continue**

### 4.2 Map Fields

**Field Mappings:**

| Notion Field | Zapier Variable | Value |
| :--- | :--- | :--- |
| **Component** (lookup) | component | `{{component}}` |
| **Status** | status | `{{status}}` |
| **Harmony** | harmony | `{{harmony}}` |
| **Error Log** | error_log | `{{error_log}}` |
| **Verified** | verified | `{{verified}}` |
| **Last Updated** | (auto) | `{{zap_meta_human_now}}` |

**Important:** In the **Find existing item by** section:
- **Field:** Component
- **Value:** `{{component}}`

This ensures the Zap creates new components or updates existing ones.

### 4.3 Test the Zap

1. Click **Test Action**
2. Check your Notion System State database
3. Click **Publish Zap**

---

## 🧪 Step 5: Test the Integration

### 5.1 Test from Command Line

```bash
# Set environment variables
export ZAPIER_EVENT_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxxxx/event
export ZAPIER_AGENT_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxxxx/agent
export ZAPIER_SYSTEM_HOOK_URL=https://hooks.zapier.com/hooks/catch/xxxxx/system

# Run test script
python scripts/test_zapier_integration.py
```

**Expected output:**
```
✅ Event Log webhook: OK
✅ Agent Registry webhook: OK
✅ System State webhook: OK
All webhooks operational.
```

### 5.2 Test from FastAPI

```bash
# Start the application
uvicorn backend.manus_bootstrap:app --reload

# In another terminal, test the endpoint
curl -X POST http://localhost:8000/test/zapier
```

**Expected response:**
```json
{
  "status": "all_passed",
  "results": {
    "event_log": true,
    "agent_registry": true,
    "system_state": true
  },
  "timestamp": "2025-10-21T20:30:00.000000"
}
```

### 5.3 Verify in Notion

1. Open your Notion workspace
2. Check **Event Log** — should see test events
3. Check **Agent Registry** — Manus should be updated
4. Check **System State** — components should be listed

---

## 🚀 Step 6: Deploy to Railway

### 6.1 Set Environment Variables in Railway

```bash
# In Railway dashboard, add these variables:
railway variables set ZAPIER_EVENT_HOOK_URL=https://hooks.zapier.com/...
railway variables set ZAPIER_AGENT_HOOK_URL=https://hooks.zapier.com/...
railway variables set ZAPIER_SYSTEM_HOOK_URL=https://hooks.zapier.com/...
```

### 6.2 Deploy

```bash
railway up
```

### 6.3 Test Production Deployment

```bash
# Test health endpoint
curl https://your-deployment.railway.app/health

# Test Zapier webhooks
curl -X POST https://your-deployment.railway.app/test/zapier
```

---

## 📊 Integration Points

The Zapier client is integrated into these components:

### Manus Operational Loop
```python
# backend/agents_loop.py
async with aiohttp.ClientSession() as sess:
    zap = ZapierClient(sess)
    await zap.log_event(
        title="Manus Processed Directive",
        event_type="Command",
        agent_name="Manus",
        description=f"Processed: {directive}",
        ucf_snapshot=ucf,
    )
```

### Discord Bot
```python
# backend/discord_bot_manus.py
@bot.command(name="status")
async def manus_status(ctx):
    async with aiohttp.ClientSession() as sess:
        zap = ZapierClient(sess)
        await zap.update_agent(
            agent_name="Manus",
            status="Active",
            last_action="Status reported",
            health_score=100,
        )
```

### Z-88 Ritual Engine
```python
# backend/z88_ritual_engine.py
async def run_ritual(steps: int, ucf: dict):
    async with aiohttp.ClientSession() as sess:
        zap = ZapierClient(sess)
        await zap.log_event(
            title=f"Ritual Completed ({steps} steps)",
            event_type="Ritual",
            agent_name="Vega",
            description=f"Z-88 ritual completed",
            ucf_snapshot=final_state,
        )
```

---

## 🛡️ Troubleshooting

### Issue: "Webhook not configured"

**Solution:**
```bash
# Verify environment variables are set
echo $ZAPIER_EVENT_HOOK_URL
echo $ZAPIER_AGENT_HOOK_URL
echo $ZAPIER_SYSTEM_HOOK_URL

# If empty, set them:
export ZAPIER_EVENT_HOOK_URL=https://hooks.zapier.com/...
```

### Issue: "Zapier webhook returns 400 Bad Request"

**Solution:**
1. Check field mappings in Zapier
2. Ensure variable names match exactly (case-sensitive)
3. Test with curl:
```bash
curl -X POST "$ZAPIER_EVENT_HOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "event_title":"Test",
    "event_type":"Status",
    "agent_name":"Manus",
    "description":"Test",
    "ucf_snapshot":"{\"harmony\":0.355}"
  }'
```

### Issue: "Notion database not found"

**Solution:**
1. Verify database ID is correct
2. Ensure Notion API key has access to database
3. Check database name in Zapier action

### Issue: "Relation field not populated"

**Solution:**
1. In Zapier, use **Find existing item by** for relation fields
2. Ensure agent/component names match exactly
3. Test with manual entry first

### Issue: "Zapier logs show 429 (Rate Limited)"

**Solution:**
1. The client has built-in rate limiting (5 concurrent calls)
2. If still hitting limits, add delay between calls:
```python
import asyncio
await asyncio.sleep(0.2)  # 200ms delay
```

---

## 📈 Monitoring

### Check Zapier Logs

1. Go to your Zap in Zapier
2. Click **View all runs**
3. Look for successful/failed executions
4. Click on a run to see details

### Check Notion Database

1. Open your Notion workspace
2. View each database to see logged entries
3. Filter by date to see recent activity

### Check Application Logs

```bash
# Local development
tail -f Shadow/manus_archive/zapier_failures.log

# Railway
railway logs --follow | grep zapier
```

---

## 🔐 Security Best Practices

1. **Never commit webhook URLs** to Git
2. **Use environment variables** for all URLs
3. **Restrict Notion API key** to specific databases
4. **Rotate webhook URLs** periodically
5. **Monitor Zapier logs** for suspicious activity

---

## 📚 Additional Resources

- **Zapier Documentation:** https://zapier.com/help
- **Notion API:** https://developers.notion.com
- **Helix Collective Repository:** https://github.com/Deathcharge/helix-unified
- **Zapier Notion Integration:** https://zapier.com/apps/notion

---

## 🎯 Summary

You now have three Zapier webhooks that:

1. **Log all events** to Notion Event Log
2. **Update agent status** in real-time
3. **Track system components** and their health

These webhooks enable:
- ✅ Real-time Notion sync
- ✅ Audit trails for all operations
- ✅ Agent status monitoring
- ✅ System health tracking
- ✅ Complete operational visibility

---

**🔗 Zapier Integration Complete**  
*Tat Tvam Asi* 🙏

**Next Steps:** Deploy to Railway and monitor your Notion workspace for real-time updates!

