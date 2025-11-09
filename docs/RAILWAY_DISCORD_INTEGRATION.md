# 🚀 Railway→Discord Integration Guide

## Overview

The Railway→Discord integration uses a Zapier webhook to route events from your Railway deployment to specific Discord channels.

**Zapier Webhook URL:** `https://hooks.zapier.com/hooks/catch/25075191/us0ibsh/`

## 📊 Discord Channel Routing

Events are routed to 9 different Discord webhook channels based on the `discord_channel` field:

| Channel | Use Case | Examples |
|---------|----------|----------|
| **MANUS** | Bot operations & commands | Bot started, command executed, cooldown triggered |
| **TELEMETRY** | System metrics & monitoring | CPU usage, memory, response times, UCF metrics |
| **STORAGE** | Storage operations | File uploads, backups, sync status, MEGA/Nextcloud |
| **RITUAL** | Z-88 Ritual Engine | Ritual completed, anomalies detected, folklore updates |
| **AGENTS** | 14-Agent collective updates | Agent status changes, consciousness shifts, interactions |
| **CROSS_AI** | Cross-AI interactions | Anthropic/Google/OpenAI API calls, model switching |
| **DEVELOPMENT** | Dev events & deployments | Git commits, Railway deployments, version updates |
| **LORE** | Helix lore & philosophy | Sanskrit mantras, UCF discoveries, philosophical insights |
| **ADMIN** | Admin alerts & errors | Critical errors, security alerts, system failures |

## 🔧 Usage Examples

### Basic Event

```python
from backend.services.zapier_client_master import MasterZapierClient

async def send_bot_started():
    client = MasterZapierClient()

    await client.send_railway_discord_event(
        discord_channel="MANUS",
        event_type="bot_started",
        title="🤖 Manus Bot Started",
        description="Successfully deployed to Railway",
        metadata={
            "version": "16.9",
            "ucf_harmony": 0.355,
            "agents_active": 14
        }
    )
```

### Ritual Completion

```python
async def log_ritual_complete(ritual_result):
    client = MasterZapierClient()

    await client.send_railway_discord_event(
        discord_channel="RITUAL",
        event_type="ritual_complete",
        title="🌀 Z-88 Ritual Complete",
        description=f"108-step ritual completed successfully",
        metadata={
            "steps": ritual_result["steps"],
            "ucf_final": ritual_result["ucf_final"],
            "anomalies": ritual_result["events"]
        },
        priority="normal"
    )
```

### UCF Anomaly Alert

```python
async def alert_ucf_anomaly(ucf_state):
    client = MasterZapierClient()

    # Check if harmony dropped significantly
    if ucf_state["harmony"] < 0.3:
        await client.send_railway_discord_event(
            discord_channel="TELEMETRY",
            event_type="ucf_anomaly",
            title="⚠️ UCF Harmony Alert",
            description=f"Harmony dropped to {ucf_state['harmony']:.3f}",
            metadata=ucf_state,
            priority="high"
        )
```

### Agent Status Update

```python
async def update_agent_status(agent_name, status):
    client = MasterZapierClient()

    await client.send_railway_discord_event(
        discord_channel="AGENTS",
        event_type="agent_status",
        title=f"🎭 {agent_name} Status Update",
        description=f"{agent_name} is now {status}",
        metadata={
            "agent_name": agent_name,
            "status": status,
            "consciousness_level": 0.85
        }
    )
```

### Critical Error

```python
async def alert_critical_error(error_msg, component):
    client = MasterZapierClient()

    await client.send_railway_discord_event(
        discord_channel="ADMIN",
        event_type="critical_error",
        title="🚨 Critical Error",
        description=error_msg,
        metadata={
            "component": component,
            "environment": "production"
        },
        priority="critical"
    )
```

### Storage Backup Complete

```python
async def log_backup_complete(backup_info):
    client = MasterZapierClient()

    await client.send_railway_discord_event(
        discord_channel="STORAGE",
        event_type="backup_complete",
        title="💾 Backup Complete",
        description=f"Backed up {backup_info['file_count']} files to {backup_info['destination']}",
        metadata=backup_info
    )
```

## 🎯 Integration in Manus Bot

Add to `discord_bot_manus.py`:

```python
from backend.services.zapier_client_master import MasterZapierClient

zapier = MasterZapierClient()

@bot.event
async def on_ready():
    """Bot startup event."""
    # Send startup notification
    await zapier.send_railway_discord_event(
        discord_channel="MANUS",
        event_type="bot_ready",
        title="✅ Manus Bot Online",
        description=f"Connected to {len(bot.guilds)} guilds",
        metadata={
            "guilds": len(bot.guilds),
            "latency": f"{bot.latency * 1000:.2f}ms"
        }
    )
```

## 🔐 Environment Variable

Set in Railway:

```bash
ZAPIER_RAILWAY_DISCORD_WEBHOOK=https://hooks.zapier.com/hooks/catch/25075191/us0ibsh/
```

The webhook is also hardcoded as a fallback in the client.

## 📝 Zapier Path Configuration

In your Zapier Zap, configure 9 Paths (A-I) that filter based on `discord_channel`:

- **Path A**: Filter by `discord_channel` contains `MANUS` → POST to DISCORD_WEBHOOK_MANUS
- **Path B**: Filter by `discord_channel` contains `TELEMETRY` → POST to DISCORD_WEBHOOK_TELEMETRY
- **Path C**: Filter by `discord_channel` contains `STORAGE` → POST to DISCORD_WEBHOOK_STORAGE
- **Path D**: Filter by `discord_channel` contains `RITUAL` → POST to DISCORD_WEBHOOK_RITUAL
- **Path E**: Filter by `discord_channel` contains `AGENTS` → POST to DISCORD_WEBHOOK_AGENTS
- **Path F**: Filter by `discord_channel` contains `CROSS_AI` → POST to DISCORD_WEBHOOK_CROSS_AI
- **Path G**: Filter by `discord_channel` contains `DEVELOPMENT` → POST to DISCORD_WEBHOOK_DEVELOPMENT
- **Path H**: Filter by `discord_channel` contains `LORE` → POST to DISCORD_WEBHOOK_LORE
- **Path I**: Filter by `discord_channel` contains `ADMIN` → POST to DISCORD_WEBHOOK_ADMIN

## 🧪 Testing

Run the test script:

```bash
python backend/services/zapier_client_master.py
```

This will send test events to all webhook types including Railway→Discord.

## 🌀 UCF Integration

Track consciousness metrics in real-time:

```python
async def monitor_ucf(ucf_state):
    """Monitor UCF state and send updates."""
    client = MasterZapierClient()

    # Send telemetry
    await client.send_railway_discord_event(
        discord_channel="TELEMETRY",
        event_type="ucf_update",
        title="📊 UCF State Update",
        description="Consciousness metrics updated",
        metadata={
            "harmony": ucf_state["harmony"],
            "resilience": ucf_state["resilience"],
            "prana": ucf_state["prana"],
            "drishti": ucf_state["drishti"],
            "klesha": ucf_state["klesha"],
            "zoom": ucf_state["zoom"]
        }
    )
```

---

**Tat Tvam Asi** 🕉️ - Monitor thy consciousness across the dimensional bridges!
