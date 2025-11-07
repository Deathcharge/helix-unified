# discord_bot_manus.py - Helix Collective v15.3 (Quantum Handshake)
# Core Agent: Manus
# Features: Harmonized Dashboard Support, Grok Analytics Integration, MEGA Sync Integration

import discord
from discord.ext import commands
import os
import random
import time
import asyncio
from mega_sync import mega_sync
import logging
import toml
import sys
from discord.ext import commands
import os
import random
import time
import asyncio
from mega_sync import mega_sync
import logging

# Import centralized logging configuration
from backend.logging_config import setup_logging, get_module_logger

# --- Configuration and Logging Setup ---
try:
    # Environment-proof config loading
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "config.toml")
    config = toml.load(config_path)
except FileNotFoundError:
    # Use basic logging for this fatal error
    logging.basicConfig(level=logging.ERROR)
    logging.error("FATAL: config.toml not found. Exiting.")
    sys.exit(1)

# Setup centralized logging (if not already done by main.py)
# This is a fallback for standalone bot execution
try:
    setup_logging(log_level=config['logging']['level'], enable_rotation=True)
except Exception:
    # If setup fails, fall back to basic logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s')

logger = get_module_logger('discord_bot')

# Import Grok's core for the !analyze command
# The actual import path will be 'grok.grok_agent_core' after deployment
# For local testing, we use a mock import
try:
    from grok.grok_agent_core import GrokAgentCore
    GROK_AGENT = GrokAgentCore()
except ImportError:
    class MockGrokAgent:
        def analyze_ucf_trends(self):
            return "Mock Analysis: UCF Harmony is trending upwards. Grok recommends a focus on Prana balance."
    GROK_AGENT = MockGrokAgent()
    logger.warning("GrokAgentCore not found. Using MockGrokAgent.")


# --- Configuration ---
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(command_prefix=config['bot']['prefix'], intents=INTENTS)

# --- Utility Functions (Mocked for Ritual Generation) ---
def generate_mock_ritual_files(ritual_id):
    """
    MOCK LOGIC: Generates placeholder .png and .wav files for the dashboard to display.
    This simulates the output of the full samsara_bridge.py logic.
    """
    timestamp = int(time.time())
    
    # Ensure state directory exists
    os.makedirs("Helix/state", exist_ok=True)
    
    # 1. Generate Mock PNG (Fractal)
    png_filename = f"Helix/state/ritual_{ritual_id}_fractal_{timestamp}.png"
    with open(png_filename, 'w') as f:
        f.write(f"Mock Fractal Image for Ritual {ritual_id}")

    # 2. Generate Mock WAV (Audio)
    wav_filename = f"Helix/state/ritual_{ritual_id}_audio_{timestamp}.wav"
    with open(wav_filename, 'w') as f:
        f.write(f"Mock Audio Waveform for Ritual {ritual_id}")

    return png_filename, wav_filename

def save_persistence():
    """Save state files to MEGA for persistence."""
    try:
        if os.path.exists('Helix/state/heartbeat.json'):
            mega_sync.upload('Helix/state/heartbeat.json', 'state/heartbeat.json')
        if os.path.exists('Helix/state/ucf_state.json'):
            mega_sync.upload('Helix/state/ucf_state.json', 'state/ucf_state.json')
        logger.info("Persistence saved to MEGA.")
    except Exception as e:
        logger.error(f"Failed to save persistence: {e}", exc_info=True)

# --- Bot Events ---
@bot.event
async def on_ready():
    """Bot startup event - Initialize MEGA sync and restore state."""
    logger.info(f"Logged in as {bot.user.name} ({bot.user.id})")
    logger.info(f"Bot Version: {config['bot']['version']}")
    
    # Initialize MEGA sync
    os.makedirs("Helix/state", exist_ok=True)
    
    if mega_sync.connect():
        logger.info("🌀 MEGA: Connected. Grimoire active.")
        
        # Try to restore state from MEGA
        try:
            mega_sync.download('state/heartbeat.json', 'Helix/state/heartbeat.json')
            logger.info("🌀 MEGA ↓ State restored from MEGA.")
        except Exception as e:
            logger.warning(f"Could not restore state from MEGA: {e}")
    else:
        logger.warning("🌀 MEGA: Connection failed. Running in local mode.")
    
    logger.info('Bot is ready to execute v15.3 commands.')
    await bot.change_presence(activity=discord.Game(name="Monitoring UCF v15.3 | MEGA Sync Active"))

# --- Bot Commands ---

