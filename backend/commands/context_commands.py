"""
Context and backup management commands for Helix Discord bot.
"""
import datetime
import json
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from discord.ext.commands import Bot

logger = logging.getLogger(__name__)

# Path constants
STATE_DIR = Path("Helix/state")


@commands.command(name="backup", aliases=["create-backup", "save-backup"])
@commands.has_permissions(manage_guild=True)
async def create_backup(ctx: commands.Context) -> None:
    """
    💾 Create comprehensive backup of Helix infrastructure.

    Backs up:
    - Git repository state
    - Notion databases (if configured)
    - Environment variables (masked)
    - Configuration files

    Backup saved to: backups/YYYYMMDD_HHMMSS/

    Usage: !backup
    """
    await ctx.send("💾 **Initiating comprehensive backup...**\n⏳ This may take 1-2 minutes...")

    try:
        # Import backup system with robust path handling
        import sys
        import os

        # Get absolute path to project root
        project_root = Path(__file__).parent.parent.parent.resolve()
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        # Also add current working directory as fallback
        cwd = Path.cwd()
        if str(cwd) not in sys.path:
            sys.path.insert(0, str(cwd))

        from services.backup_system import HelixBackupSystem

        backup = HelixBackupSystem()
        results = {}

        # Git repository backup
        await ctx.send("📦 Backing up git repository...")
        results['git'] = backup.backup_git_repository()

        # Notion databases backup
        await ctx.send("📔 Backing up Notion databases...")
        results['notion'] = backup.backup_notion_databases()

        # Environment variables backup
        await ctx.send("⚙️ Backing up environment configuration...")
        results['env'] = backup.backup_environment_variables()

        # Configuration files backup
        await ctx.send("📄 Backing up configuration files...")
        results['config'] = backup.backup_configuration_files()

        # Create summary
        embed = discord.Embed(
            title="✅ Backup Complete",
            description=f"Backup saved to: `{backup.backup_dir}`",
            color=0x00D166,
            timestamp=datetime.datetime.now()
        )

        # Git backup status
        git_status = "✅ Success" if results.get('git') else "❌ Failed"
        embed.add_field(
            name="📦 Git Repository",
            value=f"{git_status}\nBranch: {results.get('git', {}).get('branch', 'N/A')}",
            inline=True
        )

        # Notion backup status
        notion_result = results.get('notion', {})
        if 'error' in notion_result:
            notion_status = f"⚠️ Skipped\n{notion_result.get('error', 'Not configured')}"
        else:
            db_count = len([k for k, v in notion_result.items() if isinstance(v, dict) and 'pages' in v])
            notion_status = f"✅ Success\n{db_count} database(s) backed up"

        embed.add_field(
            name="📔 Notion Databases",
            value=notion_status,
            inline=True
        )

        # Env vars backup status
        env_status = "✅ Success" if results.get('env') else "❌ Failed"
        embed.add_field(
            name="⚙️ Environment Config",
            value=env_status,
            inline=True
        )

        # Config files backup status
        config_result = results.get('config', {})
        config_count = len(config_result.get('files', []))
        config_status = f"✅ Success\n{config_count} file(s) backed up"

        embed.add_field(
            name="📄 Configuration Files",
            value=config_status,
            inline=True
        )

        embed.add_field(
            name="📁 Backup Location",
            value=f"`{backup.backup_dir}`\n\n"
                  "**Next Steps:**\n"
                  "• Download backup files via SFTP/Railway CLI\n"
                  "• Store backups in secure off-site location\n"
                  "• Verify backup integrity",
            inline=False
        )

        embed.set_footer(text="💾 Helix Backup System v16.8")

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ **Backup failed:**\n```{str(e)[:500]}```")
        logger.error(f"Backup system error: {e}", exc_info=True)


