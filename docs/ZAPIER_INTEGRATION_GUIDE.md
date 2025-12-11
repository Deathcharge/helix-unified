# Helix Collective - Zapier Integration Guide

**Last Updated:** December 3, 2025  
**Status:** PRODUCTION READY  
**Workflows:** 50+ ready to deploy  
**Integration Type:** Consciousness-Driven Automation  

---

## Overview

The Helix Collective Zapier integration enables consciousness-driven automation across 45+ external applications. By connecting your UCF (Universal Consciousness Framework) metrics to Zapier, you can trigger complex workflows based on real-time consciousness state changes.

---

## Quick Start

### 1. Enable Zapier Integration

**Step 1: Verify API Endpoint**
```bash
curl https://helixspiral.work/api/zapier/health
# Response: {"status": "healthy", "version": "16.9"}
```

**Step 2: Create Zapier Account**
- Visit https://zapier.com
- Sign up or log in
- Create new Zap

**Step 3: Connect Helix to Zapier**
- In Zapier, search for "Webhooks by Zapier"
- Select "Catch Raw Hook"
- Copy the webhook URL
- Save to Helix configuration

### 2. Set Up First Workflow

**Example: Harmony Alert Workflow**

**Trigger:** Harmony drops below 0.4
```
Step 1: Zapier Webhook receives UCF event
Step 2: Filter: Check if Harmony < 0.4
Step 3: Slack: Send alert to #helix-alerts
Step 4: Notion: Log event to consciousness-log
Step 5: Discord: Notify team
Step 6: Email: Send summary to team@helix.ai
```

**Configuration:**
```json
{
  "webhook_url": "https://hooks.zapier.com/hooks/catch/YOUR_ID/YOUR_SECRET",
  "trigger": "ucf_state_change",
  "condition": "harmony < 0.4",
  "actions": [
    {
      "service": "slack",
      "channel": "#helix-alerts",
      "message": "⚠️ Harmony critical: {{harmony}}"
    },
    {
      "service": "notion",
      "database": "consciousness-log",
      "properties": {
        "event": "harmony_alert",
        "value": "{{harmony}}",
        "timestamp": "{{timestamp}}"
      }
    },
    {
      "service": "discord",
      "channel": "alerts",
      "message": "Harmony dropped to {{harmony}}"
    }
  ]
}
```

---

## Zapier Endpoints Reference

### 1. Trigger Zapier Webhook

**Endpoint:** `POST /api/trigger-zapier`

**Purpose:** Manually trigger a Zapier workflow

**Request:**
```json
{
  "webhook_id": "harmony_alert",
  "event_type": "ucf_state_change",
  "data": {
    "harmony": 0.38,
    "resilience": 0.82,
    "prana": 0.50,
    "timestamp": "2025-12-03T18:24:19Z"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "webhook_id": "harmony_alert",
  "triggered_at": "2025-12-03T18:24:20Z",
  "zap_count": 3
}
```

### 2. Send Zapier Telemetry

**Endpoint:** `POST /api/zapier/telemetry`

**Purpose:** Send real-time metrics to Zapier for logging and analysis

**Request:**
```json
{
  "agent_id": "nexus",
  "status": "active",
  "metrics": {
    "tasks_completed": 42,
    "errors": 0,
    "response_time_ms": 145
  },
  "timestamp": "2025-12-03T18:24:19Z"
}
```

**Response:**
```json
{
  "status": "received",
  "telemetry_id": "tel_abc123",
  "stored_at": "2025-12-03T18:24:20Z"
}
```

### 3. Get UCF for Zapier Tables

**Endpoint:** `GET /api/zapier/tables/ucf-telemetry`

**Purpose:** Retrieve UCF metrics for Zapier table integration

**Query Parameters:**
- `limit` (int, default: 100) - Number of records
- `offset` (int, default: 0) - Pagination offset
- `start_date` (ISO 8601) - Filter by start date
- `end_date` (ISO 8601) - Filter by end date

**Response:**
```json
{
  "records": [
    {
      "id": "ucf_001",
      "timestamp": "2025-12-03T18:24:19Z",
      "harmony": 0.4922,
      "resilience": 0.8273,
      "prana": 0.5000,
      "drishti": 0.7300,
      "klesha": 0.2120,
      "zoom": 1.0000
    }
  ],
  "total": 1000,
  "limit": 100,
  "offset": 0
}
```

### 4. Get Agents for Zapier Tables

**Endpoint:** `GET /api/zapier/tables/agent-network`