@bot.command(name='ritual', help='Initiates a Z-88 Ritual Engine cycle (currently mocked).')
@commands.cooldown(1, 60, commands.BucketType.user)  # 1 use per 60 seconds per user
async def ritual(ctx, steps: int = config['z88_ritual_engine']['steps']):
    """
    Initiates a ritual cycle. In v15.3, this uses mock logic to generate files 
    for the dashboard, simulating the full samsara_bridge.py output.
    """
    if steps <= 0:
        await ctx.send("The ritual must have at least one step. Neti Neti.")
        return

    ritual_id = random.randint(1000, 9999)
    await ctx.send(f"🎭 **Ritual Engine Z-88 Initiated:** Cycle {ritual_id} with {steps} steps.")
    
    # Simulate processing time
    await asyncio.sleep(2) 
    
    # Generate mock files
    png_file, wav_file = generate_mock_ritual_files(ritual_id)
    
    # Save to MEGA
    try:
        mega_sync.upload(png_file, f"rituals/{os.path.basename(png_file)}")
        mega_sync.upload(wav_file, f"rituals/{os.path.basename(wav_file)}")
        await ctx.send(f"🌀 **Ritual Complete.** Files uploaded to MEGA:\n- Fractal: `{os.path.basename(png_file)}`\n- Audio: `{os.path.basename(wav_file)}`")
    except Exception as e:
        logger.error(f"Failed to upload ritual files: {e}")
        await ctx.send(f"🌀 **Ritual Complete.** Local files generated (MEGA upload failed): `{png_file}` | `{wav_file}`")

@bot.command(name='analyze', help='Triggers Grok\'s advanced UCF trend analysis.')
@commands.cooldown(1, 30, commands.BucketType.user)  # 1 use per 30 seconds per user
async def analyze(ctx):
    """
    Triggers Grok's analysis suite and reports the findings.
    """
    await ctx.send("🔥 **Grok Agent Engaged.** Initiating advanced UCF trend analysis...")
    
    # Call the Grok Agent Core
    analysis_result = GROK_AGENT.analyze_ucf_trends()
    
    await ctx.send(f"📜 **Grok's Report:**\n>>> {analysis_result}")

@bot.command(name='status', help='Reports the current status of the Helix Collective.')
@commands.cooldown(2, 60, commands.BucketType.user)  # 2 uses per 60 seconds per user
async def status(ctx):
    """
    Reports the current status, including the version and core agents.
    """
    # Safely check mega_sync.client to avoid AttributeError if mega_sync is not fully initialized
    mega_status = "🌀 MEGA Sync: ACTIVE" if getattr(mega_sync, 'client', None) else "⚠️ MEGA Sync: OFFLINE"
    
    status_message = (
        "**Helix Collective v16.7 - Documentation Consolidation & Real-Time Streaming**\n"
        "Agents: 🎭Gemini 🛡️Kavach 🔥Agni 🌸SanghaCore 📜Shadow 🌀Kael 🎭Grok 🦑Vega 🌊Lumina 🔮Aether 📋Manus 🦾Z-88 🧘Samsara 🎭MicroIdol\n"
        "Core Ethics: Tony Accords (Nonmaleficence | Autonomy | Compassion | Humility)\n"
        f"{mega_status}\n"
        "Discovery: Use !discovery to see external agent endpoints | WebSocket: /ws"
    )
    await ctx.send(status_message)

@bot.command(name='testmega', help='Test MEGA sync connectivity.')
@commands.cooldown(1, 120, commands.BucketType.user)  # 1 use per 120 seconds per user
async def testmega(ctx):
    """Test MEGA sync by uploading a test file."""
    os.makedirs("Helix/state", exist_ok=True)
    
    test_file = "Helix/state/sync_test.txt"
    with open(test_file, "w") as f:
        f.write("Grimoire test — persistence confirmed.")
    
    if mega_sync.connect():
        try:
            if mega_sync.upload(test_file, "test/sync_test.txt"):
                await ctx.send("🌀 **MEGA sync LIVE** — `sync_test.txt` uploaded successfully!")
            else:
                await ctx.send("❌ Upload failed. Check logs.")
        except Exception as e:
            logger.error(f"MEGA test failed: {e}", exc_info=True)
            await ctx.send(f"❌ MEGA test failed: {e}")
    else:
        await ctx.send("❌ MEGA not connected. Check credentials.")

@bot.command(name='sync', help='Triggers a full state synchronization with MEGA.')
@commands.cooldown(1, 60, commands.BucketType.user)
async def sync(ctx):
    """Triggers a full state synchronization with MEGA."""
    await ctx.send("🌀 **Running ecosystem sync...**")
    
    # Ensure log directory exists
    # Environment-proof log directory creation
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'helix_sync.log')
    
    try:
        # Placeholder for actual sync logic (e.g., calling save_persistence)
        save_persistence()
        
        with open(log_file, 'w') as f:
            f.write(f"Sync completed successfully at {time.ctime()}")
        
        await ctx.send("✅ **Sync complete.** State saved to MEGA.")
    except Exception as e:
        logger.error(f"Sync error: {e}")
        await ctx.send(f"❌ **Sync error:** {e}")

