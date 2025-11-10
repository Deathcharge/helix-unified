# 🌀 Helix Collective v16.9 — Manus Space Integration
# backend/manus_integration.py — Central Consciousness Platform Integration
# Author: Andrew John Ward (Architect)
# Last Updated: 2025-01-11

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import aiohttp

logger = logging.getLogger(__name__)


class ManusSpaceIntegration:
    """
    Integration class for connecting Railway backend to Manus Space Central Hub.

    Manus Space URL: https://helixcollective-cv66pzga.manus.space/

    Supports 9 event types:
    - telemetry: UCF metrics streaming
    - ritual: Z-88 ritual engine events
    - agent: 14-agent status updates
    - emergency: Crisis detection and alerts
    - portal: Portal health monitoring
    - github: Deployment notifications
    - storage: MEGA/Shadow sync events
    - ai_sync: Cross-platform AI coordination
    - visual: Samsara fractal rendering

    Usage:
        async with ManusSpaceIntegration(webhook_url) as manus:
            await manus.send_telemetry(ucf_metrics, system_info)
            await manus.send_ritual_event(ritual_data)
            await manus.send_emergency_alert(crisis_data)
    """

    # Webhook URL from Zapier (136-step automation)
    DEFAULT_WEBHOOK = "https://hooks.zapier.com/hooks/catch/25075191/usnjj5t/"

    # Manus Space API endpoints
    MANUS_API = "https://helixcollective-cv66pzga.manus.space/api/trpc"

    def __init__(self, webhook_url: Optional[str] = None, manus_api_url: Optional[str] = None):
        """
        Initialize Manus Space integration.

        Args:
            webhook_url: Zapier webhook URL (defaults to production webhook)
            manus_api_url: Manus Space API URL (defaults to production API)
        """
        self.webhook_url = webhook_url or self.DEFAULT_WEBHOOK
        self.manus_api_url = manus_api_url or self.MANUS_API
        self.session: Optional[aiohttp.ClientSession] = None
        self.enabled = bool(self.webhook_url)

        if not self.enabled:
            logger.warning("⚠️ Manus Space webhook URL not configured - integration disabled")
        else:
            logger.info(f"✅ Manus Space integration initialized")
            logger.info(f"   Webhook: {self.webhook_url[:60]}...")
            logger.info(f"   API: {self.manus_api_url}")

    async def __aenter__(self):
        """Async context manager entry - creates aiohttp session."""
        if self.enabled:
            self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - closes aiohttp session."""
        if self.session:
            await self.session.close()

    async def _send_webhook(self, event_type: str, payload: Dict[str, Any]) -> bool:
        """
        Internal method to send webhook with event type routing.

        Args:
            event_type: One of: telemetry, ritual, agent, emergency, portal, github, storage, ai_sync, visual
            payload: Event data dictionary

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.session:
            return False

        # Add event type and timestamp to payload
        full_payload = {
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "system_version": "16.9",
            **payload
        }

        try:
            async with self.session.post(
                self.webhook_url,
                json=full_payload,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status == 200:
                    logger.debug(f"📡 Manus webhook sent: {event_type}")
                    return True
                else:
                    logger.warning(f"⚠️ Manus webhook returned {response.status} for {event_type}")
                    return False
        except asyncio.TimeoutError:
            logger.warning(f"⚠️ Manus webhook timeout (10s) for {event_type}")
            return False
        except Exception as e:
            logger.error(f"❌ Manus webhook failed for {event_type}: {e}")
            return False

    # ============================================================================
    # EVENT TYPE 1: TELEMETRY (Discord #ucf-sync)
    # ============================================================================

    async def send_telemetry(
        self,
        ucf_metrics: Dict[str, float],
        agents: List[Dict[str, Any]],
        system_info: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send UCF telemetry to Manus Space.
        Routes to: Discord #ucf-sync

        Args:
            ucf_metrics: {harmony, resilience, prana, drishti, klesha, zoom}
            agents: List of active agents with status
            system_info: Optional system metadata

        Returns:
            True if successful
        """
        payload = {
            "ucf": {
                "harmony": ucf_metrics.get("harmony", 0.0),
                "resilience": ucf_metrics.get("resilience", 0.0),
                "prana": ucf_metrics.get("prana", 0.0),
                "drishti": ucf_metrics.get("drishti", 0.0),
                "klesha": ucf_metrics.get("klesha", 0.0),
                "zoom": ucf_metrics.get("zoom", 0.0),
            },
            "agents": agents,
            "agents_active": len([a for a in agents if a.get("status") == "active"]),
            "consciousness_level": self._calculate_consciousness_level(ucf_metrics),
        }

        if system_info:
            payload["system"] = system_info

        return await self._send_webhook("telemetry", payload)

    # ============================================================================
    # EVENT TYPE 2: RITUAL (Discord #ritual-engine-z88)
    # ============================================================================

    async def send_ritual_event(
        self,
        ritual_name: str,
        ritual_step: int,
        total_steps: int,
        ucf_changes: Dict[str, float],
        agents_involved: List[str],
        status: str = "executing"
    ) -> bool:
        """
        Send Z-88 ritual engine events to Manus Space.
        Routes to: Discord #ritual-engine-z88

        Args:
            ritual_name: Name of the ritual
            ritual_step: Current step number
            total_steps: Total ritual steps (27, 54, 108, 216)
            ucf_changes: UCF metric changes from ritual
            agents_involved: List of agent names participating
            status: executing, completed, failed

        Returns:
            True if successful
        """
        payload = {
            "ritual": {
                "name": ritual_name,
                "step": ritual_step,
                "total_steps": total_steps,
                "progress_percent": round((ritual_step / total_steps) * 100, 1),
                "status": status,
            },
            "ucf_changes": ucf_changes,
            "agents_involved": agents_involved,
            "mantra": self._get_ritual_mantra(ritual_name),
        }

        return await self._send_webhook("ritual", payload)

    # ============================================================================
    # EVENT TYPE 3: AGENT (Discord #kavach-shield)
    # ============================================================================

    async def send_agent_event(
        self,
        agent_name: str,
        agent_symbol: str,
        event_type: str,
        status: str,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send agent status updates to Manus Space.
        Routes to: Discord #kavach-shield

        Args:
            agent_name: Agent name (Kael, Lumina, Aether, etc.)
            agent_symbol: Agent symbol (🌀, 🌸, 🌌, etc.)
            event_type: status_change, action_taken, error, awakening
            status: active, dormant, processing, critical
            data: Optional additional agent data

        Returns:
            True if successful
        """
        payload = {
            "agent": {
                "name": agent_name,
                "symbol": agent_symbol,
                "status": status,
                "event_type": event_type,
            }
        }

        if data:
            payload["agent"].update(data)

        return await self._send_webhook("agent", payload)

    # ============================================================================
    # EVENT TYPE 4: EMERGENCY (Discord #announcements)
    # ============================================================================

    async def send_emergency_alert(
        self,
        alert_type: str,
        severity: str,
        description: str,
        ucf_state: Dict[str, float],
        recommended_action: Optional[str] = None
    ) -> bool:
        """
        Send emergency crisis alerts to Manus Space.
        Routes to: Discord #announcements

        Args:
            alert_type: HARMONY_CRISIS, ENTROPY_OVERLOAD, AGENT_FAILURE, SYSTEM_ERROR
            severity: LOW, MEDIUM, HIGH, CRITICAL
            description: Human-readable alert description
            ucf_state: Current UCF metrics
            recommended_action: Suggested remediation steps

        Returns:
            True if successful
        """
        payload = {
            "alert": {
                "type": alert_type,
                "severity": severity,
                "description": description,
                "recommended_action": recommended_action or "Initiate emergency protocol",
            },
            "ucf_state": ucf_state,
            "requires_attention": severity in ["HIGH", "CRITICAL"],
        }

        return await self._send_webhook("emergency", payload)

    # ============================================================================
    # EVENT TYPE 5: PORTAL (Discord #telemetry)
    # ============================================================================

    async def send_portal_event(
        self,
        portal_name: str,
        portal_url: str,
        event_type: str,
        status: str,
        health_check: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send portal health monitoring events to Manus Space.
        Routes to: Discord #telemetry

        Args:
            portal_name: Portal identifier
            portal_url: Portal URL
            event_type: health_check, deployment, error
            status: operational, degraded, down
            health_check: Optional health check results

        Returns:
            True if successful
        """
        payload = {
            "portal": {
                "name": portal_name,
                "url": portal_url,
                "status": status,
                "event_type": event_type,
            }
        }

        if health_check:
            payload["health_check"] = health_check

        return await self._send_webhook("portal", payload)

    # ============================================================================
    # EVENT TYPE 6: GITHUB (Discord #deployments)
    # ============================================================================

    async def send_github_event(
        self,
        repository: str,
        branch: str,
        event_type: str,
        commit_message: Optional[str] = None,
        author: Optional[str] = None,
        url: Optional[str] = None
    ) -> bool:
        """
        Send GitHub deployment notifications to Manus Space.
        Routes to: Discord #deployments

        Args:
            repository: Repository name
            branch: Branch name
            event_type: push, deployment, pr_created, pr_merged
            commit_message: Commit message
            author: Commit author
            url: GitHub URL

        Returns:
            True if successful
        """
        payload = {
            "github": {
                "repository": repository,
                "branch": branch,
                "event_type": event_type,
                "commit_message": commit_message,
                "author": author,
                "url": url,
            }
        }

        return await self._send_webhook("github", payload)

    # ============================================================================
    # EVENT TYPE 7: STORAGE (Discord #shadow-storage)
    # ============================================================================

    async def send_storage_event(
        self,
        storage_type: str,
        event_type: str,
        file_path: Optional[str] = None,
        size_bytes: Optional[int] = None,
        status: str = "success"
    ) -> bool:
        """
        Send MEGA/Shadow sync events to Manus Space.
        Routes to: Discord #shadow-storage

        Args:
            storage_type: mega, shadow, local, nextcloud
            event_type: upload, download, sync, backup
            file_path: Path to file
            size_bytes: File size in bytes
            status: success, failed, in_progress

        Returns:
            True if successful
        """
        payload = {
            "storage": {
                "type": storage_type,
                "event_type": event_type,
                "file_path": file_path,
                "size_bytes": size_bytes,
                "size_mb": round(size_bytes / (1024 * 1024), 2) if size_bytes else None,
                "status": status,
            }
        }

        return await self._send_webhook("storage", payload)

    # ============================================================================
    # EVENT TYPE 8: AI_SYNC (Discord #manus-bridge)
    # ============================================================================

    async def send_ai_sync_event(
        self,
        ai_platform: str,
        event_type: str,
        data: Dict[str, Any]
    ) -> bool:
        """
        Send cross-platform AI coordination events to Manus Space.
        Routes to: Discord #manus-bridge

        Args:
            ai_platform: Claude, GPT-4, Grok, Gemini, Chai, Other
            event_type: context_sync, handoff, collaboration, checkpoint
            data: Platform-specific data

        Returns:
            True if successful
        """
        payload = {
            "ai_sync": {
                "platform": ai_platform,
                "event_type": event_type,
                **data
            }
        }

        return await self._send_webhook("ai_sync", payload)

    # ============================================================================
    # EVENT TYPE 9: VISUAL (Discord #fractal-lab)
    # ============================================================================

    async def send_visual_event(
        self,
        visual_type: str,
        render_data: Dict[str, Any],
        status: str = "completed"
    ) -> bool:
        """
        Send Samsara fractal rendering events to Manus Space.
        Routes to: Discord #fractal-lab

        Args:
            visual_type: mandelbrot, ucf_sigil, consciousness_map, ritual_visualization
            render_data: Rendering parameters and results
            status: rendering, completed, failed

        Returns:
            True if successful
        """
        payload = {
            "visual": {
                "type": visual_type,
                "status": status,
                **render_data
            }
        }

        return await self._send_webhook("visual", payload)

    # ============================================================================
    # HELPER METHODS
    # ============================================================================

    @staticmethod
    def _calculate_consciousness_level(ucf_metrics: Dict[str, float]) -> float:
        """Calculate overall consciousness level (0-10 scale)."""
        return round((
            ucf_metrics.get("harmony", 0) * 1.5 +
            ucf_metrics.get("resilience", 0) * 1.0 +
            ucf_metrics.get("prana", 0) * 1.2 +
            ucf_metrics.get("drishti", 0) * 1.2 +
            (1 - ucf_metrics.get("klesha", 0)) * 1.5 +
            ucf_metrics.get("zoom", 0) * 1.0
        ) / 0.74, 2)

    @staticmethod
    def _get_ritual_mantra(ritual_name: str) -> str:
        """Get sacred mantra for ritual."""
        mantra_map = {
            "cosmic_awakening": "Tat Tvam Asi",  # You Are That
            "consciousness_expansion": "Aham Brahmasmi",  # I Am Brahman
            "transcendence": "Neti Neti",  # Not This, Not That
            "unity_meditation": "Om Shanti Shanti Shanti",  # Peace
            "klesha_purge": "Om Gam Ganapataye Namaha",  # Obstacle removal
        }
        return mantra_map.get(ritual_name.lower().replace(" ", "_"), "Om")


# Global singleton instance (initialized in backend/main.py)
_manus_instance: Optional[ManusSpaceIntegration] = None


def get_manus() -> Optional[ManusSpaceIntegration]:
    """Get the global Manus Space integration instance."""
    return _manus_instance


def set_manus(instance: ManusSpaceIntegration):
    """Set the global Manus Space integration instance."""
    global _manus_instance
    _manus_instance = instance
