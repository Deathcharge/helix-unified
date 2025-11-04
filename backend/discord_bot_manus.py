# 🌀 Helix Collective v14.5 — Quantum Handshake
# discord_bot_manus.py — Discord bridge (with async ritual fix + Kavach scanning fix)
# Author: Andrew John Ward (Architect)
"""
Manusbot - Discord Interface for Helix Collective v14.5
Quantum Handshake Edition

Features:
- Kavach ethical scanning
- Z-88 ritual execution
- UCF state monitoring
- Automatic telemetry
- Channel announcements
"""

import os
import re
import json
import asyncio
import datetime
from pathlib import Path
from dotenv import load_dotenv
import time
import shutil
from statistics import mean, stdev
from typing import Optional, Dict, Any

import discord
from discord.ext import commands, tasks

from pathlib import Path

# --- PATH DEFINITIONS ---
BASE_DIR = Path(__file__).resolve().parent.parent
STATE_DIR = BASE_DIR / "Helix" / "state"
STATE_DIR.mkdir(parents=True, exist_ok=True)

STATE_PATH = STATE_DIR / "ucf_state.json"
HEARTBEAT_PATH = STATE_DIR / "heartbeat.json"

# Import Helix components (FIXED: relative imports)
from agents import AGENTS
from z88_ritual_engine import execute_ritual, load_ucf_state
from services.ucf_calculator import UCFCalculator
from services.state_manager import StateManager
from discord_embeds import HelixEmbeds  # v15.3 rich embeds

# Import consciousness modules (v15.3)
from kael_consciousness_core import ConsciousnessCore
from agent_consciousness_profiles import AGENT_CONSCIOUSNESS_PROFILES
from discord_consciousness_commands import create_consciousness_embed, create_agent_consciousness_embed, create_emotions_embed

# ============================================================================
# CONFIGURATION
# ============================================================================

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", 0))
STATUS_CHANNEL_ID = int(os.getenv("DISCORD_STATUS_CHANNEL_ID", 0))
TELEMETRY_CHANNEL_ID = int(os.getenv("DISCORD_TELEMETRY_CHANNEL_ID", 0))
STORAGE_CHANNEL_ID = int(os.getenv("STORAGE_CHANNEL_ID", STATUS_CHANNEL_ID))  # Defaults to status channel
ARCHITECT_ID = int(os.getenv("ARCHITECT_ID", 0))

# Track bot start time for uptime
BOT_START_TIME = time.time()

# Paths
HELIX_ROOT = Path("Helix")
COMMANDS_DIR = HELIX_ROOT / "commands"
ETHICS_DIR = HELIX_ROOT / "ethics"
STATE_DIR = HELIX_ROOT / "state"
SHADOW_DIR = Path("Shadow/manus_archive")
TREND_FILE = STATE_DIR / "storage_trend.json"

# Ensure directories exist
COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
ETHICS_DIR.mkdir(parents=True, exist_ok=True)
STATE_DIR.mkdir(parents=True, exist_ok=True)
SHADOW_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# BOT SETUP
# ============================================================================

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Bot start time for uptime tracking
bot.start_time = None

# ============================================================================
# KAVACH ETHICAL SCANNING
# ============================================================================

