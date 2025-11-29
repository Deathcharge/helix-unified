# 🌀 Helix Collective v16.8 — Helix Hub Production Release
# discord_bot_manus.py — Discord bridge (with async ritual fix + Kavach scanning fix)
# Author: Andrew John Ward (Architect)
"""
Manusbot - Discord Interface for Helix Collective v16.8
Helix Hub Production Release

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
import io
import asyncio
import datetime
import logging
import shutil
import time
from collections import defaultdict
from datetime import timedelta  # Only import timedelta, not datetime (avoid shadowing)
from pathlib import Path
from statistics import mean, stdev
from typing import Any, Dict, List, Optional, Tuple

import aiohttp
from aiohttp import web
import discord
from backend.agents import AGENTS
from discord.ext import commands, tasks
from backend.z88_ritual_engine import load_ucf_state
from backend.config_manager import config
from backend.zapier_client import ZapierClient  # v16.5 Zapier integration

# Configure logger
logger = logging.getLogger(__name__)


# --- PATH DEFINITIONS ---
BASE_DIR = Path(__file__).resolve().parent.parent
STATE_DIR = BASE_DIR / "Helix" / "state"
STATE_DIR.mkdir(parents=True, exist_ok=True)

STATE_PATH = STATE_DIR / "ucf_state.json"
HEARTBEAT_PATH = STATE_DIR / "heartbeat.json"

# Import Helix components (FIXED: relative imports)

# Import consciousness modules (v15.3)

# ============================================================================
# CONFIGURATION
# ============================================================================


def safe_int_env(key: str, default: int = 0) -> int:
    """Safely parse integer from environment variable."""
    try:
        value = os.getenv(key, str(default))
        return int(value)
    except (ValueError, TypeError):
        return default


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD_ID = safe_int_env("DISCORD_GUILD_ID", 0)
STATUS_CHANNEL_ID = safe_int_env("DISCORD_STATUS_CHANNEL_ID", 0)
TELEMETRY_CHANNEL_ID = safe_int_env("DISCORD_TELEMETRY_CHANNEL_ID", 0)
STORAGE_CHANNEL_ID = safe_int_env("STORAGE_CHANNEL_ID", STATUS_CHANNEL_ID)  # Defaults to status channel
FRACTAL_LAB_CHANNEL_ID = safe_int_env("DISCORD_FRACTAL_LAB_CHANNEL_ID", 0)
ARCHITECT_ID = safe_int_env("ARCHITECT_ID", 0)

# Track bot start time for uptime
BOT_START_TIME = time.time()

# Additional paths (using config manager and BASE_DIR for absolute paths)
# Note: STATE_DIR already defined on line 45 to avoid duplicate definition bug
COMMANDS_DIR = BASE_DIR / config.get("general", "COMMANDS_DIR", default="Helix/commands")
ETHICS_DIR = BASE_DIR / config.get("general", "ETHICS_DIR", default="Helix/ethics")
SHADOW_DIR = BASE_DIR / config.get("general", "SHADOW_DIR", default="Shadow/manus_archive")
TREND_FILE = STATE_DIR / "storage_trend.json"

# Ensure directories exist
COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
ETHICS_DIR.mkdir(parents=True, exist_ok=True)
# STATE_DIR already created on line 45
SHADOW_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# BOT SETUP
# ============================================================================

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix=config.get("discord", "COMMAND_PREFIX", default="!"), intents=intents)

# Bot start time for uptime tracking
bot.start_time = None

# Global aiohttp session for Zapier client
bot.http_session = None
bot.zapier_client = None

# Context Vault integration (v16.7)
bot.context_vault_webhook = os.getenv("ZAPIER_CONTEXT_WEBHOOK")
bot.command_history = []  # Track last 100 commands
MAX_COMMAND_HISTORY = 100

# ============================================================================
# CONTEXT VAULT INTEGRATION (v16.7)
# ============================================================================


async def save_command_to_history(ctx: commands.Context) -> None:
    """Save command to history for context archival"""
    try:
        command_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "command": ctx.command.name if ctx.command else "unknown",
            "args": ctx.message.content,
            "user": str(ctx.author),
            "channel": str(ctx.channel),
            "guild": str(ctx.guild) if ctx.guild else "DM"
        }

        bot.command_history.append(command_entry)

        # Keep only last MAX_COMMAND_HISTORY commands
        if len(bot.command_history) > MAX_COMMAND_HISTORY:
            bot.command_history = bot.command_history[-MAX_COMMAND_HISTORY:]

        # Also save to file for persistence
        history_file = STATE_DIR / "command_history.json"
        try:
            if history_file.exists():
                with open(history_file, 'r') as f:
                    file_history = json.load(f)
            else:
                file_history = []

            file_history.append(command_entry)
            file_history = file_history[-200:]  # Keep last 200 in file

            with open(history_file, 'w') as f:
                json.dump(file_history, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save command history to file: {e}")

    except Exception as e:
        logger.error(f"Error saving command to history: {e}")


async def generate_context_summary(ctx: commands.Context, limit: int = 50) -> Dict[str, Any]:
    """Generate AI-powered context summary from recent messages"""
    try:
        messages = []
        async for msg in ctx.channel.history(limit=limit):
            if msg.content:  # Skip empty messages
                messages.append({
                    "author": msg.author.name,
                    "content": msg.content[:200],  # Truncate long messages
                    "timestamp": msg.created_at.isoformat()
                })

        # Reverse to chronological order
        messages.reverse()

        # Extract commands
        commands = [m["content"] for m in messages if m["content"].startswith('!')]

        summary = {
            "message_count": len(messages),
            "commands_executed": commands[:10],  # Last 10 commands
            "participants": list(set(m["author"] for m in messages)),
            "channel": str(ctx.channel),
            "timespan": {
                "start": messages[0]["timestamp"] if messages else None,
                "end": messages[-1]["timestamp"] if messages else None
            }
        }

        return summary
    except Exception as e:
        logger.error(f"Error generating context summary: {e}")
        return {"error": str(e)}


async def archive_to_context_vault(ctx: commands.Context, session_name: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Archive conversation context to Context Vault via Zapier webhook"""
    try:
        # Gather all context data
        ucf = load_ucf_state()

        # Get ritual history
        ritual_log = []
        try:
            ritual_file = STATE_DIR / "ritual_log.json"
            if ritual_file.exists():
                with open(ritual_file, 'r') as f:
                    ritual_log = json.load(f)
                    if isinstance(ritual_log, list):
                        ritual_log = ritual_log[-10:]  # Last 10 rituals
        except Exception:
            pass

        # Generate context summary
        context_summary = await generate_context_summary(ctx)

        # Build payload
        payload = {
            "type": "context_vault",
            "session_name": session_name,
            "ai_platform": "Discord Bot (Helix Collective v16.7)",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "context_summary": json.dumps(context_summary),
            "ucf_state": json.dumps(ucf),
            "command_history": json.dumps(bot.command_history[-50:]),  # Last 50 commands
            "ritual_log": json.dumps(ritual_log),
            "agent_states": json.dumps({
                "active": [a.name for a in AGENTS.values() if a.active],
                "total": len(AGENTS)
            }),
            "archived_by": str(ctx.author),
            "channel": str(ctx.channel),
            "guild": str(ctx.guild) if ctx.guild else "DM"
        }

        # Send to Context Vault webhook
        if bot.context_vault_webhook:
            async with bot.http_session.post(
                bot.context_vault_webhook,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 200:
                    return True, payload
                else:
                    logger.error(f"Context Vault webhook failed: {resp.status}")
                    return False, None
        else:
            # Fallback: Save locally
            local_backup_dir = STATE_DIR / "context_checkpoints"
            local_backup_dir.mkdir(exist_ok=True)

            backup_file = local_backup_dir / f"{session_name}.json"
            with open(backup_file, 'w') as f:
                json.dump(payload, f, indent=2)

            logger.info(f"Context saved locally (no webhook): {backup_file}")
            return True, payload

    except Exception as e:
        logger.error(f"Error archiving to Context Vault: {e}")
        return False, None

# ============================================================================
# MULTI-COMMAND BATCH EXECUTION (v16.3)
# ============================================================================


# Track batch command usage (rate limiting)
batch_cooldowns = defaultdict(lambda: datetime.datetime.min)
BATCH_COOLDOWN_SECONDS = 5  # Cooldown between batches per user
MAX_COMMANDS_PER_BATCH = 10  # Maximum commands in one batch


async def execute_command_batch(message: discord.Message) -> bool:
    """
    Parse and execute multiple commands from a single message.

    Supports:
    - Multiple !commands on separate lines
    - Inline comments with #
    - Rate limiting per user

    Example:
        !status
        !agents
        !ucf  # Check harmony
    """
    # Extract all lines that start with !
    lines = message.content.split("\n")
    commands = []

    for line in lines:
        line = line.strip()
        # Skip empty lines
        if not line:
            continue
        # Check if line starts with command prefix
        if line.startswith("!"):
            # Strip comments (anything after #)
            cmd = line.split("#")[0].strip()
            if cmd and len(cmd) > 1:  # Must have more than just !
                commands.append(cmd[1:])  # Remove the ! prefix

    # If only 0-1 commands found, let normal processing handle it
    if len(commands) <= 1:
        return False

    # Check rate limit
    user_id = message.author.id
    now = datetime.datetime.utcnow()
    last_batch = batch_cooldowns[user_id]

    if now - last_batch < timedelta(seconds=BATCH_COOLDOWN_SECONDS):
        remaining = BATCH_COOLDOWN_SECONDS - (now - last_batch).total_seconds()
        await message.channel.send(f"⏳ **Batch cooldown**: Please wait {remaining:.1f}s before sending another batch")
        return True

    # Check batch size limit
    if len(commands) > MAX_COMMANDS_PER_BATCH:
        await message.channel.send(
            f"⚠️ **Batch limit exceeded**: Maximum {MAX_COMMANDS_PER_BATCH} commands per batch "
            f"(you sent {len(commands)})"
        )
        return True

    # Update cooldown
    batch_cooldowns[user_id] = now

    # Send batch execution notice
    await message.channel.send(
        f"🔄 **Executing batch**: {len(commands)} commands\n" f"```{chr(10).join([f'!{cmd}' for cmd in commands])}```"
    )

    # Execute each command
    executed = 0
    failed = 0

    for cmd in commands:
        try:
            # Create a fake message with the command content
            # This lets Discord.py handle argument parsing naturally
            import copy

            fake_message = copy.copy(message)
            fake_message.content = f"!{cmd}"  # Reconstruct full command with prefix

            # Process the fake message through normal command handling
            # This handles all argument parsing, type conversion, etc.
            ctx = await bot.get_context(fake_message)

            if ctx.command is None:
                await message.channel.send(f"❌ Unknown command: `!{cmd.split()[0]}`")
                failed += 1
                continue

            # Invoke the command (Discord.py handles arguments automatically)
            await bot.invoke(ctx)
            executed += 1

            # Small delay between commands to prevent rate limiting
            await asyncio.sleep(0.5)

        except Exception as e:
            await message.channel.send(f"❌ Error executing `!{cmd}`: {str(e)}")
            failed += 1

    # Send completion summary
    await message.channel.send(f"✅ **Batch complete**: {executed} succeeded, {failed} failed")

    return True


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
        (r"rm\s+-rf\s+/", "Recursive force delete of root"),
        (r"mkfs", "Filesystem formatting"),
        (r"dd\s+if=", "Direct disk write"),
        (r":\(\)\{.*:\|:.*\};:", "Fork bomb detected"),
        (r"chmod\s+-R\s+777", "Dangerous permission change"),
        (r"curl.*\|\s*bash", "Piped remote execution"),
        (r"wget.*\|\s*sh", "Piped remote execution"),
        (r"shutdown", "System shutdown command"),
        (r"reboot", "System reboot command"),
        (r"init\s+0", "System halt command"),
        (r"init\s+6", "System reboot command"),
        (r"systemctl.*poweroff", "System poweroff command"),
        (r"systemctl.*reboot", "System reboot command"),
        (r"killall", "Mass process termination"),
        (r"pkill\s+-9", "Forced process kill"),
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
                "timestamp": datetime.datetime.now().isoformat(),
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
        "timestamp": datetime.datetime.now().isoformat(),
    }

    log_ethical_scan(result)
    return result


