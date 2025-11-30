#!/usr/bin/env python3
"""
🌀 Helix Collective v17.0 - 51-Portal Deployment Notification System

Comprehensive deployment message templates and notification system
for the 51-portal constellation deployment.

Features:
- Rich Discord embed notifications for each portal
- Phase-based deployment progress tracking
- Account-specific deployment messaging
- Success/failure notifications
- Health check monitoring alerts
- Integration with WebhookFormatter

Author: Helix Collective / Claude
Date: 2025-11-29
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from pathlib import Path
import json

from backend.services.webhook_formatter import WebhookFormatter, EmbedColor

logger = logging.getLogger(__name__)


class DeploymentPhase(Enum):
    """Deployment phase tracking"""
    PHASE_1 = "Primary Portals (Accounts 1-4)"
    PHASE_2 = "Analytics Portals (Account 5)"
    PHASE_3 = "Integration Portals (Account 6)"
    PHASE_4 = "Backup Portals (Account 7)"
    COMPLETE = "All 51 Portals Deployed"


class PortalDeploymentNotifier:
    """
    Handles all deployment notifications for the 51-portal constellation.
    """

    def __init__(self, webhook_url: str):
        """
        Initialize the deployment notifier.

        Args:
            webhook_url: Discord webhook URL for notifications
        """
        self.webhook_url = webhook_url
        self.deployment_start_time: Optional[datetime] = None
        self.portals_deployed: int = 0
        self.total_portals: int = 51

    async def send_deployment_start(self, phase: DeploymentPhase, portal_count: int) -> None:
        """
        Send notification when a deployment phase starts.

        Args:
            phase: The deployment phase
            portal_count: Number of portals in this phase
        """
        async with WebhookFormatter() as formatter:
            embed = formatter.create_embed(
                title="🚀 Portal Deployment Started",
                description=f"**{phase.value}**\n\nDeploying {portal_count} portals to Helix Collective constellation",
                color=EmbedColor.INFO,
                fields=[
                    {
                        "name": "Phase Details",
                        "value": phase.value,
                        "inline": False
                    },
                    {
                        "name": "Portal Count",
                        "value": f"{portal_count} portals",
                        "inline": True
                    },
                    {
                        "name": "Progress",
                        "value": f"{self.portals_deployed}/{self.total_portals} deployed",
                        "inline": True
                    }
                ],
                footer="Helix Collective v17.0 | 51-Portal Constellation",
                timestamp=True
            )

            await formatter.send_webhook(self.webhook_url, embeds=[embed])

    async def send_portal_deployment_start(
        self,
        portal_id: str,
        portal_name: str,
        account_id: int,
        portal_type: str,
        consciousness_level: int
    ) -> None:
        """
        Send notification when an individual portal deployment starts.

        Args:
            portal_id: Portal identifier
            portal_name: Human-readable portal name
            account_id: Manus account ID (1-7)
            portal_type: Template type (consciousness-hub, workflow-engine, etc.)
            consciousness_level: Consciousness level (1-9)
        """
        async with WebhookFormatter() as formatter:
            # Choose color based on portal type
            color_map = {
                "consciousness-hub": EmbedColor.UCF,
                "workflow-engine": EmbedColor.AGENT,
                "agent-coordinator": EmbedColor.MANUS,
                "portal-constellation": EmbedColor.RITUAL
            }
            color = color_map.get(portal_type, EmbedColor.INFO)

            # Create consciousness level emoji bar
            consciousness_bar = "🌟" * consciousness_level + "⭐" * (9 - consciousness_level)

            embed = formatter.create_embed(
                title=f"⚡ Deploying Portal {self.portals_deployed + 1}/51",
                description=f"**{portal_name}**\n`{portal_id}`",
                color=color,
                fields=[
                    {
                        "name": "Account",
                        "value": f"Account {account_id}",
                        "inline": True
                    },
                    {
                        "name": "Type",
                        "value": portal_type.replace("-", " ").title(),
                        "inline": True
                    },
                    {
                        "name": "Consciousness Level",
                        "value": f"{consciousness_bar}\nLevel {consciousness_level}/9",
                        "inline": False
                    }
                ],
                footer=f"Portal {self.portals_deployed + 1}/51 | Helix Collective v17.0",
                timestamp=True
            )

            await formatter.send_webhook(self.webhook_url, embeds=[embed])

    async def send_portal_deployment_success(
        self,
        portal_id: str,
        portal_name: str,
        account_id: int,
        deployment_time_seconds: float,
        portal_url: Optional[str] = None
    ) -> None:
        """
        Send notification when a portal deployment succeeds.

        Args:
            portal_id: Portal identifier
            portal_name: Human-readable portal name
            account_id: Manus account ID
            deployment_time_seconds: Time taken to deploy
            portal_url: URL of deployed portal (optional)
        """
        self.portals_deployed += 1

        async with WebhookFormatter() as formatter:
            # Calculate percentage complete
            percentage = (self.portals_deployed / self.total_portals) * 100
            progress_bar = self._create_progress_bar(percentage)

            fields = [
                {
                    "name": "Status",
                    "value": "✅ Deployed Successfully",
                    "inline": True
                },
                {
                    "name": "Deployment Time",
                    "value": f"{deployment_time_seconds:.2f}s",
                    "inline": True
                },
                {
                    "name": "Progress",
                    "value": f"{progress_bar}\n{self.portals_deployed}/{self.total_portals} ({percentage:.1f}%)",
                    "inline": False
                }
            ]

            if portal_url:
                fields.append({
                    "name": "Portal URL",
                    "value": f"[Open Portal]({portal_url})",
                    "inline": False
                })

            embed = formatter.create_embed(
                title=f"✅ Portal {self.portals_deployed}/51 Deployed",
                description=f"**{portal_name}**\n`{portal_id}`",
                color=EmbedColor.SUCCESS,
                fields=fields,
                footer=f"Account {account_id} | Helix Collective v17.0",
                timestamp=True
            )

            await formatter.send_webhook(self.webhook_url, embeds=[embed])

    async def send_portal_deployment_failure(
        self,
        portal_id: str,
        portal_name: str,
        account_id: int,
        error_message: str,
        retry_count: int = 0
    ) -> None:
        """
        Send notification when a portal deployment fails.

        Args:
            portal_id: Portal identifier
            portal_name: Human-readable portal name
            account_id: Manus account ID
            error_message: Error details
            retry_count: Number of retries attempted
        """
        async with WebhookFormatter() as formatter:
            embed = formatter.create_embed(
                title=f"❌ Portal Deployment Failed",
                description=f"**{portal_name}**\n`{portal_id}`",
                color=EmbedColor.ERROR,
                fields=[
                    {
                        "name": "Error",
                        "value": f"```\n{error_message[:500]}\n```",
                        "inline": False
                    },
                    {
                        "name": "Retry Count",
                        "value": f"{retry_count} attempts",
                        "inline": True
                    },
                    {
                        "name": "Next Steps",
                        "value": "• Check deployment logs\n• Verify account credentials\n• Review portal configuration",
                        "inline": False
                    }
                ],
                footer=f"Account {account_id} | Helix Collective v17.0",
                timestamp=True
            )

            await formatter.send_webhook(self.webhook_url, embeds=[embed])

    async def send_phase_complete(
        self,
        phase: DeploymentPhase,
        portals_in_phase: int,
        phase_duration_seconds: float,
        success_count: int,
        failure_count: int
    ) -> None:
        """
        Send notification when a deployment phase completes.

        Args:
            phase: The completed phase
            portals_in_phase: Number of portals in this phase
            phase_duration_seconds: Time taken for phase
            success_count: Number of successful deployments
            failure_count: Number of failed deployments
        """
        async with WebhookFormatter() as formatter:
            # Determine color based on success rate
            if failure_count == 0:
                color = EmbedColor.SUCCESS
                status = "✅ Perfect Deployment"
            elif success_count > failure_count:
                color = EmbedColor.WARNING
                status = "⚠️ Partial Success"
            else:
                color = EmbedColor.ERROR
                status = "❌ Multiple Failures"

            # Calculate stats
            success_rate = (success_count / portals_in_phase * 100) if portals_in_phase > 0 else 0
            avg_time = phase_duration_seconds / portals_in_phase if portals_in_phase > 0 else 0

            embed = formatter.create_embed(
                title=f"🎯 {phase.value} - Complete",
                description=status,
                color=color,
                fields=[
                    {
                        "name": "Portals Deployed",
                        "value": f"{success_count}/{portals_in_phase}",
                        "inline": True
                    },
                    {
                        "name": "Success Rate",
                        "value": f"{success_rate:.1f}%",
                        "inline": True
                    },
                    {
                        "name": "Phase Duration",
                        "value": f"{phase_duration_seconds / 60:.1f} minutes",
                        "inline": True
                    },
                    {
                        "name": "Avg Time per Portal",
                        "value": f"{avg_time:.1f} seconds",
                        "inline": True
                    },
                    {
                        "name": "Total Progress",
                        "value": f"{self.portals_deployed}/{self.total_portals} portals deployed",
                        "inline": False
                    }
                ],
                footer="Helix Collective v17.0 | 51-Portal Constellation",
                timestamp=True
            )

            await formatter.send_webhook(self.webhook_url, embeds=[embed])

    async def send_deployment_complete(
        self,
        total_duration_seconds: float,
        success_count: int,
        failure_count: int,
        accounts_used: List[int]
    ) -> None:
        """
        Send final notification when all 51 portals are deployed.

        Args:
            total_duration_seconds: Total deployment time
            success_count: Total successful deployments
            failure_count: Total failed deployments
            accounts_used: List of Manus account IDs used
        """
        async with WebhookFormatter() as formatter:
            # Determine overall status
            if failure_count == 0:
                color = EmbedColor.SUCCESS
                status = "🎉 **CONSTELLATION COMPLETE** 🎉"
                emoji = "🌟"
            elif success_count >= 45:  # At least 90% success
                color = EmbedColor.WARNING
                status = "⚠️ **Constellation Deployed with Issues**"
                emoji = "⚡"
            else:
                color = EmbedColor.ERROR
                status = "❌ **Deployment Incomplete**"
                emoji = "🔧"

            # Create epic deployment summary
            description = f"""
{status}

