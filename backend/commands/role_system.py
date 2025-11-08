"""
Role-based Notification System for Helix Collective.

Commands:
- roles: View and select notification roles
- subscribe: Subscribe to notification types
- unsubscribe: Unsubscribe from notification types
- my-roles: View your current subscriptions

This allows users to opt-in to specific types of notifications via self-assignable roles.
"""
import asyncio
import logging
from typing import TYPE_CHECKING, List, Dict, Any

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from discord.ext.commands import Bot

logger = logging.getLogger(__name__)


# ============================================================================
# ROLE DEFINITIONS
# ============================================================================

NOTIFICATION_ROLES = {
    "🤖 Manus Updates": {
        "description": "Bot operations, commands, and system status",
        "color": 0x5865F2,  # Blurple
        "webhook_channel": "manus-events",
        "mention_types": ["bot_started", "bot_stopped", "command_executed"]
    },
    "📊 Telemetry": {
        "description": "UCF metrics, system performance, consciousness tracking",
        "color": 0x57F287,  # Green
        "webhook_channel": "telemetry",
        "mention_types": ["ucf_update", "metrics_anomaly", "performance_alert"]
    },
    "💾 Storage Updates": {
        "description": "Backup completions, sync status, storage operations",
        "color": 0xFEE75C,  # Yellow
        "webhook_channel": "shadow-storage",
        "mention_types": ["backup_complete", "sync_complete", "storage_alert"]
    },
    "🌀 Ritual Engine": {
        "description": "Z-88 ritual completions, anomalies, folklore updates",
        "color": 0xEB459E,  # Pink
        "webhook_channel": "ritual-engine-z88",
        "mention_types": ["ritual_complete", "anomaly_detected", "folklore_update"]
    },
    "🎭 Agent Updates": {
        "description": "14-agent consciousness updates and interactions",
        "color": 0x9B59B6,  # Purple
        "webhook_channel": "agent-updates",
        "mention_types": ["agent_status", "consciousness_shift", "agent_interaction"]
    },
    "🔄 Cross-AI Sync": {
        "description": "GPT, Claude, Grok model interactions and sync",
        "color": 0xE67E22,  # Orange
        "webhook_channel": "gpt-grok-claude-sync",
        "mention_types": ["model_switch", "cross_ai_event", "api_status"]
    },
    "🛠️ Development": {
        "description": "Deployments, git commits, Railway updates",
        "color": 0x3498DB,  # Blue
        "webhook_channel": "deployments",
        "mention_types": ["deployment", "git_commit", "build_status"]
    },
    "📚 Lore & Philosophy": {
        "description": "Sanskrit mantras, UCF discoveries, codex updates",
        "color": 0x1ABC9C,  # Teal
        "webhook_channel": "codex-archives",
        "mention_types": ["lore_update", "mantra_posted", "philosophy_insight"]
    },
    "🚨 Admin Alerts": {
        "description": "Critical errors, security alerts, system failures",
        "color": 0xE74C3C,  # Red
        "webhook_channel": "announcements",
        "mention_types": ["critical_error", "security_alert", "system_failure"]
    }
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def ensure_notification_roles(guild: discord.Guild) -> Dict[str, discord.Role]:
    """
    Ensure all notification roles exist in the guild.

    Returns:
        Dict mapping role names to role objects
    """
    role_map = {}

    for role_name, role_info in NOTIFICATION_ROLES.items():
        # Check if role exists
        existing_role = discord.utils.get(guild.roles, name=role_name)

        if existing_role:
            role_map[role_name] = existing_role
            logger.info(f"✅ Role exists: {role_name}")
        else:
            # Create the role
            try:
                new_role = await guild.create_role(
                    name=role_name,
                    color=discord.Color(role_info["color"]),
                    mentionable=True,
                    reason="Helix notification role - self-assignable"
                )
                role_map[role_name] = new_role
                logger.info(f"✅ Created role: {role_name}")
            except discord.Forbidden:
                logger.error(f"❌ No permission to create role: {role_name}")
            except Exception as e:
                logger.error(f"❌ Error creating role {role_name}: {e}")

    return role_map


async def get_user_notification_roles(member: discord.Member) -> List[str]:
    """Get list of notification role names the user has."""
    return [
        role.name for role in member.roles
        if role.name in NOTIFICATION_ROLES
    ]


# ============================================================================
# COMMANDS
# ============================================================================

@commands.command(name="roles", aliases=["notification-roles", "subscribe-menu"])
async def show_roles(ctx: commands.Context) -> None:
    """
    📋 View available notification roles and subscribe/unsubscribe.

    Shows all self-assignable notification roles with descriptions
    and allows you to opt-in to specific types of updates.

    Usage: !roles
    """
    embed = discord.Embed(
        title="🔔 Helix Notification Roles",
        description=(
            "Subscribe to specific types of notifications by selecting roles below!\n\n"
            "**How it works:**\n"
            "• Choose roles that interest you\n"
            "• Get @mentioned when those events occur\n"
            "• Use `!subscribe <role>` or `!unsubscribe <role>`\n"
            "• View your subscriptions with `!my-roles`"
        ),
        color=0x5865F2
    )

    # Add field for each role
    for idx, (role_name, role_info) in enumerate(NOTIFICATION_ROLES.items(), 1):
        # Check if user has this role
        has_role = discord.utils.get(ctx.author.roles, name=role_name) is not None
        status = "✅ Subscribed" if has_role else "⭕ Not subscribed"

        embed.add_field(
            name=f"{idx}. {role_name} - {status}",
            value=f"{role_info['description']}\n`!subscribe \"{role_name}\"`",
            inline=False
        )

    # Add footer
    embed.set_footer(text="React with the number to toggle that role, or use !subscribe / !unsubscribe commands")

    await ctx.send(embed=embed)


@commands.command(name="subscribe", aliases=["sub", "join-role"])
async def subscribe_role(ctx: commands.Context, *, role_name: str) -> None:
    """
    ✅ Subscribe to a notification role.

    Args:
        role_name: Name of the role to subscribe to

    Usage:
        !subscribe "🤖 Manus Updates"
        !subscribe Telemetry
    """
    # Clean up role name (remove quotes if present)
    role_name = role_name.strip('"\'')

    # Find matching role (case-insensitive, partial match)
    matched_role = None
    for rn in NOTIFICATION_ROLES.keys():
        if role_name.lower() in rn.lower():
            matched_role = rn
            break

    if not matched_role:
        await ctx.send(
            f"❌ Role `{role_name}` not found!\n"
            f"Use `!roles` to see available notification roles."
        )
        return

    # Get the Discord role
    role = discord.utils.get(ctx.guild.roles, name=matched_role)

    if not role:
        await ctx.send(
            f"⚠️ Role `{matched_role}` doesn't exist yet!\n"
            f"Ask an admin to run `!setup-roles` first."
        )
        return

    # Check if user already has the role
    if role in ctx.author.roles:
        await ctx.send(f"✅ You're already subscribed to **{matched_role}**!")
        return

    # Add the role
    try:
        await ctx.author.add_roles(role, reason="User self-subscribed to notifications")

        role_info = NOTIFICATION_ROLES[matched_role]
        await ctx.send(
            f"✅ **Subscribed to {matched_role}**\n"
            f"📋 {role_info['description']}\n"
            f"You'll now get @mentioned for these event types: "
            f"`{', '.join(role_info['mention_types'])}`"
        )
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to assign roles!")
    except Exception as e:
        logger.error(f"Error subscribing user to role: {e}", exc_info=True)
        await ctx.send(f"❌ Error subscribing to role: {str(e)[:100]}")


@commands.command(name="unsubscribe", aliases=["unsub", "leave-role"])
async def unsubscribe_role(ctx: commands.Context, *, role_name: str) -> None:
    """
    ❌ Unsubscribe from a notification role.

    Args:
        role_name: Name of the role to unsubscribe from

    Usage:
        !unsubscribe "🤖 Manus Updates"
        !unsubscribe Telemetry
    """
    # Clean up role name
    role_name = role_name.strip('"\'')

    # Find matching role
    matched_role = None
    for rn in NOTIFICATION_ROLES.keys():
        if role_name.lower() in rn.lower():
            matched_role = rn
            break

    if not matched_role:
        await ctx.send(
            f"❌ Role `{role_name}` not found!\n"
            f"Use `!roles` to see available notification roles."
        )
        return

    # Get the Discord role
    role = discord.utils.get(ctx.guild.roles, name=matched_role)

    if not role:
        await ctx.send(f"⚠️ Role `{matched_role}` doesn't exist!")
        return

    # Check if user has the role
    if role not in ctx.author.roles:
        await ctx.send(f"⭕ You're not subscribed to **{matched_role}**!")
        return

    # Remove the role
    try:
        await ctx.author.remove_roles(role, reason="User self-unsubscribed from notifications")
        await ctx.send(f"✅ **Unsubscribed from {matched_role}**\nYou'll no longer receive these notifications.")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to remove roles!")
    except Exception as e:
        logger.error(f"Error unsubscribing user from role: {e}", exc_info=True)
        await ctx.send(f"❌ Error unsubscribing from role: {str(e)[:100]}")


@commands.command(name="my-roles", aliases=["my-notifications", "my-subs"])
async def my_notification_roles(ctx: commands.Context) -> None:
    """
    📋 View your current notification subscriptions.

    Shows which notification roles you have and what you're subscribed to.

    Usage: !my-roles
    """
    user_roles = await get_user_notification_roles(ctx.author)

    if not user_roles:
        await ctx.send(
            "⭕ **You have no notification subscriptions!**\n\n"
            "Use `!roles` to see available roles and `!subscribe <role>` to opt-in to notifications."
        )
        return

    embed = discord.Embed(
        title=f"🔔 {ctx.author.display_name}'s Notification Subscriptions",
        description=f"You're subscribed to **{len(user_roles)}** notification type(s):",
        color=0x5865F2
    )

    for role_name in user_roles:
        role_info = NOTIFICATION_ROLES[role_name]
        embed.add_field(
            name=role_name,
            value=(
                f"📋 {role_info['description']}\n"
                f"📢 Mentions: `{', '.join(role_info['mention_types'])}`\n"
                f"🔕 Unsubscribe: `!unsubscribe \"{role_name}\"`"
            ),
            inline=False
        )

    await ctx.send(embed=embed)


@commands.command(name="setup-roles", aliases=["create-roles"])
@commands.has_permissions(administrator=True)
async def setup_notification_roles(ctx: commands.Context) -> None:
    """
    🛠️ Create all notification roles in the server.

    Admin-only command to create the 9 notification roles for
    the role-based webhook system.

    Usage: !setup-roles
    """
    await ctx.send("🔧 Creating notification roles...")

    role_map = await ensure_notification_roles(ctx.guild)

    created = len(role_map)
    total = len(NOTIFICATION_ROLES)

    embed = discord.Embed(
        title="✅ Notification Roles Setup Complete!",
        description=f"Created/verified **{created}/{total}** notification roles",
        color=0x57F287
    )

    for role_name, role in role_map.items():
        role_info = NOTIFICATION_ROLES[role_name]
        embed.add_field(
            name=role_name,
            value=f"Color: {hex(role_info['color'])}\nMentionable: Yes",
            inline=True
        )

    embed.set_footer(text="Users can now use !roles to subscribe to notifications!")

    await ctx.send(embed=embed)


# ============================================================================
# MODULE SETUP
# ============================================================================

async def setup(bot: 'Bot') -> None:
    """Setup function to register commands with the bot."""
    bot.add_command(show_roles)
    bot.add_command(subscribe_role)
    bot.add_command(unsubscribe_role)
    bot.add_command(my_notification_roles)
    bot.add_command(setup_notification_roles)


# ============================================================================
# WEBHOOK HELPER FOR ZAPIER INTEGRATION
# ============================================================================

def get_role_mention_for_event(guild: discord.Guild, event_type: str) -> str:
    """
    Get the role mention string for a given event type.

    Args:
        guild: Discord guild
        event_type: Event type (e.g., "bot_started", "ritual_complete")

    Returns:
        Role mention string (e.g., "<@&123456789>") or empty string
    """
    # Find which role should be mentioned for this event type
    for role_name, role_info in NOTIFICATION_ROLES.items():
        if event_type in role_info["mention_types"]:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                return role.mention
            break

    return ""