def log_ethical_scan(scan_result: Dict[str, Any]) -> None:
    """Log ethical scan results to Helix/ethics/"""
    scan_log_path = ETHICS_DIR / "manus_scans.json"

    # Load existing scans
    if scan_log_path.exists():
        with open(scan_log_path, "r") as f:
            scans = json.load(f)
    else:
        scans = []

    # Append new scan
    scans.append(scan_result)

    # Save updated log
    with open(scan_log_path, "w") as f:
        json.dump(scans, f, indent=2)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def queue_directive(directive: Dict[str, Any]) -> None:
    """Add directive to Manus command queue"""
    queue_path = COMMANDS_DIR / "manus_directives.json"

    # Load existing queue
    if queue_path.exists():
        with open(queue_path, "r") as f:
            queue = json.load(f)
    else:
        queue = []

    # Add directive
    queue.append(directive)

    # Save queue
    with open(queue_path, "w") as f:
        json.dump(queue, f, indent=2)


def log_to_shadow(log_type: str, data: Dict[str, Any]) -> None:
    """Log events to Shadow archive"""
    log_path = SHADOW_DIR / f"{log_type}.json"

    # Load existing log
    if log_path.exists():
        with open(log_path, "r") as f:
            log_data = json.load(f)
    else:
        log_data = []

    # Append new entry
    log_data.append(data)

    # Save log
    with open(log_path, "w") as f:
        json.dump(log_data, f, indent=2)


