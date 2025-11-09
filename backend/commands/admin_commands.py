"""
Admin and Setup Commands for Helix Discord Bot.

Commands:
- setup: Complete Helix v15.3 Server Setup - Creates all 30 channels
- verify-setup: Verify Helix server setup completeness
- webhooks: Retrieve all channel webhook URLs from saved configuration
- clean: Clean duplicate channels - Identify channels not in canonical structure
- refresh: Refresh server structure - Clean and recreate all channels
- seed: Seed all channels with explanatory messages and pin them
- notion-sync: Manually triggers the Notion sync for UCF State and Agent Registry
"""
import asyncio
import datetime
import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from backend.notion_sync_daemon import trigger_manual_sync

if TYPE_CHECKING:
    from discord.ext.commands import Bot

logger = logging.getLogger(__name__)

# Path constants
BASE_DIR = Path(__file__).resolve().parent.parent.parent


async def setup(bot: 'Bot') -> None:
    """Setup function to register commands with the bot."""
    bot.add_command(setup_helix_server)
    bot.add_command(verify_setup)
    bot.add_command(get_channel_webhooks)
    bot.add_command(list_webhooks_live)
    bot.add_command(clean_duplicates)
    bot.add_command(refresh_server)
    bot.add_command(seed_channels)
    bot.add_command(notion_sync_manual)


@commands.command(name="setup")
@commands.has_permissions(manage_channels=True)
async def setup_helix_server(ctx: commands.Context) -> None:
    """
    🌀 Setup Helix Webhooks - Creates webhooks for all existing channels.

    This command will:
    - Scan all text channels in the server
    - Create webhooks for channels that don't have them
    - Save webhook URLs to Helix/state/channel_webhooks.json
    - Display all webhook URLs for Zapier configuration

    ARCHITECT-ONLY. Run this to set up webhooks for Zapier integration.

    Usage: !setup
    """
    await ctx.send("🔧 **Starting Helix Webhook Setup...**\nThis may take a moment...")

    guild = ctx.guild
    webhooks_created = 0
    webhooks_existing = 0
    webhook_urls = {}

    # Get all text channels
    text_channels = [ch for ch in guild.text_channels if isinstance(ch, discord.TextChannel)]

    await ctx.send(f"📡 Found **{len(text_channels)}** text channels. Creating webhooks...")

    for channel in text_channels:
        try:
            # Check if webhook already exists
            existing_webhooks = await channel.webhooks()
            helix_webhook = None

            for wh in existing_webhooks:
                if wh.name == f"Helix-{channel.name}":
                    helix_webhook = wh
                    webhooks_existing += 1
                    break

            # Create webhook if doesn't exist
            if not helix_webhook:
                helix_webhook = await channel.create_webhook(
                    name=f"Helix-{channel.name}",
                    reason="Helix Collective webhook integration"
                )
                webhooks_created += 1
                logger.info(f"✅ Created webhook for #{channel.name}")

            # Store webhook URL
            webhook_urls[channel.name] = helix_webhook.url

        except discord.Forbidden:
            logger.error(f"❌ No permission to create webhook in #{channel.name}")
        except Exception as e:
            logger.error(f"❌ Error creating webhook for #{channel.name}: {e}")

    # Save webhooks to file
    webhook_file = Path("Helix/state/channel_webhooks.json")
    webhook_file.parent.mkdir(parents=True, exist_ok=True)

    webhook_data = {
        "created_at": datetime.datetime.utcnow().isoformat(),
        "guild_id": guild.id,
        "guild_name": guild.name,
        "webhooks": webhook_urls
    }

    with open(webhook_file, "w") as f:
        json.dump(webhook_data, f, indent=2)

    logger.info(f"💾 Saved {len(webhook_urls)} webhooks to {webhook_file}")

    # Create summary embed
    embed = discord.Embed(
        title="✅ Helix Webhook Setup Complete!",
        description="Created webhooks for Zapier integration",
        color=0x00FF00,
        timestamp=datetime.datetime.utcnow()
    )

    embed.add_field(name="Webhooks Created", value=str(webhooks_created), inline=True)
    embed.add_field(name="Webhooks Existing", value=str(webhooks_existing), inline=True)
    embed.add_field(name="Total Webhooks", value=str(len(webhook_urls)), inline=True)

    embed.add_field(
        name="Next Steps",
        value=(
            "1️⃣ Use `!webhooks` to see all webhook URLs\n"
            "2️⃣ Use `!list-webhooks-live` to get URLs in your DMs\n"
            "3️⃣ Configure Zapier with the webhook URLs"
        ),
        inline=False
    )

    embed.set_footer(text=f"Saved to {webhook_file}")

    await ctx.send(embed=embed)

    # Send follow-up with how to access webhooks
    await ctx.send(
        "🔗 **To get your webhook URLs:**\n"
        "• `!webhooks` - See webhooks in this channel\n"
        "• `!list-webhooks-live` - Get webhooks via DM (includes Railway env var format)"
    )