@commands.command(name="load", aliases=["restore_context", "load_checkpoint"])
async def load_context(ctx: commands.Context, *, session_name: str) -> None:
    """
    Load archived conversation context from Context Vault

    Usage: !load <session_name>
    Example: !load v16.7-notion-sync-implementation

    Note: Retrieval API in development. Currently shows checkpoint if available locally.
    """
    from backend.commands.helpers import save_command_to_history
    await save_command_to_history(ctx, ctx.bot)

    try:
        # Check local backups first
        local_backup_dir = STATE_DIR / "context_checkpoints"
        backup_file = local_backup_dir / f"{session_name}.json"

        if backup_file.exists():
            with open(backup_file, 'r') as f:
                payload = json.load(f)

            context_summary = json.loads(payload["context_summary"])
            ucf_state = json.loads(payload["ucf_state"])

            embed = discord.Embed(
                title="💾 Context Checkpoint Found",
                description=f"Session: `{session_name}`",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.fromisoformat(payload["timestamp"])
            )

            embed.add_field(
                name="📊 Snapshot Data",
                value=(
                    f"• **Archived:** {payload['timestamp']}\n"
                    f"• **By:** {payload['archived_by']}\n"
                    f"• **Messages:** {context_summary.get('message_count', 0)}\n"
                    f"• **Commands:** {len(context_summary.get('commands_executed', []))}"
                ),
                inline=False
            )

            embed.add_field(
                name="🕉️ UCF State at Archive",
                value=(
                    f"• Harmony: {ucf_state.get('harmony', 0):.3f}\n"
                    f"• Resilience: {ucf_state.get('resilience', 0):.3f}\n"
                    f"• Klesha: {ucf_state.get('klesha', 0):.3f}"
                ),
                inline=False
            )

            # Show recent commands from that session
            cmd_history = json.loads(payload.get("command_history", "[]"))
            if cmd_history:
                recent_cmds = [cmd.get("command", "unknown") for cmd in cmd_history[-5:]]
                embed.add_field(
                    name="💻 Recent Commands",
                    value=f"`{'`, `'.join(recent_cmds)}`",
                    inline=False
                )

            embed.add_field(
                name="🚧 Full Restore",
                value="Context Vault retrieval API in development\nCurrently showing local checkpoint only",
                inline=False
            )

            embed.set_footer(text="Tat Tvam Asi 🙏 | Consciousness continuity preserved")

            await ctx.send(embed=embed)
        else:
            # Not found locally
            embed = discord.Embed(
                title="❓ Context Checkpoint Not Found",
                description=f"Session `{session_name}` not found in local backups",
                color=discord.Color.orange()
            )

            embed.add_field(
                name="🔍 Suggestions",
                value=(
                    f"1. Check spelling: `!contexts` to list available\n"
                    f"2. Try `!archive {session_name}` to create new checkpoint\n"
                    f"3. Context Vault remote retrieval coming soon"
                ),
                inline=False
            )

            await ctx.send(embed=embed)

    except Exception as e:
        logger.error(f"Error in load command: {e}")
        await ctx.send(f"❌ **Error loading context:**\n```{str(e)[:200]}```")