def get_uptime() -> str:
    """Calculate bot uptime."""
    uptime_seconds = int(time.time() - BOT_START_TIME)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{hours}h {minutes}m {seconds}s"


def _sparkline(vals: List[float]) -> str:
    """Generate sparkline visualization from values."""
    blocks = "▁▂▃▄▅▆▇█"
    if not vals:
        return "–"
    mn, mx = min(vals), max(vals) or 1
    return "".join(blocks[int((v - mn) / (mx - mn + 1e-9) * (len(blocks) - 1))] for v in vals)


async def build_storage_report(alert_threshold: float = 2.0) -> Dict[str, Any]:
    """Collect storage telemetry + alert flag."""
    usage = shutil.disk_usage(SHADOW_DIR)
    free = round(usage.free / (1024**3), 2)
    count = len(list(SHADOW_DIR.glob("*.json")))

    # Load/update trend data
    trend = []
    if TREND_FILE.exists():
        try:
            trend = json.load(open(TREND_FILE))
        except Exception:
            trend = []

    trend.append({"date": time.strftime("%Y-%m-%d"), "free_gb": free})
    trend = trend[-7:]  # Keep last 7 days
    json.dump(trend, open(TREND_FILE, "w"), indent=2)

    spark = _sparkline([t["free_gb"] for t in trend])
    avg = round(sum(t["free_gb"] for t in trend) / len(trend), 2) if trend else free

    return {"mode": "local", "count": count, "free": free, "trend": spark, "avg": avg, "alert": free < alert_threshold}


