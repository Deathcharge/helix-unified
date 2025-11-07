"""
Discord Publisher
=================

Publishes sync summaries to Discord via webhooks.

Author: Manus AI
Version: 1.0
"""

import logging
import os
from datetime import datetime
from typing import Dict, Optional

import aiohttp

logger = logging.getLogger("HelixSync.DiscordPublisher")


class DiscordPublisher:
    """Publishes sync updates to Discord"""

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.getenv("DISCORD_SYNC_WEBHOOK", "")

    async def publish(self, data: Dict, export_paths: Dict):
        """Publish sync summary to Discord"""
        if not self.webhook_url:
            logger.warning("Discord webhook URL not configured, skipping publish")
            return

        logger.info("Publishing to Discord...")

        embed = self.create_embed(data, export_paths)

        payload = {"content": "🌀 **Helix Ecosystem Sync Complete**", "embeds": [embed]}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 204:
                        logger.info("Discord publish successful")
                    else:
                        logger.error(f"Discord publish failed: {response.status}")
        except Exception as e:
            logger.error(f"Failed to publish to Discord: {e}")
            raise

    def create_embed(self, data: Dict, export_paths: Dict) -> Dict:
        """Create Discord embed from sync data"""
        timestamp = data.get("timestamp", datetime.utcnow().isoformat())

        embed = {
            "title": "🌀 Helix Ecosystem Sync",
            "description": "Automated synchronization complete",
            "color": 0x9333EA,  # Purple
            "timestamp": timestamp,
            "fields": [],
        }

        # GitHub summary
        if "github" in data:
            github_summary = data["github"].get("summary", {})
            embed["fields"].append(
                {
                    "name": "📦 GitHub",
                    "value": f"**Repos:** {github_summary.get('total_repos', 0)}\n"
                    f"**Commits Today:** {github_summary.get('total_commits_today', 0)}\n"
                    f"**Open Issues:** {github_summary.get('total_open_issues', 0)}",
                    "inline": True,
                }
            )

        # UCF State
        if "ucf_state" in data:
            ucf = data["ucf_state"]
            embed["fields"].append(
                {
                    "name": "🌀 UCF State",
                    "value": f"**Harmony:** {ucf.get('harmony', 0):.3f}\n"
                    f"**Emotion:** {ucf.get('collective_emotion', 'Unknown')}\n"
                    f"**Ethics:** {ucf.get('ethical_alignment', 0):.2f}",
                    "inline": True,
                }
            )

        # Agent Metrics
        if "agent_metrics" in data:
            agents = data["agent_metrics"]
            embed["fields"].append(
                {
                    "name": "🤖 Agents",
                    "value": f"**Total:** {agents.get('total_agents', 0)}\n"
                    f"**Active:** {agents.get('active_agents', 0)}\n"
                    f"**Tasks:** {agents.get('total_tasks', 0)}",
                    "inline": True,
                }
            )

        # Export info
        if export_paths:
            formats = ", ".join(export_paths.keys())
            embed["fields"].append({"name": "📤 Exports", "value": f"Generated: {formats}", "inline": False})

        # Footer
        embed["footer"] = {"text": "Helix Sync Service v1.0 • Tat Tvam Asi 🙏"}

        return embed
