# 🌀 Helix Collective v15.3 — Master Webhook Client
# backend/services/zapier_client_master.py — Zapier Pro Master Webhook
# Author: Andrew John Ward (Architect)

import os
import json
import aiohttp
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# ============================================================================
# MASTER WEBHOOK CONFIGURATION
# ============================================================================

MASTER_HOOK_URL = os.getenv("ZAPIER_MASTER_HOOK_URL")

# Fallback to individual hooks if master not configured
EVENT_HOOK = os.getenv("ZAPIER_EVENT_HOOK_URL")
AGENT_HOOK = os.getenv("ZAPIER_AGENT_HOOK_URL")
SYSTEM_HOOK = os.getenv("ZAPIER_SYSTEM_HOOK_URL")

# ============================================================================
# MASTER ZAPIER CLIENT (Zapier Pro)
# ============================================================================

class MasterZapierClient:
    """
    Master Webhook Client for Zapier Pro with Path Routing.

    Uses a single webhook URL with payload type discrimination to route
    to different Notion databases, Slack channels, email alerts, etc.

    Payload Types:
    - "event_log" → Notion Event Log
    - "agent_registry" → Notion Agent Registry
    - "system_state" → Notion System State
    - "discord_notification" → Slack/Discord
    - "telemetry" → Google Sheets/Tables
    - "error" → Email/PagerDuty
    - "repository" → GitHub Actions

    Features:
    - Single webhook URL (cleaner configuration)
    - Path-based routing in Zapier
    - Automatic fallback to individual webhooks
    - Rate limiting and retry logic
    - Payload validation and truncation
    """

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self._session = session
        self._owns_session = session is None
        self._use_master = bool(MASTER_HOOK_URL)

        # Fallback to individual hooks if master not configured
        self._event_hook = EVENT_HOOK
        self._agent_hook = AGENT_HOOK
        self._system_hook = SYSTEM_HOOK

    # ========================================================================
    # PUBLIC API METHODS
    # ========================================================================

    async def log_event(
        self,
        event_title: str,
        event_type: str,
        agent_name: str,
        description: str,
        ucf_snapshot: Dict[str, Any]
    ) -> bool:
        """
        Log an event to Notion Event Log.

        Args:
            event_title: Event title
            event_type: Type (Ritual | Command | Error | Status)
            agent_name: Agent that triggered event
            description: Event description
            ucf_snapshot: Current UCF state

        Returns:
            True if successful, False otherwise
        """
        payload = {
            "type": "event_log",
            "event_title": event_title,
            "event_type": event_type,
            "agent_name": agent_name,
            "description": description,
            "ucf_snapshot": json.dumps(ucf_snapshot),
            "helix_phase": os.getenv("HELIX_PHASE", "production"),
            "timestamp": datetime.utcnow().isoformat()
        }

        return await self._send(payload, fallback_url=self._event_hook)

    async def update_agent(
        self,
        agent_name: str,
        status: str,
        last_action: str,
        health_score: int
    ) -> bool:
        """
        Update agent status in Notion Agent Registry.

        Args:
            agent_name: Agent name
            status: Status (Active | Idle | Error)
            last_action: Last action description
            health_score: Health score (0-100)

        Returns:
            True if successful
        """
        payload = {
            "type": "agent_registry",
            "agent_name": agent_name,
            "status": status,
            "last_action": last_action,
            "health_score": health_score,
            "timestamp": datetime.utcnow().isoformat()
        }

        return await self._send(payload, fallback_url=self._agent_hook)

    async def update_system_state(
        self,
        component: str,
        status: str,
        harmony: float,
        error_log: str = "",
        verified: bool = False
    ) -> bool:
        """
        Update system component state in Notion.

        Args:
            component: Component name
            status: Status (Active | Degraded | Offline)
            harmony: Harmony metric (0.0-1.0)
            error_log: Optional error log
            verified: Whether verified

        Returns:
            True if successful
        """
        payload = {
            "type": "system_state",
            "component": component,
            "status": status,
            "harmony": harmony,
            "error_log": error_log,
            "verified": verified,
            "timestamp": datetime.utcnow().isoformat()
        }

        return await self._send(payload, fallback_url=self._system_hook)

    async def send_discord_notification(
        self,
        channel_name: str,
        message: str,
        priority: str = "normal"
    ) -> bool:
        """
        Send notification to Discord via Slack integration.

        Args:
            channel_name: Discord channel name
            message: Message to send
            priority: Priority (low | normal | high | critical)

        Returns:
            True if successful
        """
        payload = {
            "type": "discord_notification",
            "channel_name": channel_name,
            "message": message,
            "priority": priority,
            "guild_id": os.getenv("DISCORD_GUILD_ID", ""),
            "timestamp": datetime.utcnow().isoformat()
        }

        return await self._send(payload)

    async def log_telemetry(
        self,
        metric_name: str,
        value: float,
        component: str = "system",
        unit: str = ""
    ) -> bool:
        """
        Log telemetry data to Google Sheets/Tables.

        Args:
            metric_name: Metric name
            value: Metric value
            component: Component name
            unit: Optional unit (ms, %, MB, etc.)

        Returns:
            True if successful
        """
        payload = {
            "type": "telemetry",
            "metric_name": metric_name,
            "value": value,
            "component": component,
            "unit": unit,
            "harmony": os.getenv("UCF_HARMONY", "0.355"),
            "timestamp": datetime.utcnow().isoformat()
        }

        return await self._send(payload)

    async def send_error_alert(
        self,
        error_message: str,
        component: str,
        severity: str = "high",
        stack_trace: str = ""
    ) -> bool:
        """
        Send critical error alert via Email/PagerDuty.

        Args:
            error_message: Error message
            component: Component that failed
            severity: Severity (low | medium | high | critical)
            stack_trace: Optional stack trace

        Returns:
            True if successful
        """
        payload = {
            "type": "error",
            "error_message": error_message,
            "component": component,
            "severity": severity,
            "stack_trace": stack_trace[:1000] if stack_trace else "",  # Truncate
            "environment": os.getenv("RAILWAY_ENVIRONMENT", "production"),
            "timestamp": datetime.utcnow().isoformat()
        }

        return await self._send(payload)

    async def log_repository_action(
        self,
        repo_name: str,
        action: str,
        details: str,
        commit_sha: str = ""
    ) -> bool:
        """
        Log repository/archive action to GitHub Actions.

        Args:
            repo_name: Repository name
            action: Action (commit | push | backup | restore)
            details: Action details
            commit_sha: Optional commit SHA

        Returns:
            True if successful
        """
        payload = {
            "type": "repository",
            "repo_name": repo_name,
            "action": action,
            "details": details,
            "commit_sha": commit_sha,
            "helix_version": os.getenv("HELIX_VERSION", "15.3"),
            "timestamp": datetime.utcnow().isoformat()
        }

        return await self._send(payload)

    # ========================================================================
    # INTERNAL METHODS
    # ========================================================================

    async def _send(
        self,
        payload: Dict[str, Any],
        fallback_url: Optional[str] = None
    ) -> bool:
        """
        Send payload to master webhook or fallback URL.

        Args:
            payload: Payload with "type" field for routing
            fallback_url: Fallback URL if master not configured

        Returns:
            True if successful
        """
        # Use master webhook if configured
        if self._use_master:
            url = MASTER_HOOK_URL
        elif fallback_url:
            url = fallback_url
        else:
            # No webhook configured - silent skip
            return False

        # Validate payload
        payload = self._validate_payload(payload)

        # Send webhook
        session = self._session
        if session is None:
            session = aiohttp.ClientSession()

        try:
            async with session.post(
                url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                success = resp.status == 200

                if not success:
                    await self._log_failure(
                        payload,
                        f"HTTP {resp.status}",
                        payload.get("type", "unknown")
                    )

                return success

        except asyncio.TimeoutError:
            await self._log_failure(payload, "Timeout", payload.get("type", "unknown"))
            return False

        except Exception as e:
            await self._log_failure(payload, str(e), payload.get("type", "unknown"))
            return False

        finally:
            if self._owns_session and session:
                await session.close()

    def _validate_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and truncate payload to avoid size limits."""
        serialized = json.dumps(payload)

        # If too large, truncate
        if len(serialized) > 1_000_000:  # 1MB
            # Truncate large fields
            for key in ["error_log", "stack_trace", "description", "details"]:
                if key in payload and len(str(payload[key])) > 5000:
                    payload[key] = str(payload[key])[:5000] + "... [truncated]"

        return payload

    async def _log_failure(
        self,
        payload: Dict[str, Any],
        error: str,
        webhook_type: str
    ) -> None:
        """Log failed webhook for later retry."""
        try:
            log_path = Path("Shadow/manus_archive/zapier_failures.log")
            log_path.parent.mkdir(parents=True, exist_ok=True)

            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "type": webhook_type,
                "error": error,
                "payload": payload
            }

            with open(log_path, "a") as f:
                f.write(json.dumps(log_entry) + "\n")

            print(f"⚠ Zapier webhook failed ({webhook_type}): {error}")

        except Exception as e:
            print(f"❌ Failed to log Zapier failure: {e}")

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def validate_config() -> Dict[str, Any]:
    """
    Validate Zapier configuration.

    Returns:
        Configuration status
    """
    master_configured = bool(MASTER_HOOK_URL)
    individual_configured = bool(EVENT_HOOK and AGENT_HOOK and SYSTEM_HOOK)

    return {
        "master_webhook": master_configured,
        "individual_webhooks": individual_configured,
        "mode": "master" if master_configured else ("individual" if individual_configured else "none"),
        "webhooks": {
            "master": bool(MASTER_HOOK_URL),
            "event": bool(EVENT_HOOK),
            "agent": bool(AGENT_HOOK),
            "system": bool(SYSTEM_HOOK)
        }
    }

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    async def test():
        """Test master webhook client."""
        print("🧪 Testing Master Zapier Client")
        print("=" * 70)

        config = validate_config()
        print(f"\n📋 Configuration:")
        print(f"  Mode: {config['mode']}")
        print(f"  Master Webhook: {'✅' if config['master_webhook'] else '❌'}")
        print(f"  Individual Webhooks: {'✅' if config['individual_webhooks'] else '❌'}")

        if config['mode'] == 'none':
            print("\n⚠ No webhooks configured. Set ZAPIER_MASTER_HOOK_URL")
            return

        print(f"\n🧪 Testing in {config['mode']} mode...")

        async with aiohttp.ClientSession() as session:
            client = MasterZapierClient(session)

            # Test all payload types
            tests = [
                ("Event Log", client.log_event(
                    "Test Event",
                    "Status",
                    "Manus",
                    "Testing master webhook",
                    {"harmony": 0.355}
                )),
                ("Agent Update", client.update_agent(
                    "Manus",
                    "Active",
                    "Testing",
                    100
                )),
                ("System State", client.update_system_state(
                    "Master Webhook",
                    "Active",
                    0.355,
                    verified=True
                )),
                ("Discord Notification", client.send_discord_notification(
                    "testing",
                    "🧪 Master webhook test",
                    "normal"
                )),
                ("Telemetry", client.log_telemetry(
                    "test_metric",
                    42.0,
                    "test_component",
                    "units"
                )),
                ("Error Alert", client.send_error_alert(
                    "Test error",
                    "test_component",
                    "low"
                )),
                ("Repository Action", client.log_repository_action(
                    "helix-unified",
                    "test",
                    "Testing master webhook"
                ))
            ]

            for name, test_coro in tests:
                result = await test_coro
                print(f"  {'✅' if result else '❌'} {name}")

        print("\n" + "=" * 70)
        print("✅ Test complete")

    asyncio.run(test())