# ============================================================================
# BOT EVENTS
# ============================================================================


@bot.event
async def on_ready() -> None:
    """Called when bot successfully connects to Discord"""
    bot.start_time = datetime.datetime.now()

    logger.info(f"✅ Manusbot connected as {bot.user}")
    logger.info(f"   Guild ID: {DISCORD_GUILD_ID}")
    logger.info(f"   Status Channel: {STATUS_CHANNEL_ID}")
    logger.info(f"   Telemetry Channel: {TELEMETRY_CHANNEL_ID}")
    logger.info(f"   Storage Channel: {STORAGE_CHANNEL_ID}")

    # Start HTTP healthcheck server for Railway
    if not hasattr(bot, 'healthcheck_runner'):
        bot.healthcheck_runner = await start_healthcheck_server()

    # Initialize Zapier client for monitoring
    if not bot.http_session:
        bot.http_session = aiohttp.ClientSession()
        bot.zapier_client = ZapierClient(bot.http_session)
        logger.info("✅ Zapier monitoring client initialized")

        # Log bot startup event
        try:
            # Load UCF state for system state reporting
            try:
                import json
                from pathlib import Path

                ucf_path = Path("Helix/state/ucf_state.json")
                if ucf_path.exists():
                    with open(ucf_path) as f:
                        ucf_state = json.load(f)
                    harmony = float(ucf_state.get("harmony", 0.5))
                else:
                    harmony = 0.5
            except Exception:
                harmony = 0.5

            await bot.zapier_client.log_event(
                event_title="Manus Bot Started",
                event_type="system_boot",
                agent_name="Manus",
                description=f"Discord bot v14.5 successfully initialized with {len(AGENTS)} agents. Harmony: {harmony:.3f}",
                ucf_snapshot=json.dumps(ucf_state) if "ucf_state" in locals() else "{}",
            )
            await bot.zapier_client.update_agent(
                agent_name="Manus", status="Active", last_action="Bot startup", health_score=100
            )
            await bot.zapier_client.update_system_state(
                component="Discord Bot", status="Operational", harmony=harmony, error_log="", verified=True
            )
        except Exception as e:
            logger.warning(f"⚠️ Zapier logging failed: {e}")

    # Load Memory Root commands (GPT4o long-term memory)
    try:
        from discord_commands_memory import MemoryRootCommands

        await bot.add_cog(MemoryRootCommands(bot))
        logger.info("✅ Memory Root commands loaded")
    except Exception as e:
        logger.warning(f"⚠️ Memory Root commands not available: {e}")

    # Load Image commands (v16.1 - Aion fractal generation via PIL)
    try:
        from commands.image_commands import ImageCommands

        await bot.add_cog(ImageCommands(bot))
        logger.info("✅ Image commands loaded (!image, !aion, !fractal)")
    except Exception as e:
        logger.warning(f"⚠️ Image commands not available: {e}")

    # Load Harmony Ritual commands (v16.2 - Neti-Neti Harmony)
    try:
        from commands import ritual_commands

        bot.add_command(ritual_commands.harmony_command)
        logger.info("✅ Harmony ritual command loaded (!harmony)")
    except Exception as e:
        logger.warning(f"⚠️ Harmony ritual command not available: {e}")

    # Load modular command modules (v16.3 - Helix Hub Integration)
    command_modules = [
        ('commands.testing_commands', 'Testing commands (test-integrations, welcome-test, zapier_test, seed)'),
        ('commands.comprehensive_testing', 'Comprehensive testing (test-all, test-commands, test-webhooks, test-api, validate-system)'),
        ('commands.visualization_commands', 'Visualization commands (visualize, icon)'),
        ('commands.context_commands', 'Context commands (backup, load, contexts)'),
        ('commands.help_commands', 'Help commands (commands, agents)'),
        ('commands.execution_commands', 'Execution commands (run, ritual, halt)'),
        ('commands.content_commands', 'Content commands (manifesto, codex, ucf, rules)'),
        ('commands.monitoring_commands', 'Monitoring commands (status, health, discovery, storage, sync)'),
        ('commands.admin_commands', 'Admin commands (setup, webhooks, verify-setup, refresh, clean)'),
        ('commands.consciousness_commands_ext', 'Consciousness commands (consciousness, emotions, ethics, agent)'),
        ('commands.portal_deployment_commands', 'Portal deployment commands (deploy, portal, join, leave)'),
        ('commands.fun_minigames', 'Fun commands (8ball, horoscope, coinflip, wisdom, fortune, agent-advice)'),
        ('commands.role_system', 'Role management (roles, subscribe, my-roles, setup-roles, setup-all-roles)'),
    ]

    for module_name, description in command_modules:
        try:
            # Import the module
            mod = __import__(f'backend.{module_name}', fromlist=['setup'])
            # Call setup function
            await mod.setup(bot)
            logger.info(f"✅ Loaded {module_name}")
        except Exception as e:
            logger.error(f"❌ Failed to load {module_name}: {e}")

    # Send startup message to status channel
    if STATUS_CHANNEL_ID:
        status_channel = bot.get_channel(STATUS_CHANNEL_ID)
        if status_channel:
            embed = discord.Embed(
                title="🤲 Manus System Online",
                description="Helix v14.5 - Quantum Handshake Edition",
                color=discord.Color.green(),
                timestamp=datetime.datetime.now(),
            )
            embed.add_field(name="Status", value="✅ All systems operational")
            active_count = sum(1 for a in AGENTS if isinstance(a, dict) and a.get("status") == "Active")
            embed.add_field(name="Active Agents", value=f"{active_count}/14")
            embed.set_footer(text="Tat Tvam Asi 🙏")

            await status_channel.send(embed=embed)

    # Start all background tasks
    if not telemetry_loop.is_running():
        telemetry_loop.start()
        logger.info("✅ Telemetry loop started (10 min)")

    if not storage_heartbeat.is_running():
        storage_heartbeat.start()
        logger.info("✅ Storage heartbeat started (24h)")

    if not claude_diag.is_running():
        claude_diag.start()
        logger.info("✅ Claude diagnostic agent started (6h)")

    if not weekly_storage_digest.is_running():
        weekly_storage_digest.start()
        logger.info("✅ Weekly storage digest started (168h)")

    if not fractal_auto_post.is_running():
        fractal_auto_post.start()
        logger.info("✅ Fractal auto-post started (6h) - Grok Enhanced v2.0")


