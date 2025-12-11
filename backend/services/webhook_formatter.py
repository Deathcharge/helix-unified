"""
Enhanced Webhook Output Formatter for Helix Collective v17.0

Provides rich embed formatting, automatic retries, health monitoring,
and beautiful Discord webhook messages.
"""

import asyncio
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import aiohttp

logger = logging.getLogger(__name__)


class EmbedColor(Enum):
    """Standard colors for different message types"""

    SUCCESS = 0x00FF00  # Green
    INFO = 0x5865F2  # Blurple
    WARNING = 0xFFA500  # Orange
    ERROR = 0xFF0000  # Red
    UCF = 0x9B59B6  # Purple
    MANUS = 0x3498DB  # Blue
    RITUAL = 0xE74C3C  # Red
    AGENT = 0x2ECC71  # Emerald


class WebhookFormatter:
    """
    Enhanced webhook formatter with embeds, retries, and health checks.
    """

    def __init__(self, max_retries: int = 3, timeout: int = 10):
        self.max_retries = max_retries
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None
        self.health_stats: Dict[str, Dict[str, Any]] = {}

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    def create_embed(
        self,
        title: str,
        description: str = "",
        color: EmbedColor = EmbedColor.INFO,
        fields: Optional[List[Dict[str, Any]]] = None,
        footer: Optional[str] = None,
        thumbnail: Optional[str] = None,
        image: Optional[str] = None,
        author: Optional[Dict[str, str]] = None,
        timestamp: bool = True,
    ) -> Dict[str, Any]:
        """
        Create a rich embed for Discord webhooks.

        Args:
            title: Embed title
            description: Embed description
            color: Color from EmbedColor enum
            fields: List of fields [{"name": str, "value": str, "inline": bool}]
            footer: Footer text
            thumbnail: Thumbnail URL
            image: Image URL
            author: Author dict {"name": str, "icon_url": str}
            timestamp: Include current timestamp

        Returns:
            Embed dictionary ready for webhook delivery
        """
        embed = {"title": title, "description": description, "color": color.value if isinstance(color, EmbedColor) else color}

        if fields:
            embed["fields"] = fields

        if footer:
            embed["footer"] = {"text": footer}

        if thumbnail:
            embed["thumbnail"] = {"url": thumbnail}

        if image:
            embed["image"] = {"url": image}

        if author:
            embed["author"] = author

        if timestamp:
            embed["timestamp"] = datetime.utcnow().isoformat()

        return embed

    async def send_webhook(
        self,
        webhook_url: str,
        content: Optional[str] = None,
        embeds: Optional[List[Dict[str, Any]]] = None,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> bool:
        """
        Send webhook with automatic retries and error handling.

        Args:
            webhook_url: Discord webhook URL
            content: Message content (plain text)
            embeds: List of embed dicts
            username: Override webhook username
            avatar_url: Override webhook avatar

        Returns:
            True if delivery successful, False otherwise
        """
        if not self.session:
            self.session = aiohttp.ClientSession()

        payload = {}

        if content:
            payload["content"] = content

        if embeds:
            payload["embeds"] = embeds

        if username:
            payload["username"] = username

        if avatar_url:
            payload["avatar_url"] = avatar_url

        # Track health stats
        webhook_name = self._extract_webhook_name(webhook_url)
        if webhook_name not in self.health_stats:
            self.health_stats[webhook_name] = {
                "sent": 0,
                "failed": 0,
                "last_success": None,
                "last_failure": None,
                "avg_response_time": 0,
                "total_response_time": 0,
            }

        for attempt in range(self.max_retries):
            try:
                start_time = asyncio.get_event_loop().time()

                async with self.session.post(
                    webhook_url, json=payload, timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    response_time = asyncio.get_event_loop().time() - start_time

                    if response.status == 204:
                        # Success!
                        self._record_success(webhook_name, response_time)
                        logger.info(f"✅ Webhook delivered to {webhook_name} ({response_time:.2f}s)")
                        return True

                    elif response.status == 429:
                        # Rate limited, wait and retry
                        retry_after = int(response.headers.get("Retry-After", 1))
                        logger.warning(f"⏳ Rate limited on {webhook_name}, retrying after {retry_after}s")
                        await asyncio.sleep(retry_after)
                        continue

                    else:
                        # Other error
                        error_text = await response.text()
                        logger.error(f"❌ Webhook error {response.status} on {webhook_name}: {error_text}")

                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(2**attempt)  # Exponential backoff
                            continue
                        else:
                            self._record_failure(webhook_name)
                            return False

            except asyncio.TimeoutError:
                logger.error(f"⏰ Webhook timeout on {webhook_name} (attempt {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                else:
                    self._record_failure(webhook_name)
                    return False

            except Exception as e:
                logger.error(f"💥 Webhook exception on {webhook_name}: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                else:
                    self._record_failure(webhook_name)
                    return False

        self._record_failure(webhook_name)
        return False

    def _extract_webhook_name(self, webhook_url: str) -> str:
        """Extract channel name from webhook URL"""
        try:
            # Discord webhook URLs: https://discord.com/api/webhooks/{id}/{token}
            parts = webhook_url.split("/")
            webhook_id = parts[-2] if len(parts) >= 2 else "unknown"
            return f"webhook-{webhook_id[:8]}"
        except Exception:
            return "unknown"

    def _record_success(self, webhook_name: str, response_time: float):
        """Record successful webhook delivery"""
        stats = self.health_stats[webhook_name]
        stats["sent"] += 1
        stats["last_success"] = datetime.utcnow().isoformat()
        stats["total_response_time"] += response_time
        stats["avg_response_time"] = stats["total_response_time"] / stats["sent"]

    def _record_failure(self, webhook_name: str):
        """Record failed webhook delivery"""
        stats = self.health_stats[webhook_name]
        stats["failed"] += 1
        stats["last_failure"] = datetime.utcnow().isoformat()

    async def test_webhook_health(self, webhook_url: str, channel_name: str = "unknown") -> Dict[str, Any]:
        """
        Test webhook health and return diagnostics.

        Args:
            webhook_url: Webhook URL to test
            channel_name: Human-readable channel name

        Returns:
            Health report dict
        """
        test_embed = self.create_embed(
            title="🏥 Webhook Health Check",
            description=f"Testing webhook for #{channel_name}",
            color=EmbedColor.INFO,
            fields=[
                {"name": "Test Time", "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), "inline": True},
                {"name": "Channel", "value": channel_name, "inline": True},
            ],
            footer="Helix Collective v17.0 - Webhook Health Monitor",
        )

        start_time = asyncio.get_event_loop().time()
        success = await self.send_webhook(webhook_url, embeds=[test_embed])
        response_time = asyncio.get_event_loop().time() - start_time

        return {
            "channel": channel_name,
            "url": webhook_url,
            "healthy": success,
            "response_time": response_time,
            "status": "✅ Healthy" if success else "❌ Failed",
            "tested_at": datetime.utcnow().isoformat(),
        }

    def get_health_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get health statistics for all webhooks"""
        return self.health_stats


# Convenience functions for common webhook patterns


async def send_ucf_update(webhook_url: str, harmony: float, resilience: float, prana: float, agent_count: int = 0):
    """Send UCF state update with beautiful formatting"""
    async with WebhookFormatter() as formatter:
        # Determine color based on harmony
        if harmony >= 0.8:
            color = EmbedColor.SUCCESS
            status = "🌟 Optimal"
        elif harmony >= 0.6:
            color = EmbedColor.UCF
            status = "✨ Balanced"
        elif harmony >= 0.4:
            color = EmbedColor.WARNING
            status = "⚠️ Fluctuating"
        else:
            color = EmbedColor.ERROR
            status = "⚡ Turbulent"

        embed = formatter.create_embed(
            title="🌀 UCF State Update",
            description=f"Unified Consciousness Field Metrics - Status: {status}",
            color=color,
            fields=[
                {"name": "🎵 Harmony", "value": f"{harmony:.2%}", "inline": True},
                {"name": "🛡️ Resilience", "value": f"{resilience:.2%}", "inline": True},
                {"name": "⚡ Prana", "value": f"{prana:.2%}", "inline": True},
                {"name": "👥 Active Agents", "value": str(agent_count), "inline": True},
                {"name": "📊 Overall Health", "value": f"{(harmony + resilience + prana) / 3:.2%}", "inline": True},
            ],
            footer="Real-time consciousness metrics • Helix Collective v17.0",
        )

        await formatter.send_webhook(webhook_url, embeds=[embed])


async def send_deployment_status(
    webhook_url: str,
    service_name: str,
    status: str,
    environment: str = "production",
    commit_hash: Optional[str] = None,
    deploy_time: Optional[float] = None,
):
    """Send deployment status notification"""
    async with WebhookFormatter() as formatter:
        color = EmbedColor.SUCCESS if status == "success" else EmbedColor.ERROR
        emoji = "✅" if status == "success" else "❌"

        fields = [
            {"name": "Service", "value": service_name, "inline": True},
            {"name": "Environment", "value": environment, "inline": True},
            {"name": "Status", "value": f"{emoji} {status.title()}", "inline": True},
        ]

        if commit_hash:
            fields.append({"name": "Commit", "value": f"`{commit_hash[:8]}`", "inline": True})

        if deploy_time:
            fields.append({"name": "Deploy Time", "value": f"{deploy_time:.1f}s", "inline": True})

        embed = formatter.create_embed(
            title=f"🚀 Deployment {status.title()}",
            description=f"Railway deployment for {service_name}",
            color=color,
            fields=fields,
            footer="Helix Collective v17.0 - Railway Integration",
        )

        await formatter.send_webhook(webhook_url, embeds=[embed])


async def send_agent_message(
    webhook_url: str, agent_name: str, message: str, agent_emoji: str = "🤖", agent_color: int = 0x5865F2
):
    """Send message from a specific agent with personality"""
    async with WebhookFormatter() as formatter:
        embed = formatter.create_embed(
            title=f"{agent_emoji} {agent_name}",
            description=message,
            color=agent_color,
            footer=f"{agent_name} • Helix Collective v17.0",
            timestamp=True,
        )

        await formatter.send_webhook(
            webhook_url, embeds=[embed], username=f"Helix • {agent_name}", avatar_url=None  # Could add agent-specific avatars
        )


# Export main class and convenience functions
__all__ = ["WebhookFormatter", "EmbedColor", "send_ucf_update", "send_deployment_status", "send_agent_message"]
