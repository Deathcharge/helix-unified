# 🌀 Helix Collective v14.5 — Notion Integration Guide

## Overview

The Helix Collective integrates with Notion to provide persistent memory, audit trails, and context sharing across sessions. This document explains how to set up and use the Notion integration.

---

## 🗄️ Notion Database Schema

### 1. **Agent Registry** (Database ID: `2f65aab794a64ec48bcc46bf760f128f`)

Tracks all 14 agents in the collective.

| Property | Type | Description |
| :--- | :--- | :--- |
| **Agent Name** | Title | Name of the agent (e.g., "Kael", "Manus") |
| **Symbol** | Text | Unicode symbol (e.g., "🜂", "🤲") |
| **Role** | Text | Agent's role description |
| **Status** | Select | "Active", "Pending", "Offline", "Error" |
| **Last Action** | Text | Most recent action taken |
| **Health Score** | Number | 0-100 health metric |
| **Last Updated** | Date | Timestamp of last update |

**Sample Entry:**
```
Agent Name: Manus
Symbol: 🤲
Role: Operational Executor
Status: Active
Last Action: Deployed to Railway
Health Score: 100
Last Updated: 2025-10-21
```

---

### 2. **System State** (Database ID: `009a946d04fb46aa83e4481be86f09ef`)

Tracks core system components and their status.

| Property | Type | Description |
| :--- | :--- | :--- |
| **Component** | Title | Component name (e.g., "Discord Bot", "Z-88 Ritual Engine") |
| **Status** | Select | "Ready", "Offline", "Error", "Active" |
| **Harmony** | Number | Current harmony metric (0.0-1.0) |
| **Last Updated** | Date | Timestamp of last update |
| **Error Log** | Text | Latest error message (if any) |
| **Verification** | Checkbox | Whether component passed verification |

**Sample Entry:**
```
Component: Discord Bot
Status: Active
Harmony: 0.355
Last Updated: 2025-10-21
Error Log: (empty)
Verification: ✓
```

---

### 3. **Event Log** (Database ID: `acb01d4a955d4775aaeb2310d1da1102`)

Immutable record of all system events.

| Property | Type | Description |
| :--- | :--- | :--- |
| **Event** | Title | Event name (e.g., "Ritual Executed", "Agent Status Changed") |
| **Timestamp** | Date | When the event occurred |
| **Event Type** | Select | "Status", "Command", "Error", "Setup", "Ritual" |
| **Agent** | Relation | Link to agent in Agent Registry |
| **Description** | Text | Detailed event description |
| **UCF Snapshot** | Text | JSON snapshot of UCF state at event time |

**Sample Entry:**
```
Event: Z-88 Ritual Completed
Timestamp: 2025-10-21 14:30 UTC
Event Type: Ritual
Agent: [Link to Manus]
Description: Executed 108-step ritual. Harmony increased to 0.375.
UCF Snapshot: {"harmony": 0.375, "klesha": 0.008, "prana": 0.52}
```

---

### 4. **Context Snapshots** (Database ID: `d704854868474666b4b774750f8b134a`)

Captures session context for continuity.

| Property | Type | Description |
| :--- | :--- | :--- |
| **Session ID** | Title | Unique session identifier |
| **AI System** | Select | "Claude", "GPT4o", "Manus", etc. |
| **Created** | Date | Session start time |
| **Summary** | Text | High-level summary of session work |
| **Key Decisions** | Text | Important decisions made |
| **Next Steps** | Text | Recommended next actions |
| **Full Context** | Text | Complete JSON context object |

**Sample Entry:**
```
Session ID: claude-2025-10-21-helix-v14.5
AI System: Claude
Created: 2025-10-21 15:00 UTC
Summary: Validated complete Helix v14.5 codebase...
Key Decisions: Use unified monorepo, FastAPI + Discord bot...
Next Steps: Seed Notion databases, Deploy to Railway...
Full Context: {version: 14.5, agents: 14, ...}
```

---

## 🔧 Setup Instructions

### Step 1: Create Notion Workspace & Databases

