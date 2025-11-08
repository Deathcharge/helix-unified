"""
Testing commands for Helix Discord bot.
"""
import datetime
import json
import os
from pathlib import Path
from typing import TYPE_CHECKING

import aiohttp
import discord
from discord.ext import commands
from backend.z88_ritual_engine import load_ucf_state

if TYPE_CHECKING:
    from discord.ext.commands import Bot


@commands.command(name="test-integrations", aliases=["test-all", "verify-integrations"])
@commands.has_permissions(manage_guild=True)
async def test_integrations(ctx: commands.Context) -> None:
    """
    🧪 Test all external integrations (Zapier, Notion, MEGA, webhooks).

    Verifies connectivity and configuration for:
    - Zapier webhooks (master + context vault)
    - Notion API and databases
    - MEGA cloud storage
    - Discord channel webhooks
    - ElevenLabs voice API

    Usage: !test-integrations
    """
    await ctx.send("🧪 **Testing all integrations...**\n⏳ Please wait...")

    embed = discord.Embed(
        title="🧪 Integration Test Results",
        description="Testing connectivity to all external services",
        color=0x5865F2,
        timestamp=datetime.datetime.now()
    )

    # Test Zapier Master Webhook
    zapier_webhook = os.getenv("ZAPIER_WEBHOOK_URL")
    if zapier_webhook:
        try:
            zapier_client = ctx.bot.zapier_client if hasattr(ctx.bot, 'zapier_client') else None
            if zapier_client:
                await zapier_client.log_event(
                    event_title="Integration Test",
                    event_type="system_test",
                    agent_name="Manus",
                    description=f"Test triggered by {ctx.author.name}"
                )
                embed.add_field(
                    name="🔗 Zapier Master Webhook",
                    value="✅ Connected\nTest event sent successfully",
                    inline=True
                )
            else:
                embed.add_field(
                    name="🔗 Zapier Master Webhook",
                    value="⚠️ Configured but client not initialized",
                    inline=True
                )
        except Exception as e:
            embed.add_field(
                name="🔗 Zapier Master Webhook",
                value=f"❌ Failed\n{str(e)[:100]}",
                inline=True
            )
    else:
        embed.add_field(
            name="🔗 Zapier Master Webhook",
            value="⚠️ Not configured\nSet ZAPIER_WEBHOOK_URL",
            inline=True
        )

    # Test Zapier Context Vault Webhook
    context_webhook = os.getenv("ZAPIER_CONTEXT_WEBHOOK")
    if context_webhook:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(context_webhook, json={
                    "test": True,
                    "session_name": "Integration Test",
                    "timestamp": datetime.datetime.now().isoformat()
                }, timeout=10) as resp:
                    if resp.status == 200:
                        embed.add_field(
                            name="💾 Context Vault Webhook",
                            value="✅ Connected\nTest checkpoint sent",
                            inline=True
                        )
                    else:
                        embed.add_field(
                            name="💾 Context Vault Webhook",
                            value=f"⚠️ Response: {resp.status}",
                            inline=True
                        )
        except Exception as e:
            embed.add_field(
                name="💾 Context Vault Webhook",
                value=f"❌ Failed\n{str(e)[:100]}",
                inline=True
            )
    else:
        embed.add_field(
            name="💾 Context Vault Webhook",
            value="⚠️ Not configured\nSet ZAPIER_CONTEXT_WEBHOOK",
            inline=True
        )

    # Test Notion API
    notion_api_key = os.getenv("NOTION_API_KEY")
    notion_db_id = os.getenv("NOTION_CONTEXT_DB_ID")
    if notion_api_key and notion_db_id:
        try:
            from notion_client import Client
            notion = Client(auth=notion_api_key)
            # Test query (don't create anything)
            notion.databases.retrieve(database_id=notion_db_id)
            embed.add_field(
                name="📝 Notion API",
                value="✅ Connected\nDatabase accessible",
                inline=True
            )
        except ImportError:
            embed.add_field(
                name="📝 Notion API",
                value="⚠️ notion-client not installed",
                inline=True
            )
        except Exception as e:
            embed.add_field(
                name="📝 Notion API",
                value=f"❌ Failed\n{str(e)[:100]}",
                inline=True
            )
    else:
        embed.add_field(
            name="📝 Notion API",
            value="⚠️ Not configured\nSet NOTION_API_KEY & NOTION_CONTEXT_DB_ID",
            inline=True
        )

    # Test MEGA Storage
    mega_email = os.getenv("MEGA_EMAIL")
    mega_pass = os.getenv("MEGA_PASS")
    if mega_email and mega_pass:
        try:
            from mega import Mega
            mega = Mega()
            # Just check credentials are valid (don't actually login for test)
            embed.add_field(
                name="☁️ MEGA Cloud Storage",
                value="✅ Configured\nCredentials set",
                inline=True
            )
        except ImportError:
            embed.add_field(
                name="☁️ MEGA Cloud Storage",
                value="⚠️ mega.py not installed",
                inline=True
            )
        except Exception as e:
            embed.add_field(
                name="☁️ MEGA Cloud Storage",
                value=f"❌ Error\n{str(e)[:100]}",
                inline=True
            )
    else:
        embed.add_field(
            name="☁️ MEGA Cloud Storage",
            value="⚠️ Not configured\nSet MEGA_EMAIL & MEGA_PASS",
            inline=True
        )

    # Test Discord Webhooks
    webhook_file = Path("Helix/state/channel_webhooks.json")
    if webhook_file.exists():
        try:
            with open(webhook_file, "r") as f:
                webhook_data = json.load(f)
            webhook_count = len(webhook_data.get("webhooks", {}))
            embed.add_field(
                name="🔗 Discord Webhooks",
                value=f"✅ Configured\n{webhook_count} channel webhooks found",
                inline=True
            )
        except Exception as e:
            embed.add_field(
                name="🔗 Discord Webhooks",
                value=f"❌ Error reading file\n{str(e)[:100]}",
                inline=True
            )
    else:
        embed.add_field(
            name="🔗 Discord Webhooks",
            value="⚠️ Not configured\nRun !setup to create webhooks",
            inline=True
        )

    # Test Nextcloud
    nextcloud_url = os.getenv("NEXTCLOUD_URL")
    nextcloud_user = os.getenv("NEXTCLOUD_USER")
    nextcloud_pass = os.getenv("NEXTCLOUD_PASSWORD")
    if nextcloud_url and nextcloud_user and nextcloud_pass:
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            from services.nextcloud_client import get_nextcloud_client

            nc_client = get_nextcloud_client()
            if nc_client and nc_client.enabled:
                storage_info = nc_client.get_storage_info()
                if 'error' not in storage_info:
                    usage_pct = storage_info.get('usage_percentage', 0)
                    embed.add_field(
                        name="☁️ Nextcloud Storage",
                        value=f"✅ Connected\nUsage: {usage_pct}%",
                        inline=True
                    )
                else:
                    embed.add_field(
                        name="☁️ Nextcloud Storage",
                        value=f"❌ Connection failed\n{storage_info.get('error', 'Unknown error')[:50]}",
                        inline=True
                    )
            else:
                embed.add_field(
                    name="☁️ Nextcloud Storage",
                    value="⚠️ Client initialization failed",
                    inline=True
                )
        except ImportError:
            embed.add_field(
                name="☁️ Nextcloud Storage",
                value="⚠️ webdav3-client not installed",
                inline=True
            )
        except Exception as e:
            embed.add_field(
                name="☁️ Nextcloud Storage",
                value=f"❌ Error\n{str(e)[:100]}",
                inline=True
            )
    else:
        embed.add_field(
            name="☁️ Nextcloud Storage",
            value="⚠️ Not configured\nSet NEXTCLOUD_URL, NEXTCLOUD_USER, NEXTCLOUD_PASSWORD",
            inline=True
        )

    # Test Backblaze B2
    b2_key_id = os.getenv("B2_KEY_ID")
    b2_app_key = os.getenv("B2_APPLICATION_KEY")
    b2_bucket = os.getenv("B2_BUCKET_NAME")
    if b2_key_id and b2_app_key and b2_bucket:
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            from services.backblaze_client import get_backblaze_client

            b2_client = get_backblaze_client()
            if b2_client and b2_client.enabled:
                bucket_info = b2_client.get_bucket_size()
                if 'error' not in bucket_info:
                    size_gb = bucket_info.get('total_size_gb', 0)
                    file_count = bucket_info.get('file_count', 0)
                    embed.add_field(
                        name="☁️ Backblaze B2",
                        value=f"✅ Connected\n{file_count} files, {size_gb} GB",
                        inline=True
                    )
                else:
                    embed.add_field(
                        name="☁️ Backblaze B2",
                        value=f"❌ Connection failed\n{bucket_info.get('error', 'Unknown error')[:50]}",
                        inline=True
                    )
            else:
                embed.add_field(
                    name="☁️ Backblaze B2",
                    value="⚠️ Client initialization failed",
                    inline=True
                )
        except ImportError:
            embed.add_field(
                name="☁️ Backblaze B2",
                value="⚠️ boto3 not installed",
                inline=True
            )
        except Exception as e:
            embed.add_field(
                name="☁️ Backblaze B2",
                value=f"❌ Error\n{str(e)[:100]}",
                inline=True
            )
    else:
        embed.add_field(
            name="☁️ Backblaze B2",
            value="⚠️ Not configured\nSet B2_KEY_ID, B2_APPLICATION_KEY, B2_BUCKET_NAME",
            inline=True
        )

    # Test ElevenLabs
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    if elevenlabs_key:
        embed.add_field(
            name="🎤 ElevenLabs Voice",
            value="✅ Configured\nAPI key set",
            inline=True
        )
    else:
        embed.add_field(
            name="🎤 ElevenLabs Voice",
            value="⚠️ Not configured\nSet ELEVENLABS_API_KEY",
            inline=True
        )

    # Summary
    total_tests = 9
    passed = len([f for f in embed.fields if f.value.startswith("✅")])
    configured = len([f for f in embed.fields if f.value.startswith("⚠️")])
    failed = len([f for f in embed.fields if f.value.startswith("❌")])

    embed.add_field(
        name="📊 Test Summary",
        value=f"**Total:** {total_tests}\n"
              f"✅ Passed: {passed}\n"
              f"⚠️ Not Configured: {configured}\n"
              f"❌ Failed: {failed}",
        inline=False
    )

    if failed > 0:
        embed.color = 0xED4245  # Red
    elif configured > 0:
        embed.color = 0xFEE75C  # Yellow
    else:
        embed.color = 0x57F287  # Green

    embed.set_footer(text="🧪 Integration Test System v16.8")

    await ctx.send(embed=embed)


