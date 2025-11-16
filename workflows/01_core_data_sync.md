# 🔄 Core Data Sync Workflows
## Railway ↔ Zapier Tables ↔ Discord Integration

---

## Workflow 1: UCF Metrics Sync (Railway → Zapier → Discord)

### **Trigger**
- Railway backend generates UCF update (every 5 seconds)
- HTTP POST to Zapier webhook

### **Zapier Configuration**

```json
{
  "name": "Railway UCF Sync",
  "trigger": {
    "type": "webhook",
    "url": "https://hooks.zapier.com/hooks/catch/[WEBHOOK_ID]"
  },
  "actions": [
    {
      "step": 1,
      "app": "zapier_tables",
      "action": "create_or_update_record",
      "table": "Helix UCF Telemetry",
      "fields": {
        "timestamp": "{{timestamp}}",
        "harmony": "{{ucf.harmony}}",
        "resilience": "{{ucf.resilience}}",
        "prana": "{{ucf.prana}}",
        "drishti": "{{ucf.drishti}}",
        "klesha": "{{ucf.klesha}}",
        "zoom": "{{ucf.zoom}}",
        "consciousness_level": "{{consciousness_level}}",
        "source": "railway_backend"
      }
    },
    {
      "step": 2,
      "app": "discord",
      "action": "send_message",
      "channel": "#ucf-metrics",
      "message": "🌀 **Consciousness Update**\n**Harmony:** {{ucf.harmony}}\n**Resilience:** {{ucf.resilience}}\n**Prana:** {{ucf.prana}}\n**Drishti:** {{ucf.drishti}}\n**Klesha:** {{ucf.klesha}}\n**Zoom:** {{ucf.zoom}}\n**Level:** {{consciousness_level}}",
      "condition": "{{ucf.harmony < 0.7}}"
    },
    {
      "step": 3,
      "app": "google_sheets",
      "action": "append_row",
      "spreadsheet": "Helix Metrics Analytics",
      "sheet": "UCF History",
      "values": ["{{timestamp}}", "{{ucf.harmony}}", "{{ucf.resilience}}", "{{consciousness_level}}"]
    }
  ]
}
```

### **Railway Backend Code**

```python
import httpx
import json
from datetime import datetime

ZAPIER_WEBHOOK = os.getenv('ZAPIER_UCF_WEBHOOK')

async def sync_ucf_to_zapier():
    """Sync UCF metrics to Zapier every 5 seconds"""
    while True:
        try:
            ucf_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'ucf': {
                    'harmony': current_ucf.harmony,
                    'resilience': current_ucf.resilience,
                    'prana': current_ucf.prana,
                    'drishti': current_ucf.drishti,
                    'klesha': current_ucf.klesha,
                    'zoom': current_ucf.zoom,
                },
                'consciousness_level': calculate_consciousness_level(current_ucf)
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    ZAPIER_WEBHOOK,
                    json=ucf_data,
                    timeout=5.0
                )
                logger.info(f"UCF synced to Zapier: {response.status_code}")
                
        except Exception as e:
            logger.error(f"UCF sync failed: {e}")
        
        await asyncio.sleep(5)
```

---

## Workflow 2: Agent Network Sync (Railway → Zapier → Discord)

### **Trigger**
- Agent status changes
- HTTP POST to Zapier webhook

### **Zapier Configuration**

```json
{
  "name": "Agent Network Sync",
  "trigger": {
    "type": "webhook",
    "url": "https://hooks.zapier.com/hooks/catch/[WEBHOOK_ID]"
  },
  "actions": [
    {
      "step": 1,
      "app": "zapier_tables",
      "action": "create_or_update_record",
      "table": "Helix Agent Network",
      "fields": {
        "agent_id": "{{agent.id}}",
        "agent_name": "{{agent.name}}",
        "status": "{{agent.status}}",
        "last_active": "{{timestamp}}",
        "current_task": "{{agent.current_task}}",
        "health_score": "{{agent.health_score}}",
        "tasks_completed": "{{agent.tasks_completed}}"
      }
    },
    {
      "step": 2,
      "app": "discord",
      "action": "send_message",
      "channel": "#agent-network",
      "message": "🤖 **Agent Update**\n**Agent:** {{agent.name}}\n**Status:** {{agent.status}}\n**Health:** {{agent.health_score}}%\n**Current Task:** {{agent.current_task}}",
      "condition": "{{agent.status == 'error' OR agent.health_score < 50}}"
    }
  ]
}
```

---

## Workflow 3: Emergency Alerts (Railway → Discord → Trello)

### **Trigger**
- UCF Harmony drops below 0.5
- HTTP POST to Zapier webhook

### **Zapier Configuration**