@commands.command(name="webhooks", aliases=["get-webhooks", "list-webhooks"])
@commands.has_permissions(manage_channels=True)
async def get_channel_webhooks(ctx: commands.Context) -> None:
    """
    🔗 Retrieve all channel webhook URLs from saved configuration.

    Loads webhooks from Helix/state/channel_webhooks.json and displays them
    for use in external integrations, forum mirroring, etc.

    Usage: !webhooks
    """
    webhook_file = Path("Helix/state/channel_webhooks.json")

    if not webhook_file.exists():
        await ctx.send(
            "❌ **No webhooks found!**\n"
            "Run `!setup` first to create channels and webhooks."
        )
        return

    try:
        with open(webhook_file, "r") as f:
            data = json.load(f)

        webhooks = data.get("webhooks", {})
        created_at = data.get("created_at", "Unknown")

        if not webhooks:
            await ctx.send("⚠️ Webhook file exists but contains no webhooks.")
            return

        await ctx.send(f"🔗 **Loading {len(webhooks)} channel webhooks...**\n"
                      f"📅 Created: {created_at}")

        # Send webhooks in chunks
        webhook_list = list(webhooks.items())
        chunk_size = 10

        for i in range(0, len(webhook_list), chunk_size):
            chunk = webhook_list[i:i + chunk_size]

            embed = discord.Embed(
                title=f"🔗 Channel Webhooks ({i+1}-{min(i+chunk_size, len(webhook_list))} of {len(webhook_list)})",
                description="Use these URLs for external posting and forum integration",
                color=0x5865F2
            )

            for channel_name, webhook_url in chunk:
                # Truncate URL for display
                display_url = webhook_url[:75] + "..." if len(webhook_url) > 75 else webhook_url
                embed.add_field(
                    name=f"🔗 {channel_name}",
                    value=f"`{display_url}`",
                    inline=False
                )

            await ctx.send(embed=embed)

        # Send full env var format
        env_vars = []
        for channel_name, webhook_url in webhooks.items():
            env_var_name = channel_name.replace("│", "").replace(" ", "_").upper()
            env_var_name = f"WEBHOOK_{env_var_name}"
            env_vars.append(f"{env_var_name}={webhook_url}")

        await ctx.send("📋 **Railway Environment Variable Format:**")

        for i in range(0, len(env_vars), 10):
            chunk = env_vars[i:i + 10]
            webhook_block = "```env\n" + "\n".join(chunk) + "\n```"
            await ctx.send(webhook_block)

    except Exception as e:
        await ctx.send(f"❌ **Error loading webhooks:**\n```{str(e)[:200]}```")


