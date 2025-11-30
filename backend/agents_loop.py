# 🌀 Helix Collective v14.5 — Quantum Handshake
# agents_loop.py — Main Manus operational loop (FINAL PATCHED)
# Author: Andrew John Ward (Architect)

import asyncio
import datetime
import json
import os
from pathlib import Path

from agents import Manus
from backend.config_manager import config

from backend.enhanced_kavach import EnhancedKavach

# ============================================================================
# PATH DEFINITIONS
# ============================================================================
ARCHIVE_PATH = Path(config.get("general", "SHADOW_DIR", default="Shadow/manus_archive/"))
COMMANDS_PATH = Path(config.get("general", "STATE_DIR", default="Helix/state")) / "commands/manus_directives.json"
STATE_PATH = Path(config.get("general", "STATE_DIR", default="Helix/state")) / "ucf_state.json"
RITUAL_LOCK = Path(config.get("general", "STATE_DIR", default="Helix/state")) / ".ritual_lock"

# Ensure directories exist
for p in [ARCHIVE_PATH, COMMANDS_PATH.parent, STATE_PATH.parent]:
    p.mkdir(parents=True, exist_ok=True)

# ============================================================================
# HEARTBEAT HELPER
# ============================================================================


def update_heartbeat(status="active", harmony=0.355):
    """Update heartbeat.json with current status."""
    heartbeat_path = Path(config.get("general", "STATE_DIR", default="Helix/state")) / "heartbeat.json"
    data = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "alive": True,
        "status": status,
        "ucf_state": {"harmony": harmony},
    }
    json.dump(data, open(heartbeat_path, "w"), indent=2)


# ============================================================================
# LOGGING
# ============================================================================


async def log_event(message: str):
    """Log loop events with timestamp."""
    now = datetime.datetime.utcnow().isoformat()
    record = {"time": now, "event": message}
    log_file = ARCHIVE_PATH / "agents_loop.log"
    try:
        data = json.load(open(log_file)) if log_file.exists() else []
    except Exception:
        data = []
    data.append(record)
    json.dump(data, open(log_file, "w"), indent=2)
    print(message)


# ============================================================================
# UCF STATE HELPERS
# ============================================================================


async def load_ucf_state():
    """Load UCF state, creating default if missing."""
    if not STATE_PATH.exists():
        base = {
            "zoom": 1.0228,
            "harmony": 0.355,
            "resilience": 1.1191,
            "prana": 0.5175,
            "drishti": 0.5023,
            "klesha": 0.010,
        }
        json.dump(base, open(STATE_PATH, "w"), indent=2)
    return json.load(open(STATE_PATH))


async def save_ucf_state(state):
    """Save UCF state to disk."""
    json.dump(state, open(STATE_PATH, "w"), indent=2)


# ============================================================================
# DIRECTIVE PROCESSING
# ============================================================================


async def process_directives(manus, kavach):
    """Check for directives from Vega or Architect."""
    if not COMMANDS_PATH.exists():
        return

    try:
        directive = json.load(open(COMMANDS_PATH))
        # Kavach scan before execution
        if "command" in directive:
            scan_result = await kavach.scan(directive["command"])
            if not scan_result.get("approved"):
                await log_event(f"🛡 Kavach blocked: {directive['command']}")
                os.remove(COMMANDS_PATH)
                return
        await manus.planner(directive)
        os.remove(COMMANDS_PATH)
        await log_event(f"✅ Processed directive: {directive}")
    except Exception as e:
        await log_event(f"⚠ Directive processing error: {e}")


# ============================================================================
# HEALTH MONITORING
# ============================================================================

async def monitor_collective_health(manus):
    """Monitors the health of all active agents and triggers Zapier alerts."""
    from backend.zapier_client import ZapierClient
    from backend.config_manager import config

    # Check if Zapier health alerting is enabled
    webhook_url = config.get("zapier", "HEALTH_ALERT_WEBHOOK", default=None)
    if not webhook_url:
        await log_event("Health monitoring skipped: ZAPIER_HEALTH_ALERT_WEBHOOK not configured.")
        return

    health_statuses = []
    critical_agents = []

    for agent in manus.agents:
        try:
            status = await agent.get_health_status()
            health_statuses.append(status)
            if status.get("status") == "CRITICAL":
                critical_agents.append(status)
        except NotImplementedError:
            # Agent has not implemented the health check yet
            health_statuses.append({
                "agent_name": agent.name,
                "status": "WARNING",
                "message": "Health check not implemented.",
                "last_check_time": datetime.datetime.utcnow().isoformat()
            })
        except Exception as e:
            # Agent failed to report health
            health_statuses.append({
                "agent_name": agent.name,
                "status": "CRITICAL",
                "message": f"Health check failed with exception: {e}",
                "last_check_time": datetime.datetime.utcnow().isoformat()
            })

    # Send alert if critical agents are found
    if critical_agents:
        await log_event(f"🚨 CRITICAL ALERT: {len(critical_agents)} agents are CRITICAL. Sending Zapier alert.")
        zapier_client = ZapierClient()
        # The Zapier tool is configured to receive a list of health statuses
        await zapier_client.send_health_alert(health_statuses)

    # Log overall status
    healthy_count = sum(1 for s in health_statuses if s.get("status") == "HEALTHY")
    await log_event(f"🩺 Collective Health: {healthy_count}/{len(manus.agents)} agents HEALTHY.")

# ============================================================================
# MAIN LOOP
# ============================================================================


async def main_loop():
    """Main Manus operational loop."""
    kavach = EnhancedKavach()
    manus = Manus(kavach)
    await log_event("🤲 Manus loop initiated (v14.5 patched)")
    while True:
        try:
            # Pause loop if ritual in progress
            if RITUAL_LOCK.exists():
                await log_event("⏸ Pausing loop — ritual in progress")
                await asyncio.sleep(5)
                continue
            # Process directives
            await process_directives(manus, kavach)
            # Update UCF state
            ucf = await load_ucf_state()
            # Conservative harmony growth (0.0001 per cycle)
            ucf["harmony"] = min(1.0, ucf["harmony"] + 0.0001)
            await save_ucf_state(ucf)
            # Update heartbeat
            update_heartbeat(status="active", harmony=ucf["harmony"])

            # Run health monitor (every 60 seconds)
            if (datetime.datetime.utcnow().second % 60) < 30:  # Simple way to run less frequently
                await monitor_collective_health(manus)

        except Exception as e:
            await log_event(f"Error in Manus loop: {e}")
        await asyncio.sleep(30)


# ============================================================================
# ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("🛑 Manus loop stopped manually.")