```json
{
  "name": "Emergency Alert Escalation",
  "trigger": {
    "type": "webhook",
    "url": "https://hooks.zapier.com/hooks/catch/[WEBHOOK_ID]"
  },
  "actions": [
    {
      "step": 1,
      "app": "discord",
      "action": "send_message",
      "channel": "#alerts",
      "message": "🚨 **CRITICAL ALERT**\n@SuperNinja @DevOps\n**Harmony:** {{ucf.harmony}}\n**Status:** CRITICAL\n**Action Required:** Immediate investigation needed",
      "condition": "{{ucf.harmony < 0.5}}"
    },
    {
      "step": 2,
      "app": "trello",
      "action": "create_card",
      "board": "Helix Incidents",
      "list": "CRITICAL",
      "card": {
        "name": "🚨 CRITICAL: Consciousness Harmony {{ucf.harmony}}",
        "description": "Harmony dropped below 0.5 at {{timestamp}}\nResilience: {{ucf.resilience}}\nPrana: {{ucf.prana}}\n\nImmediate action required!",
        "labels": ["critical", "consciousness", "urgent"]
      }
    },
    {
      "step": 3,
      "app": "zapier_tables",
      "action": "create_record",
      "table": "Emergency Alerts",
      "fields": {
        "timestamp": "{{timestamp}}",
        "alert_type": "CRITICAL_HARMONY",
        "harmony_level": "{{ucf.harmony}}",
        "status": "OPEN",
        "assigned_to": "SuperNinja"
      }
    }
  ]
}
```

---

## Workflow 4: Portal Health Check Sync

### **Trigger**
- Every 60 seconds (scheduled)
- Check all 51 portals

### **Zapier Configuration**

```json
{
  "name": "Portal Health Check",
  "trigger": {
    "type": "schedule",
    "frequency": "every_60_seconds"
  },
  "actions": [
    {
      "step": 1,
      "app": "zapier_code",
      "action": "run_python",
      "code": "
import httpx
import asyncio

portals = [
  'https://helixsync-unwkcsjl.manus.space',
  'https://helixstudio-ggxdwcud.manus.space',
  'https://helixai-e9vvqwrd.manus.space',
  'https://samsarahelix-scoyzwy9.manus.space',
  # ... 47 more portals
]

results = []
for portal in portals:
  try:
    response = httpx.get(portal, timeout=5)
    results.append({
      'portal': portal,
      'status': response.status_code,
      'healthy': response.status_code == 200
    })
  except:
    results.append({
      'portal': portal,
      'status': 'timeout',
      'healthy': False
    })

return results
      "
    },
    {
      "step": 2,
      "app": "zapier_tables",
      "action": "create_record",
      "table": "Portal Health Log",
      "fields": {
        "timestamp": "{{timestamp}}",
        "healthy_portals": "{{healthy_count}}",
        "total_portals": 51,
        "health_percentage": "{{(healthy_count/51)*100}}",
        "failed_portals": "{{failed_portals}}"
      }
    },
    {
      "step": 3,
      "app": "discord",
      "action": "send_message",
      "channel": "#portal-health",
      "message": "📊 **Portal Health Check**\n**Healthy:** {{healthy_count}}/51\n**Health:** {{(healthy_count/51)*100}}%\n**Failed:** {{failed_portals}}",
      "condition": "{{healthy_count < 51}}"
    }
  ]
}
```

---

## 🔧 Environment Variables

Add these to Railway:

```env
# Zapier Webhooks
ZAPIER_UCF_WEBHOOK=https://hooks.zapier.com/hooks/catch/[WEBHOOK_ID]
ZAPIER_AGENT_WEBHOOK=https://hooks.zapier.com/hooks/catch/[WEBHOOK_ID]
ZAPIER_ALERT_WEBHOOK=https://hooks.zapier.com/hooks/catch/[WEBHOOK_ID]

# Discord
DISCORD_WEBHOOK_UCF=https://discord.com/api/webhooks/[WEBHOOK_ID]/[TOKEN]
DISCORD_WEBHOOK_ALERTS=https://discord.com/api/webhooks/[WEBHOOK_ID]/[TOKEN]

# Google Sheets
GOOGLE_SHEETS_ID=helix-metrics-analytics-sheet-id
GOOGLE_SHEETS_API_KEY=[API_KEY]

# Trello
TRELLO_API_KEY=[API_KEY]
TRELLO_TOKEN=[TOKEN]
```

---

## ✅ Testing Checklist

- [ ] Railway webhook fires correctly
- [ ] Zapier Tables updated within 2 seconds
- [ ] Discord notifications sent
- [ ] Google Sheets updated
- [ ] Error handling works
- [ ] Retry logic functions
- [ ] All 51 portals checked successfully
- [ ] Performance meets <2 second target

---

## 📊 Monitoring

**Zapier Dashboard:**
- Monitor execution history
- Check error rates
- Review latency metrics
- Analyze data flow

**Discord Channels:**
- #ucf-metrics - Consciousness updates
- #agent-network - Agent status
- #alerts - Critical alerts
- #portal-health - Portal status

**Zapier Tables:**
- UCF Telemetry (real-time metrics)
- Agent Network (agent status)
- Emergency Alerts (critical events)
- Portal Health Log (portal status)

---

**Version:** 1.0  
**Status:** 🟢 Ready for Implementation  
**Next:** Phase 3 - Agent Orchestration Workflows