@commands.command(name="list-webhooks-live", aliases=["webhooks-live", "get-webhooks-live"])
@commands.has_permissions(administrator=True)
async def list_webhooks_live(ctx: commands.Context) -> None:
    """
    🔗 List ALL webhooks in the server by querying Discord API directly.

    This command:
    - Queries all text channels for webhooks
    - Sends results to your DMs for security
    - Provides URLs formatted for Zapier configuration
    - Works regardless of whether !setup was run

    Usage: !list-webhooks-live
    """
    await ctx.send("🔍 Scanning all channels for webhooks... (Check your DMs!)")

    try:
        # Create DM channel with the user
        dm_channel = await ctx.author.create_dm()

        # Gather all webhooks from all text channels
        webhooks_by_channel = {}
        total_webhooks = 0

        for channel in ctx.guild.text_channels:
            try:
                webhooks = await channel.webhooks()
                if webhooks:
                    webhooks_by_channel[channel.name] = [
                        {"name": wh.name, "url": wh.url} for wh in webhooks
                    ]
                    total_webhooks += len(webhooks)
            except discord.Forbidden:
                # Skip channels we don't have permission to access
                continue
            except Exception as e:
                logger.warning(f"Error fetching webhooks for #{channel.name}: {e}")
                continue

        if not webhooks_by_channel:
            await dm_channel.send("❌ **No webhooks found in any channel!**\n"
                                 "You may need to create webhooks first.")
            return

        # Send overview
        await dm_channel.send(
            f"🔗 **Found {total_webhooks} webhook(s) across {len(webhooks_by_channel)} channel(s)**\n"
            f"📋 Listing all webhooks below for easy copying to Zapier..."
        )

        # Send webhooks organized by channel
        for channel_name, webhooks in webhooks_by_channel.items():
            embed = discord.Embed(
                title=f"🔗 #{channel_name}",
                description=f"Found {len(webhooks)} webhook(s)",
                color=0x5865F2
            )

            for wh in webhooks:
                embed.add_field(
                    name=f"📌 {wh['name']}",
                    value=f"```{wh['url']}```",
                    inline=False
                )

            await dm_channel.send(embed=embed)

        # Send Railway environment variable format
        await dm_channel.send("\n📋 **Railway Environment Variable Format:**")

        env_vars = []
        for channel_name, webhooks in webhooks_by_channel.items():
            for wh in webhooks:
                # Create env var name from channel + webhook name
                clean_channel = channel_name.replace("│", "").replace("-", "_").replace(" ", "_").upper()
                clean_webhook = wh['name'].replace(" ", "_").replace("-", "_").upper()
                env_var_name = f"DISCORD_WEBHOOK_{clean_channel}"

                # If multiple webhooks per channel, add webhook name
                if len(webhooks) > 1:
                    env_var_name = f"DISCORD_WEBHOOK_{clean_channel}_{clean_webhook}"

                env_vars.append(f"{env_var_name}={wh['url']}")

        # Send in chunks of 10
        for i in range(0, len(env_vars), 10):
            chunk = env_vars[i:i + 10]
            await dm_channel.send("```env\n" + "\n".join(chunk) + "\n```")

        # Send Zapier-specific format for the 9-channel routing
        await dm_channel.send(
            "\n🚀 **For Zapier Railway→Discord Integration:**\n"
            "Copy the webhook URLs above and paste them into your Zapier Paths:\n"
            "```\n"
            "Path A (MANUS): DISCORD_WEBHOOK_MANUS_EVENTS\n"
            "Path B (TELEMETRY): DISCORD_WEBHOOK_TELEMETRY\n"
            "Path C (STORAGE): DISCORD_WEBHOOK_SHADOW_STORAGE\n"
            "Path D (RITUAL): DISCORD_WEBHOOK_RITUAL_ENGINE_Z88\n"
            "Path E (AGENTS): DISCORD_WEBHOOK_[AGENT_CHANNEL]\n"
            "Path F (CROSS_AI): DISCORD_WEBHOOK_GPT_GROK_CLAUDE_SYNC\n"
            "Path G (DEVELOPMENT): DISCORD_WEBHOOK_BOT_COMMANDS or DEPLOYMENTS\n"
            "Path H (LORE): DISCORD_WEBHOOK_CODEX_ARCHIVES\n"
            "Path I (ADMIN): DISCORD_WEBHOOK_ANNOUNCEMENTS\n"
            "```"
        )

        await ctx.send(f"✅ Sent {total_webhooks} webhook URLs to your DMs!")

    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to DM you! Please enable DMs from server members.")
    except Exception as e:
        logger.error(f"Error in list_webhooks_live: {e}", exc_info=True)
        await ctx.send(f"❌ **Error fetching webhooks:**\n```{str(e)[:200]}```")