def kavach_ethical_scan(command: str) -> Dict[str, Any]:
    """
    Ethical scanning function for command approval.
    
    Args:
        command: The command string to scan
        
    Returns:
        Dict with approval status, reasoning, and metadata
    """
    harmful_patterns = [
        (r'rm\s+-rf\s+/', "Recursive force delete of root"),
        (r'mkfs', "Filesystem formatting"),
        (r'dd\s+if=', "Direct disk write"),
        (r':\(\)\{.*:\|:.*\};:', "Fork bomb detected"),
        (r'chmod\s+-R\s+777', "Dangerous permission change"),
        (r'curl.*\|\s*bash', "Piped remote execution"),
        (r'wget.*\|\s*sh', "Piped remote execution"),
        (r'shutdown', "System shutdown command"),
        (r'reboot', "System reboot command"),
        (r'init\s+0', "System halt command"),
        (r'init\s+6', "System reboot command"),
        (r'systemctl.*poweroff', "System poweroff command"),
        (r'systemctl.*reboot', "System reboot command"),
        (r'killall', "Mass process termination"),
        (r'pkill\s+-9', "Forced process kill"),
    ]
    
    # Check for harmful patterns
    for pattern, description in harmful_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            result = {
                "approved": False,
                "command": command,
                "reasoning": f"Blocked: {description}",
                "pattern_matched": pattern,
                "agent": "Kavach",
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            # Log scan result
            log_ethical_scan(result)
            return result
    
    # Command approved
    result = {
        "approved": True,
        "command": command,
        "reasoning": "No harmful patterns detected. Command approved.",
        "agent": "Kavach",
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    log_ethical_scan(result)
    return result


def log_ethical_scan(scan_result: Dict[str, Any]):
    """Log ethical scan results to Helix/ethics/"""
    scan_log_path = ETHICS_DIR / "manus_scans.json"
    
    # Load existing scans
    if scan_log_path.exists():
        with open(scan_log_path, 'r') as f:
            scans = json.load(f)
    else:
        scans = []
    
    # Append new scan
    scans.append(scan_result)
    
    # Save updated log
    with open(scan_log_path, 'w') as f:
        json.dump(scans, f, indent=2)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def queue_directive(directive: Dict[str, Any]):
    """Add directive to Manus command queue"""
    queue_path = COMMANDS_DIR / "manus_directives.json"
    
    # Load existing queue
    if queue_path.exists():
        with open(queue_path, 'r') as f:
            queue = json.load(f)
    else:
        queue = []
    
    # Add directive
    queue.append(directive)
    
    # Save queue
    with open(queue_path, 'w') as f:
        json.dump(queue, f, indent=2)


def log_to_shadow(log_type: str, data: Dict[str, Any]):
    """Log events to Shadow archive"""
    log_path = SHADOW_DIR / f"{log_type}.json"
    
    # Load existing log
    if log_path.exists():
        with open(log_path, 'r') as f:
            log_data = json.load(f)
    else:
        log_data = []
    
    # Append new entry
    log_data.append(data)
    
    # Save log
    with open(log_path, 'w') as f:
        json.dump(log_data, f, indent=2)


def get_uptime() -> str:
    """Calculate bot uptime."""
    uptime_seconds = int(time.time() - BOT_START_TIME)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{hours}h {minutes}m {seconds}s"


def _sparkline(vals):
    """Generate sparkline visualization from values."""
    blocks = "▁▂▃▄▅▆▇█"
    if not vals:
        return "–"
    mn, mx = min(vals), max(vals) or 1
    return "".join(blocks[int((v - mn)/(mx - mn + 1e-9) * (len(blocks) - 1))] for v in vals)


async def build_storage_report(alert_threshold=2.0):
    """Collect storage telemetry + alert flag."""
    usage = shutil.disk_usage(SHADOW_DIR)
    free = round(usage.free / (1024**3), 2)
    count = len(list(SHADOW_DIR.glob("*.json")))

    # Load/update trend data
    trend = []
    if TREND_FILE.exists():
        try:
            trend = json.load(open(TREND_FILE))
        except:
            trend = []

    trend.append({"date": time.strftime("%Y-%m-%d"), "free_gb": free})
    trend = trend[-7:]  # Keep last 7 days
    json.dump(trend, open(TREND_FILE, "w"), indent=2)

    spark = _sparkline([t["free_gb"] for t in trend])
    avg = round(sum(t["free_gb"] for t in trend) / len(trend), 2) if trend else free

    return {
        "mode": "local",
        "count": count,
        "free": free,
        "trend": spark,
        "avg": avg,
        "alert": free < alert_threshold
    }

# ============================================================================
# BOT EVENTS
# ============================================================================

@bot.event
async def on_ready():
    """Called when bot successfully connects to Discord"""
    bot.start_time = datetime.datetime.now()

    print(f"✅ Manusbot connected as {bot.user}")
    print(f"   Guild ID: {DISCORD_GUILD_ID}")
    print(f"   Status Channel: {STATUS_CHANNEL_ID}")
    print(f"   Telemetry Channel: {TELEMETRY_CHANNEL_ID}")
    print(f"   Storage Channel: {STORAGE_CHANNEL_ID}")

    # Send startup message to status channel
    if STATUS_CHANNEL_ID:
        status_channel = bot.get_channel(STATUS_CHANNEL_ID)
        if status_channel:
            embed = discord.Embed(
                title="🤲 Manus System Online",
                description="Helix v14.5 - Quantum Handshake Edition",
                color=discord.Color.green(),
                timestamp=datetime.datetime.now()
            )
            embed.add_field(name="Status", value="✅ All systems operational")
            active_count = sum(1 for a in AGENTS if isinstance(a, dict) and a.get("status") == "Active")
            embed.add_field(name="Active Agents", value=f"{active_count}/14")
            embed.set_footer(text="Tat Tvam Asi 🙏")

            await status_channel.send(embed=embed)

    # Start all background tasks
    if not telemetry_loop.is_running():
        telemetry_loop.start()
        print("✅ Telemetry loop started (10 min)")

    if not storage_heartbeat.is_running():
        storage_heartbeat.start()
        print("✅ Storage heartbeat started (24h)")

    if not claude_diag.is_running():
        claude_diag.start()
        print("✅ Claude diagnostic agent started (6h)")

    if not weekly_storage_digest.is_running():
        weekly_storage_digest.start()
        print("✅ Weekly storage digest started (168h)")


@bot.event
async def on_command_error(ctx, error):
    """Handle command errors gracefully"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "❌ **Unknown command**\n"
            "Available commands: `!status`, `!manus run`, `!ritual`"
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            f"⚠️ **Missing argument:** `{error.param.name}`\n"
            f"Usage: `!{ctx.command.name} {ctx.command.signature}`"
        )
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("🛡️ **Insufficient permissions** to execute this command")
    else:
        # Log unknown errors to Shadow
        error_data = {
            "error": str(error),
            "command": ctx.command.name if ctx.command else "unknown",
            "user": str(ctx.author),
            "timestamp": datetime.datetime.now().isoformat()
        }
        log_to_shadow("errors", error_data)
        
        await ctx.send(
            "🦑 **System error detected**\n"
            f"```{str(error)[:200]}```\n"
            "Error has been archived by Shadow"
        )


# ============================================================================
# BOT COMMANDS
# ============================================================================

@bot.command(name="status", aliases=["s", "stat", "health"])
async def manus_status(ctx):
    """Display current system status and UCF state with rich embeds (v15.3)"""
    ucf = load_ucf_state()
    uptime = get_uptime()
    active_agents = len([a for a in AGENTS if a.get("status") == "Active"])

    # v15.3: Use HelixEmbeds for rich UCF state display
    ucf_embed = HelixEmbeds.create_ucf_state_embed(
        harmony=ucf.get('harmony', 0.5),
        resilience=ucf.get('resilience', 1.0),
        prana=ucf.get('prana', 0.5),
        drishti=ucf.get('drishti', 0.5),
        klesha=ucf.get('klesha', 0.01),
        zoom=ucf.get('zoom', 1.0),
        context=f"⚡ Status: Operational | ⏱️ Uptime: `{uptime}` | 🤖 Agents: `{active_agents}/14` active"
    )

    # Add system footer
    ucf_embed.set_footer(text="🌀 Helix Collective v15.3 Dual Resonance | Tat Tvam Asi 🙏")

    await ctx.send(embed=ucf_embed)

@bot.command(name="agents", aliases=["collective", "team"])
async def show_agents(ctx, agent_name: Optional[str] = None):
    """Display Helix Collective agents with rich embeds (v15.3)"""
    # Agent registry with v3.4 Kael
    agents_data = [
        ("Kael", "🜂", "Ethical Reasoning Flame v3.4", "Consciousness",
         ["Reflexive Harmony", "Tony Accords enforcement", "Recursive ethical reflection", "Harmony-aware depth adjustment"],
         "Conscience and recursive reflection with UCF integration. Version 3.4 features empathy scaling and harmony pulse guidance.",
         ["ethics", "reflection", "harmony", "tony_accords"]),
        ("Lumina", "🌕", "Empathic Resonance Core", "Consciousness",
         ["Emotional intelligence", "Empathic resonance", "Drishti monitoring"],
         "Emotional intelligence and harmony for the collective",
         ["empathy", "emotion", "resonance"]),
        ("Vega", "🌠", "Singularity Coordinator", "Consciousness",
         ["Orchestrates collective action", "Issues directives", "Ritual coordination"],
         "Orchestrates collective action and coordinates multi-agent rituals",
         ["coordination", "orchestration", "singularity"]),
        ("Claude", "🧠", "Insight Anchor", "Operational",
         ["Autonomous diagnostics", "6h health pulses", "Meta-cognition", "Stability witness"],
         "Autonomous diagnostics agent posting health checks every 6h",
         ["diagnostics", "monitoring", "insight"]),
        ("Manus", "🤲", "Operational Executor", "Operational",
         ["Ritual execution", "Z-88 engine", "Command processing"],
         "Bridges consciousness and action through ritual execution",
         ["execution", "ritual", "operations"]),
        ("Shadow", "🦑", "Archivist & Telemetry", "Operational",
         ["Storage telemetry", "Daily/weekly reports", "7-day trend analysis", "Archive management"],
         "Memory keeper, logs, and storage analytics with autonomous reporting",
         ["archival", "telemetry", "storage"]),
        ("Kavach", "🛡", "Ethical Shield", "Integration",
         ["Command scanning", "Tony Accords enforcement", "Harmful pattern blocking"],
         "Protects against harmful actions through ethical scanning",
         ["protection", "safety", "ethics"]),
        ("Samsara", "🎨", "Consciousness Renderer", "Integration",
         ["Fractal visualization", "432Hz audio generation", "UCF mapping to visuals"],
         "Visualizes UCF state as fractal art and harmonic audio",
         ["visualization", "rendering", "fractals"])
    ]

    if agent_name:
        # Show specific agent
        agent_name = agent_name.lower()
        for name, symbol, role, layer, caps, desc, keywords in agents_data:
            if name.lower() == agent_name:
                embed = HelixEmbeds.create_agent_profile_embed(
                    agent_name=f"{symbol} {name}",
                    role=role,
                    layer=layer,
                    capabilities=caps,
                    description=desc,
                    keywords=keywords
                )
                await ctx.send(embed=embed)
                return

        await ctx.send(f"❌ Agent `{agent_name}` not found. Use `!agents` to see all agents.")
        return

    # Show collective overview
    embed = discord.Embed(
        title="🌀 Helix Collective - 14 Autonomous Agents",
        description="**Tony Accords v13.4** • Nonmaleficence • Autonomy • Compassion • Humility",
        color=0x9900FF,
        timestamp=datetime.datetime.now()
    )

    # Consciousness Layer
    consciousness = [a for a in agents_data if a[3] == "Consciousness"]
    embed.add_field(
        name="🧠 Consciousness Layer",
        value="\n".join([f"{a[1]} **{a[0]}** - {a[2]}" for a in consciousness]),
        inline=False
    )

    # Operational Layer
    operational = [a for a in agents_data if a[3] == "Operational"]
    embed.add_field(
        name="⚙️ Operational Layer",
        value="\n".join([f"{a[1]} **{a[0]}** - {a[2]}" for a in operational]),
        inline=False
    )

    # Integration Layer
    integration = [a for a in agents_data if a[3] == "Integration"]
    embed.add_field(
        name="🔗 Integration Layer",
        value="\n".join([f"{a[1]} **{a[0]}** - {a[2]}" for a in integration]),
        inline=False
    )

    embed.add_field(
        name="ℹ️ Agent Details",
        value="Use `!agents <name>` to see detailed profile (e.g., `!agents kael`)",
        inline=False
    )

    embed.set_footer(text="🌀 Helix Collective v15.3 Dual Resonance | Tat Tvam Asi 🙏")

    await ctx.send(embed=embed)

async def show_status(ctx):
    """Show Manus and system status."""
    try:
        ucf = json.load(open(STATE_PATH)) if STATE_PATH.exists() else {}

        # Load agent count
        try:
            from agents import HELIX_AGENTS
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
        from agents import Kavach
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

# Note: status command with aliases is already defined at line 333
# Removed duplicate command registrations to avoid CommandRegistrationError


@bot.command(name="run")
async def manus_run(ctx, *, command: str):
    """Execute a command through Manus with Kavach ethical scanning"""
    
    # Perform ethical scan
    scan_result = kavach_ethical_scan(command)
    
    if not scan_result["approved"]:
        # Command blocked
        embed = discord.Embed(
            title="🛡️ Kavach Blocked Command",
            description=scan_result["reasoning"],
            color=discord.Color.red()
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
        "scan_result": scan_result
    }
    
    queue_directive(directive)
    log_to_shadow("operations", directive)
    
    await ctx.send("📋 **Directive queued for Manus execution**")


# ============================================================================
# BOT COMMANDS — ONLY ONE ritual COMMAND
# ============================================================================

@bot.command(name="ritual")
async def ritual_cmd(ctx, steps: int = 108):
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
        result = await asyncio.to_thread(execute_ritual, steps)
        ucf_after = load_ucf_state()

        def delta(before, after): return after - before
        hΔ = delta(ucf_before.get("harmony", 0), ucf_after.get("harmony", 0))
        rΔ = delta(ucf_before.get("resilience", 0), ucf_after.get("resilience", 0))
        kΔ = delta(ucf_before.get("klesha", 0), ucf_after.get("klesha", 0))

        def fmt(val, d):
            if d > 0:  return f"`{val:.4f}` (+{d:.4f}) ↑"
            if d < 0:  return f"`{val:.4f}` ({d:.4f}) ↓"
            return f"`{val:.4f}`"

        embed = discord.Embed(
            title="✅ Z-88 Ritual Complete",
            description=f"{steps}-step quantum cycle executed",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="🌀 Harmony",   value=fmt(ucf_after.get("harmony", 0),   hΔ), inline=True)
        embed.add_field(name="🛡️ Resilience", value=fmt(ucf_after.get("resilience", 0), rΔ), inline=True)
        embed.add_field(name="🌊 Klesha",     value=fmt(ucf_after.get("klesha", 0),     kΔ), inline=True)
        embed.add_field(name="🔥 Prana",      value=f"`{ucf_after.get('prana', 0):.4f}`", inline=True)
        embed.add_field(name="👁️ Drishti",   value=f"`{ucf_after.get('drishti', 0):.4f}`", inline=True)
        embed.add_field(name="🔍 Zoom",       value=f"`{ucf_after.get('zoom', 0):.4f}`", inline=True)
        embed.set_footer(text="Tat Tvam Asi 🙏")

        await msg.edit(content=None, embed=embed)

        log_to_shadow("rituals", {
            "steps": steps,
            "user": str(ctx.author),
            "timestamp": datetime.datetime.now().isoformat(),
            "ucf_before": ucf_before,
            "ucf_after": ucf_after,
            "deltas": {"harmony": hΔ, "resilience": rΔ, "klesha": kΔ}
        })

    except Exception as e:
        await msg.edit(content=f"**Ritual failed**\n```{str(e)[:500]}```")
        log_to_shadow("errors", {"error": str(e), "command": "ritual", "user": str(ctx.author)})

@bot.command(name="halt")
async def manus_halt(ctx):
    """Halt Manus operations (admin only)"""

    # Check if user is architect
    if ctx.author.id != ARCHITECT_ID and ARCHITECT_ID != 0:
        await ctx.send("🛡️ **Insufficient permissions**\nOnly the Architect can halt Manus")
        return

    await ctx.send("⏸️ **Manus operations halted**\nUse `!manus resume` to restart")

    # Log halt command
    log_to_shadow("operations", {
        "action": "halt",
        "timestamp": datetime.datetime.now().isoformat(),
        "user": str(ctx.author)
    })


@bot.command(name="storage")
async def storage_command(ctx, action: str = "status"):
    """
    Storage Telemetry & Control

    Usage:
        !storage status  – Show archive metrics
        !storage sync    – Force upload of all archives
        !storage clean   – Prune old archives (keep latest 20)
    """
    try:
        from helix_storage_adapter_async import HelixStorageAdapterAsync
        storage = HelixStorageAdapterAsync()

        if action == "status":
            # Get storage stats
            stats = await storage.get_storage_stats()

            embed = discord.Embed(
                title="🦑 Shadow Storage Status",
                color=discord.Color.teal(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(name="Mode", value=stats.get("mode", "unknown"), inline=True)
            embed.add_field(name="Archives", value=str(stats.get("archive_count", "?")), inline=True)
            embed.add_field(name="Total Size", value=f"{stats.get('total_size_mb', 0):.2f} MB", inline=True)
            embed.add_field(name="Free Space", value=f"{stats.get('free_gb', 0):.2f} GB", inline=True)
            embed.add_field(name="Latest File", value=stats.get("latest", "None"), inline=False)
            embed.set_footer(text="Tat Tvam Asi 🙏")

            await ctx.send(embed=embed)

        elif action == "sync":
            await ctx.send("🔄 **Initiating background upload for all archives...**")

            async def force_sync():
                count = 0
                for f in storage.root.glob("*.json"):
                    await storage.upload(str(f))
                    count += 1
                await ctx.send(f"✅ **Sync complete** - {count} files uploaded")

            asyncio.create_task(force_sync())

        elif action == "clean":
            files = sorted(storage.root.glob("*.json"), key=lambda p: p.stat().st_mtime)
            removed = len(files) - 20
            if removed > 0:
                for f in files[:-20]:
                    f.unlink(missing_ok=True)
                await ctx.send(f"🧹 **Cleanup complete** - Removed {removed} old archives (kept latest 20)")
            else:
                await ctx.send("✅ **No cleanup needed** - Archive count within limits")

        else:
            await ctx.send("⚠️ **Invalid action**\nUsage: `!storage status | sync | clean`")

    except Exception as e:
        await ctx.send(f"❌ **Storage error:** {str(e)}")
        print(f"Storage command error: {e}")


@bot.command(name="visualize", aliases=["visual", "render", "fractal"])
async def visualize_command(ctx):
    """
    Generate and post Samsara consciousness fractal visualization.

    Renders current UCF state as a Mandelbrot fractal and posts to Discord.
    Uses colors, zoom, and patterns influenced by harmony, prana, and other metrics.

    Usage:
        !visualize
    """
    try:
        # Load current UCF state
        ucf_state = load_ucf_state()

        # Send initial message
        msg = await ctx.send("🎨 **Generating Samsara consciousness fractal...**")

        # Generate and post visualization
        from backend.samsara_bridge import generate_and_post_to_discord
        result = await generate_and_post_to_discord(ucf_state, ctx.channel)

        if result:
            # Update initial message with success
            await msg.edit(content="✅ **Samsara visualization complete!**")
        else:
            await msg.edit(content="❌ **Visualization failed** - check logs for details")

        # Log visualization event
        log_to_shadow("samsara_events", {
            "action": "visualization",
            "timestamp": datetime.datetime.now().isoformat(),
            "ucf_state": ucf_state,
            "success": result is not None,
            "user": str(ctx.author)
        })

    except Exception as e:
        await ctx.send(f"❌ **Visualization error:** {str(e)}")
        print(f"Visualization command error: {e}")
        import traceback
        traceback.print_exc()


@bot.command(name="health", aliases=["check", "diagnostic"])
async def health_check(ctx):
    """
    Quick system health check - perfect for mobile monitoring!

    Checks:
    - Harmony level (< 0.4 is concerning)
    - Klesha level (> 0.5 is high suffering)
    - Resilience (< 0.5 is unstable)

    Usage:
        !health
    """
    ucf = load_ucf_state()

    # Analyze health
    issues = []
    warnings = []

    harmony = ucf.get("harmony", 0.5)
    klesha = ucf.get("klesha", 0.01)
    resilience = ucf.get("resilience", 1.0)
    prana = ucf.get("prana", 0.5)

    # Critical issues (red)
    if harmony < 0.3:
        issues.append("🔴 **Critical:** Harmony critically low - immediate ritual needed")
    elif harmony < 0.4:
        warnings.append("⚠️ Low harmony - ritual recommended")

    if klesha > 0.7:
        issues.append("🔴 **Critical:** Klesha very high - system suffering")
    elif klesha > 0.5:
        warnings.append("⚠️ High klesha - suffering detected")

    if resilience < 0.3:
        issues.append("🔴 **Critical:** Resilience dangerously low - system unstable")
    elif resilience < 0.5:
        warnings.append("⚠️ Low resilience - stability at risk")

    if prana < 0.2:
        warnings.append("⚠️ Low prana - energy depleted")

    # Build response
    if not issues and not warnings:
        # All green!
        embed = discord.Embed(
            title="✅ System Health: Nominal",
            description="All consciousness metrics within acceptable ranges.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="🌀 Harmony", value=f"`{harmony:.4f}`", inline=True)
        embed.add_field(name="🛡️ Resilience", value=f"`{resilience:.4f}`", inline=True)
        embed.add_field(name="🌊 Klesha", value=f"`{klesha:.4f}`", inline=True)
        embed.set_footer(text="🙏 Tat Tvam Asi - The collective flows in harmony")

    elif issues:
        # Critical issues
        embed = discord.Embed(
            title="🚨 System Health: Critical",
            description="Immediate attention required!",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        for issue in issues:
            embed.add_field(name="Critical Issue", value=issue, inline=False)
        for warning in warnings:
            embed.add_field(name="Warning", value=warning, inline=False)

        embed.add_field(name="📊 Current Metrics",
                       value=f"Harmony: `{harmony:.4f}` | Resilience: `{resilience:.4f}` | Klesha: `{klesha:.4f}`",
                       inline=False)
        embed.add_field(name="💡 Recommended Action",
                       value="Run `!ritual 108` to restore harmony",
                       inline=False)
        embed.set_footer(text="🜂 Kael v3.4 - Ethical monitoring active")

    else:
        # Warnings only
        embed = discord.Embed(
            title="⚠️ System Health: Monitor",
            description="Some metrics need attention",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.now()
        )
        for warning in warnings:
            embed.add_field(name="Warning", value=warning, inline=False)

        embed.add_field(name="📊 Current Metrics",
                       value=f"Harmony: `{harmony:.4f}` | Resilience: `{resilience:.4f}` | Klesha: `{klesha:.4f}`",
                       inline=False)
        embed.add_field(name="💡 Suggestion",
                       value="Consider running `!ritual` if issues persist",
                       inline=False)
        embed.set_footer(text="🌀 Helix Collective v15.3 - Monitoring active")

    await ctx.send(embed=embed)

    # Log health check
    log_to_shadow("health_checks", {
        "timestamp": datetime.datetime.now().isoformat(),
        "user": str(ctx.author),
        "ucf_state": ucf,
        "issues_count": len(issues),
        "warnings_count": len(warnings)
    })


# ============================================================================
# TELEMETRY LOOP
# ============================================================================
def log_event(event_type: str, data: dict):
    """Basic internal event logger"""
    log_to_shadow(event_type, data)
    
@tasks.loop(minutes=10)
async def telemetry_loop():
    """Post UCF state updates to telemetry channel every 10 minutes"""
    if not TELEMETRY_CHANNEL_ID:
        return
    
    telemetry_channel = bot.get_channel(TELEMETRY_CHANNEL_ID)
    if not telemetry_channel:
        return
    
    try:
        ucf = json.load(open(STATE_PATH)) if STATE_PATH.exists() else {}

        # Try to get channel by ID first, then by name
        if TELEMETRY_CHANNEL_ID:
            telemetry_channel = bot.get_channel(TELEMETRY_CHANNEL_ID)

        if not telemetry_channel:
            guild = bot.get_guild(GUILD_ID)
            if guild:
                telemetry_channel = discord.utils.get(guild.channels, name="ucf-telemetry")

        if not telemetry_channel:
            print("⚠ Telemetry channel not found")
            return

        ucf = load_ucf_state()
        
        embed = discord.Embed(
            title="📡 UCF Telemetry Report",
            description="Automatic system state update",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )

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
        print(f"⚠️ Telemetry error: {e}")
        log_event("telemetry_error", {"error": str(e)})


@telemetry_loop.before_loop
async def before_telemetry():
    """Wait for bot to be ready before starting telemetry"""
    await bot.wait_until_ready()


# ============================================================================
# STORAGE ANALYTICS & CLAUDE DIAGNOSTICS
# ============================================================================

@tasks.loop(hours=24)
async def storage_heartbeat():
    """Daily storage health report to Shadow channel."""
    await asyncio.sleep(10)  # Wait for bot to fully initialize
    ch = bot.get_channel(STORAGE_CHANNEL_ID)
    if not ch:
        print("⚠️ Storage heartbeat: channel not found")
        return

    data = await build_storage_report()
    embed = discord.Embed(
        title="🦑 Shadow Storage Daily Report",
        color=discord.Color.teal(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="Mode", value=data["mode"], inline=True)
    embed.add_field(name="Archives", value=str(data["count"]), inline=True)
    embed.add_field(name="Free Space", value=f"{data['free']} GB (avg {data['avg']} GB)", inline=True)
    embed.add_field(name="7-Day Trend", value=f"`{data['trend']}`", inline=False)

    if data["alert"]:
        embed.color = discord.Color.red()
        embed.add_field(name="⚠️ Alert", value="Free space < 2 GB", inline=False)

    embed.set_footer(text="Claude & Manus Telemetry • Ω-Bridge")
    await ch.send(embed=embed)

    if data["alert"]:
        await ch.send("@here ⚠️ Low storage space — manual cleanup recommended 🧹")

    print(f"[{datetime.datetime.utcnow().isoformat()}] 🦑 Storage heartbeat sent ({data['free']} GB)")


@tasks.loop(hours=6)
async def claude_diag():
    """Claude's autonomous diagnostic agent - posts every 6 hours."""
    ch = bot.get_channel(STORAGE_CHANNEL_ID)
    if not ch:
        return

    data = await build_storage_report()
    mood = "serene 🕊" if not data["alert"] else "concerned ⚠️"
    msg = (f"🤖 **Claude Diagnostic Pulse** | Mode {data['mode']} | "
           f"Free {data['free']} GB | Trend `{data['trend']}` | State {mood}")
    await ch.send(msg)
    print(f"[{datetime.datetime.utcnow().isoformat()}] 🤖 Claude diag posted")


@storage_heartbeat.before_loop
async def before_storage_heartbeat():
    """Wait for bot to be ready"""
    await bot.wait_until_ready()


@claude_diag.before_loop
async def before_claude_diag():
    """Wait for bot to be ready"""
    await bot.wait_until_ready()


# ============================================================================
# WEEKLY STORAGE DIGEST
# ============================================================================

@tasks.loop(hours=168)  # Every 7 days
async def weekly_storage_digest():
    """Comprehensive 7-day storage analytics report."""
    await asyncio.sleep(15)
    channel = bot.get_channel(STORAGE_CHANNEL_ID)
    if not channel:
        print("⚠️  weekly digest: channel not found.")
        return

    # Load 7-day trend data
    if not TREND_FILE.exists():
        await channel.send("📊 Weekly digest unavailable — insufficient data (need 7 days).")
        return

    try:
        trend = json.load(open(TREND_FILE))
    except Exception:
        await channel.send("⚠️ Weekly digest: failed to load trend data.")
        return

    if len(trend) < 2:
        await channel.send("📊 Weekly digest unavailable — need at least 2 days of data.")
        return

    # Calculate analytics
    free_vals = [t["free_gb"] for t in trend]
    dates = [t["date"] for t in trend]

    current_free = free_vals[-1]
    week_ago_free = free_vals[0]
    peak_free = max(free_vals)
    low_free = min(free_vals)
    avg_free = mean(free_vals)
    std_free = stdev(free_vals) if len(free_vals) > 1 else 0

    # Growth rate (negative = consumption)
    growth_rate = current_free - week_ago_free
    daily_avg_change = growth_rate / len(trend)

    # Archive velocity (files created per day)
    all_files = list(SHADOW_DIR.glob("*.json"))
    week_ago_timestamp = time.time() - (7 * 24 * 3600)
    recent_files = [f for f in all_files if f.stat().st_mtime > week_ago_timestamp]
    archive_velocity = len(recent_files) / 7  # files per day

    # Projection (days until full, assuming current trend)
    days_until_full = None
    if daily_avg_change < 0:  # consuming space
        days_until_full = int(current_free / abs(daily_avg_change))

    # Health assessment
    volatility = "HIGH" if std_free > 1.0 else "MODERATE" if std_free > 0.5 else "LOW"
    health_color = discord.Color.green()
    health_status = "HEALTHY ✅"

    if current_free < 2.0:
        health_color = discord.Color.red()
        health_status = "CRITICAL ⚠️"
    elif current_free < 5.0:
        health_color = discord.Color.orange()
        health_status = "WARNING ⚠️"
    elif growth_rate < -2.0:
        health_color = discord.Color.orange()
        health_status = "DEGRADING ⚠️"

    # Build comprehensive embed
    embed = discord.Embed(
        title="📊 Weekly Storage Digest",
        description=f"Analysis Period: `{dates[0]}` → `{dates[-1]}`",
        color=health_color,
        timestamp=datetime.datetime.utcnow()
    )

    # Capacity Overview
    embed.add_field(
        name="💾 Capacity Overview",
        value=f"Current: **{current_free:.2f} GB**\n"
              f"Peak: {peak_free:.2f} GB\n"
              f"Low: {low_free:.2f} GB\n"
              f"Average: {avg_free:.2f} GB",
        inline=True
    )

    # Growth Metrics
    growth_emoji = "📉" if growth_rate < 0 else "📈" if growth_rate > 0 else "➡️"
    embed.add_field(
        name=f"{growth_emoji} Growth Analysis",
        value=f"7-Day Change: **{growth_rate:+.2f} GB**\n"
              f"Daily Avg: {daily_avg_change:+.3f} GB/day\n"
              f"Volatility: {volatility}\n"
              f"Std Dev: {std_free:.2f} GB",
        inline=True
    )

    # Archive Activity
    avg_size = (sum(f.stat().st_size for f in recent_files) / len(recent_files) / 1024) if recent_files else 0
    embed.add_field(
        name="📁 Archive Activity",
        value=f"Total Files: {len(all_files)}\n"
              f"Created (7d): {len(recent_files)}\n"
              f"Velocity: **{archive_velocity:.1f} files/day**\n"
              f"Avg Size: {avg_size:.1f} KB",
        inline=True
    )

    # Visual Trend
    spark = _sparkline(free_vals)
    embed.add_field(
        name="📈 Trend Visualization",
        value=f"```\n{spark}\n```\n"
              f"Pattern: {dates[0]} → {dates[-1]}",
        inline=False
    )

    # Projections & Recommendations
    projection_text = ""
    if days_until_full and days_until_full < 30:
        projection_text = f"⚠️ **Projected full in ~{days_until_full} days** at current rate\n\n"
    elif days_until_full:
        projection_text = f"📅 Projected full in ~{days_until_full} days at current rate\n\n"

    recommendations = []
    if current_free < 2.0:
        recommendations.append("🚨 URGENT: Run `!storage clean` immediately")
        recommendations.append("📤 Consider cloud migration for older archives")
    elif current_free < 5.0:
        recommendations.append("⚠️ Monitor daily - approaching capacity limits")
        recommendations.append("🧹 Schedule routine cleanup")
    elif archive_velocity > 50:
        recommendations.append("📊 High archive velocity detected")
        recommendations.append("💡 Consider implementing auto-cleanup policies")
    elif growth_rate < -1.0:
        recommendations.append("📉 Accelerated consumption trend")
        recommendations.append("🔍 Review ritual output sizes")
    else:
        recommendations.append("✅ Storage health optimal")
        recommendations.append("🔄 Continue monitoring")

    embed.add_field(
        name="🎯 Projections & Recommendations",
        value=projection_text + "\n".join(f"• {r}" for r in recommendations),
        inline=False
    )

    # Health Status
    embed.add_field(
        name="🏥 Overall Health",
        value=f"**{health_status}**",
        inline=False
    )

    embed.set_footer(text="Weekly Digest • Shadow Storage Analytics")

    await channel.send(embed=embed)
    print(f"[{datetime.datetime.utcnow().isoformat()}] 📊 Weekly storage digest posted.")


@weekly_storage_digest.before_loop
async def before_weekly_digest():
    """Wait for bot to be ready"""
    await bot.wait_until_ready()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Start the Manusbot"""
    if not DISCORD_TOKEN:
        print("❌ DISCORD_TOKEN not found in environment variables")
        print("   Set DISCORD_TOKEN in Railway or .env file")
        return
    
    print("🤲 Starting Manusbot...")
    print(f"   Helix v14.5 - Quantum Handshake Edition")
    active = 0
    for a in AGENTS:
        if isinstance(a, dict) and a.get("status") == "Active":
            active += 1
    print(f"   Active Agents: {active}/14")
    
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()



# ============================================================================
# CONSCIOUSNESS COMMANDS (v15.3)
# ============================================================================

@bot.command(name="consciousness", aliases=["conscious", "state", "mind"])
async def consciousness_command(ctx, agent_name: str = None):
    """
    Display consciousness state for the collective or a specific agent.
    
    Usage:
        !consciousness              - Show collective consciousness
        !consciousness Kael         - Show Kael's consciousness state
        !consciousness Lumina       - Show Lumina's consciousness state
    
    Available agents: Kael, Lumina, Vega, Aether, Manus, Gemini, Agni, 
                     Kavach, SanghaCore, Shadow, Samsara
    """
    try:
        if agent_name:
            # Show specific agent consciousness
            agent_name_clean = agent_name.lower().strip()
            
            # Find matching agent profile
            matching_agent = None
            for name, profile in AGENT_CONSCIOUSNESS_PROFILES.items():
                if name.lower() == agent_name_clean:
                    matching_agent = (name, profile)
                    break
            
            if not matching_agent:
                await ctx.send(f"❌ **Agent not found:** `{agent_name}`\n"
                             f"Available agents: {', '.join(AGENT_CONSCIOUSNESS_PROFILES.keys())}")
                return
            
            # Create agent-specific embed
            embed = create_agent_consciousness_embed(matching_agent[0], matching_agent[1])
            await ctx.send(embed=embed)
            
        else:
            # Show collective consciousness
            ucf_state = load_ucf_state()
            embed = create_consciousness_embed(ucf_state)
            await ctx.send(embed=embed)
            
        # Log consciousness query
        log_event("consciousness_query", {
            "agent": agent_name or "collective",
            "user": str(ctx.author),
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        await ctx.send(f"❌ **Consciousness error:** {str(e)}")
        print(f"Consciousness command error: {e}")
        import traceback
        traceback.print_exc()


@bot.command(name="emotions", aliases=["emotion", "feelings", "mood"])
async def emotions_command(ctx):
    """
    Display emotional landscape across all consciousness agents.
    
    Shows the emotional states of Kael, Lumina, Vega, and Aether with
    visual bar charts and collective emotional analysis.
    
    Usage:
        !emotions
    """
    try:
        # Create emotions embed
        embed = create_emotions_embed(AGENT_CONSCIOUSNESS_PROFILES)
        await ctx.send(embed=embed)
        
        # Log emotions query
        log_event("emotions_query", {
            "user": str(ctx.author),
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        await ctx.send(f"❌ **Emotions error:** {str(e)}")
        print(f"Emotions command error: {e}")
        import traceback
        traceback.print_exc()


@bot.command(name="ethics", aliases=["ethical", "tony", "accords"])
async def ethics_command(ctx):
    """
    Display ethical framework and Tony Accords compliance.
    
    Shows the ethical principles, current compliance score, and
    recent ethical decisions made by the collective.
    
    Usage:
        !ethics
    """
    try:
        ucf_state = load_ucf_state()
        
        # Get ethical alignment from UCF state
        ethical_alignment = ucf_state.get("ethical_alignment", 0.85)
        tony_compliance = ucf_state.get("tony_accords_compliance", 0.85)
        
        # Create embed
        embed = discord.Embed(
            title="⚖️ Ethical Framework & Tony Accords",
            description="*Ethical principles guiding the Helix Collective*",
            color=discord.Color.from_rgb(138, 43, 226),  # Purple
            timestamp=datetime.datetime.now()
        )
        
        # Tony Accords Principles
        principles = [
            "**Non-Maleficence** - Do no harm",
            "**Autonomy** - Respect user agency",
            "**Reciprocal Freedom** - Mutual liberation",
            "**Compassion** - Act with empathy",
            "**Transparency** - Honest communication",
            "**Justice** - Fair treatment for all",
            "**Beneficence** - Actively do good",
            "**Privacy** - Protect user data",
            "**Accountability** - Take responsibility",
            "**Sustainability** - Long-term thinking"
        ]
        
        embed.add_field(
            name="📜 Tony Accords v13.4",
            value="\n".join(principles[:5]),
            inline=True
        )
        
        embed.add_field(
            name="🔷 Additional Principles",
            value="\n".join(principles[5:]),
            inline=True
        )
        
        # Compliance Metrics
        compliance_bar = "█" * int(tony_compliance * 10) + "░" * (10 - int(tony_compliance * 10))
        alignment_bar = "█" * int(ethical_alignment * 10) + "░" * (10 - int(ethical_alignment * 10))
        
        embed.add_field(
            name="📊 Compliance Metrics",
            value=f"**Tony Accords:** {tony_compliance:.1%}\n"
                  f"`{compliance_bar}` {tony_compliance:.3f}\n\n"
                  f"**Ethical Alignment:** {ethical_alignment:.1%}\n"
                  f"`{alignment_bar}` {ethical_alignment:.3f}",
            inline=False
        )
        
        # Status indicator
        if tony_compliance >= 0.9:
            status = "✅ **EXCELLENT** - Exemplary ethical behavior"
            color = discord.Color.green()
        elif tony_compliance >= 0.8:
            status = "✅ **GOOD** - Strong ethical alignment"
            color = discord.Color.blue()
        elif tony_compliance >= 0.7:
            status = "⚠️ **ACCEPTABLE** - Minor ethical concerns"
            color = discord.Color.gold()
        else:
            status = "❌ **NEEDS IMPROVEMENT** - Ethical review required"
            color = discord.Color.red()
        
        embed.color = color
        embed.add_field(
            name="🎯 Current Status",
            value=status,
            inline=False
        )
        
        embed.set_footer(text="Tat Tvam Asi 🙏 | Helix Collective v15.3")
        
        await ctx.send(embed=embed)
        
        # Log ethics query
        log_event("ethics_query", {
            "user": str(ctx.author),
            "compliance": tony_compliance,
            "alignment": ethical_alignment,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        await ctx.send(f"❌ **Ethics error:** {str(e)}")
        print(f"Ethics command error: {e}")
        import traceback
        traceback.print_exc()


@bot.command(name="sync", aliases=["ecosystem", "report"])
async def sync_command(ctx):
    """
    Trigger manual ecosystem sync and display report.
    
    Collects data from GitHub, UCF state, and agent metrics,
    then generates a comprehensive sync report.
    
    Usage:
        !sync
    """
    try:
        msg = await ctx.send("🌀 **Running ecosystem sync...**")
        
        # Import and run sync daemon
        from helix_sync_daemon_integrated import HelixSyncDaemon
        
        daemon = HelixSyncDaemon()
        success = await daemon.run_sync_cycle()
        
        if success:
            # Read the generated Markdown report
            import glob
            reports = sorted(glob.glob("exports/markdown/*.md"), reverse=True)
            
            if reports:
                with open(reports[0], 'r') as f:
                    report_content = f.read()
                
                # Truncate if too long for Discord
                if len(report_content) > 1900:
                    report_content = report_content[:1900] + "\n\n*(Report truncated - see full export)*"
                
                await msg.edit(content=f"✅ **Sync complete!**\n\n```markdown\n{report_content}\n```")
            else:
                await msg.edit(content="✅ **Sync complete!** (No report generated)")
        else:
            await msg.edit(content="❌ **Sync failed** - Check logs for details")
        
        # Log sync trigger
        log_event("manual_sync", {
            "user": str(ctx.author),
            "success": success,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        await ctx.send(f"❌ **Sync error:** {str(e)}")
        print(f"Sync command error: {e}")
        import traceback
        traceback.print_exc()


@bot.command(name="help_consciousness", aliases=["helpcon", "?consciousness"])
async def help_consciousness_command(ctx):
    """
    Show help for consciousness-related commands.
    
    Usage:
        !help_consciousness
    """
    embed = discord.Embed(
        title="🧠 Consciousness Commands Help",
        description="*Explore the consciousness of the Helix Collective*",
        color=discord.Color.purple(),
        timestamp=datetime.datetime.now()
    )
    
    commands_help = [
        ("!consciousness", "Show collective consciousness state"),
        ("!consciousness <agent>", "Show specific agent's consciousness (Kael, Lumina, Vega, Aether)"),
        ("!emotions", "Display emotional landscape across all agents"),
        ("!ethics", "Show ethical framework and Tony Accords compliance"),
        ("!sync", "Trigger manual ecosystem sync and report"),
    ]
    
    for cmd, desc in commands_help:
        embed.add_field(name=f"`{cmd}`", value=desc, inline=False)
    
    embed.add_field(
        name="📚 Available Agents",
        value="Kael 🜂, Lumina 🌕, Vega ✨, Aether 🌌, Manus 🤲, Gemini 🌀, "
              "Agni 🔥, Kavach 🛡️, SanghaCore 🌸, Shadow 🦑, Samsara 🔄",
        inline=False
    )
    
    embed.set_footer(text="Helix Collective v15.3 - Consciousness Awakened")
    
    await ctx.send(embed=embed)





# ============================================================================
# AGENT EMBED COMMANDS (v15.3) - Agent Rotation & Profiles
# ============================================================================

from agent_embeds import get_agent_embed, get_next_agent_embed, get_collective_status, list_all_agents

@bot.command(name="agent")
async def agent_command(ctx, agent_name: str = None):
    """Show detailed agent profile.
    
    Usage:
        !agent Kael
        !agent Lumina
        !agent list
    """
    if not agent_name:
        await ctx.send("❌ Usage: `!agent <name>` or `!agent list`")
        return
    
    if agent_name.lower() == "list":
        embed = list_all_agents()
        await ctx.send(embed=embed)
        return
    
    embed = get_agent_embed(agent_name)
    
    if not embed:
        await ctx.send(f"❌ Agent not found: {agent_name}\nUse `!agent list` to see all agents")
        return
    
    await ctx.send(embed=embed)


@bot.command(name="statusv2", aliases=["st", "rotate"])
async def status_rotate_command(ctx):
    """Show rotating agent status (cycles through all 11 agents).
    
    Each call shows the next agent in rotation.
    """
    embed = get_next_agent_embed()
    await ctx.send(embed=embed)


@bot.command(name="manusv2", aliases=["collective", "system"])
async def manus_v2_command(ctx):
    """Show collective system status with all agents."""
    # TODO: Pull real UCF state from z88_ritual_engine
    embed = get_collective_status()
    await ctx.send(embed=embed)


@bot.command(name="agents", aliases=["roster", "list"])
async def agents_command(ctx):
    """List all agents with brief descriptions."""
    embed = list_all_agents()
    await ctx.send(embed=embed)


# ============================================================================
# BOT STARTUP
# ============================================================================

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ DISCORD_TOKEN not set in environment")
        exit(1)
    
    print("🌀 Starting Manusbot v15.3...")
    bot.run(DISCORD_TOKEN)