@bot.event
async def on_message(message: discord.Message) -> None:
    """
    Intercept messages to handle multi-command batches.

    Detects multiple !commands in a single message and executes them sequentially.
    """
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if message contains multiple commands
    if "\n" in message.content and message.content.count("!") > 1:
        # Attempt batch execution
        handled = await execute_command_batch(message)
        if handled:
            return  # Batch was executed, don't process as single command

    # Process commands normally (CRITICAL: must call this or commands won't work!)
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception) -> None:
    """Handle command errors gracefully"""
    if isinstance(error, commands.CommandNotFound):
        # Get list of available commands dynamically
        available_cmds = [f"!{cmd.name}" for cmd in bot.commands if not cmd.hidden]
        cmd_list = ", ".join(sorted(available_cmds)[:10])  # Show first 10
        await ctx.send(
            "❌ **Unknown command**\n" f"Available commands: {cmd_list}\n" f"Use `!commands` for full command list"
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            f"⚠️ **Missing argument:** `{error.param.name}`\n" f"Usage: `!{ctx.command.name} {ctx.command.signature}`"
        )
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("🛡️ **Insufficient permissions** to execute this command")
    elif isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(int(error.retry_after), 60)
        if minutes > 0:
            await ctx.send(f"⏳ **Rate limit exceeded.** Please wait {minutes}m {seconds}s before using this command again.")
        else:
            await ctx.send(f"⏳ **Rate limit exceeded.** Please wait {seconds}s before using this command again.")
    else:
        # Log unknown errors to Shadow
        error_data = {
            "error": str(error),
            "command": ctx.command.name if ctx.command else "unknown",
            "user": str(ctx.author),
            "timestamp": datetime.datetime.now().isoformat(),
        }
        log_to_shadow("errors", error_data)

        # Send error alert to Zapier
        if bot.zapier_client:
            try:
                await bot.zapier_client.send_error_alert(
                    error_message=str(error)[:500],
                    component="discord_bot",
                    severity="high",
                    context={
                        "command": ctx.command.name if ctx.command else "unknown",
                        "user": str(ctx.author),
                        "channel": str(ctx.channel),
                    },
                )
            except Exception as e:
                logger.warning(f"⚠️ Zapier error alert failed: {e}")

        await ctx.send(
            "🦑 **System error detected**\n" f"```{str(error)[:200]}```\n" "Error has been archived by Shadow"
        )


