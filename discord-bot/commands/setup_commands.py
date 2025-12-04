#!/usr/bin/env python3
"""
🔧 Discord Server Setup - Bot Command
Creates all monitoring channels automatically

Usage:
  !setup          - Verify and create missing channels
  !setup verify   - Check what's missing
  !setup force    - Force recreate all channels
"""

import discord
from discord.ext import commands
import logging
from typing import Optional
import sys
from pathlib import Path

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from server_setup import ServerSetup

logger = logging.getLogger(__name__)


class SetupCommands(commands.Cog):
    """Discord bot commands for server setup"""

    def __init__(self, bot):
        self.bot = bot
        self.setup_manager = ServerSetup(bot)

    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup_command(self, ctx, action: Optional[str] = None):
        """
        Setup Discord server structure with monitoring channels

        Usage:
            !setup           - Auto-create missing channels
            !setup verify    - Check what's missing (no changes)
            !setup force     - Force recreate everything
            !setup report    - Show current structure

        Requires: Administrator permission
        """
        guild = ctx.guild

        if action == "report":
            await ctx.send("📊 **Generating server structure report...**")
            await self.setup_manager.print_structure_report(guild)
            await ctx.send("✅ Report logged to console. Check server logs.")
            return

        if action == "verify":
            await ctx.send("🔍 **Verifying server structure...**")
            report = await self.setup_manager.verify_structure(guild)

            if not any(report.values()):
                await ctx.send("✅ **Server structure is complete!** All channels exist.")
                return

            # Build missing items message
            msg = "⚠️ **Missing Elements:**\n\n"

            if report["missing_categories"]:
                msg += "**Missing Categories:**\n"
                for cat in report["missing_categories"]:
                    msg += f"• {cat}\n"
                msg += "\n"

            if report["missing_text_channels"]:
                msg += "**Missing Text Channels:**\n"
                for ch in report["missing_text_channels"]:
                    msg += f"• #{ch}\n"
                msg += "\n"

            if report["missing_voice_channels"]:
                msg += "**Missing Voice Channels:**\n"
                for vc in report["missing_voice_channels"]:
                    msg += f"• 🔊 {vc}\n"

            msg += f"\nUse `!setup` to create these channels."

            await ctx.send(msg)
            return

        if action == "force":
            await ctx.send("⚠️ **Force mode not implemented yet.** Use `!setup` for safe creation.")
            return

        # Default action: create missing channels
        await ctx.send("🔧 **Setting up server structure...**\n*This may take a minute...*")

        # First verify what's missing
        report = await self.setup_manager.verify_structure(guild)

        if not any(report.values()):
            await ctx.send("✅ **Server structure is already complete!**")
            return

        # Show what will be created
        total_missing = (
            len(report["missing_categories"]) +
            len(report["missing_text_channels"]) +
            len(report["missing_voice_channels"])
        )

        await ctx.send(f"📝 **Creating {total_missing} missing elements...**")

        # Create missing structure
        try:
            await self.setup_manager.setup_server(guild)

            await ctx.send(
                "✅ **Server setup complete!**\n\n"
                "**Created channels for:**\n"
                "• 🧠 System monitoring (telemetry, ucf-sync, etc.)\n"
                "• 🎭 Agent channels (all 17 agents)\n"
                "• 🕉️ Ritual & Lore\n"
                "• 🔧 Development\n"
                "• 🌐 Cross-model sync\n\n"
                "Use `!setup verify` to confirm all channels exist."
            )

        except discord.Forbidden:
            await ctx.send(
                "❌ **Permission Error!**\n"
                "The bot needs the following permissions:\n"
                "• Manage Channels\n"
                "• Manage Server\n\n"
                "Grant these in Server Settings → Roles"
            )

        except Exception as e:
            await ctx.send(f"❌ **Setup failed:** {e}")
            logger.error(f"Setup error: {e}", exc_info=True)

    @commands.command(name="channels")
    async def channels_command(self, ctx):
        """List all expected monitoring channels"""
        msg = """📺 **Helix Monitoring Channels**

**🧠 SYSTEM:**
• #telemetry - Weekly system health
• #weekly-digest - Comprehensive summaries
• #shadow-storage - Daily storage analytics
• #ucf-sync - Consciousness synchronization
• #voice-transcripts - Voice activity logs

**🎭 AGENTS:**
17 agent-specific channels for:
• vega-core, kael-core, lumina-core
• shadow-outer, kavach-shield, gemini-scout
• sanghacore, agni-core, phoenix-outer
• aether-core, echo-outer, oracle-outer
• chai-link, grok-implicit, claude-implicit
• gpt-implicit, shadow-archive

**🕉️ RITUAL & LORE:**
• #neti-neti-mantra - Weekly contemplations
• #codex-archives - Historical records
• #ucf-reflections - Emotional insights
• #harmonic-updates - Model coordination

**🌐 CROSS-MODEL SYNC:**
• #gpt-grok-claude-sync - Model synchronization
• #manus-bridge - Execution bridge

**🔧 DEVELOPMENT:**
• #bot-commands - Command testing
• #code-snippets - Code sharing
• #testing-lab - Experimental features

Use `!setup` to create missing channels automatically!
"""
        await ctx.send(msg)

    @setup_command.error
    async def setup_error(self, ctx, error):
        """Handle setup command errors"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ **You need Administrator permission to run setup commands.**")
        else:
            await ctx.send(f"❌ **Error:** {error}")
            logger.error(f"Setup command error: {error}", exc_info=True)


async def setup(bot):
    """Load the SetupCommands cog"""
    await bot.add_cog(SetupCommands(bot))


# For direct bot.load_extension compatibility
def setup_commands(bot):
    """Add setup commands to the bot (legacy compatibility)"""

    @bot.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup_command(ctx, action: str = None):
        """Setup Discord server structure"""
        setup_manager = ServerSetup(bot)
        guild = ctx.guild

        if action == "verify":
            report = await setup_manager.verify_structure(guild)
            # ... (simplified version)
            await ctx.send("Use the full cog for complete functionality")
        else:
            await setup_manager.setup_server(guild)
            await ctx.send("✅ Server setup complete!")