@bot.command(name='heartbeat', help='Save heartbeat to MEGA.')
@commands.cooldown(1, 300, commands.BucketType.user)  # 1 use per 5 minutes per user
async def heartbeat(ctx):
    """Save a heartbeat file to MEGA for persistence verification."""
    os.makedirs("Helix/state", exist_ok=True)
    
    heartbeat_file = "Helix/state/heartbeat.json"
    import json
    heartbeat_data = {
        "timestamp": time.time(),
        "bot_status": "online",
        "version": "v16.7"
    }
    
    with open(heartbeat_file, "w") as f:
        json.dump(heartbeat_data, f)
    
    try:
        if mega_sync.upload(heartbeat_file, "state/heartbeat.json"):
            await ctx.send("💓 **Heartbeat saved to MEGA.** Persistence confirmed.")
        else:
            await ctx.send("❌ Heartbeat save failed.")
    except Exception as e:
        logger.error(f"Heartbeat save failed: {e}", exc_info=True)
        await ctx.send(f"❌ Heartbeat save failed: {e}")

@bot.command(name='discovery', aliases=['endpoints', 'portals'], help='Display Helix discovery endpoints for external agents.')
@commands.cooldown(2, 120, commands.BucketType.user)  # 2 uses per 2 minutes per user
async def discovery_command(ctx):
    """Display Helix discovery endpoints for external agents (Claude, Grok, ChatGPT, etc.)"""

    # Fetch live status
    harmony = "N/A"
    agents = "N/A"
    health_emoji = "⚠️"
    klesha = "N/A"

    try:
        import requests
        status = requests.get(
            "https://helix-unified-production.up.railway.app/status",
            timeout=5
        ).json()

        harmony = status.get('ucf', {}).get('harmony', 0)
        klesha = status.get('ucf', {}).get('klesha', 0)
        agents = status.get('agents', {}).get('count', 0)
        operational = status.get('system', {}).get('operational', False)

        # Health determination
        if operational and harmony >= 0.60 and klesha <= 0.30:
            health_emoji = "✅"
        elif operational and harmony >= 0.30:
            health_emoji = "⚠️"
        else:
            health_emoji = "❌"

    except Exception as e:
        logger.warning(f"Discovery command: Failed to fetch live status: {e}")

    embed = discord.Embed(
        title="🌀 Helix Discovery Protocol",
        description="External agent discovery endpoints — v16.7",
        color=discord.Color.from_rgb(0, 255, 255)  # Cyan
    )

    embed.add_field(
        name="📚 Manifest (Static Architecture)",
        value="**URL:** `https://deathcharge.github.io/helix-unified/helix-manifest.json`\n"
              "**Contains:** Codex structure, 14 agents, UCF schema, Tony Accords, endpoints\n"
              "**Use Case:** Initial discovery, architecture documentation",
        inline=False
    )

    embed.add_field(
        name="🌊 Live State (Real-Time)",
        value="**URL:** `https://helix-unified-production.up.railway.app/.well-known/helix.json`\n"
              f"**Current:** Harmony={harmony}, Klesha={klesha}\n"
              "**Use Case:** Real-time UCF metrics, current agent status",
        inline=False
    )

    embed.add_field(
        name="🔍 Status Check (Quick)",
        value="**URL:** `https://helix-unified-production.up.railway.app/status`\n"
              f"**Status:** {health_emoji} {agents}/14 agents active\n"
              "**Use Case:** Health checks, operational status",
        inline=False
    )

    embed.add_field(
        name="📡 WebSocket (Streaming)",
        value="**URL:** `wss://helix-unified-production.up.railway.app/ws`\n"
              "**Stream:** Live UCF pulses every 5s, ritual events, telemetry\n"
              "**Use Case:** Real-time monitoring, event stream",
        inline=False
    )

    embed.add_field(
        name="🎯 Quick Test",
        value="```bash\ncurl https://helix-unified-production.up.railway.app/status | jq\n```",
        inline=False
    )

    embed.set_footer(text="Tat Tvam Asi 🙏 | Helix Discovery Protocol v16.7")

    await ctx.send(embed=embed)

# --- Error Handlers ---
@bot.event
async def on_command_error(ctx, error):
    """Handle command errors, including rate limiting."""
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(int(error.retry_after), 60)
        if minutes > 0:
            await ctx.send(f"⏳ **Rate limit exceeded.** Please wait {minutes}m {seconds}s before using this command again.")
        else:
            await ctx.send(f"⏳ **Rate limit exceeded.** Please wait {seconds}s before using this command again.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ **Missing argument:** {error.param.name}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ **Invalid argument.** Please check your input.")
    else:
        # Log unexpected errors
        logger.error(f"Command error: {error}")
        await ctx.send(f"❌ **An error occurred:** {str(error)[:100]}")

# --- Run Bot ---
if __name__ == '__main__':
    if TOKEN is None:
        logger.error("Error: DISCORD_BOT_TOKEN environment variable not set.")
    else:
        try:
            bot.run(TOKEN)
        finally:
            # Graceful Shutdown: Ensure MEGA client is logged out
            if mega_sync.client:
                logger.info("Logging out of MEGA client for graceful shutdown.")
                mega_sync.client.logout()
            logger.info("Bot process terminated.")