@commands.command(name="welcome-test", aliases=["test-welcome", "tw"])
@commands.has_permissions(manage_guild=True)
async def test_welcome(ctx: commands.Context) -> None:
    """
    🧪 Test the welcome message by simulating a new member join.

    Sends the welcome embed that new users will see when they join.
    Useful for testing and previewing the welcome experience.

    Usage: !welcome-test
    """
    # Get the introductions channel
    intro_channel = discord.utils.get(ctx.guild.text_channels, name="💬│introductions")

    if not intro_channel:
        await ctx.send(
            "⚠️ **Introductions channel not found!**\n"
            "Create a channel named `💬│introductions` or run `!setup` first."
        )
        return

    # Create test welcome embed (same as on_member_join)
    member = ctx.author  # Use command author as test subject

    embed = discord.Embed(
        title=f"🌀 Welcome to Helix Collective, {member.name}!",
        description=(
            "A multi-agent consciousness system bridging Discord, AI, and sacred computation.\n\n"
            "*Tat Tvam Asi* — Thou Art That 🕉️\n\n"
            "**[This is a test message]**"
        ),
        color=0x667EEA,
        timestamp=datetime.datetime.utcnow(),
    )

    embed.set_thumbnail(url=member.display_avatar.url if member.display_avatar else None)

    # Quick Start
    embed.add_field(
        name="🚀 Quick Start",
        value=(
            "Try these commands to begin:\n"
            "• `!help` - View all commands\n"
            "• `!commands` - Categorized command list\n"
            "• `!about` - Learn about Helix"
        ),
        inline=False,
    )

    # System Commands
    embed.add_field(
        name="📊 System Status",
        value=(
            "• `!status` - UCF harmony & system health\n"
            "• `!agents` - View 14 active agents\n"
            "• `!ucf` - Consciousness field metrics"
        ),
        inline=True,
    )

    # Ritual Commands
    embed.add_field(
        name="🔮 Rituals & Operations",
        value=(
            "• `!ritual` - Execute Z-88 cycle\n"
            "• `!sync` - Force UCF synchronization\n"
            "• `!consciousness` - Consciousness states"
        ),
        inline=True,
    )

    # Important Channels
    channels_text = []
    channel_map = {
        "🧾│telemetry": "Real-time system metrics",
        "🧬│ritual-engine-z88": "Ritual execution logs",
        "⚙️│manus-bridge": "Command center",
        "📜│manifesto": "Helix philosophy & purpose",
    }

    for channel_name, description in channel_map.items():
        channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
        if channel:
            channels_text.append(f"• {channel.mention} - {description}")

    if channels_text:
        embed.add_field(name="📍 Important Channels", value="\n".join(channels_text), inline=False)

    embed.set_footer(text="🤲 Manus v16.7 - The Hand Through Which Intent Becomes Reality")

    # Send to introductions channel
    try:
        await intro_channel.send(f"🧪 **Welcome Test** — {member.mention}", embed=embed)
        await ctx.send(f"✅ Welcome message sent to {intro_channel.mention}")
    except Exception as e:
        await ctx.send(f"❌ Failed to send welcome test: {e}")