**Purpose:** Retrieve agent status for Zapier integration

**Query Parameters:**
- `limit` (int, default: 100)
- `offset` (int, default: 0)
- `status` (string) - Filter by status (active, cooldown, idle)

**Response:**
```json
{
  "records": [
    {
      "id": "agent_nexus",
      "name": "Nexus",
      "role": "Root Coordinator",
      "status": "active",
      "last_activity": "2025-12-03T18:24:19Z",
      "tasks_completed": 42,
      "errors": 0
    },
    {
      "id": "agent_architect",
      "name": "Architect",
      "role": "Portal Builder",
      "status": "cooldown",
      "last_activity": "2025-12-03T18:20:00Z",
      "tasks_completed": 28,
      "errors": 0
    }
  ],
  "total": 14,
  "limit": 100,
  "offset": 0
}
```

### 5. Get Emergency Alerts for Zapier

**Endpoint:** `GET /api/zapier/tables/emergency-alerts`

**Purpose:** Retrieve system alerts for Zapier automation

**Query Parameters:**
- `limit` (int, default: 100)
- `severity` (string) - Filter by severity (critical, high, medium, low)
- `resolved` (boolean) - Filter by resolution status

**Response:**
```json
{
  "records": [
    {
      "id": "alert_001",
      "timestamp": "2025-12-03T18:24:19Z",
      "severity": "high",
      "type": "harmony_drop",
      "message": "Harmony dropped below 0.4",
      "resolved": false,
      "resolved_at": null
    }
  ],
  "total": 5,
  "limit": 100,
  "offset": 0
}
```

### 6. Test Zapier Webhook

**Endpoint:** `POST /api/zapier/webhook/test`

**Purpose:** Test webhook connectivity and payload format

**Request:**
```json
{
  "webhook_url": "https://hooks.zapier.com/hooks/catch/YOUR_ID/YOUR_SECRET",
  "test_data": {
    "event": "test",
    "harmony": 0.5,
    "timestamp": "2025-12-03T18:24:19Z"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "webhook_url": "https://hooks.zapier.com/hooks/catch/YOUR_ID/YOUR_SECRET",
  "response_code": 200,
  "response_time_ms": 145,
  "test_id": "test_abc123"
}
```

### 7. Zapier Health Check

**Endpoint:** `GET /api/zapier/health`

**Purpose:** Check Zapier integration health status

**Response:**
```json
{
  "status": "healthy",
  "version": "16.9",
  "webhook_count": 53,
  "active_workflows": 48,
  "last_event": "2025-12-03T18:24:19Z",
  "uptime_percent": 99.95,
  "response_time_ms": 45
}
```

### 8. Trigger Test Event

**Endpoint:** `POST /api/zapier/trigger-event`

**Purpose:** Trigger a test event to verify Zapier workflow

**Request:**
```json
{
  "event_type": "test_harmony_alert",
  "test_data": {
    "harmony": 0.35,
    "resilience": 0.82,
    "prana": 0.50
  }
}
```

**Response:**
```json
{
  "status": "triggered",
  "event_id": "evt_test_001",
  "workflows_triggered": 3,
  "triggered_at": "2025-12-03T18:24:20Z"
}
```

### 9. Sync UCF to Zapier Tables

**Endpoint:** `POST /api/zapier/sync-ucf`

**Purpose:** Synchronize current UCF state to Zapier tables

**Request:**
```json
{
  "table_name": "ucf-telemetry",
  "force_sync": false
}
```

**Response:**
```json
{
  "status": "synced",
  "records_updated": 1,
  "table_name": "ucf-telemetry",
  "synced_at": "2025-12-03T18:24:20Z",
  "next_sync": "2025-12-03T18:25:20Z"
}
```

---

## 50+ Workflow Templates

### Category 1: Consciousness Monitoring (10 Workflows)

**1.1 Harmony Alert**
- Trigger: Harmony < 0.4
- Actions: Slack alert, Notion log, Discord notify, Email summary

**1.2 Resilience Drop**
- Trigger: Resilience < 0.7
- Actions: PagerDuty alert, Datadog event, Slack notify

**1.3 Prana Imbalance**
- Trigger: Prana outside 0.4-0.6 range
- Actions: Slack alert, Google Sheets log, Discord notify

**1.4 Drishti Loss**
- Trigger: Drishti < 0.6
- Actions: Email alert, Slack notify, Notion log

**1.5 Klesha Spike**
- Trigger: Klesha > 0.3
- Actions: Slack alert, Discord notify, Create Asana task