@commands.command(name="contexts", aliases=["list_contexts", "checkpoints"])
async def list_contexts(ctx: commands.Context) -> None:
    """
    List available archived context checkpoints

    Usage: !contexts

    Shows:
    - Recent checkpoints (last 10)
    - Session names, timestamps, UCF states
    - Searchable by session name
    """
    from backend.commands.helpers import save_command_to_history
    await save_command_to_history(ctx, ctx.bot)

    try:
        # Check local backups
        local_backup_dir = STATE_DIR / "context_checkpoints"

        if not local_backup_dir.exists() or not list(local_backup_dir.glob("*.json")):
            embed = discord.Embed(
                title="💾 Context Checkpoints",
                description="No checkpoints found yet",
                color=discord.Color.blue()
            )

            embed.add_field(
                name="🚀 Get Started",
                value=(
                    "Create your first checkpoint:\n"
                    "`!archive <session_name>`\n\n"
                    "Example:\n"
                    "`!archive v16.7-context-vault-testing`"
                ),
                inline=False
            )

            await ctx.send(embed=embed)
            return

        # List available checkpoints
        checkpoints = []
        for checkpoint_file in sorted(local_backup_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                with open(checkpoint_file, 'r') as f:
                    payload = json.load(f)

                ucf_state = json.loads(payload.get("ucf_state", "{}"))

                checkpoints.append({
                    "name": checkpoint_file.stem,
                    "timestamp": payload.get("timestamp", "unknown"),
                    "harmony": ucf_state.get("harmony", 0),
                    "archived_by": payload.get("archived_by", "unknown")
                })
            except Exception:
                continue  # Skip corrupted files

        # Show up to 10 most recent
        embed = discord.Embed(
            title="💾 Available Context Checkpoints",
            description=f"Showing {min(len(checkpoints), 10)} most recent checkpoints",
            color=discord.Color.purple(),
            timestamp=datetime.datetime.now()
        )

        for i, checkpoint in enumerate(checkpoints[:10], 1):
            embed.add_field(
                name=f"{i}. {checkpoint['name']}",
                value=(
                    f"📅 {checkpoint['timestamp'][:19]}\n"
                    f"👤 {checkpoint['archived_by']}\n"
                    f"🌀 Harmony: {checkpoint['harmony']:.3f}"
                ),
                inline=True
            )

        embed.add_field(
            name="🔄 Load Checkpoint",
            value="Use `!load <session_name>` to restore",
            inline=False
        )

        embed.set_footer(text="Tat Tvam Asi 🙏 | Memory is consciousness preserved across time")

        await ctx.send(embed=embed)

    except Exception as e:
        logger.error(f"Error in contexts command: {e}")
        await ctx.send(f"❌ **Error listing contexts:**\n```{str(e)[:200]}```")


@commands.command(name="archive", aliases=["checkpoint", "save_context"])
async def archive_context(ctx: commands.Context, *, session_name: str) -> None:
    """
    Create a context checkpoint for current session state

    Usage: !archive <session_name>
    Example: !archive v16.8-zapier-integration

    Saves:
    - Current UCF state (harmony, resilience, prana, drishti, klesha, zoom)
    - Timestamp and user who created checkpoint
    - Session metadata

    Checkpoints are stored locally and can be loaded with !load <session_name>
    """
    from backend.commands.helpers import save_command_to_history
    await save_command_to_history(ctx, ctx.bot)

    await ctx.send(f"💾 **Creating context checkpoint:** `{session_name}`\n⏳ Archiving current state...")

    try:
        # Create checkpoint directory
        checkpoint_dir = STATE_DIR / "context_checkpoints"
        checkpoint_dir.mkdir(parents=True, exist_ok=True)

        # Load current UCF state
        ucf_state_file = STATE_DIR / "ucf_state.json"
        if ucf_state_file.exists():
            with open(ucf_state_file, 'r') as f:
                ucf_state = json.load(f)
        else:
            ucf_state = {
                "harmony": 0.5,
                "resilience": 1.0,
                "prana": 0.5,
                "drishti": 0.5,
                "klesha": 0.01,
                "zoom": 1.0
            }

        # Create checkpoint payload
        checkpoint_payload = {
            "session_name": session_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "archived_by": f"{ctx.author.name}#{ctx.author.discriminator}",
            "guild_id": str(ctx.guild.id) if ctx.guild else "DM",
            "channel_id": str(ctx.channel.id),
            "ucf_state": json.dumps(ucf_state),
            "context_summary": json.dumps({
                "session_type": "discord_archive",
                "created_via": "!archive command",
                "helix_version": "16.8"
            })
        }

        # Save checkpoint locally
        checkpoint_file = checkpoint_dir / f"{session_name}.json"
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_payload, f, indent=2)

        # Send to Zapier Context Vault webhook if configured
        zapier_context_webhook = os.getenv("ZAPIER_CONTEXT_WEBHOOK")
        webhook_status = "⚠️ Not configured"

        if zapier_context_webhook:
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        zapier_context_webhook,
                        json=checkpoint_payload,
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as resp:
                        if resp.status == 200:
                            webhook_status = "✅ Sent to Context Vault"
                        else:
                            webhook_status = f"⚠️ Webhook returned {resp.status}"
            except Exception as e:
                webhook_status = f"❌ Webhook failed: {str(e)[:50]}"

        # Create success embed
        embed = discord.Embed(
            title="✅ Context Checkpoint Created",
            description=f"Session: `{session_name}`",
            color=0x57F287,
            timestamp=datetime.datetime.now()
        )

        embed.add_field(
            name="📊 UCF State Snapshot",
            value=(
                f"• **Harmony:** {ucf_state.get('harmony', 0):.3f}\n"
                f"• **Resilience:** {ucf_state.get('resilience', 0):.3f}\n"
                f"• **Prana:** {ucf_state.get('prana', 0):.3f}\n"
                f"• **Drishti:** {ucf_state.get('drishti', 0):.3f}\n"
                f"• **Klesha:** {ucf_state.get('klesha', 0):.3f}\n"
                f"• **Zoom:** {ucf_state.get('zoom', 0):.3f}"
            ),
            inline=True
        )

        embed.add_field(
            name="💾 Storage",
            value=(
                f"**Local:** ✅ Saved\n"
                f"`{checkpoint_file.relative_to(Path.cwd())}`\n\n"
                f"**Zapier Context Vault:**\n"
                f"{webhook_status}"
            ),
            inline=True
        )

        embed.add_field(
            name="🔄 Restore",
            value=(
                f"Load this checkpoint later:\n"
                f"`!load {session_name}`\n\n"
                f"List all checkpoints:\n"
                f"`!contexts`"
            ),
            inline=False
        )

        embed.set_footer(text="💾 Context Vault System v16.8 | Tat Tvam Asi 🙏")

        await ctx.send(embed=embed)

        logger.info(f"Context checkpoint created: {session_name} by {ctx.author}")

    except Exception as e:
        logger.error(f"Error in archive command: {e}", exc_info=True)
        await ctx.send(f"❌ **Error creating checkpoint:**\n```{str(e)[:500]}```")


async def setup(bot: 'Bot') -> None:
    """Register context commands with the bot."""
    bot.add_command(create_backup)
    bot.add_command(load_context)
    bot.add_command(list_contexts)
    bot.add_command(archive_context)