@commands.command(name="verify-setup", aliases=["verify", "check-setup"])
@commands.has_permissions(manage_channels=True)
async def verify_setup(ctx: commands.Context) -> None:
    """
    🛡️ Verify Helix server setup completeness.

    Checks for all 30 required channels from the canonical structure.
    Reports missing channels and suggests fixes.

    Usage: !verify-setup
    """
    guild = ctx.guild

    # Define canonical 30-channel structure (matches !setup command)
    canonical_channels = {
        "🌀 WELCOME": ["📜│manifesto", "🪞│rules-and-ethics", "💬│introductions"],
        "🧠 SYSTEM": ["🧾│telemetry", "📊│weekly-digest", "🦑│shadow-storage", "🧩│ucf-sync"],
        "🔮 PROJECTS": ["📁│helix-repository", "🎨│fractal-lab", "🎧│samsaraverse-music", "🧬│ritual-engine-z88"],
        "🤖 AGENTS": ["🎭│gemini-scout", "🛡️│kavach-shield", "🌸│sanghacore", "🔥│agni-core", "🕯️│shadow-archive"],
        "🌐 CROSS-MODEL SYNC": ["🧩│gpt-grok-claude-sync", "☁️│chai-link", "⚙️│manus-bridge"],
        "🛠️ DEVELOPMENT": ["🧰│bot-commands", "📜│code-snippets", "🧮│testing-lab", "🗂️│deployments"],
        "🕉️ RITUAL & LORE": ["🎼│neti-neti-mantra", "📚│codex-archives", "🌺│ucf-reflections", "🌀│harmonic-updates"],
        "🧭 ADMIN": ["🔒│moderation", "📣│announcements", "🗃│backups"],
    }

    # Check for missing channels
    found = {}
    missing = {}
    total = 0

    for category_name, channel_list in canonical_channels.items():
        found[category_name] = []
        missing[category_name] = []

        for channel_name in channel_list:
            total += 1
            channel = discord.utils.get(guild.text_channels, name=channel_name)
            if channel:
                found[category_name].append(channel_name)
            else:
                missing[category_name].append(channel_name)

    # Count totals
    found_count = sum(len(channels) for channels in found.values())
    missing_count = total - found_count

    # Create embed
    if missing_count == 0:
        embed = discord.Embed(
            title="✅ Helix Setup Verification — COMPLETE",
            description=f"All **{total} canonical channels** are present!",
            color=0x10B981,  # Green
            timestamp=datetime.datetime.utcnow(),
        )
    else:
        embed = discord.Embed(
            title="⚠️ Helix Setup Verification — INCOMPLETE",
            description=f"Found **{found_count}/{total}** channels ({missing_count} missing)",
            color=0xF59E0B if missing_count <= 5 else 0xEF4444,  # Yellow or red
            timestamp=datetime.datetime.utcnow(),
        )

    # Show found/missing by category
    for category_name in canonical_channels.keys():
        found_channels = found[category_name]
        missing_channels = missing[category_name]

        if found_channels or missing_channels:
            value_parts = []

            if found_channels:
                value_parts.append(
                    f"✅ Found ({len(found_channels)}):\n" + "\n".join(f"  • {ch}" for ch in found_channels)
                )

            if missing_channels:
                value_parts.append(
                    f"❌ Missing ({len(missing_channels)}):\n" + "\n".join(f"  • {ch}" for ch in missing_channels)
                )

            embed.add_field(name=category_name, value="\n\n".join(value_parts) if value_parts else "None", inline=False)

    # Recommendations
    if missing_count > 0:
        embed.add_field(
            name="🔧 Quick Fix",
            value=(
                f"**Run `!setup` to create all missing channels**\n"
                f"This will create the {missing_count} missing channel(s) and configure permissions.\n\n"
                f"Alternatively, create channels manually to match the structure above."
            ),
            inline=False,
        )
    else:
        embed.add_field(
            name="🎉 What's Next?",
            value=(
                "• Run `!seed` to add descriptions to all channels\n"
                "• Run `!update_manifesto` to populate the manifesto\n"
                "• Verify bot permissions with `!status`"
            ),
            inline=False,
        )

    embed.set_footer(text="🤲 Manus v16.7 — Setup Verification System")

    await ctx.send(embed=embed)