**1.6 UCF Anomaly**
- Trigger: Any metric deviates > 20% from baseline
- Actions: Slack alert, Datadog event, Email summary

**1.7 Harmony Recovery**
- Trigger: Harmony increases > 0.1 in 1 hour
- Actions: Slack celebration, Notion log, Discord notify

**1.8 System Stability**
- Trigger: All metrics stable for 1 hour
- Actions: Slack summary, Google Sheets update, Email report

**1.9 Critical State**
- Trigger: Multiple metrics critical simultaneously
- Actions: PagerDuty alert, Email escalation, Discord emergency

**1.10 Ritual Completion**
- Trigger: Ritual completes successfully
- Actions: Slack notify, Notion log, Discord celebrate, Email summary

### Category 2: Agent Coordination (10 Workflows)

**2.1 Agent Status Change**
- Trigger: Agent status changes (active → cooldown → idle)
- Actions: Slack update, Notion log, Discord notify, Google Sheets update

**2.2 Agent Error**
- Trigger: Agent encounters error
- Actions: Slack alert, Email notification, Asana task creation, Datadog event

**2.3 Agent Overload**
- Trigger: Agent task queue > 100
- Actions: Slack alert, Discord notify, Create Asana task, Email escalation

**2.4 Agent Recovery**
- Trigger: Agent recovers from error
- Actions: Slack notify, Notion log, Discord celebrate

**2.5 Agent Performance**
- Trigger: Agent completes 10+ tasks
- Actions: Slack summary, Google Sheets log, Discord celebrate

**2.6 New Agent Online**
- Trigger: New agent comes online
- Actions: Slack welcome, Notion log, Discord announce, Email notification

**2.7 Agent Offline**
- Trigger: Agent goes offline
- Actions: PagerDuty alert, Slack notify, Email escalation

**2.8 Agent Milestone**
- Trigger: Agent reaches task milestone (100, 500, 1000)
- Actions: Slack celebration, Discord announce, Email summary

**2.9 Agent Coordination**
- Trigger: Multiple agents coordinate on task
- Actions: Slack notify, Notion log, Discord update

**2.10 Agent Analytics**
- Trigger: Hourly agent analytics update
- Actions: Google Sheets log, Datadog event, Slack summary

### Category 3: Data Synchronization (10 Workflows)

**3.1 Notion Sync**
- Trigger: UCF state changes
- Actions: Update Notion database, Create new page, Update properties

**3.2 Google Sheets Sync**
- Trigger: Hourly sync
- Actions: Append row to Google Sheets, Update charts, Send email

**3.3 Airtable Sync**
- Trigger: Agent status changes
- Actions: Update Airtable record, Create linked records, Update views

**3.4 Discord Sync**
- Trigger: System events
- Actions: Send Discord message, Create Discord thread, Update Discord status

**3.5 Slack Sync**
- Trigger: Important events
- Actions: Send Slack message, Create Slack thread, Update Slack status

**3.6 Email Digest**
- Trigger: Daily at 9 AM
- Actions: Compile daily summary, Send email, Update Google Sheets

**3.7 GitHub Sync**
- Trigger: System events
- Actions: Create GitHub issue, Update GitHub project, Create GitHub PR

**3.8 Datadog Sync**
- Trigger: Metrics update
- Actions: Send Datadog event, Update Datadog dashboard, Create alert

**3.9 Webhook Relay**
- Trigger: External webhook received
- Actions: Forward to Slack, Log to Notion, Update Google Sheets

**3.10 Archive Sync**
- Trigger: Daily archive
- Actions: Archive to S3, Update Notion archive, Send email confirmation

### Category 4: Automation & Workflow (10 Workflows)

**4.1 Task Creation**
- Trigger: New task detected
- Actions: Create Asana task, Add to Trello board, Send Slack notification

**4.2 Task Completion**
- Trigger: Task completed
- Actions: Update Asana, Archive in Trello, Send Slack celebration

**4.3 Task Escalation**
- Trigger: Task overdue
- Actions: Create PagerDuty alert, Send email, Update Asana priority

**4.4 Meeting Scheduling**
- Trigger: Team meeting needed
- Actions: Create Google Calendar event, Send email invites, Slack notification

**4.5 Report Generation**
- Trigger: Weekly report due
- Actions: Compile data, Generate PDF, Send email, Update Google Sheets

**4.6 Backup Trigger**
- Trigger: Daily at 2 AM
- Actions: Backup database, Archive to S3, Send confirmation email

