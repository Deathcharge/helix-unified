# backend/main.py (v15.5 - Stable & Refactored)

from .services.notion_client import get_notion_client
from .bot_commands import *  # This registers all commands defined with @bot.command
from . import agents
import asyncio
import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
import discord
from discord.ext import commands

# --- Load Environment & Apply Patches ---
load_dotenv()

# pycryptodome patch for MEGA
try:
    import Cryptodome
    sys.modules['Crypto'] = Cryptodome
    print("✅ Crypto import compatibility layer is active.")
except ImportError:
    print("⚠️ pycryptodome not found - MEGA sync may fail.")

# --- Create Bot Instance FIRST ---
intents = discord.Intents.default()
intents.message_content = True  # Required for message content access
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Import Helix Modules AFTER bot is created ---

# --- FastAPI Lifespan Manager (for startup/shutdown) ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown of background services."""
    print("🌀 Helix Collective v15.5 - Startup Sequence")

    # 1. Initialize Notion Client and inject into agents module
    print("Initializing Notion Client...")
    agents.notion_client = await get_notion_client()  # Uses NOTION_API_KEY from env

    # 2. Start Discord Bot in a background task
    discord_token = os.getenv("DISCORD_TOKEN")
    if not discord_token:
        print("❌ DISCORD_TOKEN not found. Bot cannot start.")
        yield  # Still yield to let FastAPI run, but bot will be offline
        return

    bot_task = asyncio.create_task(bot.start(discord_token))
    print("🤖 Discord bot task started.")

    # 3. Wait for bot to be ready before starting agent loops
    await bot.wait_until_ready()
    print(f"✅ Bot connected as {bot.user}")

    # 4. Start Manus operational loop
    manus_agent = agents.AGENTS.get("Manus")
    if manus_agent:
        asyncio.create_task(manus_agent.loop())
        print("🤲 Manus operational loop task started.")

    print("✅ Helix Collective is fully operational.")
    yield

    # --- Shutdown Sequence ---
    print("🌙 Helix Collective - Shutdown Sequence")
    await bot.close()
    bot_task.cancel()

# --- FastAPI App Definition ---
app = FastAPI(
    title="🌀 Helix Collective v15.5",
    description="Embodied Continuum Edition - Multi-Agent AI System",
    version="15.5.0",
    lifespan=lifespan
)

# --- API Endpoints (Unchanged) ---


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "15.5.0", "timestamp": datetime.utcnow().isoformat()}


@app.get("/")
async def root():
    return {"message": "🌀 Helix Collective v15.5 is operational."}

# Add other endpoints like /status, /agents as needed.

# --- Main Entry Point (for uvicorn) ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting FastAPI server on host 0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