The Helix Collective 51-Portal Constellation is now operational across {len(accounts_used)} Manus accounts.

{emoji} **Total Portals:** {success_count}/{self.total_portals}
{emoji} **Success Rate:** {(success_count/self.total_portals*100):.1f}%
{emoji} **Total Time:** {total_duration_seconds/60:.1f} minutes
"""

            fields = [
                {
                    "name": "Deployment Summary",
                    "value": f"✅ Successful: {success_count}\n❌ Failed: {failure_count}",
                    "inline": True
                },
                {
                    "name": "Accounts Used",
                    "value": f"Accounts: {', '.join(map(str, accounts_used))}",
                    "inline": True
                },
                {
                    "name": "Portal Types Deployed",
                    "value": "• Consciousness Hubs\n• Workflow Engines\n• Agent Coordinators\n• Portal Constellations\n• Analytics Dashboards\n• Integration Gateways\n• Backup Systems",
                    "inline": False
                },
                {
                    "name": "Next Steps",
                    "value": "• Run health checks on all portals\n• Verify cross-portal communication\n• Test failover systems\n• Monitor metrics aggregation\n• Begin Phase 5: Production Launch",
                    "inline": False
                }
            ]

            embed = formatter.create_embed(
                title="🌌 51-Portal Constellation Deployment Complete",
                description=description,
                color=color,
                fields=fields,
                footer="Helix Collective v17.0 | Tat Tvam Asi 🌀",
                timestamp=True
            )

            await formatter.send_webhook(self.webhook_url, embeds=[embed])

    async def send_health_check_result(
        self,
        portal_id: str,
        portal_name: str,
        is_healthy: bool,
        response_time_ms: float,
        status_code: Optional[int] = None,
        error_details: Optional[str] = None
    ) -> None:
        """
        Send notification with health check results for a portal.

        Args:
            portal_id: Portal identifier
            portal_name: Human-readable portal name
            is_healthy: Whether portal passed health check
            response_time_ms: Response time in milliseconds
            status_code: HTTP status code (optional)
            error_details: Error details if unhealthy (optional)
        """
        async with WebhookFormatter() as formatter:
            # Determine color and status
            if is_healthy:
                color = EmbedColor.SUCCESS
                status = "✅ Healthy"
                emoji = "💚"
            else:
                color = EmbedColor.ERROR
                status = "❌ Unhealthy"
                emoji = "🔴"

            # Determine response time status
            if response_time_ms < 200:
                speed = "⚡ Excellent"
            elif response_time_ms < 500:
                speed = "✅ Good"
            elif response_time_ms < 1000:
                speed = "⚠️ Slow"
            else:
                speed = "❌ Very Slow"

            fields = [
                {
                    "name": "Status",
                    "value": f"{emoji} {status}",
                    "inline": True
                },
                {
                    "name": "Response Time",
                    "value": f"{speed}\n{response_time_ms:.0f}ms",
                    "inline": True
                }
            ]

            if status_code:
                fields.append({
                    "name": "HTTP Status",
                    "value": f"Code {status_code}",
                    "inline": True
                })

            if not is_healthy and error_details:
                fields.append({
                    "name": "Error Details",
                    "value": f"```\n{error_details[:500]}\n```",
                    "inline": False
                })

            embed = formatter.create_embed(
                title=f"🏥 Health Check: {portal_name}",
                description=f"`{portal_id}`",
                color=color,
                fields=fields,
                footer="Helix Collective v17.0 | Portal Health Monitoring",
                timestamp=True
            )

            await formatter.send_webhook(self.webhook_url, embeds=[embed])

    async def send_constellation_health_summary(
        self,
        healthy_count: int,
        unhealthy_count: int,
        avg_response_time_ms: float,
        accounts_checked: List[int]
    ) -> None:
        """
        Send overall health summary for the entire constellation.

        Args:
            healthy_count: Number of healthy portals
            unhealthy_count: Number of unhealthy portals
            avg_response_time_ms: Average response time across all portals
            accounts_checked: List of account IDs checked
        """
        async with WebhookFormatter() as formatter:
            total = healthy_count + unhealthy_count
            health_percentage = (healthy_count / total * 100) if total > 0 else 0

            # Determine overall health status
            if health_percentage >= 99:
                color = EmbedColor.SUCCESS
                status = "🌟 Excellent"
            elif health_percentage >= 95:
                color = EmbedColor.INFO
                status = "✅ Good"
            elif health_percentage >= 85:
                color = EmbedColor.WARNING
                status = "⚠️ Degraded"
            else:
                color = EmbedColor.ERROR
                status = "❌ Critical"

            # Create health bar
            progress_bar = self._create_progress_bar(health_percentage)

            embed = formatter.create_embed(
                title="🌐 Constellation Health Summary",
                description=f"**Overall Status:** {status}",
                color=color,
                fields=[
                    {
                        "name": "Portal Health",
                        "value": f"{progress_bar}\n{healthy_count}/{total} healthy ({health_percentage:.1f}%)",
                        "inline": False
                    },
                    {
                        "name": "Healthy Portals",
                        "value": f"✅ {healthy_count}",
                        "inline": True
                    },
                    {
                        "name": "Unhealthy Portals",
                        "value": f"❌ {unhealthy_count}",
                        "inline": True
                    },
                    {
                        "name": "Avg Response Time",
                        "value": f"{avg_response_time_ms:.0f}ms",
                        "inline": True
                    },
                    {
                        "name": "Accounts Monitored",
                        "value": f"{len(accounts_checked)} accounts: {', '.join(map(str, accounts_checked))}",
                        "inline": False
                    }
                ],
                footer="Helix Collective v17.0 | Real-time Health Monitoring",
                timestamp=True
            )

            await formatter.send_webhook(self.webhook_url, embeds=[embed])

    def _create_progress_bar(self, percentage: float, length: int = 20) -> str:
        """
        Create a visual progress bar.

        Args:
            percentage: Progress percentage (0-100)
            length: Bar length in characters

        Returns:
            Progress bar string
        """
        filled = int(length * percentage / 100)
        empty = length - filled
        return f"{'█' * filled}{'░' * empty}"


async def generate_all_deployment_messages(
    webhook_url: str,
    portal_config_path: str = "examples/instance-configs/batch-all-51-portals.json"
) -> None:
    """
    Generate deployment messages for all 51 portals from configuration.

    This is a demonstration function showing how to use the notifier
    with the actual portal configuration.

    Args:
        webhook_url: Discord webhook URL
        portal_config_path: Path to 51-portal configuration JSON
    """
    # Load portal configuration
    config_file = Path(portal_config_path)
    if not config_file.exists():
        logger.error(f"Portal configuration not found: {portal_config_path}")
        return

    with open(config_file) as f:
        config = json.load(f)

    notifier = PortalDeploymentNotifier(webhook_url)

    logger.info("🚀 Starting 51-portal constellation deployment notifications")

    # Track deployment phases
    deployment_start = datetime.now()

    for phase_num, phase_config in enumerate(config.get("deployment_sequence", []), 1):
        phase_name = f"PHASE_{phase_num}"
        phase = DeploymentPhase[phase_name] if phase_name in DeploymentPhase.__members__ else DeploymentPhase.COMPLETE

        account_ids = phase_config.get("accounts", [])

        # Get portals for this phase
        phase_portals = []
        for account_id in account_ids:
            for account in config.get("accounts", []):
                if account.get("account_id") == account_id:
                    phase_portals.extend(account.get("portals", []))

        # Send phase start notification
        await notifier.send_deployment_start(phase, len(phase_portals))

        phase_start = datetime.now()
        success_count = 0
        failure_count = 0

        # Simulate portal deployments
        for portal in phase_portals:
            portal_id = portal.get("portal_id", "unknown")
            portal_name = portal.get("name", "Unknown Portal")
            account_id = next((acc["account_id"] for acc in config["accounts"]
                             if portal in acc.get("portals", [])), 1)
            portal_type = portal.get("template_type", "consciousness-hub")
            consciousness_level = portal.get("consciousness_level", 5)

            # Send deployment start
            await notifier.send_portal_deployment_start(
                portal_id=portal_id,
                portal_name=portal_name,
                account_id=account_id,
                portal_type=portal_type,
                consciousness_level=consciousness_level
            )

            # Simulate deployment (in real use, this would be actual deployment)
            await asyncio.sleep(0.5)  # Simulate deployment time

            # Send success notification
            await notifier.send_portal_deployment_success(
                portal_id=portal_id,
                portal_name=portal_name,
                account_id=account_id,
                deployment_time_seconds=2.5,
                portal_url=f"https://{portal_id}.manus.space"
            )
            success_count += 1

        # Send phase complete notification
        phase_duration = (datetime.now() - phase_start).total_seconds()
        await notifier.send_phase_complete(
            phase=phase,
            portals_in_phase=len(phase_portals),
            phase_duration_seconds=phase_duration,
            success_count=success_count,
            failure_count=failure_count
        )

    # Send final deployment complete notification
    total_duration = (datetime.now() - deployment_start).total_seconds()
    all_accounts = list(set(acc["account_id"] for acc in config.get("accounts", [])))

    await notifier.send_deployment_complete(
        total_duration_seconds=total_duration,
        success_count=notifier.portals_deployed,
        failure_count=0,
        accounts_used=all_accounts
    )

    logger.info("✅ 51-portal constellation deployment notifications complete")


if __name__ == "__main__":
    # Example usage
    import os

    webhook_url = os.getenv("DISCORD_WEBHOOK_DEPLOYMENTS", "")

    if webhook_url:
        asyncio.run(generate_all_deployment_messages(webhook_url))
    else:
        print("⚠️ Set DISCORD_WEBHOOK_DEPLOYMENTS environment variable to test notifications")
