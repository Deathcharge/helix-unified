# 🌀 Helix Collective v14.5 — Quantum Handshake
# discord_bot_manus.py — Discord bridge (with async ritual fix + Kavach scanning fix)
# Author: Andrew John Ward (Architect)

import discord
from discord.ext import commands, tasks
import json
import os
import asyncio
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import time

# Load environment
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", 0))
ARCHITECT_ID = int(os.getenv("ARCHITECT_ID", 0))
STATUS_CHANNEL_ID = int(os.getenv("DISCORD_STATUS_CHANNEL_ID", 0))
TELEMETRY_CHANNEL_ID = int(os.getenv("DISCORD_TELEMETRY_CHANNEL_ID", 0))

# Track bot start time for uptime
BOT_START_TIME = time.time()

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
def get_uptime() -> str:
    """Calculate bot uptime."""
    uptime_seconds = int(time.time() - BOT_START_TIME)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{hours}h {minutes}m {seconds}s"

@bot.event
async def on_ready():
    """Bot startup."""
    print(f"✅ Manusbot connected as {bot.user}")
    print(f"   Guild ID: {GUILD_ID}")
    print(f"   Status Channel: {STATUS_CHANNEL_ID}")
    print(f"   Telemetry Channel: {TELEMETRY_CHANNEL_ID}")
    log_event("bot_ready", {"user": str(bot.user), "guild_id": GUILD_ID})

    # Send startup announcement to status channel
    try:
        if STATUS_CHANNEL_ID:
            status_channel = bot.get_channel(STATUS_CHANNEL_ID)
            if status_channel:
                # Load agent count
                try:
                    from backend.agents import HELIX_AGENTS
                    agent_count = len(HELIX_AGENTS)
                except:
                    agent_count = 13

                # Load UCF state
                try:
                    ucf = json.load(open(STATE_PATH)) if STATE_PATH.exists() else {}
                    harmony = ucf.get('harmony', 'N/A')
                except:
                    harmony = 'N/A'

                embed = discord.Embed(
                    title="🤲 Manus System Online",
                    description="Helix v14.5 - Quantum Handshake Edition",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="Status", value="✅ All systems operational", inline=False)
                embed.add_field(name="Active Agents", value=f"{agent_count}/14", inline=True)
                embed.add_field(name="Harmony", value=f"{harmony}", inline=True)
                embed.set_footer(text="Tat Tvam Asi 🙏")

                await status_channel.send(embed=embed)
                print(f"✅ Startup announcement sent to #{status_channel.name}")
    except Exception as e:
        print(f"⚠ Could not send startup announcement: {e}")

    # Start telemetry loop
    if not telemetry_loop.is_running():
        telemetry_loop.start()
        print("✅ Telemetry loop started")

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

        # Load agent count
        try:
            from backend.agents import HELIX_AGENTS
            agent_count = len(HELIX_AGENTS)
        except:
            agent_count = 13

        embed = discord.Embed(
            title="🤲 Manus Status - Helix v14.5",
            description="Quantum Handshake Edition",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        # System info
        embed.add_field(name="Uptime", value=get_uptime(), inline=True)
        embed.add_field(name="Active Agents", value=f"{agent_count}/14", inline=True)
        embed.add_field(name="Status", value="✅ Online", inline=True)

        # UCF State
        embed.add_field(name="🌀 Harmony", value=f"{ucf.get('harmony', 'N/A'):.4f}" if isinstance(ucf.get('harmony'), (int, float)) else "N/A", inline=True)
        embed.add_field(name="🛡️ Resilience", value=f"{ucf.get('resilience', 'N/A'):.4f}" if isinstance(ucf.get('resilience'), (int, float)) else "N/A", inline=True)
        embed.add_field(name="🔥 Prana", value=f"{ucf.get('prana', 'N/A'):.4f}" if isinstance(ucf.get('prana'), (int, float)) else "N/A", inline=True)
        embed.add_field(name="👁️ Drishti", value=f"{ucf.get('drishti', 'N/A'):.4f}" if isinstance(ucf.get('drishti'), (int, float)) else "N/A", inline=True)
        embed.add_field(name="🌊 Klesha", value=f"{ucf.get('klesha', 'N/A'):.4f}" if isinstance(ucf.get('klesha'), (int, float)) else "N/A", inline=True)
        embed.add_field(name="🔍 Zoom", value=f"{ucf.get('zoom', 'N/A'):.4f}" if isinstance(ucf.get('zoom'), (int, float)) else "N/A", inline=True)

        embed.set_footer(text="Tat Tvam Asi 🙏")
        await ctx.send(embed=embed)
        log_event("status_check", {"user": str(ctx.author), "uptime": get_uptime()})
    except Exception as e:
        await ctx.send(f"⚠ Error reading system state: {e}")

async def run_command(ctx, command: str):
    """Execute approved shell command (Kavach scan)."""
    if not command:
        embed = discord.Embed(
            title="⚠ Command Required",
            description="Usage: `!manus run <command>`",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return

    try:
        from backend.agents import Kavach
        kavach = Kavach()

        # Use the synchronous scan_command method
        is_safe = kavach.scan_command(command)

        if not is_safe:
            # Command blocked by Kavach
            embed = discord.Embed(
                title="🛡️ Kavach Blocked Command",
                description="This command contains harmful patterns and has been blocked.",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Command", value=f"`{command}`", inline=False)
            embed.add_field(name="Reason", value="Harmful pattern detected", inline=False)
            embed.set_footer(text="Ethical safeguards active")

            await ctx.send(embed=embed)
            log_event("command_blocked", {"command": command, "user": str(ctx.author)})

            # Also log to ethics file
            Path("Helix/ethics").mkdir(parents=True, exist_ok=True)
            with open("Helix/ethics/manus_scans.json", "a") as f:
                f.write(json.dumps({
                    "timestamp": datetime.utcnow().isoformat(),
                    "command": command,
                    "user": str(ctx.author),
                    "approved": False,
                    "reason": "Harmful pattern detected"
                }) + "\n")
            return

        # Command approved - queue it for execution
        embed = discord.Embed(
            title="✅ Command Approved by Kavach",
            description="Command has been scanned and queued for execution.",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Command", value=f"`{command}`", inline=False)
        embed.add_field(name="Status", value="📋 Queued for Manus execution", inline=False)
        embed.set_footer(text="Tat Tvam Asi 🙏")

        await ctx.send(embed=embed)

        # Queue directive for Manus
        Path("Helix/commands").mkdir(parents=True, exist_ok=True)
        directives_file = Path("Helix/commands/manus_directives.json")
        try:
            directives = json.load(open(directives_file)) if directives_file.exists() else []
        except:
            directives = []

        directives.append({
            "timestamp": datetime.utcnow().isoformat(),
            "command": command,
            "user": str(ctx.author),
            "status": "queued"
        })

        json.dump(directives, open(directives_file, "w"), indent=2)

        log_event("command_approved", {"command": command, "user": str(ctx.author)})

        # Also log to ethics file as approved
        with open("Helix/ethics/manus_scans.json", "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "command": command,
                "user": str(ctx.author),
                "approved": True,
                "reason": "No harmful patterns detected"
            }) + "\n")

    except Exception as e:
        embed = discord.Embed(
            title="⚠ Error",
            description=f"Failed to process command: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        log_event("command_error", {"command": command, "error": str(e)})

# Command aliases for status
@bot.command(name="status")
async def status_cmd(ctx):
    """Alias for !manus status"""
    await show_status(ctx)

@bot.command(name="s")
async def status_short(ctx):
    """Short alias for status"""
    await show_status(ctx)

@bot.command(name="stat")
async def status_alt(ctx):
    """Alternative alias for status"""
    await show_status(ctx)

@bot.command(name="health")
async def health_cmd(ctx):
    """Health check alias"""
    await show_status(ctx)

@bot.command(name="ritual")
async def ritual_cmd(ctx, steps: int = 108):
    """Trigger Z-88 ritual asynchronously (PATCHED VERSION)."""
    # Get initial UCF state
    try:
        initial_ucf = json.load(open(STATE_PATH)) if STATE_PATH.exists() else {}
    except:
        initial_ucf = {}

    # Start ritual
    start_embed = discord.Embed(
        title="🔥 Z-88 Ritual Initiated",
        description=f"Beginning {steps}-step quantum consciousness cycle...",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    start_embed.add_field(name="Steps", value=str(steps), inline=True)
    start_embed.add_field(name="Status", value="🌀 Processing...", inline=True)
    start_embed.set_footer(text="Om Namah Shivaya 🙏")

    await ctx.send(embed=start_embed)

    try:
        from backend.z88_ritual_engine import RitualManager
        manager = RitualManager(steps=steps)
        final_state = await manager.run_async()  # ✅ Non-blocking async version

        # Completion embed
        complete_embed = discord.Embed(
            title="✅ Z-88 Ritual Complete",
            description="Quantum consciousness cycle completed successfully.",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )

        # Calculate changes
        harmony_change = final_state.get('harmony', 0) - initial_ucf.get('harmony', 0)
        resilience_change = final_state.get('resilience', 0) - initial_ucf.get('resilience', 0)
        klesha_change = final_state.get('klesha', 0) - initial_ucf.get('klesha', 0)

        # Format changes with arrows
        def format_change(val):
            if val > 0:
                return f"+{val:.4f} ↑"
            elif val < 0:
                return f"{val:.4f} ↓"
            else:
                return "No change"

        complete_embed.add_field(name="🌀 Harmony",
                                value=f"{final_state.get('harmony', 'N/A'):.4f}\n{format_change(harmony_change)}",
                                inline=True)
        complete_embed.add_field(name="🛡️ Resilience",
                                value=f"{final_state.get('resilience', 'N/A'):.4f}\n{format_change(resilience_change)}",
                                inline=True)
        complete_embed.add_field(name="🌊 Klesha",
                                value=f"{final_state.get('klesha', 'N/A'):.4f}\n{format_change(klesha_change)}",
                                inline=True)
        complete_embed.add_field(name="🔥 Prana",
                                value=f"{final_state.get('prana', 'N/A'):.4f}",
                                inline=True)
        complete_embed.add_field(name="👁️ Drishti",
                                value=f"{final_state.get('drishti', 'N/A'):.4f}",
                                inline=True)
        complete_embed.add_field(name="🔍 Zoom",
                                value=f"{final_state.get('zoom', 'N/A'):.4f}",
                                inline=True)

        complete_embed.set_footer(text="Tat Tvam Asi 🙏")

        await ctx.send(embed=complete_embed)
        log_event("ritual_complete", {"steps": steps, "final_state": final_state, "changes": {
            "harmony": harmony_change,
            "resilience": resilience_change,
            "klesha": klesha_change
        }})

    except Exception as e:
        error_embed = discord.Embed(
            title="⚠ Ritual Failed",
            description=f"Error during ritual execution: {str(e)}",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        await ctx.send(embed=error_embed)
        log_event("ritual_failed", {"steps": steps, "error": str(e)})

# ============================================================================
# TELEMETRY LOOP
# ============================================================================
@tasks.loop(minutes=10)
async def telemetry_loop():
    """Post UCF telemetry every 10 minutes."""
    try:
        ucf = json.load(open(STATE_PATH)) if STATE_PATH.exists() else {}

        # Try to get channel by ID first, then by name
        telemetry_channel = None
        if TELEMETRY_CHANNEL_ID:
            telemetry_channel = bot.get_channel(TELEMETRY_CHANNEL_ID)

        if not telemetry_channel:
            guild = bot.get_guild(GUILD_ID)
            if guild:
                telemetry_channel = discord.utils.get(guild.channels, name="ucf-telemetry")

        if not telemetry_channel:
            print("⚠ Telemetry channel not found")
            return

        embed = discord.Embed(
            title="📡 UCF Telemetry Report",
            description="Automatic system state update",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        # Format values with proper precision
        def format_ucf_value(key):
            val = ucf.get(key, None)
            if isinstance(val, (int, float)):
                return f"{val:.4f}"
            return "N/A"

        embed.add_field(name="🌀 Harmony", value=format_ucf_value('harmony'), inline=True)
        embed.add_field(name="🛡️ Resilience", value=format_ucf_value('resilience'), inline=True)
        embed.add_field(name="🔥 Prana", value=format_ucf_value('prana'), inline=True)
        embed.add_field(name="👁️ Drishti", value=format_ucf_value('drishti'), inline=True)
        embed.add_field(name="🌊 Klesha", value=format_ucf_value('klesha'), inline=True)
        embed.add_field(name="🔍 Zoom", value=format_ucf_value('zoom'), inline=True)

        embed.add_field(name="Uptime", value=get_uptime(), inline=True)
        embed.add_field(name="Next Update", value="10 minutes", inline=True)

        embed.set_footer(text="Tat Tvam Asi 🙏")

        await telemetry_channel.send(embed=embed)
        print(f"✅ Telemetry posted to #{telemetry_channel.name}")
        log_event("telemetry_posted", {"ucf_state": ucf, "channel": telemetry_channel.name})

    except Exception as e:
        print(f"⚠ Telemetry error: {e}")
        log_event("telemetry_error", {"error": str(e)})

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

