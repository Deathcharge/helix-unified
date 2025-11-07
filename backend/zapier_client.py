import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

import aiohttp

logger = logging.getLogger(__name__)


class ZapierClient:
    """Production-ready Zapier client for Helix Collective monitoring"""

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.master_hook_url = os.getenv("ZAPIER_MASTER_HOOK_URL")
        self.rate_limit = asyncio.Semaphore(5)  # Max 5 concurrent requests

    async def _send_webhook(self, payload: Dict[str, Any]) -> Optional[Dict]:
        """Send webhook with rate limiting and error handling"""
        if not self.master_hook_url:
            logger.warning("ZAPIER_MASTER_HOOK_URL not configured")
            return None

        async with self.rate_limit:
            try:
                # Add common metadata
                payload.update(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "helix_phase": os.getenv("HELIX_PHASE", "unknown"),
                        "helix_version": os.getenv("HELIX_VERSION", "unknown"),
                        "environment": os.getenv("RAILWAY_ENVIRONMENT", "local"),
                    }
                )

                async with self.session.post(
                    self.master_hook_url, json=payload, timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        logger.info(f"Zapier webhook sent: {payload.get('type', 'unknown')}")
                        return await resp.json()
                    else:
                        logger.error(f"Zapier webhook failed: {resp.status}")

            except Exception as e:
                logger.error(f"Zapier webhook error: {e}")

            return None

    # WEEK 1: Core Monitoring (FREE TIER)
    async def log_event(
        self, event_title: str, event_type: str, agent_name: str, description: str, ucf_snapshot: Optional[str] = None
    ) -> bool:
        """Path A: Log events to Notion Event Log"""
        payload = {
            "type": "event_log",
            "event_title": event_title,
            "event_type": event_type,
            "agent_name": agent_name,
            "description": description,
            "ucf_snapshot": ucf_snapshot or "{}",
            "discord_channel": self._get_relevant_channel(event_type),
        }
        result = await self._send_webhook(payload)
        return result is not None

    async def update_agent(self, agent_name: str, status: str, last_action: str, health_score: int) -> bool:
        """Path B: Update agent status in Notion Agent Registry"""
        payload = {
            "type": "agent_registry",
            "agent_name": agent_name,
            "status": status,
            "last_action": last_action,
            "health_score": health_score,
            "last_updated": datetime.now().isoformat(),
        }
        result = await self._send_webhook(payload)
        return result is not None

    async def update_system_state(
        self, component: str, status: str, harmony: float, error_log: str = "", verified: bool = True
    ) -> bool:
        """Path C: Update system state in Notion"""
        payload = {
            "type": "system_state",
            "component": component,
            "status": status,
            "harmony": str(harmony),
            "error_log": error_log,
            "verified": verified,
        }
        result = await self._send_webhook(payload)
        return result is not None

    # WEEK 2: Telemetry (ZAPIER PRO)
    async def log_telemetry(
        self, metric_name: str, value: float, component: str = "system", metadata: Optional[Dict] = None
    ) -> bool:
        """Path E: Send telemetry data to Google Sheets/Tables"""
        payload = {
            "type": "telemetry",
            "metric_name": metric_name,
            "value": value,
            "component": component,
            "harmony": self._get_current_harmony(),
            "metadata": json.dumps(metadata or {}),
            "guild_id": os.getenv("DISCORD_GUILD_ID"),
        }
        result = await self._send_webhook(payload)
        return result is not None

    # WEEK 3: Alert System (ZAPIER PRO)
    async def send_discord_notification(self, channel_name: str, message: str, priority: str = "normal") -> bool:
        """Path D: Send Discord alerts to Slack"""
        payload = {
            "type": "discord_notification",
            "channel_name": channel_name,
            "message": message,
            "priority": priority,
            "channel_id": self._get_channel_id(channel_name),
        }
        result = await self._send_webhook(payload)
        return result is not None

    async def send_error_alert(
        self, error_message: str, component: str, severity: str = "high", context: Optional[Dict] = None
    ) -> bool:
        """Path F: Send critical error alerts via Email + Slack"""
        payload = {
            "type": "error",
            "error_message": error_message,
            "component": component,
            "severity": severity,
            "context": json.dumps(context or {}),
            "stack_trace": "",  # Add if available
            "affected_channels": self._get_affected_channels(component),
        }
        result = await self._send_webhook(payload)
        return result is not None

    # WEEK 4: Advanced Automation (ZAPIER PRO)
    async def log_repository_action(
        self, repo_name: str, action: str, details: str, commit_hash: Optional[str] = None
    ) -> bool:
        """Path G: Repository management and GitHub integration"""
        payload = {
            "type": "repository",
            "repo_name": repo_name,
            "action": action,  # commit, backup, issue_created, etc.
            "details": details,
            "commit_hash": commit_hash,
            "mega_backup_status": os.getenv("MEGA_REMOTE_DIR", "unknown"),
            "archive_path": os.getenv("ARCHIVE_PATH", "/tmp"),
        }
        result = await self._send_webhook(payload)
        return result is not None

    # Helper methods
    def _get_current_harmony(self) -> str:
        """Get current UCF harmony level"""
        try:
            ucf_path = os.getenv("UCF_STATE_PATH")
            if ucf_path and os.path.exists(ucf_path):
                with open(ucf_path, "r") as f:
                    ucf_data = json.load(f)
                    return str(ucf_data.get("harmony", 0.5))
        except Exception:
            pass
        return "0.5"  # Default harmony

    def _get_channel_id(self, channel_name: str) -> str:
        """Get Discord channel ID from environment variables"""
        channel_map = {
            "manus-bridge": os.getenv("DISCORD_MANUS_BRIDGE_CHANNEL_ID"),
            "ritual-engine": os.getenv("DISCORD_RITUAL_ENGINE_CHANNEL_ID"),
            "telemetry": os.getenv("DISCORD_TELEMETRY_CHANNEL_ID"),
            "status": os.getenv("DISCORD_STATUS_CHANNEL_ID"),
            "backup": os.getenv("DISCORD_BACKUP_CHANNEL_ID"),
            "deployments": os.getenv("DISCORD_DEPLOYMENTS_CHANNEL_ID"),
        }
        return channel_map.get(channel_name, os.getenv("DISCORD_STATUS_CHANNEL_ID", ""))

    def _get_relevant_channel(self, event_type: str) -> str:
        """Get relevant Discord channel for event type"""
        if "ritual" in event_type.lower():
            return "ritual-engine"
        elif "agent" in event_type.lower():
            return "manus-bridge"
        elif "error" in event_type.lower():
            return "status"
        else:
            return "telemetry"

    def _get_affected_channels(self, component: str) -> list:
        """Get list of channels affected by component errors"""
        channel_mappings = {
            "discord_bot": ["manus-bridge", "status"],
            "z88_engine": ["ritual-engine", "status"],
            "mega_sync": ["backup", "status"],
            "agents": ["manus-bridge", "telemetry"],
        }
        return channel_mappings.get(component, ["status"])


# Convenience functions for easy integration


async def quick_log_event(title: str, agent: str = "System", description: str = ""):
    """Quick event logging without session management"""
    async with aiohttp.ClientSession() as session:
        zap = ZapierClient(session)
        await zap.log_event(title, "Status", agent, description)


async def quick_error_alert(error: str, component: str = "System"):
    """Quick error alert without session management"""
    async with aiohttp.ClientSession() as session:
        zap = ZapierClient(session)
        await zap.send_error_alert(error, component, "high")
