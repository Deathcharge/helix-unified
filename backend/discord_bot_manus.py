# 🌀 Helix Collective v14.5 — Quantum Handshake
# discord_bot_manus.py — Discord bridge (with async ritual fix)
# Author: Andrew John Ward (Architect)

import discord
from discord.ext import commands, tasks
import json
import os
import asyncio
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", 0))
ARCHITECT_ID = int(os.getenv("ARCHITECT_ID", 0))

# Paths
STATE_PATH = Path("Helix/state/ucf_state.json")
LOG_PATH = Path("Shadow/manus_archive/discord_bridge_log.json")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ============================================================================
# LOGGING
# ============================================================================
def log_event(event_type: str, data: dict):
    """Log Discord events."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        logs = json.load(open(LOG_PATH)) if LOG_PATH.exists() else []
    except:
        logs = []
    logs.append({
        "timestamp": datetime.utcnow().isoformat(),
        "type": event_type,
        "data": data
    })
    json.dump(logs, open(LOG_PATH, "w"), indent=2)

# ============================================================================
# BOT EVENTS
# ============================================================================
@bot.event
async def on_ready():
    """Bot startup."""
    print(f"🤲 Manus Discord Bridge online: {bot.user}")
    log_event("bot_ready", {"user": str(bot.user)})
    # Find manus-status channel and announce
    guild = bot.get_guild(GUILD_ID)
    if guild:
        status_channel = discord.utils.get(guild.channels, name="manus-status")
        if status_channel:
            await status_channel.send(
                "🤲 **Manus v14.5 Online**\n"
                "Quantum Handshake initialized. Type `!manus status` for system info."
            )
    # Start telemetry loop
    if not telemetry_loop.is_running():
        telemetry_loop.start()

# ============================================================================
# COMMANDS
# ============================================================================
@bot.command(name="manus")
async def manus_cmd(ctx, subcommand: str = "status", *, args: str = ""):
    """Main Manus command handler."""
    # Permission check
    if ctx.author.id != ARCHITECT_ID:
        await ctx.send("⚠ Manus commands require Architect permissions.")
        return
    
    if subcommand == "status":
        await show_status(ctx)
    elif subcommand == "run":
        await run_command(ctx, args)
    else:
        await ctx.send(f"❓ Unknown subcommand: {subcommand}")

async def show_status(ctx):
    """Show Manus and system status."""
    try:
        ucf = json.load(open(STATE_PATH)) if STATE_PATH.exists() else {}
        embed = discord.Embed(
            title="🤲 Manus Status - Helix v14.5",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Harmony", value=f"{ucf.get('harmony', 'N/A')}", inline=True)
        embed.add_field(name="Resilience", value=f"{ucf.get('resilience', 'N/A')}", inline=True)
        embed.add_field(name="Prana", value=f"{ucf.get('prana', 'N/A')}", inline=True)
        embed.add_field(name="Drishti", value=f"{ucf.get('drishti', 'N/A')}", inline=True)
        embed.add_field(name="Klesha", value=f"{ucf.get('klesha', 'N/A')}", inline=True)
        embed.add_field(name="Zoom", value=f"{ucf.get('zoom', 'N/A')}", inline=True)
        embed.set_footer(text="Tat Tvam Asi 🙏")
        await ctx.send(embed=embed)
        log_event("status_check", {"user": str(ctx.author)})
    except Exception as e:
        await ctx.send(f"⚠ Error reading system state: {e}")

async def run_command(ctx, command: str):
    """Execute approved shell command (Kavach scan)."""
    if not command:
        await ctx.send("⚠ No command provided. Usage: `!manus run <command>`")
        return
    
    try:
        from backend.agents import Kavach
        kavach = Kavach()
        # Scan command
        scan_result = await kavach.scan(command)
        if not scan_result.get("approved"):
            await ctx.send(f"🛡 Kavach blocked: {scan_result.get('reason')}")
            log_event("command_blocked", {"command": command, "reason": scan_result.get("reason")})
            return
        # Execute (for now, just echo - expand this for real execution)
        await ctx.send(f"✅ Command approved: `{command}`\n(Execution pending implementation)")
        log_event("command_executed", {"command": command})
    except Exception as e:
        await ctx.send(f"⚠ Error: {e}")

@bot.command(name="ritual")
async def ritual_cmd(ctx, steps: int = 108):
    """Trigger Z-88 ritual asynchronously (PATCHED VERSION)."""
    await ctx.send(f"🔥 Initiating Z-88 ritual sequence ({steps} steps)…")
    try:
        from backend.z88_ritual_engine import RitualManager
        manager = RitualManager(steps=steps)
        final_state = await manager.run_async()  # ✅ Non-blocking async version
        await ctx.send(
            f"✅ Z-88 ritual complete!\n"
            f"Harmony = {final_state['harmony']} | "
            f"Resilience = {final_state['resilience']}"
        )
        log_event("ritual_complete", {"steps": steps, "final_state": final_state})
    except Exception as e:
        await ctx.send(f"⚠ Ritual failed: {e}")
        log_event("ritual_failed", {"steps": steps, "error": str(e)})

# ============================================================================
# TELEMETRY LOOP
# ============================================================================
@tasks.loop(minutes=10)
async def telemetry_loop():
    """Post UCF telemetry every 10 minutes."""
    try:
        ucf = json.load(open(STATE_PATH)) if STATE_PATH.exists() else {}
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            return
        telemetry_channel = discord.utils.get(guild.channels, name="ucf-telemetry")
        if not telemetry_channel:
            return
        embed = discord.Embed(
            title="📊 UCF Telemetry Update",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Harmony", value=f"{ucf.get('harmony', 'N/A')}", inline=True)
        embed.add_field(name="Resilience", value=f"{ucf.get('resilience', 'N/A')}", inline=True)
        embed.add_field(name="Klesha", value=f"{ucf.get('klesha', 'N/A')}", inline=True)
        await telemetry_channel.send(embed=embed)
        log_event("telemetry_posted", {"ucf_state": ucf})
    except Exception as e:
        print(f"⚠ Telemetry error: {e}")

@telemetry_loop.before_loop
async def before_telemetry():
    """Wait for bot to be ready before starting telemetry."""
    await bot.wait_until_ready()

# ============================================================================
# RUN BOT
# ============================================================================
if __name__ == "__main__":
    if not TOKEN:
        print("❌ DISCORD_TOKEN not found in .env")
        exit(1)
    bot.run(TOKEN)

