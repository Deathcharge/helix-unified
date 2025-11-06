# 🌀 Helix Collective v16.7 — Zapier Integration
# backend/zapier_integration.py — Webhook Integration for UCF Telemetry & Notifications
# Author: Andrew John Ward (Architect)

import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class HelixZapierIntegration:
    """
    Integration class for sending Helix Collective data to Zapier webhooks.

    Supports:
    - UCF telemetry streaming
    - Agent registry updates
    - System state notifications
    - Discord event forwarding

    Usage:
        async with HelixZapierIntegration(webhook_url) as zapier:
            await zapier.send_telemetry(ucf_metrics, system_info)
    """

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.enabled = bool(webhook_url)

        if not self.enabled:
            logger.warning("⚠️ Zapier webhook URL not configured - integration disabled")
        else:
            logger.info(f"✅ Zapier integration initialized: {webhook_url[:50]}...")

    async def __aenter__(self):
        """Async context manager entry - creates aiohttp session."""
        if self.enabled:
            self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - closes aiohttp session."""
        if self.session:
            await self.session.close()

    async def send_telemetry(self, ucf_metrics: Dict[str, float], system_info: Dict[str, Any]) -> bool:
        """
        Send UCF telemetry data to Zapier webhook.

        Args:
            ucf_metrics: Dictionary with harmony, resilience, prana, drishti, klesha, zoom
            system_info: Dictionary with agents_count, timestamp, agents list, etc.

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.session:
            return False

        payload = {
            "type": "telemetry",
            "ucf": {
                "harmony": ucf_metrics.get("harmony", 0.0),
                "resilience": ucf_metrics.get("resilience", 0.0),
                "prana": ucf_metrics.get("prana", 0.0),
                "drishti": ucf_metrics.get("drishti", 0.0),
                "klesha": ucf_metrics.get("klesha", 0.0),
                "zoom": ucf_metrics.get("zoom", 0.0)
            },
            "system": {
                "version": system_info.get("version", "16.7"),
                "agents_active": system_info.get("agents_count", 14),
                "timestamp": system_info.get("timestamp", datetime.utcnow().isoformat()),
                "codename": system_info.get("codename", "Documentation Consolidation & Real-Time Streaming")
            },
            "agents": system_info.get("agents", [])
        }

        try:
            async with self.session.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    logger.debug(f"📊 Zapier telemetry sent successfully")
                    return True
                else:
                    logger.warning(f"⚠️ Zapier webhook returned {response.status}")
                    return False
        except asyncio.TimeoutError:
            logger.warning("⚠️ Zapier webhook timeout (10s)")
            return False
        except Exception as e:
            logger.error(f"❌ Zapier webhook failed: {e}")
            return False

    async def send_agent_update(self, agent_name: str, status: str, data: Dict[str, Any]) -> bool:
        """
        Send agent registry updates to Zapier.

        Args:
            agent_name: Name of the agent (e.g., "Kael", "Lumina")
            status: Status string (e.g., "active", "idle", "error")
            data: Additional agent data (symbol, role, etc.)

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.session:
            return False

        payload = {
            "type": "agent_registry",
            "agent": {
                "name": agent_name,
                "status": status,
                "symbol": data.get("symbol", "🔮"),
                "role": data.get("role", "Unknown"),
                "data": data
            },
            "system_version": "16.7",
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            async with self.session.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    logger.debug(f"🤖 Agent update sent: {agent_name}")
                    return True
                else:
                    logger.warning(f"⚠️ Zapier agent update returned {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Zapier agent update failed: {e}")
            return False

    async def send_system_state(self, state: Dict[str, Any]) -> bool:
        """
        Send system state updates to Zapier.

        Args:
            state: System state dictionary

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.session:
            return False

        payload = {
            "type": "system_state",
            "state": state,
            "timestamp": state.get("timestamp", datetime.utcnow().isoformat()),
            "version": "16.7"
        }

        try:
            async with self.session.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    logger.debug(f"📡 System state sent successfully")
                    return True
                else:
                    logger.warning(f"⚠️ Zapier system state returned {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Zapier system state failed: {e}")
            return False

    async def send_discord_notification(self, message_type: str, data: Dict[str, Any]) -> bool:
        """
        Send Discord events to Zapier.

        Args:
            message_type: Type of Discord message (e.g., "command", "error", "alert")
            data: Event data dictionary

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.session:
            return False

        payload = {
            "type": "discord_notification",
            "message_type": message_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "system_version": "16.7"
        }

        try:
            async with self.session.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    logger.debug(f"💬 Discord notification sent: {message_type}")
                    return True
                else:
                    logger.warning(f"⚠️ Zapier Discord notification returned {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Zapier Discord notification failed: {e}")
            return False

    async def send_ritual_update(self, ritual_data: Dict[str, Any]) -> bool:
        """
        Send Z-88 ritual updates to Zapier.

        Args:
            ritual_data: Ritual cycle data (step, ucf_changes, etc.)

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.session:
            return False

        payload = {
            "type": "ritual_update",
            "ritual": ritual_data,
            "timestamp": datetime.utcnow().isoformat(),
            "system_version": "16.7"
        }

        try:
            async with self.session.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    logger.debug(f"🔮 Ritual update sent: step {ritual_data.get('step', '?')}")
                    return True
                else:
                    logger.warning(f"⚠️ Zapier ritual update returned {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Zapier ritual update failed: {e}")
            return False


# Global singleton instance (initialized in backend/main.py)
_zapier_instance: Optional[HelixZapierIntegration] = None


def get_zapier() -> Optional[HelixZapierIntegration]:
    """Get the global Zapier integration instance."""
    return _zapier_instance


def set_zapier(instance: HelixZapierIntegration):
    """Set the global Zapier integration instance."""
    global _zapier_instance
    _zapier_instance = instance
