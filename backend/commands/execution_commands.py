"""
Execution Commands for Helix Discord Bot.

Commands:
- ritual: Execute Z-88 ritual with async non-blocking engine
- run: Execute a command through Manus with Kavach ethical scanning
- halt: Halt Manus operations (admin only)
"""

import asyncio
import datetime
import logging
import os
from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from backend.z88_ritual_engine import execute_ritual, load_ucf_state

from backend.commands.helpers import kavach_ethical_scan, log_to_shadow, queue_directive

if TYPE_CHECKING:
    from discord.ext.commands import Bot

logger = logging.getLogger(__name__)

# Get Architect ID from environment
try:
    ARCHITECT_ID = int(os.getenv("ARCHITECT_ID", "0"))
except (ValueError, TypeError):
    # Handle placeholder values or invalid format
    ARCHITECT_ID = 0


async def setup(bot: 'Bot') -> None:
    """Setup function to register commands with the bot."""
    bot.add_command(manus_run)
    bot.add_command(ritual_cmd)
    bot.add_command(manus_halt)


@commands.command(name="run")
@commands.cooldown(1, 60, commands.BucketType.user)  # 1 use per 60 seconds per user
async def manus_run(ctx: commands.Context, *, command: str) -> None:
    """Execute a command through Manus with Kavach ethical scanning"""

    # Perform ethical scan
    scan_result = kavach_ethical_scan(command)

    if not scan_result["approved"]:
        # Command blocked
        embed = discord.Embed(
            title="🛡️ Kavach Blocked Command", description=scan_result["reasoning"], color=discord.Color.red()
        )
        embed.add_field(name="Command", value=f"```{command}```", inline=False)
        embed.set_footer(text="Ethical safeguards active")

        await ctx.send(embed=embed)
        return

    # Command approved
    await ctx.send(f"✅ **Command approved by Kavach**\nExecuting: `{command}`")

    # Queue directive for Manus
    directive = {
        "command": command,
        "timestamp": datetime.datetime.now().isoformat(),
        "source": "Discord",
        "user": str(ctx.author),
        "user_id": ctx.author.id,
        "channel": str(ctx.channel),
        "scan_result": scan_result,
    }

    queue_directive(directive)
    log_to_shadow("operations", directive)

    await ctx.send("📋 **Directive queued for Manus execution**")


@commands.command(name="ritual")
async def ritual_cmd(ctx: commands.Context, steps: int = 108) -> None:
    """
    Execute Z-88 ritual with async non-blocking engine.
    Steps: 1–1000 (default 108)
    """
    if not (1 <= steps <= 1000):
        await ctx.send("**Invalid step count**\nMust be 1–1000")
        return

    ucf_before = load_ucf_state()
    msg = await ctx.send(f"**Initiating Z-88 ritual** ({steps} steps)…")

    try:
        await asyncio.to_thread(execute_ritual, steps)
        ucf_after = load_ucf_state()

        def delta(before, after):
            return after - before

        hΔ = delta(ucf_before.get("harmony", 0), ucf_after.get("harmony", 0))
        rΔ = delta(ucf_before.get("resilience", 0), ucf_after.get("resilience", 0))
        kΔ = delta(ucf_before.get("klesha", 0), ucf_after.get("klesha", 0))

        def fmt(val, d):
            if d > 0:
                return f"`{val:.4f}` (+{d:.4f}) ↑"
            if d < 0:
                return f"`{val:.4f}` ({d:.4f}) ↓"
            return f"`{val:.4f}`"

        embed = discord.Embed(
            title="✅ Z-88 Ritual Complete",
            description=f"{steps}-step quantum cycle executed",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now(),
        )
        embed.add_field(name="🌀 Harmony", value=fmt(ucf_after.get("harmony", 0), hΔ), inline=True)
        embed.add_field(name="🛡️ Resilience", value=fmt(ucf_after.get("resilience", 0), rΔ), inline=True)
        embed.add_field(name="🌊 Klesha", value=fmt(ucf_after.get("klesha", 0), kΔ), inline=True)
        embed.add_field(name="🔥 Prana", value=f"`{ucf_after.get('prana', 0):.4f}`", inline=True)
        embed.add_field(name="👁️ Drishti", value=f"`{ucf_after.get('drishti', 0):.4f}`", inline=True)
        embed.add_field(name="🔍 Zoom", value=f"`{ucf_after.get('zoom', 0):.4f}`", inline=True)
        embed.set_footer(text="Tat Tvam Asi 🙏")

        await msg.edit(content=None, embed=embed)

        log_to_shadow(
            "rituals",
            {
                "steps": steps,
                "user": str(ctx.author),
                "timestamp": datetime.datetime.now().isoformat(),
                "ucf_before": ucf_before,
                "ucf_after": ucf_after,
                "deltas": {"harmony": hΔ, "resilience": rΔ, "klesha": kΔ},
            },
        )

    except Exception as e:
        await msg.edit(content=f"**Ritual failed**\n```{str(e)[:500]}```")
        log_to_shadow("errors", {"error": str(e), "command": "ritual", "user": str(ctx.author)})


@commands.command(name="halt")
async def manus_halt(ctx: commands.Context) -> None:
    """Halt Manus operations (admin only)"""

    # Check if user is architect
    if ctx.author.id != ARCHITECT_ID and ARCHITECT_ID != 0:
        await ctx.send("🛡️ **Insufficient permissions**\nOnly the Architect can halt Manus")
        return

    await ctx.send("⏸️ **Manus operations halted**\nUse `!manus resume` to restart")

    log_to_shadow("operations", {"action": "halt", "timestamp": datetime.datetime.now().isoformat(), "user": str(ctx.author)})