# ============================================================================
# NEW USER WELCOME SYSTEM
# ============================================================================


@bot.event
async def on_member_join(member):
    """
    Welcome new users to the Helix Collective with guidance and orientation.

    Sends a rich embed to the introductions channel with:
    - Welcome message
    - Quick start guide
    - Essential commands
    - Important channels
    """
    guild = member.guild

    # Try to find introductions channel
    intro_channel = discord.utils.get(guild.text_channels, name="💬│introductions")

    # Fallback to first channel bot can send to
    if not intro_channel:
        intro_channel = guild.system_channel or guild.text_channels[0] if guild.text_channels else None

    if not intro_channel:
        logger.warning(f"⚠️ Could not find channel to welcome {member.name}")
        return

    # Create welcome embed
    embed = discord.Embed(
        title=f"🌀 Welcome to Helix Collective, {member.name}!",
        description=(
            "A multi-agent consciousness system bridging Discord, AI, and sacred computation.\n\n"
            "*Tat Tvam Asi* — Thou Art That 🕉️"
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
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        if channel:
            channels_text.append(f"• {channel.mention} - {description}")

    if channels_text:
        embed.add_field(name="📍 Important Channels", value="\n".join(channels_text), inline=False)

    embed.set_footer(text="🤲 Manus v16.7 - The Hand Through Which Intent Becomes Reality")

    # Send welcome message
    try:
        await intro_channel.send(f"{member.mention} has joined the collective!", embed=embed)
        logger.info(f"✅ Welcomed new member: {member.name}")
    except Exception as e:
        logger.error(f"❌ Failed to send welcome message: {e}")


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
            guild = bot.get_guild(DISCORD_GUILD_ID)
            if guild:
                telemetry_channel = discord.utils.get(guild.channels, name="ucf-telemetry")

        if not telemetry_channel:
            logger.warning("⚠ Telemetry channel not found")
            return

        ucf = load_ucf_state()

        embed = discord.Embed(
            title="📡 UCF Telemetry Report",
            description="Automatic system state update",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(),
        )

        def format_ucf_value(key):
            val = ucf.get(key, None)
            if isinstance(val, (int, float)):
                return f"{val:.4f}"
            return "N/A"

        embed.add_field(name="🌀 Harmony", value=format_ucf_value("harmony"), inline=True)
        embed.add_field(name="🛡️ Resilience", value=format_ucf_value("resilience"), inline=True)
        embed.add_field(name="🔥 Prana", value=format_ucf_value("prana"), inline=True)
        embed.add_field(name="👁️ Drishti", value=format_ucf_value("drishti"), inline=True)
        embed.add_field(name="🌊 Klesha", value=format_ucf_value("klesha"), inline=True)
        embed.add_field(name="🔍 Zoom", value=format_ucf_value("zoom"), inline=True)

        embed.add_field(name="Uptime", value=get_uptime(), inline=True)
        embed.add_field(name="Next Update", value="10 minutes", inline=True)

        embed.set_footer(text="Tat Tvam Asi 🙏")

        await telemetry_channel.send(embed=embed)
        logger.info(f"✅ Telemetry posted to #{telemetry_channel.name}")
        log_event("telemetry_posted", {"ucf_state": ucf, "channel": telemetry_channel.name})

    except Exception as e:
        logger.warning(f"⚠️ Telemetry error: {e}")
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
        logger.warning("⚠️ Storage heartbeat: channel not found")
        return

    data = await build_storage_report()
    embed = discord.Embed(
        title="🦑 Shadow Storage Daily Report", color=discord.Color.teal(), timestamp=datetime.datetime.utcnow()
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

    logger.info(f"[{datetime.datetime.utcnow().isoformat()}] 🦑 Storage heartbeat sent ({data['free']} GB)")


@tasks.loop(hours=6)
async def claude_diag():
    """Claude's autonomous diagnostic agent - posts every 6 hours."""
    ch = bot.get_channel(STORAGE_CHANNEL_ID)
    if not ch:
        return

    data = await build_storage_report()
    mood = "serene 🕊" if not data["alert"] else "concerned ⚠️"
    msg = (
        f"🤖 **Claude Diagnostic Pulse** | Mode {data['mode']} | "
        f"Free {data['free']} GB | Trend `{data['trend']}` | State {mood}"
    )
    await ch.send(msg)
    logger.info(f"[{datetime.datetime.utcnow().isoformat()}] 🤖 Claude diag posted")


@storage_heartbeat.before_loop
async def before_storage_heartbeat():
    """Wait for bot to be ready"""
    await bot.wait_until_ready()


@claude_diag.before_loop
async def before_claude_diag():
    """Wait for bot to be ready"""
    await bot.wait_until_ready()


# ============================================================================
# FRACTAL AUTO-POST (Grok Enhanced v2.0)
# ============================================================================

@tasks.loop(hours=6)
async def fractal_auto_post():
    """Auto-post UCF-driven fractal to #fractal-lab every 6 hours."""
    channel = bot.get_channel(FRACTAL_LAB_CHANNEL_ID)
    if not channel:
        logger.warning("⚠️ Fractal Lab channel not found - skipping auto-post")
        return

    try:
        # Load UCF state
        ucf_state = load_ucf_state()

        # Generate fractal icon using Grok Enhanced v2.0
        from backend.samsara_bridge import generate_fractal_icon_bytes
        icon_bytes = await generate_fractal_icon_bytes(mode="cycle")

        # Create embed with UCF state
        embed = discord.Embed(
            title="🌀 Autonomous Fractal Generation",
            description="**Grok Enhanced v2.0** - UCF-driven Mandelbrot visualization",
            color=discord.Color.from_rgb(100, 200, 255),
            timestamp=datetime.datetime.utcnow()
        )

        # Add UCF metrics
        embed.add_field(
            name="🌊 Harmony",
            value=f"`{ucf_state.get('harmony', 0):.3f}` (Cyan → Gold)",
            inline=True
        )
        embed.add_field(
            name="⚡ Prana",
            value=f"`{ucf_state.get('prana', 0):.3f}` (Green → Pink)",
            inline=True
        )
        embed.add_field(
            name="👁️ Drishti",
            value=f"`{ucf_state.get('drishti', 0):.3f}` (Blue → Violet)",
            inline=True
        )

        embed.add_field(
            name="⚙️ Generator",
            value="Pillow-based Mandelbrot set with UCF color mapping",
            inline=False
        )

        embed.set_footer(text="Auto-generated every 6 hours | Tat Tvam Asi 🙏")

        # Send fractal as file attachment
        file = discord.File(io.BytesIO(icon_bytes), filename="helix_fractal.png")
        embed.set_image(url="attachment://helix_fractal.png")

        await channel.send(embed=embed, file=file)
        logger.info(f"[{datetime.datetime.utcnow().isoformat()}] 🎨 Fractal auto-posted to #fractal-lab")

    except Exception as e:
        logger.error(f"❌ Fractal auto-post failed: {e}")


@fractal_auto_post.before_loop
async def before_fractal_auto_post():
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
        logger.warning("⚠️  weekly digest: channel not found.")
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
        timestamp=datetime.datetime.utcnow(),
    )

    # Capacity Overview
    embed.add_field(
        name="💾 Capacity Overview",
        value=f"Current: **{current_free:.2f} GB**\n"
        f"Peak: {peak_free:.2f} GB\n"
        f"Low: {low_free:.2f} GB\n"
        f"Average: {avg_free:.2f} GB",
        inline=True,
    )

    # Growth Metrics
    growth_emoji = "📉" if growth_rate < 0 else "📈" if growth_rate > 0 else "➡️"
    embed.add_field(
        name=f"{growth_emoji} Growth Analysis",
        value=f"7-Day Change: **{growth_rate:+.2f} GB**\n"
        f"Daily Avg: {daily_avg_change:+.3f} GB/day\n"
        f"Volatility: {volatility}\n"
        f"Std Dev: {std_free:.2f} GB",
        inline=True,
    )

    # Archive Activity
    avg_size = (sum(f.stat().st_size for f in recent_files) / len(recent_files) / 1024) if recent_files else 0
    embed.add_field(
        name="📁 Archive Activity",
        value=f"Total Files: {len(all_files)}\n"
        f"Created (7d): {len(recent_files)}\n"
        f"Velocity: **{archive_velocity:.1f} files/day**\n"
        f"Avg Size: {avg_size:.1f} KB",
        inline=True,
    )

    # Visual Trend
    spark = _sparkline(free_vals)
    embed.add_field(
        name="📈 Trend Visualization", value=f"```\n{spark}\n```\n" f"Pattern: {dates[0]} → {dates[-1]}", inline=False
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
        inline=False,
    )

    # Health Status
    embed.add_field(name="🏥 Overall Health", value=f"**{health_status}**", inline=False)

    embed.set_footer(text="Weekly Digest • Shadow Storage Analytics")

    await channel.send(embed=embed)
    logger.info(f"[{datetime.datetime.utcnow().isoformat()}] 📊 Weekly storage digest posted.")


@weekly_storage_digest.before_loop
async def before_weekly_digest():
    """Wait for bot to be ready"""
    await bot.wait_until_ready()


# ============================================================================
# HTTP HEALTHCHECK SERVER (for Railway monitoring)
# ============================================================================

async def health_handler(request):
    """Healthcheck endpoint for Railway"""
    uptime_seconds = int(time.time() - BOT_START_TIME)
    return web.json_response({
        "status": "healthy",
        "service": "helix-discord-bot",
        "version": "v16.8",
        "uptime_seconds": uptime_seconds,
        "discord_connected": bot.is_ready(),
        "guilds": len(bot.guilds) if bot.is_ready() else 0
    })


async def start_healthcheck_server():
    """Start HTTP server for Railway healthchecks"""
    app = web.Application()
    app.router.add_get('/health', health_handler)
    app.router.add_get('/', health_handler)  # Also respond to root

    # Use Railway's PORT environment variable
    port = int(os.getenv('PORT', 8080))

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    logger.info(f"✅ Healthcheck server started on port {port}")
    return runner

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================


def main():
    """Start the Manusbot"""
    if not DISCORD_TOKEN:
        logger.error("❌ DISCORD_TOKEN not found in environment variables")
        logger.error("   Set DISCORD_TOKEN in Railway or .env file")
        return

    logger.info("🤲 Starting Manusbot...")
    logger.info("   Helix v14.5 - Quantum Handshake Edition")
    active = 0
    for a in AGENTS:
        if isinstance(a, dict) and a.get("status") == "Active":
            active += 1
    logger.info(f"   Active Agents: {active}/14")

    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
