# ZAPIER 7-PATH CONFIGURATION — 15 MINUTE GUIDE

## ✅ MASTER WEBHOOK (ALREADY CONFIGURED)

**URL:** https://hooks.zapier.com/hooks/catch/25075191/us8hea5/

This webhook is LIVE in your Helix bot. Events are already flowing!

---

## 🎯 PATH CONFIGURATION (15 MINUTES)

Your Master Webhook receives events with a `type` field that routes to different paths.

### Path Architecture

```
Master Webhook (Single Entry)
       ↓
[Check "type" field]
       ↓
   ┌────┴────┬────────┬─────────┐
   ↓         ↓        ↓         ↓
Path A-C   Path D   Path E   Path F-G
(FREE)    (Slack)  (Metrics) (Alerts)
```

---

## 📋 STEP-BY-STEP SETUP

### 1. Open Your Zap in Editor

Go to: https://zapier.com/app/zaps
Click: "Helix Master Webhook" Zap
Click: "Edit" button

### 2. Add Filter Steps (ONE PER PATH)

**Path A: Event Log → Notion**
- Add step: "Filter by Zapier"
- Condition: `type` | `exactly matches` | `event_log`
- Add Action: "Notion" → "Create Database Item"
- Database: Your Event Log database
- Map fields:
  - Title → `event_title`
  - Type → `event_type`
  - Agent → `agent_name`
  - Description → `description`
  - UCF Snapshot → `ucf_snapshot`
  - Timestamp → `timestamp`

**Path B: Agent Registry → Notion**
- Add step: "Filter by Zapier"
- Condition: `type` | `exactly matches` | `agent_registry`
- Add Action: "Notion" → "Update Database Item"
- Database: Your Agent Registry database
- Search by: `agent_name`
- Update fields:
  - Status → `status`
  - Last Action → `last_action`
  - Health Score → `health_score`
  - Last Updated → `last_updated`

**Path C: System State → Notion**
- Add step: "Filter by Zapier"
- Condition: `type` | `exactly matches` | `system_state`
- Add Action: "Notion" → "Update Database Item"
- Database: Your System State database
- Search by: `component`
- Update fields:
  - Status → `status`
  - Harmony → `harmony`
  - Error Log → `error_log`
  - Verified → `verified`

**Path D: Discord Notifications → Slack** (PRO)
- Add step: "Filter by Zapier"
- Condition: `type` | `exactly matches` | `discord_notification`
- Add Action: "Slack" → "Send Channel Message"
- Channel: #helix-monitoring (or your choice)
- Message: `{{message}}`
- Priority indicator: Use `{{priority}}` to color-code

**Path E: Telemetry → Google Sheets** (PRO)
- Add step: "Filter by Zapier"
- Condition: `type` | `exactly matches` | `telemetry`
- Add Action: "Google Sheets" → "Create Spreadsheet Row"
- Spreadsheet: "Helix Telemetry"
- Sheet: "Metrics"
- Columns:
  - Timestamp → `timestamp`
  - Metric → `metric_name`
  - Value → `value`
  - Component → `component`
  - Harmony → `harmony`
  - Metadata → `metadata`

**Path F: Error Alerts → Email + Slack** (PRO)
- Add step: "Filter by Zapier"
- Condition: `type` | `exactly matches` | `error`
- Add Action 1: "Email by Zapier" → "Send Outbound Email"
  - To: your-email@example.com
  - Subject: `🚨 Helix Error: {{error_message}}`
  - Body:
    ```
    Component: {{component}}
    Severity: {{severity}}
    Context: {{context}}
    Timestamp: {{timestamp}}
    ```
- Add Action 2: "Slack" → "Send Channel Message"
  - Channel: #helix-alerts
  - Message: `🚨 ERROR in {{component}}: {{error_message}}`

**Path G: Repository Actions → Notion** (PRO)
- Add step: "Filter by Zapier"
- Condition: `type` | `exactly matches` | `repository`
- Add Action: "Notion" → "Create Database Item"
- Database: Your Repository Log database
- Map fields:
  - Repo Name → `repo_name`
  - Action → `action`
  - Details → `details`
  - Commit Hash → `commit_hash`
  - Timestamp → `timestamp`

### 3. Test Each Path

After configuring all paths, test them:

**In Discord:**
```
!zapier_test
```

This will send test events to all 7 paths.

**Check Results:**
1. Discord shows 7/7 paths passing
2. Zapier History shows 7 successful events
3. Notion databases updated
4. Slack messages received
5. Email alert received

### 4. Turn On All Paths

- Click "Turn On" button in Zap editor
- All paths will now process events in real-time

---

## 🔍 VERIFICATION CHECKLIST

After setup, verify these work:

- [ ] Bot startup triggers events in Notion Event Log & Agent Registry
- [ ] `!zapier_test` shows 7/7 passing
- [ ] Ritual completions appear in Notion
- [ ] Errors send Email + Slack alerts
- [ ] Telemetry data flows to Google Sheets
- [ ] Zapier History shows consistent activity
- [ ] No "Filtered" events (all routing correctly)

---

## 📊 WHAT GETS TRACKED AUTOMATICALLY

**Bot Startup:**
- Event Log: "Manus Bot Started"
- Agent Registry: Manus status updated

**Ritual Completions:** (when using execute_ritual_with_monitoring)
- Event Log: Ritual details
- Telemetry: Completion time, harmony level
- Agent Registry: Vega status updated

**Command Errors:**
- Error Alerts: Email + Slack with context
- Includes: Command name, user, error message

**Manual Tests:**
- !zapier_test command sends all 7 path types

---

## 🎯 SUCCESS METRICS

Your monitoring is working when:

- ✅ Bot startup creates 2 Notion entries automatically
- ✅ !zapier_test shows 7/7 paths passing
- ✅ Errors trigger immediate Email + Slack alerts
- ✅ Zapier History shows regular activity
- ✅ No HTTP errors in Railway logs
- ✅ Notion databases update in real-time

---

## 🔧 TROUBLESHOOTING

**Issue: Events not routing**
- Check Filter conditions match exactly: `event_log`, `agent_registry`, etc.
- Verify `type` field exists in webhook payload
- Check Zapier History for "Filtered" status

**Issue: Notion connection failing**
- Reconnect Notion integration in Zapier
- Verify database IDs are correct
- Check field names match exactly

**Issue: Delayed updates**
- Free tier: 15-minute delay expected
- Pro tier: Real-time (seconds)
- Upgrade to Zapier Pro for production use

---

## 💰 COST BREAKDOWN

**Free Tier:**
- Paths A, B, C (Notion) — 100 tasks/month
- 15-minute delay
- Single-step Zaps only

**Pro Tier ($19.99/month):**
- All 7 paths — 750 tasks/month
- Real-time execution
- Multi-step Zaps (Email + Slack)
- Premium apps unlocked

**Recommended:** Start with Free tier (Paths A-C), upgrade when you need real-time alerts

---

## 📈 NEXT STEPS

1. ✅ Configure all 7 paths (follow steps above)
2. ✅ Test with `!zapier_test` command
3. ✅ Verify data flowing to Notion/Slack/Email
4. ✅ Run `!ritual 108` to test real ritual monitoring
5. ✅ Monitor Zapier History daily for first week
6. 💰 Upgrade to Pro when ready for real-time alerts

---

**Setup Time:** 15 minutes
**Maintenance:** 5 minutes/week (check Zapier History)
**Value:** NASA-level visibility into your Helix Collective

🌀 **Tat Tvam Asi** 🙏