1. Go to [notion.so](https://notion.so)
2. Create a new workspace or use existing one
3. Create 4 new databases:
   - **Agent Registry**
   - **System State**
   - **Event Log**
   - **Context Snapshots**

### Step 2: Get Notion API Key

1. Go to [notion.com/my-integrations](https://notion.com/my-integrations)
2. Click "New integration"
3. Name it "Helix Collective"
4. Select your workspace
5. Copy the **Internal Integration Token**
6. Save this as `NOTION_API_KEY` in your `.env` file

### Step 3: Connect Databases to Integration

For each database:
1. Open the database in Notion
2. Click "..." (three dots) → "Connections"
3. Click "Connect to" and select your integration
4. Copy the database ID from the URL (the 32-character hex string)

Update your `.env` file:
```bash
NOTION_API_KEY=secret_xxxxxxxxxxxxx

# Database IDs from your Notion workspace
NOTION_SYSTEM_STATE_DB=your_system_state_db_id
NOTION_AGENT_REGISTRY_DB=your_agent_registry_db_id
NOTION_EVENT_LOG_DB=your_event_log_db_id
NOTION_CONTEXT_DB=your_context_db_id
```

### Step 4: Install Dependencies

```bash
pip install notion-client==2.2.3
```

---

## 📊 Seeding Initial Data

The `seed_notion_data.py` script populates Notion with initial data for all 14 agents, system components, and sample events.

### Run the Seeding Script

```bash
# Set your Notion API key
export NOTION_API_KEY=secret_xxxxxxxxxxxxx

# Run from project root
PYTHONPATH=. python scripts/seed_notion_data.py
```

**Expected Output:**
```
======================================================================
🌀 HELIX COLLECTIVE v14.5 — NOTION SEEDING SEQUENCE
======================================================================

📋 Seeding Agents...
✅ Created agent Kael in Notion
✅ Created agent Lumina in Notion
... (12 more agents)
✅ Agents seeded: 14 created, 0 failed

⚙️ Seeding System Components...
✅ Updated component Discord Bot
✅ Updated component Z-88 Ritual Engine
... (5 more components)
✅ Components seeded: 7 created, 0 failed

📝 Seeding Sample Events...
✅ Logged event: Helix v14.5 Verification Complete
✅ Logged event: Notion Database Setup Complete
✅ Logged event: Unified Monorepo Created
✅ Events seeded: 3 created, 0 failed

📸 Seeding Context Snapshot...
✅ Context snapshot seeded
✅ Context snapshot seeded: 1 created, 0 failed

======================================================================
SEEDING COMPLETE: 25 items created, 0 failed
======================================================================

✅ Results saved to Shadow/manus_archive/notion_seeding_results.json
```

---

## 🔗 Zapier Automation

Zapier bridges Manus operations to Notion, automatically logging events and status updates.

### Zap 1: Manus → Notion Event Log

**Trigger:** Webhook (when Manus completes a task)  
**Action:** Create page in Event Log

**Webhook URL:** `https://your-railway-app.up.railway.app/zapier/event`

**Payload to send from Manus:**
```json
{
  "event_title": "Manus Completed Task",
  "event_type": "Command",
  "agent_name": "Manus",
  "description": "Executed directive: create repository",
  "ucf_snapshot": {"harmony": 0.355}
}
```

**Zapier Configuration:**
1. Create new Zap
2. Trigger: Webhooks by Zapier → Catch Raw Hook
3. Copy the webhook URL
4. Action: Notion → Create Database Item
5. Database: Event Log
6. Map fields:
   - Event (title) → `{{event_title}}`
   - Timestamp → `{{zap_meta_human_now}}`
   - Event Type → `{{event_type}}`
   - Agent → Find relation to `{{agent_name}}`
   - Description → `{{description}}`
   - UCF Snapshot → `{{ucf_snapshot}}`

### Zap 2: Manus → Notion Agent Registry (Update Status)

**Trigger:** Webhook (when Manus starts/stops)  
**Action:** Update page in Agent Registry

**Webhook URL:** `https://your-railway-app.up.railway.app/zapier/agent-status`

**Payload:**
```json
{
  "agent_name": "Manus",
  "status": "Active",
  "last_action": "Repository created",
  "health_score": 100
}
```

**Zapier Configuration:**
1. Create new Zap
2. Trigger: Webhooks by Zapier → Catch Raw Hook
3. Action: Notion → Update Database Item
4. Database: Agent Registry
5. Search: "Agent Name" equals `{{agent_name}}`
6. Update fields:
   - Status → `{{status}}`
   - Last Action → `{{last_action}}`
   - Health Score → `{{health_score}}`
   - Last Updated → `{{zap_meta_human_now}}`

### Zap 3: System Component Status Updates

**Trigger:** Webhook  
**Action:** Update or create System State entry

**Webhook URL:** `https://your-railway-app.up.railway.app/zapier/component-status`

**Payload:**
```json
{
  "component_name": "Discord Bot",
  "status": "Active",
  "harmony": 0.355,
  "error_log": "",
  "verified": true
}
```

---

## 🐍 Using Notion Client in Code

### Basic Usage

```python
from backend.services.notion_client import get_notion_client

# Initialize client
notion = await get_notion_client()

# Log an event
await notion.log_event(
    event_title="Ritual Executed",
    event_type="Ritual",
    agent_name="Manus",
    description="Executed 108-step Z-88 ritual",
    ucf_snapshot={"harmony": 0.375, "klesha": 0.008}
)

# Update agent status
await notion.update_agent_status(
    agent_name="Manus",
    status="Active",
    last_action="Ritual completed",
    health_score=100
)

# Update system component
await notion.update_system_component(
    component_name="Discord Bot",
    status="Active",
    harmony=0.355,
    verified=True
)

# Save context snapshot
await notion.save_context_snapshot(
    session_id="session-123",
    ai_system="Claude",
    summary="Completed Phase 6",
    key_decisions="Integrated Notion",
    next_steps="Deploy to Railway",
    full_context={"phase": 6}
)
```

### Integration in FastAPI

```python
from fastapi import FastAPI
from backend.services.notion_client import get_notion_client

app = FastAPI()

@app.on_event("startup")
async def startup():
    """Initialize Notion client on startup."""
    notion = await get_notion_client()
    if notion:
        print("✅ Notion client initialized")
    else:
        print("⚠ Notion client unavailable")

@app.post("/api/log-event")
async def log_event(event_data: dict):
    """Log event to Notion."""
    notion = await get_notion_client()
    if not notion:
        return {"error": "Notion unavailable"}
    
    page_id = await notion.log_event(**event_data)
    return {"notion_page_id": page_id}
```

---

## 📈 Monitoring & Verification

### Check Notion Connection

```bash
# Test Notion client
PYTHONPATH=. python -c "
import asyncio
from backend.services.notion_client import get_notion_client

async def test():
    notion = await get_notion_client()
    if notion:
        health = await notion.health_check()
        print('✅ Notion connection healthy' if health else '❌ Notion connection failed')

asyncio.run(test())
"
```

### View Zapier Logs

1. Go to [zapier.com](https://zapier.com)
2. Click "My Apps" → "Zaps"
3. Select your Zap
4. Click "View Logs" to see webhook calls and results

### View Notion Audit Trail

All Notion changes are tracked automatically:
1. Open any Notion database
2. Click "..." → "Database info"
3. Scroll to "Last edited by" to see change history

---

## 🚀 Deployment to Railway

When deploying to Railway, set these environment variables:

```bash
NOTION_API_KEY=secret_xxxxxxxxxxxxx
NOTION_SYSTEM_STATE_DB=009a946d04fb46aa83e4481be86f09ef
NOTION_AGENT_REGISTRY_DB=2f65aab794a64ec48bcc46bf760f128f
NOTION_EVENT_LOG_DB=acb01d4a955d4775aaeb2310d1da1102
NOTION_CONTEXT_DB=d704854868474666b4b774750f8b134a
```

---

## 🔐 Security Considerations

1. **API Key Protection:** Never commit `NOTION_API_KEY` to Git
2. **Database Permissions:** Restrict Notion integration to specific databases
3. **Audit Trail:** All Notion operations are logged and auditable
4. **Rate Limiting:** Notion API has rate limits; implement backoff if needed

---

## 📚 References

- [Notion API Documentation](https://developers.notion.com)
- [notion-client Python Library](https://github.com/ramnes/notion-sdk-py)
- [Zapier Notion Integration](https://zapier.com/apps/notion)

---

**🤲 Manus v14.5 - Notion Integration Complete**  
*Tat Tvam Asi* 🙏