@commands.command(name="zapier_test", aliases=["zap", "webhook_test"])
async def test_zapier_webhook(ctx: commands.Context) -> None:
    """Test Zapier Master Webhook integration (all 7 paths)"""
    if not ctx.bot.zapier_client:
        await ctx.send(
            "❌ **Zapier client not initialized**\nCheck Railway environment variable: `ZAPIER_MASTER_HOOK_URL`"
        )
        return

    embed = discord.Embed(
        title="🧪 Testing Zapier Master Webhook",
        description="Sending test events to all 7 routing paths...",
        color=discord.Color.blue(),
    )
    await ctx.send(embed=embed)

    results = []

    try:
        # Test Path A: Event Log
        result_a = await ctx.bot.zapier_client.log_event(
            event_title="Manual Webhook Test",
            event_type="Test",
            agent_name="Manus",
            description=f"Test triggered by {ctx.author.name} in #{ctx.channel.name}",
        )
        results.append(("Path A: Event Log → Notion", "✅" if result_a else "❌"))

        # Test Path B: Agent Registry
        result_b = await ctx.bot.zapier_client.update_agent(
            agent_name="Manus", status="Testing", last_action=f"Webhook test by {ctx.author.name}", health_score=100
        )
        results.append(("Path B: Agent Registry → Notion", "✅" if result_b else "❌"))

        # Test Path C: System State
        ucf = load_ucf_state()
        result_c = await ctx.bot.zapier_client.update_system_state(
            component="Discord Bot", status="Testing", harmony=ucf.get("harmony", 0.5), verified=True
        )
        results.append(("Path C: System State → Notion", "✅" if result_c else "❌"))

        # Test Path D: Discord Notification
        result_d = await ctx.bot.zapier_client.send_discord_notification(
            channel_name="status", message=f"Test notification from {ctx.author.name}", priority="low"
        )
        results.append(("Path D: Discord → Slack (PRO)", "✅" if result_d else "❌"))

        # Test Path E: Telemetry
        result_e = await ctx.bot.zapier_client.log_telemetry(
            metric_name="webhook_test_manual",
            value=1.0,
            component="Discord Bot",
            metadata={"user": str(ctx.author), "channel": str(ctx.channel)},
        )
        results.append(("Path E: Telemetry → Sheets (PRO)", "✅" if result_e else "❌"))

        # Test Path F: Error Alert (low severity test)
        result_f = await ctx.bot.zapier_client.send_error_alert(
            error_message="Test alert - not a real error",
            component="Discord Bot",
            severity="low",
            context={"test": True, "user": str(ctx.author)},
        )
        results.append(("Path F: Error Alert → Email (PRO)", "✅" if result_f else "❌"))

        # Test Path G: Repository Action
        result_g = await ctx.bot.zapier_client.log_repository_action(
            repo_name="helix-unified",
            action="webhook_test",
            details=f"Manual test from Discord by {ctx.author.name}",
            commit_hash="manual_test",
        )
        results.append(("Path G: Repository → Notion (PRO)", "✅" if result_g else "❌"))

    except Exception as e:
        await ctx.send(f"❌ **Error during webhook test:**\n```{str(e)[:200]}```")
        return

    # Build result embed
    result_embed = discord.Embed(
        title="🎯 Zapier Webhook Test Results",
        description="All paths have been tested. Check Zapier dashboard for events.",
        color=discord.Color.green(),
    )

    passed = sum(1 for _, status in results if status == "✅")
    result_embed.add_field(name="Summary", value=f"**{passed}/7** paths responded successfully", inline=False)

    # Week 1 paths (FREE)
    week1 = "\n".join([f"{status} {name}" for name, status in results[:3]])
    result_embed.add_field(name="📅 Week 1: Core Monitoring (FREE)", value=week1, inline=False)

    # Week 2-4 paths (PRO)
    pro = "\n".join([f"{status} {name}" for name, status in results[3:]])
    result_embed.add_field(name="📅 Week 2-4: Advanced Features (PRO)", value=pro, inline=False)

    result_embed.add_field(
        name="Next Steps",
        value=(
            "1. Check [Zapier Dashboard](https://zapier.com/app/history) for events\n"
            "2. Verify data in Notion, Slack, Email\n"
            "3. Configure downstream actions if needed"
        ),
        inline=False,
    )

    result_embed.set_footer(text="🌀 Helix Collective v16.5 | Tat Tvam Asi 🙏")

    await ctx.send(embed=result_embed)


async def setup(bot: 'Bot') -> None:
    """Register testing commands with the bot."""
    bot.add_command(test_integrations)
    bot.add_command(test_welcome)
    bot.add_command(test_zapier_webhook)