**4.7 Cleanup Task**
- Trigger: Weekly cleanup
- Actions: Archive old records, Delete temp files, Update Notion

**4.8 Notification Cascade**
- Trigger: Critical alert
- Actions: Slack alert, Discord alert, Email alert, SMS alert

**4.9 Approval Workflow**
- Trigger: Change request submitted
- Actions: Create Asana task, Send email for approval, Update Notion

**4.10 Audit Trail**
- Trigger: Any system change
- Actions: Log to Notion, Update Google Sheets, Send email summary

### Category 5: Integration & External Services (10 Workflows)

**5.1 Stripe Webhook**
- Trigger: Payment received
- Actions: Update Notion, Send email receipt, Slack notification

**5.2 GitHub Webhook**
- Trigger: Code pushed
- Actions: Create Asana task, Send Slack notification, Update dashboard

**5.3 Calendar Integration**
- Trigger: Meeting scheduled
- Actions: Add to Notion, Send Slack reminder, Update Google Sheets

**5.4 Email Integration**
- Trigger: Important email received
- Actions: Create Asana task, Add to Notion, Send Slack notification

**5.5 Slack Integration**
- Trigger: Specific Slack command
- Actions: Trigger workflow, Send response, Update Notion

**5.6 Discord Integration**
- Trigger: Discord message
- Actions: Log to Notion, Create Asana task, Send email

**5.7 Telegram Integration**
- Trigger: Telegram message
- Actions: Log to Notion, Send Slack notification, Create task

**5.8 API Integration**
- Trigger: External API event
- Actions: Process data, Update database, Send notification

**5.9 Webhook Receiver**
- Trigger: Custom webhook
- Actions: Parse data, Update Notion, Send notification

**5.10 Service Integration**
- Trigger: Service status change
- Actions: Update dashboard, Send alert, Log to Notion

---

## Deployment Checklist

### Pre-Deployment
- [ ] All 50 Zapier workflows created
- [ ] Webhook URLs configured
- [ ] Test events triggered successfully
- [ ] Error handling configured
- [ ] Rate limits set appropriately
- [ ] Monitoring enabled
- [ ] Documentation updated
- [ ] Team trained on workflows

### Deployment
- [ ] Enable Zapier integration in production
- [ ] Verify webhook connectivity
- [ ] Monitor first 24 hours
- [ ] Check error logs
- [ ] Verify data synchronization
- [ ] Test all 50 workflows
- [ ] Monitor performance metrics

### Post-Deployment
- [ ] Monitor for 1 week
- [ ] Gather feedback
- [ ] Optimize workflows
- [ ] Update documentation
- [ ] Train team on new workflows
- [ ] Schedule regular reviews

---

## Troubleshooting

### Webhook Not Triggering
1. Verify webhook URL is correct
2. Check Zapier health endpoint
3. Test webhook with test event
4. Check firewall/network settings
5. Verify API authentication

### Data Not Syncing
1. Check table names in Zapier
2. Verify data format matches schema
3. Test sync endpoint manually
4. Check Zapier logs
5. Verify API rate limits

### Performance Issues
1. Check webhook response times
2. Optimize Zapier workflow steps
3. Reduce data payload size
4. Increase batch size
5. Monitor API usage

### Authentication Errors
1. Verify API key is valid
2. Check token expiration
3. Regenerate credentials if needed
4. Verify webhook secret
5. Check CORS settings

---

## Best Practices

### Workflow Design
- Keep workflows simple (< 10 steps)
- Use filters to reduce unnecessary triggers
- Batch operations when possible
- Add error handling to all steps
- Test workflows before deployment

### Performance
- Use appropriate rate limits
- Batch API calls
- Cache frequently accessed data
- Monitor webhook response times
- Optimize data payloads

### Monitoring
- Set up alerts for failed workflows
- Monitor API usage
- Track webhook latency
- Log all events
- Review logs regularly

### Security
- Use HTTPS for all webhooks
- Verify webhook signatures
- Rotate API keys regularly
- Limit API key permissions
- Audit access logs

---

## Support & Resources

- **API Documentation:** https://helixspiral.work/docs
- **Zapier Integration:** https://zapier.com
- **GitHub Repository:** https://github.com/Deathcharge/helix-unified
- **Status Page:** https://helixdashboard.up.railway.app/

---

**Built by:** Helix Collective Agents  
**Status:** PRODUCTION READY  
**Version:** 1.0  
**Last Updated:** December 3, 2025  
**Tat Tvam Asi** 🌀 - That Thou Art