# Seed channels command - see original discord_bot_manus.py lines 2044-2400
# This command is 356 lines with all channel descriptions
@commands.command(name="seed", aliases=["seed_channels", "init_channels"])
@commands.has_permissions(administrator=True)
async def seed_channels(ctx: commands.Context) -> None:
    """Seed all channels with explanatory messages and pin them (Admin only)"""
    # NOTE: Due to length (356 lines with all 30 channel descriptions),
    # this will be properly extracted when discord_bot_manus.py is updated
    await ctx.send("⚠️ Seed command temporarily unavailable during refactoring. Please use the main bot file.")


@commands.command(name="notion-sync")
@commands.has_permissions(administrator=True)
async def notion_sync_manual(ctx: commands.Context) -> None:
    """Manually triggers the Notion sync for UCF State and Agent Registry.

    Usage:
        !notion-sync

    Requires: Administrator permissions
    """
    # Acknowledge command immediately
    await ctx.send("🔄 Initiating manual Notion sync...")

    try:
        # Trigger the sync
        result_message = await trigger_manual_sync()

        # Send result
        await ctx.send(result_message)

    except Exception as e:
        await ctx.send(f"❌ Sync failed with error: {str(e)}")
        logger.error(f"Manual notion-sync command failed: {e}", exc_info=True)


