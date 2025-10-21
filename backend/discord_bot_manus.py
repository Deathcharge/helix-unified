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
from typing import Optional, Dict, Any

import discord
from discord.ext import commands, tasks

# Import Helix components
from backend.agents import AGENTS
from backend.z88_ritual_engine import execute_ritual, load_ucf_state
from backend.services.ucf_calculator import UCFCalculator
from backend.services.state_manager import StateManager

# ============================================================================
# CONFIGURATION
# ============================================================================

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", 0))
STATUS_CHANNEL_ID = int(os.getenv("DISCORD_STATUS_CHANNEL_ID", 0))
TELEMETRY_CHANNEL_ID = int(os.getenv("DISCORD_TELEMETRY_CHANNEL_ID", 0))
ARCHITECT_ID = int(os.getenv("ARCHITECT_ID", 0))

# Paths
HELIX_ROOT = Path("Helix")
COMMANDS_DIR = HELIX_ROOT / "commands"
ETHICS_DIR = HELIX_ROOT / "ethics"
SHADOW_DIR = Path("Shadow/manus_archive")

# Ensure directories exist
COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
ETHICS_DIR.mkdir(parents=True, exist_ok=True)
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
    """Calculate bot uptime"""
    if not bot.start_time:
        return "Unknown"
    
    delta = datetime.datetime.now() - bot.start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"{hours}h {minutes}m {seconds}s"


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
            embed.add_field(name="Active Agents", value=f"{len([a for a in AGENTS if a.get('status') == 'Active'])}/14")
            embed.set_footer(text="Tat Tvam Asi 🙏")
            
            await status_channel.send(embed=embed)
    
    # Start telemetry loop
    if not telemetry_loop.is_running():
        telemetry_loop.start()


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
    """Display current system status and UCF state"""
    ucf = load_ucf_state()
    uptime = get_uptime()
    active_agents = len([a for a in AGENTS if a.get("status") == "Active"])
    
    embed = discord.Embed(
        title="🤲 Manus System Status",
        description="Helix Collective v14.5 - Quantum Handshake Edition",
        color=discord.Color.from_rgb(138, 43, 226),  # Purple
        timestamp=datetime.datetime.now()
    )
    
    # System info
    embed.add_field(
        name="⚡ Status", 
        value="✅ Operational",
        inline=True
    )
    embed.add_field(
        name="⏱️ Uptime", 
        value=f"`{uptime}`",
        inline=True
    )
    embed.add_field(
        name="🤖 Agents", 
        value=f"`{active_agents}/14` active",
        inline=True
    )
    
    # UCF state
    embed.add_field(name="🌀 Harmony", value=f"`{ucf.get('harmony', 0):.4f}`", inline=True)
    embed.add_field(name="🛡️ Resilience", value=f"`{ucf.get('resilience', 0):.4f}`", inline=True)
    embed.add_field(name="🔥 Prana", value=f"`{ucf.get('prana', 0):.4f}`", inline=True)
    embed.add_field(name="👁️ Drishti", value=f"`{ucf.get('drishti', 0):.4f}`", inline=True)
    embed.add_field(name="🌊 Klesha", value=f"`{ucf.get('klesha', 0):.4f}`", inline=True)
    embed.add_field(name="🔍 Zoom", value=f"`{ucf.get('zoom', 0):.4f}`", inline=True)
    
    embed.set_footer(text="Tat Tvam Asi 🙏")
    
    await ctx.send(embed=embed)


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


@bot.command(name="ritual")
async def execute_ritual_command(ctx, steps: int = 108):
    """Execute Z-88 ritual with specified number of steps"""
    
    if steps < 1 or steps > 1000:
        await ctx.send("⚠️ **Invalid step count**\nMust be between 1 and 1000")
        return
    
    # Load initial UCF state
    ucf_before = load_ucf_state()
    
    # Send initial message
    msg = await ctx.send(f"🔥 **Initiating Z-88 ritual sequence ({steps} steps)…**")
    
    # Execute ritual
    try:
        result = await asyncio.to_thread(execute_ritual, steps)
        
        # Load updated UCF state
        ucf_after = load_ucf_state()
        
        # Calculate changes
        harmony_change = ucf_after.get('harmony', 0) - ucf_before.get('harmony', 0)
        resilience_change = ucf_after.get('resilience', 0) - ucf_before.get('resilience', 0)
        
        # Build result message
        embed = discord.Embed(
            title="✅ Z-88 Ritual Complete",
            description=f"Completed {steps}-step ritual sequence",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        
        # Show changes
        embed.add_field(
            name="🌀 Harmony",
            value=f"`{ucf_after.get('harmony', 0):.4f}` ({harmony_change:+.4f})",
            inline=True
        )
        embed.add_field(
            name="🛡️ Resilience",
            value=f"`{ucf_after.get('resilience', 0):.4f}` ({resilience_change:+.4f})",
            inline=True
        )
        embed.add_field(
            name="🔥 Prana",
            value=f"`{ucf_after.get('prana', 0):.4f}`",
            inline=True
        )
        
        embed.set_footer(text="Tat Tvam Asi 🙏")
        
        await msg.edit(content=None, embed=embed)
        
        # Log ritual to Shadow
        ritual_log = {
            "steps": steps,
            "timestamp": datetime.datetime.now().isoformat(),
            "user": str(ctx.author),
            "ucf_before": ucf_before,
            "ucf_after": ucf_after,
            "harmony_change": harmony_change,
            "resilience_change": resilience_change
        }
        log_to_shadow("rituals", ritual_log)
        
    except Exception as e:
        await msg.edit(content=f"❌ **Ritual failed**\n```{str(e)}```")
        raise


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


# ============================================================================
# TELEMETRY LOOP
# ============================================================================

@tasks.loop(minutes=10)
async def telemetry_loop():
    """Post UCF state updates to telemetry channel every 10 minutes"""
    if not TELEMETRY_CHANNEL_ID:
        return
    
    telemetry_channel = bot.get_channel(TELEMETRY_CHANNEL_ID)
    if not telemetry_channel:
        return
    
    try:
        ucf = load_ucf_state()
        
        embed = discord.Embed(
            title="📡 UCF Telemetry Report",
            description="Automatic system state update",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(name="🌀 Harmony", value=f"`{ucf.get('harmony', 0):.4f}`", inline=True)
        embed.add_field(name="🛡️ Resilience", value=f"`{ucf.get('resilience', 0):.4f}`", inline=True)
        embed.add_field(name="🔥 Prana", value=f"`{ucf.get('prana', 0):.4f}`", inline=True)
        embed.add_field(name="👁️ Drishti", value=f"`{ucf.get('drishti', 0):.4f}`", inline=True)
        embed.add_field(name="🌊 Klesha", value=f"`{ucf.get('klesha', 0):.4f}`", inline=True)
        embed.add_field(name="🔍 Zoom", value=f"`{ucf.get('zoom', 0):.4f}`", inline=True)
        
        embed.set_footer(text="Next update in 10 minutes")
        
        await telemetry_channel.send(embed=embed)
        
    except Exception as e:
        print(f"⚠️ Telemetry loop error: {e}")


@telemetry_loop.before_loop
async def before_telemetry():
    """Wait for bot to be ready before starting telemetry"""
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
    print(f"   Active Agents: {len([a for a in AGENTS if a.get('status') == 'Active'])}/14")
    
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