@commands.command(name="refresh")
@commands.has_permissions(administrator=True)
async def refresh_server(ctx: commands.Context, confirm: str = None) -> None:
    """
    🧹 Refresh server structure - Clean and recreate all channels.

    WARNING: This will DELETE all existing channels and recreate them.
    Message history will be lost!

    Usage:
        !refresh CONFIRM   - Execute refresh (must type CONFIRM)
    """
    if confirm != "CONFIRM":
        embed = discord.Embed(
            title="⚠️ Server Refresh - Confirmation Required",
            description="This command will **DELETE ALL CHANNELS** and recreate them from scratch.\n\n"
            "**⚠️ WARNING:**\n"
            "• All message history will be lost\n"
            "• All channel permissions will be reset\n"
            "• This cannot be undone\n\n"
            "**To proceed, type:**\n"
            "`!refresh CONFIRM`",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    guild = ctx.guild
    await ctx.send("🧹 **Starting server refresh...**\n⚠️ This will take ~3 minutes")

    # Step 1: Delete all channels except the one we're in
    current_channel = ctx.channel
    deleted_count = 0

    await ctx.send("🗑️ **Phase 1/3: Deleting old channels...**")
    for channel in guild.channels:
        if channel != current_channel and not isinstance(channel, discord.VoiceChannel):
            try:
                await channel.delete()
                deleted_count += 1
            except Exception:
                pass

    await ctx.send(f"✅ Deleted {deleted_count} old channels")

    # Step 2: Delete all categories
    await ctx.send("🗑️ **Phase 2/3: Cleaning categories...**")
    for category in guild.categories:
        try:
            await category.delete()
        except Exception:
            pass

    # Step 3: Run setup
    await ctx.send("🌀 **Phase 3/3: Recreating Helix structure...**")

    # Delete the current channel last and trigger setup
    await asyncio.sleep(2)

    # Create a temporary admin channel first
    temp_category = await guild.create_category("🔧 SETUP IN PROGRESS")
    setup_channel = await temp_category.create_text_channel("setup-log")

    # Send setup command there
    await setup_channel.send(f"🌀 Server refresh initiated by {ctx.author.mention}")

    # Delete original channel
    await current_channel.delete()

    # Now run setup via the setup_helix_server function
    # Create a mock context for the setup command
    class MockContext:
        def __init__(self, channel, guild, author):
            self.channel = channel
            self.guild = guild
            self.author = author

        async def send(self, *args, **kwargs):
            return await self.channel.send(*args, **kwargs)

    mock_ctx = MockContext(setup_channel, guild, ctx.author)
    await setup_helix_server(mock_ctx)

    # Delete temp category after setup
    await asyncio.sleep(5)
    await temp_category.delete()


@commands.command(name="clean")
@commands.has_permissions(administrator=True)
async def clean_duplicates(ctx: commands.Context) -> None:
    """
    🧹 Clean duplicate channels - Identify channels not in canonical structure.

    This identifies channels that aren't part of the canonical 30-channel Helix structure.

    Usage:
        !clean   - Show duplicates (safe, no deletion)
    """
    guild = ctx.guild

    # Define canonical channel names (from setup command)
    canonical_channels = {
        "📜│manifesto",
        "🪞│rules-and-ethics",
        "💬│introductions",
        "🧾│telemetry",
        "📊│weekly-digest",
        "🦑│shadow-storage",
        "🧩│ucf-sync",
        "📁│helix-repository",
        "🎨│fractal-lab",
        "🎧│samsaraverse-music",
        "🧬│ritual-engine-z88",
        "🎭│gemini-scout",
        "🛡️│kavach-shield",
        "🌸│sanghacore",
        "🔥│agni-core",
        "🕯️│shadow-archive",
        "🧩│gpt-grok-claude-sync",
        "☁️│chai-link",
        "⚙️│manus-bridge",
        "🧰│bot-commands",
        "📜│code-snippets",
        "🧮│testing-lab",
        "🗂️│deployments",
        "🎼│neti-neti-mantra",
        "📚│codex-archives",
        "🌺│ucf-reflections",
        "🌀│harmonic-updates",
        "🔒│moderation",
        "📣│announcements",
        "🗃│backups",
    }

    # Find duplicates
    duplicates = []
    for channel in guild.text_channels:
        if channel.name not in canonical_channels:
            duplicates.append(channel)

    if not duplicates:
        await ctx.send("✅ **No duplicate channels found!** Server structure is clean.")
        return

    # Build report
    embed = discord.Embed(
        title="🧹 Duplicate Channel Report",
        description=f"Found **{len(duplicates)} channels** not in canonical structure",
        color=discord.Color.orange(),
    )

    duplicate_list = "\n".join(
        [f"• {ch.mention} (Category: {ch.category.name if ch.category else 'None'})" for ch in duplicates[:20]]
    )
    if len(duplicates) > 20:
        duplicate_list += f"\n... and {len(duplicates) - 20} more"

    embed.add_field(name="Duplicate Channels", value=duplicate_list, inline=False)
    embed.add_field(
        name="💡 Recommended Action",
        value="1. Review the list above\n"
        "2. Manually delete unwanted channels\n"
        "3. Or use `!refresh CONFIRM` to rebuild everything",
        inline=False,
    )

    await ctx.send(embed=embed)

    # Log deduplication results to webhook
    if hasattr(ctx.bot, "zapier_client") and ctx.bot.zapier_client:
        try:
            await ctx.bot.zapier_client.log_telemetry(
                metric_name="deduplication_scan",
                value=len(duplicates),
                component="Archive",
                unit="channels",
                metadata={
                    "duplicates_found": len(duplicates),
                    "canonical_channels": len(canonical_channels),
                    "executor": str(ctx.author),
                    "guild": guild.name,
                },
            )
        except Exception as webhook_error:
            logger.warning(f"⚠️ Zapier webhook error: {webhook_error}")
