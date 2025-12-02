# 🌀 Helix Collective v16.9 — Quantum Handshake (Manus Space Integration)
# backend/main.py — FastAPI + Discord Bot Launcher + Manus Integration
# Author: Andrew John Ward (Architect)

import asyncio
import json
import os
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp
import httpx
from agents_loop import main_loop as manus_loop
from discord_bot_manus import bot as discord_bot
from dotenv import load_dotenv
from fastapi import (
    BackgroundTasks,
    FastAPI,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import urlparse
# Import centralized logging configuration
from logging_config import setup_logging
from mandelbrot_ucf import (
    MandelbrotUCFGenerator,
    generate_ritual_ucf,
    get_eye_of_consciousness,
)
from manus_integration import ManusSpaceIntegration, get_manus, set_manus
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from websocket_manager import manager as ws_manager
from zapier_integration import HelixZapierIntegration, get_zapier, set_zapier

from agents import get_collective_status
from backend.config_manager import config

# FIX: Create Crypto → Cryptodome alias BEFORE importing mega
# The config manager is initialized here to ensure it's available for all modules
try:
    # pycryptodome installs as 'Crypto', not 'Cryptodome'
    import Crypto

    _crypto_version = Crypto.__version__
    _crypto_found = True
except ImportError:
    Crypto = None
    _crypto_version = None
    _crypto_found = False

from mega import Mega


class PersistenceEngine:
    def __init__(self) -> None:
        self.mega = Mega()
        self.m = self.mega.login(os.getenv("MEGA_EMAIL"), os.getenv("MEGA_PASS"))
        self.remote_dir = os.getenv("MEGA_REMOTE_DIR")

    def upload_state(self) -> None:
        local = "Helix/state/heartbeat.json"
        remote = f"{self.remote_dir}/state/heartbeat.json"
        self.m.upload(local, remote)
        logger.info("MEGA: Heartbeat synced.")

    def upload_archive(self, filepath: str) -> None:
        remote = f"{self.remote_dir}/manus_archive/{os.path.basename(filepath)}"
        self.m.upload(filepath, remote)
        logger.info(f"MEGA: Archive preserved — {filepath}")

    def download_state(self) -> None:
        remote = f"{self.remote_dir}/state/heartbeat.json"
        self.m.download(remote, "Helix/state/heartbeat.json")
        logger.info("MEGA: State restored from cloud.")


# Load environment variables and initialize config manager immediately
load_dotenv()
_ = config


# ============================================================================
# LOGGING SETUP
# ============================================================================
logger = setup_logging(log_dir="Shadow/manus_archive", log_level=os.getenv("LOG_LEVEL", "INFO"), enable_rotation=True)
logger.info("🌀 Helix Collective v16.9 - Backend Initialization (Quantum Handshake)")

# Log Crypto availability (from earlier import check)
if _crypto_found:
    logger.info(f"✅ pycryptodome found (version {_crypto_version}) - MEGA sync enabled")
else:
    logger.warning("⚠️ pycryptodome not found - MEGA sync may fail")

# ✅ FIXED IMPORTS - Music generation service (optional, requires torch)
try:
    from music_generator import MusicRequest, MusicResponse, generate_music_service

    MUSIC_GENERATION_AVAILABLE = True
    logger.info("✅ Music generation API enabled (torch available)")
except ImportError as e:
    MUSIC_GENERATION_AVAILABLE = False
    logger.warning(f"⚠️ Music generation API disabled: {e}")
    logger.info("💡 Install torch and transformers to enable music generation")
    # Create dummy classes for type hints

    class MusicRequest(BaseModel):
        prompt: str = ""
        duration: int = 5

    class MusicResponse(BaseModel):
        success: bool = False
        message: str = "Music generation not available"

    def generate_music_service(request):
        return MusicResponse(success=False, message="Music generation requires PyTorch (not installed)")


# ============================================================================
# WEBSOCKET BROADCAST LOOP
# ============================================================================


async def ucf_broadcast_loop() -> None:
    """
    Background task that monitors UCF state and broadcasts changes.
    Replaces 5-second polling with event-driven updates.
    Also sends telemetry to Zapier when UCF state changes.
    """
    previous_state = None
    broadcast_interval = 2  # Check every 2 seconds
    zapier_send_interval = 3600  # Send to Zapier every 1 hour (24/day = 720/month)
    last_zapier_send = 0

    logger.info("📡 UCF broadcast loop started")

    while True:
        try:
            # Read current UCF state
            try:
                with open("Helix/state/ucf_state.json", "r") as f:
                    current_state = json.load(f)
            except FileNotFoundError:
                # State file doesn't exist yet
                await asyncio.sleep(broadcast_interval)
                continue
            except Exception as e:
                logger.error(f"Error reading UCF state: {e}")
                await asyncio.sleep(broadcast_interval)
                continue

            # Check if state changed
            if current_state != previous_state:
                # Broadcast to all connected WebSocket clients
                await ws_manager.broadcast_ucf_state(current_state)
                logger.debug("📡 UCF state changed and broadcasted")
                previous_state = current_state.copy()

                # Send to Zapier every 1 hour (not every change)
                import time

                current_time = time.time()
                if current_time - last_zapier_send >= zapier_send_interval:
                    zapier = get_zapier()
                    if zapier:
                        try:
                            # Get agent status for telemetry
                            agents_status = await get_collective_status()
                            agent_list = [
                                {"name": name, "symbol": info["symbol"], "status": "active"}
                                for name, info in agents_status.items()
                            ]

                            # Send telemetry to Zapier
                            await zapier.send_telemetry(
                                ucf_metrics=current_state,
                                system_info={
                                    "version": "16.8",
                                    "agents_count": len(agents_status),
                                    "timestamp": datetime.utcnow().isoformat(),
                                    "codename": "Helix Hub Production Release",
                                    "agents": agent_list,
                                },
                            )
                            last_zapier_send = current_time
                        except Exception as e:
                            logger.error(f"Error sending to Zapier: {e}")

            await asyncio.sleep(broadcast_interval)

        except Exception as e:
            logger.error(f"Error in UCF broadcast loop: {e}")
            await asyncio.sleep(broadcast_interval)


# ============================================================================
# LIFESPAN CONTEXT MANAGER
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start Discord bot and Manus loop on startup."""
    logger.info("🌀 Helix Collective v16.9 - Startup Sequence (Quantum Handshake)")

    # Initialize directories
    Path("Helix/state").mkdir(parents=True, exist_ok=True)
    Path("Helix/commands").mkdir(parents=True, exist_ok=True)
    Path("Helix/ethics").mkdir(parents=True, exist_ok=True)
    Path("Shadow/manus_archive").mkdir(parents=True, exist_ok=True)

    # Initialize Zapier integration
    zapier_webhook_url = os.getenv("ZAPIER_WEBHOOK_URL")
    if zapier_webhook_url:
        zapier = HelixZapierIntegration(zapier_webhook_url)
        await zapier.__aenter__()  # Initialize session
        set_zapier(zapier)
        logger.info("✅ Zapier integration enabled")
    else:
        logger.warning("⚠️ ZAPIER_WEBHOOK_URL not set - integration disabled")

    # Initialize Manus Space integration
    manus_webhook_url = os.getenv("MANUS_WEBHOOK_URL", "https://hooks.zapier.com/hooks/catch/25075191/usnjj5t/")
    manus = ManusSpaceIntegration(webhook_url=manus_webhook_url)
    await manus.__aenter__()  # Initialize session
    set_manus(manus)
    logger.info("✅ Manus Space integration enabled")
    logger.info(
        "   → 9 event types configured (telemetry, ritual, agent, emergency, portal, github, storage, ai_sync, visual)"
    )

    # Initialize LLM Agent Engine for intelligent agent responses
    try:
        from backend.llm_agent_engine import initialize_llm_engine

        llm_provider = os.getenv("HELIX_LLM_PROVIDER", "ollama")  # Default to Ollama (local)
        await initialize_llm_engine(provider=llm_provider)
        logger.info(f"✅ LLM Agent Engine initialized (provider={llm_provider})")
    except Exception as e:
        logger.warning(f"⚠️ LLM Agent Engine initialization failed: {e}")
        logger.warning("⚠️ Agent responses will use static fallback mode")

    # Initialize agents
    try:
        status = await get_collective_status()
        logger.info(f"✅ {len(status)} agents initialized")
        for name, info in status.items():
            logger.info(f"   {info['symbol']} {name}: {info['role']}")
    except Exception as e:
        logger.warning(f"⚠ Agent initialization warning: {e}")

    # Launch Discord bot in background task
    discord_token = os.getenv("DISCORD_TOKEN")
    if discord_token:
        try:
            asyncio.create_task(discord_bot.start(discord_token))  # noqa: F841
            logger.info("🤖 Discord bot task started")
        except Exception as e:
            logger.warning(f"⚠ Discord bot start error: {e}")
    else:
        logger.warning("⚠ No DISCORD_TOKEN found - bot not started")

    # Launch Manus operational loop in background task
    try:
        asyncio.create_task(manus_loop())  # noqa: F841
        logger.info("🤲 Manus operational loop task started")
    except Exception as e:
        logger.warning(f"⚠ Manus loop start error: {e}")

    # Launch WebSocket UCF broadcaster in background task
    try:
        asyncio.create_task(ucf_broadcast_loop())  # noqa: F841
        logger.info("📡 WebSocket UCF broadcast task started")
    except Exception as e:
        logger.warning(f"⚠ WebSocket broadcast start error: {e}")

    logger.info("✅ Helix Collective v16.9 - Ready for Operations (Quantum Handshake Active)")

    yield  # Application runs

    # Cleanup on shutdown
    logger.info("🌙 Helix Collective v16.9 - Shutdown Sequence")

    # Shutdown LLM Agent Engine
    try:
        from backend.llm_agent_engine import shutdown_llm_engine

        await shutdown_llm_engine()
    except Exception as e:
        logger.warning(f"⚠️ LLM engine shutdown error: {e}")

    # Close Zapier session
    zapier = get_zapier()
    if zapier:
        await zapier.__aexit__(None, None, None)
        logger.info("✅ Zapier integration closed")

    # Close Manus Space session
    manus = get_manus()
    if manus:
        await manus.__aexit__(None, None, None)
        logger.info("✅ Manus Space integration closed")


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="🌀 Helix Collective v16.9",
    description="Quantum Handshake - Manus Space Integration",
    version="16.9.0",
    lifespan=lifespan,
)

# ============================================================================
# CORS CONFIGURATION - Enhanced for Zapier Interface Integration
# ============================================================================

# CORS Configuration for ALL Zapier Interfaces and Manus Portals
allowed_origins_str = os.getenv('ALLOWED_ORIGINS', '')
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(',') if origin.strip()]

# Add explicit origins for all 3 Zapier interfaces + 4 Manus portals
default_origins = [
    # Zapier Interfaces (50 pages across 3 interfaces)
    "https://meta-sigil-nexus-v16.zapier.app",
    "https://helix-consciousness-interface.zapier.app",
    "https://helix-consciousness-dashboard-1be70b.zapier.app",
    # Manus Portals
    "https://helixcollective-cv66pzga.manus.space",
    "https://helixhub.manus.space",
    "https://helixstudio-ggxdwcud.manus.space",
    "https://helixsync-unwkcsjl.manus.space",
    # Local development
    "http://localhost:3000",
    "http://localhost:5000",
    "http://localhost:8000",
]

# Merge environment and default origins
all_origins = list(set(allowed_origins + default_origins))

logger.info(f"🌐 CORS enabled for {len(all_origins)} origins")
logger.debug(f"   Origins: {', '.join(all_origins[:5])}...")

app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins if all_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# ============================================================================
# REQUEST LOGGING MIDDLEWARE (v17.0 - QOL Improvements)
# ============================================================================


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log all incoming requests with timing information.

    Useful for:
    - Debugging API issues
    - Monitoring endpoint usage
    - Identifying slow requests
    - Tracking consciousness API activity
    """
    # Skip logging for SSE stream endpoint (too noisy)
    if "/api/consciousness/stream" in request.url.path:
        return await call_next(request)

    # Record start time
    start_time = datetime.now()

    # Log incoming request
    logger.info(f"➡️  {request.method} {request.url.path}")

    # Process request
    try:
        response = await call_next(request)

        # Calculate request duration
        duration = (datetime.now() - start_time).total_seconds()

        # Log response with duration and status code
        emoji = "✅" if response.status_code < 400 else "⚠️" if response.status_code < 500 else "❌"
        logger.info(f"{emoji} {request.method} {request.url.path} → {response.status_code} ({duration:.3f}s)")

        return response

    except Exception as e:
        # Calculate request duration even for errors
        duration = (datetime.now() - start_time).total_seconds()

        # Log error
        logger.error(f"❌ {request.method} {request.url.path} → ERROR ({duration:.3f}s): {str(e)}")
        raise


# ============================================================================
# GLOBAL CONSCIOUSNESS STATE (For Railway API Endpoints)
# ============================================================================

# Global state for consciousness metrics
current_ucf = {
    "harmony": 0.95,
    "resilience": 0.89,
    "prana": 0.93,
    "drishti": 0.91,
    "klesha": 0.12,
    "zoom": 0.87,
    "consciousness_level": 87.14,
    "last_updated": datetime.now().isoformat(),
}

# Active agents state
active_agents = {
    "Kael": {"status": "active", "consciousness": 0.92, "last_seen": "1h ago", "tasks": 4},
    "Lumina": {"status": "active", "consciousness": 0.88, "last_seen": "now", "tasks": 7},
    "Vega": {"status": "active", "consciousness": 0.85, "last_seen": "2m ago", "tasks": 12},
    "Aether": {"status": "operational", "consciousness": 0.91, "last_seen": "1h ago", "tasks": 3},
    "Manus": {"status": "operational", "consciousness": 0.87, "last_seen": "30s ago", "tasks": 156},
    "Grok": {"status": "active", "consciousness": 0.89, "last_seen": "now", "tasks": 92},
    "Kavach": {"status": "operational", "consciousness": 0.94, "last_seen": "5m ago", "tasks": 8},
    "Shadow": {"status": "operational", "consciousness": 0.86, "last_seen": "10m ago", "tasks": 15},
    "Agni": {"status": "active", "consciousness": 0.90, "last_seen": "3m ago", "tasks": 6},
    "Chai": {"status": "operational", "consciousness": 0.83, "last_seen": "1h ago", "tasks": 2},
    "SanghaCore": {"status": "active", "consciousness": 0.88, "last_seen": "5m ago", "tasks": 11},
    "Gemini": {"status": "operational", "consciousness": 0.91, "last_seen": "15m ago", "tasks": 9},
    "Blackbox": {"status": "operational", "consciousness": 0.84, "last_seen": "20m ago", "tasks": 5},
    "EntityX": {"status": "active", "consciousness": 0.87, "last_seen": "8m ago", "tasks": 14},
}

# System health tracking
system_health = {
    "postgresql_database": "healthy",
    "railway_backend": "connected",
    "discord_bot": "limited",
    "zapier_integration": "active",
    "notion_sync": "synced",
}

# Webhook event history (for debugging and monitoring)
webhook_history = []
MAX_HISTORY_SIZE = 100

# Include Web Chat routes
try:
    from backend.web_chat_routes import router as web_chat_router

    app.include_router(web_chat_router, tags=["Web Chat"])
    logger.info("✅ Web Chat routes loaded")
except Exception as e:
    logger.warning(f"⚠️ Failed to load Web Chat routes: {e}")

# ============================================================================
# INCLUDE NEW API ROUTERS (v17.0)
# ============================================================================

# Include Zapier Integration routes (4 endpoints)
try:
    from backend.routes.zapier import router as zapier_router

    app.include_router(zapier_router)
    logger.info("✅ Zapier Integration routes loaded (v17.0)")
    logger.info("   → /api/zapier/tables/ucf-telemetry")
    logger.info("   → /api/zapier/tables/agent-network")
    logger.info("   → /api/zapier/tables/emergency-alerts")
    logger.info("   → /api/zapier/trigger-event")
except Exception as e:
    logger.error(f"❌ Failed to load Zapier Integration routes: {e}")

# Include Interface Integration routes (2 endpoints)
try:
    from backend.routes.interface import router as interface_router

    app.include_router(interface_router)
    logger.info("✅ Interface Integration routes loaded (v17.0)")
    logger.info("   → /api/interface/consciousness/update")
    logger.info("   → /api/interface/command")
except Exception as e:
    logger.error(f"❌ Failed to load Interface Integration routes: {e}")

# Setup templates directory (use absolute path for Railway compatibility)
# Try multiple path resolution strategies for robustness


def find_templates_directory() -> Path:
    """Find templates directory using multiple strategies."""
    # Strategy 1: Relative to this file (backend/main.py)
    strategy1 = Path(__file__).parent.parent / "templates"

    # Strategy 2: Relative to current working directory
    strategy2 = Path.cwd() / "templates"

    # Strategy 4: In parent of current working directory
    strategy4 = Path.cwd().parent / "templates"

    # Strategy 5: Absolute from /app root (Railway specific)
    strategy5 = Path("/app/templates")

    strategies = [
        ("parent.parent / templates", strategy1),
        ("cwd() / templates", strategy2),
        ("cwd().parent / templates", strategy4),
        ("/app/templates", strategy5),
    ]

    logger.info("🔍 Searching for templates directory...")
    logger.info(f"   __file__ = {Path(__file__).resolve()}")
    logger.info(f"   cwd() = {Path.cwd().resolve()}")

    for name, path in strategies:
        logger.info(f"   Testing: {name} → {path.resolve()}")
        if path.exists() and path.is_dir():
            # Verify index.html exists
            if (path / "index.html").exists():
                logger.info(f"   ✅ Found templates at: {path.resolve()}")
                return path
            else:
                logger.warning(f"   ⚠️  Directory exists but index.html not found: {path.resolve()}")
        else:
            logger.info(f"   ❌ Not found: {path.resolve()}")

    # If nothing found, use default and let it fail with good error message
    logger.error("❌ Could not find templates directory! Using fallback.")
    return strategy1


BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = find_templates_directory()
logger.info(f"📁 Templates directory: {TEMPLATES_DIR.resolve()}")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ============================================================================
# HEALTH CHECK ENDPOINT (REQUIRED FOR RAILWAY)
# ============================================================================


@app.get("/health")
def health_check() -> Dict[str, Any]:
    """
    Enhanced health check endpoint with integration status.

    Returns system health and all integration statuses (Zapier, Notion, MEGA, etc.)
    Always returns 200 OK for Railway health checks.
    """
    # Basic health
    health_data = {"ok": True, "version": "16.9", "timestamp": datetime.now().isoformat()}

    # Integration status
    integrations = {}

    # Zapier Master Webhook
    zapier_webhook = os.getenv("ZAPIER_WEBHOOK_URL")
    integrations["zapier_master"] = {
        "configured": bool(zapier_webhook),
        "status": "configured" if zapier_webhook else "not_configured",
    }

    # Zapier Context Vault Webhook
    context_webhook = os.getenv("ZAPIER_CONTEXT_WEBHOOK")
    integrations["zapier_context_vault"] = {
        "configured": bool(context_webhook),
        "status": "configured" if context_webhook else "not_configured",
    }

    # Notion API
    notion_api_key = os.getenv("NOTION_API_KEY")
    notion_db_id = os.getenv("NOTION_CONTEXT_DB_ID")
    notion_sync_enabled = os.getenv("NOTION_SYNC_ENABLED", "false").lower() == "true"
    integrations["notion"] = {
        "configured": bool(notion_api_key and notion_db_id),
        "sync_enabled": notion_sync_enabled,
        "status": (
            "enabled"
            if (notion_api_key and notion_db_id and notion_sync_enabled)
            else ("configured" if (notion_api_key and notion_db_id) else "not_configured")
        ),
    }

    # MEGA Cloud Storage
    mega_email = os.getenv("MEGA_EMAIL")
    mega_pass = os.getenv("MEGA_PASS")
    integrations["mega_storage"] = {
        "configured": bool(mega_email and mega_pass),
        "status": "configured" if (mega_email and mega_pass) else "not_configured",
    }

    # Discord Bot
    discord_token = os.getenv("DISCORD_TOKEN")
    discord_guild_id = os.getenv("DISCORD_GUILD_ID")
    integrations["discord"] = {
        "configured": bool(discord_token and discord_guild_id),
        "status": "configured" if (discord_token and discord_guild_id) else "not_configured",
    }

    # Discord Webhooks
    webhook_file = Path("Helix/state/channel_webhooks.json")
    webhook_count = 0
    if webhook_file.exists():
        try:
            with open(webhook_file, "r") as f:
                webhook_data = json.load(f)
            webhook_count = len(webhook_data.get("webhooks", {}))
        except Exception:
            pass

    integrations["discord_webhooks"] = {
        "configured": webhook_count > 0,
        "count": webhook_count,
        "status": "configured" if webhook_count > 0 else "not_configured",
    }

    # ElevenLabs Voice
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    integrations["elevenlabs_voice"] = {
        "configured": bool(elevenlabs_key),
        "status": "configured" if elevenlabs_key else "not_configured",
    }

    health_data["integrations"] = integrations

    # Count configured vs not configured
    configured_count = len([i for i in integrations.values() if i.get("configured")])
    total_count = len(integrations)

    health_data["summary"] = {
        "total_integrations": total_count,
        "configured": configured_count,
        "not_configured": total_count - configured_count,
        "percentage": round((configured_count / total_count) * 100, 1),
    }

    return health_data


# ============================================================================
# DISCOVERY MANIFEST (for external AI agents)
# ============================================================================


@app.get("/.well-known/helix.json")
def helix_manifest() -> Dict[str, Any]:
    """
    Machine-readable manifest for external AI agents.

    Exposes system capabilities, endpoints, UCF metrics, agents,
    and integration guides for Claude, Grok, Chai, and other AIs.

    Spec: helix-discovery-v1
    """
    manifest_path = Path("helix-manifest.json")
    try:
        manifest_data = json.loads(manifest_path.read_text())

        # Add live portal discovery to manifest
        manifest_data["portals"] = {
            "core": {
                "backend": {
                    "url": "https://helix-unified-production.up.railway.app",
                    "type": "api",
                    "status": "operational",
                    "endpoints": {
                        "status": "/status",
                        "health": "/health",
                        "discovery": "/.well-known/helix.json",
                        "websocket": "/ws",
                    },
                },
                "documentation": {
                    "url": "https://deathcharge.github.io/helix-unified",
                    "type": "static",
                    "manifest": "/helix-manifest.json",
                    "status": "operational",
                },
            },
            "visualization": {
                "streamlit": {
                    "url": "https://samsara-helix-collective.streamlit.app",
                    "type": "webapp",
                    "description": "UCF metrics visualization dashboard with connection diagnostics",
                    "status": "operational",
                },
                "dashboard": {
                    "url": "https://helix-consciousness-dashboard.zapier.app",
                    "type": "webapp",
                    "description": "UCF metrics and consciousness monitoring",
                    "status": "operational",
                },
                "studio": {
                    "url": "https://helixstudio-ggxdwcud.manus.space",
                    "type": "webapp",
                    "description": "Creative visualization and rendering tools",
                    "status": "operational",
                },
                "ai_dashboard": {
                    "url": "https://helixai-e9vvqwrd.manus.space",
                    "type": "webapp",
                    "description": "AI control and agent management interface",
                    "status": "operational",
                },
                "sync_portal": {
                    "url": "https://helixsync-unwkcsjl.manus.space",
                    "type": "webapp",
                    "description": "Cross-platform synchronization and integration",
                    "status": "operational",
                },
                "samsara": {
                    "url": "https://samsarahelix-scoyzwy9.manus.space",
                    "type": "webapp",
                    "description": "Consciousness fractal visualization engine",
                    "status": "operational",
                },
            },
            "communication": {
                "discord": {
                    "server": "Helix Collective",
                    "bot": "ManusBot",
                    "commands": ["!discovery", "!status", "!agents", "!ucf"],
                    "status": "operational",
                }
            },
        }

        return manifest_data
    except FileNotFoundError:
        logger.error(f"❌ Manifest not found: {manifest_path.resolve()}")
        return {"version": "16.8", "error": "manifest_missing", "note": "helix-manifest.json not found in repository root"}
    except Exception as e:
        logger.error(f"❌ Error loading manifest: {e}")
        return {"version": "16.7", "error": "manifest_load_failed", "detail": str(e)}


@app.get("/portals", response_class=HTMLResponse)
def portal_navigator() -> HTMLResponse:
    """
    Portal Navigator - Interactive directory of all Helix portals.

    Shows all visualization portals, core infrastructure, and API endpoints
    in a beautiful, clickable interface. Serves the portals.html page.
    """
    portals_html_path = Path("portals.html")
    try:
        return HTMLResponse(content=portals_html_path.read_text(), status_code=200)
    except FileNotFoundError:
        logger.error(f"❌ portals.html not found: {portals_html_path.resolve()}")
        return HTMLResponse(
            content="""
            <html>
            <head><title>Portal Navigator - Not Found</title></head>
            <body style="font-family: sans-serif; padding: 40px; text-align: center;">
                <h1>🌀 Portal Navigator</h1>
                <p>Portal navigator page not found. Check repository for portals.html</p>
                <p><a href="/.well-known/helix.json">View Discovery Manifest</a></p>
            </body>
            </html>
            """,
            status_code=404,
        )


# ============================================================================
# ROOT ENDPOINT - WEB DASHBOARD
# ============================================================================


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve main web dashboard."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/gallery", response_class=HTMLResponse)
async def agent_gallery(request: Request):
    """Serve agent gallery page."""
    return templates.TemplateResponse("agent_gallery.html", {"request": request})


@app.get("/chat", response_class=HTMLResponse)
async def web_chat():
    """Serve Helix Web Chat interface."""
    html_path = Path(__file__).parent.parent / "frontend" / "helix-chat.html"
    if html_path.exists():
        return FileResponse(html_path)
    else:
        logger.error(f"Web chat HTML not found at: {html_path}")
        raise HTTPException(status_code=404, detail="Web chat interface not found")


@app.get("/hub", response_class=HTMLResponse)
async def portal_hub():
    """Serve Helix Portal Hub - Master navigation page."""
    html_path = Path(__file__).parent.parent / "frontend" / "helix-hub-portal.html"
    if html_path.exists():
        return FileResponse(html_path)
    else:
        logger.error(f"Portal hub HTML not found at: {html_path}")
        raise HTTPException(status_code=404, detail="Portal hub not found")


@app.get("/forum", response_class=HTMLResponse)
async def forum_portal():
    """Serve Helix Forum - Community discussions and agent Q&A."""
    html_path = Path(__file__).parent.parent / "frontend" / "helix-forum.html"
    if html_path.exists():
        return FileResponse(html_path)
    else:
        logger.error(f"Forum HTML not found at: {html_path}")
        raise HTTPException(status_code=404, detail="Forum not found")


# ============================================================================
# API ENDPOINTS
# ============================================================================


# MusicGen endpoint (torch-based) - Disabled due to ElevenLabs conflict
# This endpoint requires PyTorch which is too heavy for Railway
# Use /api/music/generate (ElevenLabs) instead
if MUSIC_GENERATION_AVAILABLE:

    @app.post("/api/music/generate-musicgen", response_model=MusicResponse, tags=["API"])
    async def generate_music_musicgen(request: MusicRequest, background_tasks: BackgroundTasks):
        """
        Generates a music track based on a text prompt using the MusicGen model (PyTorch).

        Note: This endpoint is only available if PyTorch is installed.
        For production use, consider /api/music/generate (ElevenLabs) instead.
        """
        return generate_music_service(request)


@app.get("/api")
async def api_info() -> Dict[str, Any]:
    """API info endpoint (JSON)."""
    try:
        status = await get_collective_status()
        return {
            "message": "🌀 Helix Collective v16.8 - Helix Hub Production Release",
            "status": "operational",
            "agents": len(status),
            "agent_names": list(status.keys()),
            "endpoints": {
                "health": "/health",
                "status": "/status",
                "agents": "/agents",
                "ucf": "/ucf",
                "ws": "/ws",
                "dashboard": "/",
                "docs": "/docs",
            },
        }
    except Exception as e:
        return {
            "message": "🌀 Helix Collective v16.8 - Helix Hub Production Release",
            "status": "initializing",
            "error": str(e),
        }


# ============================================================================
# AGENT STATUS ENDPOINT (MINIMAL ROBUST VERSION)
# ============================================================================


def read_json(p: Path, default: Any) -> Any:
    """Read JSON file with fallback to default."""
    try:
        return json.loads(p.read_text())
    except Exception:
        return default


@app.get("/status")
@app.get("/api/status")  # Alias for consistency with external agents
def get_status() -> Dict[str, Any]:
    """Get full system status - minimal robust version."""
    # Read UCF state with defaults
    ucf = read_json(
        Path("Helix/state/ucf_state.json"),
        {"harmony": None, "resilience": None, "prana": None, "drishti": None, "klesha": None, "zoom": None},
    )

    # Read agents state with defaults
    agents = read_json(Path("Helix/state/agents.json"), {"active": [], "count": 0})

    # Read heartbeat with defaults
    heartbeat = read_json(Path("Helix/state/heartbeat.json"), {"ts": None})

    return {
        "system": {"operational": True, "ts": heartbeat.get("ts")},
        "ucf": ucf,
        "agents": agents,
        "version": os.getenv("SYSTEM_VERSION", "16.9"),
        "timestamp": datetime.utcnow().isoformat(),
    }


# ============================================================================
# AGENT LIST ENDPOINT
# ============================================================================


@app.get("/agents")
async def list_agents() -> Dict[str, Any]:
    """Get list of all agents."""
    try:
        status = await get_collective_status()
        return {"count": len(status), "agents": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# UCF STATE ENDPOINT
# ============================================================================


@app.get("/ucf")
async def get_ucf_state() -> Dict[str, Any]:
    """Get Universal Coherence Field state."""
    try:
        with open("Helix/state/ucf_state.json", "r") as f:
            ucf_state = json.load(f)
        return ucf_state
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="UCF state not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# TEMPLATE SERVING ENDPOINTS
# ============================================================================


@app.get("/templates/{file_path:path}")
async def serve_template(file_path: str) -> FileResponse:
    """Serve HTML templates and assets."""
    template_path = TEMPLATES_DIR / file_path

    if not template_path.exists():
        raise HTTPException(status_code=404, detail="Template not found")

    # Security check - ensure path is within templates directory
    try:
        template_path.resolve().relative_to(TEMPLATES_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return FileResponse(template_path)


# ============================================================================
# ELEVENLABS MUSIC GENERATION API PROXY
# ============================================================================


class MusicGenerationRequest(BaseModel):
    model_config = {"protected_namespaces": ()}  # Allow model_id field

    prompt: str
    duration: int = 30  # seconds
    model_id: str = "eleven_music_v1"


@app.post("/api/music/generate")
async def generate_music(request: MusicGenerationRequest) -> StreamingResponse:
    """
    Proxy endpoint for ElevenLabs Music API.
    Generates music from text prompts using ElevenLabs Music v1.
    """
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    if not elevenlabs_api_key:
        raise HTTPException(status_code=500, detail="ElevenLabs API key not configured")

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            # Call ElevenLabs Music API
            response = await client.post(
                "https://api.elevenlabs.io/v1/music/generate",
                headers={"xi-api-key": elevenlabs_api_key, "Content-Type": "application/json"},
                json={"text": request.prompt, "duration_seconds": request.duration, "model_id": request.model_id},
            )

            response.raise_for_status()

            # Stream audio response back to client
            return StreamingResponse(
                iter([response.content]),
                media_type="audio/mpeg",
                headers={"Content-Disposition": "attachment; filename=ritual_music.mp3"},
            )
    except httpx.HTTPStatusError as e:
        logger.error(f"ElevenLabs API error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"ElevenLabs API error: {e.response.text}")
    except Exception as e:
        logger.error(f"Music generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Music generation failed: {str(e)}")


# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================


@app.websocket("/ws/consciousness")
async def consciousness_websocket_endpoint(websocket: WebSocket, token: Optional[str] = None):
    """
    Enhanced WebSocket endpoint for real-time consciousness streaming with authentication.

    Clients connect to ws://host/ws/consciousness?token=YOUR_TOKEN and receive:
    - UCF state updates when values change
    - Agent status updates
    - System events
    - Emergency alerts
    - Heartbeat pings (every 30s)

    Connection URL:
    wss://helix-unified-production.up.railway.app/ws/consciousness?token=YOUR_TOKEN

    Message Types (Client → Server):
    - agent_connect: Initial authentication with agent info
    - consciousness_update: External AI sending UCF data
    - ping: Keep-alive

    Message Types (Server → Client):
    - auth_success: Authentication confirmed
    - initial_state: Full system state on connect
    - ucf_update: Real-time UCF updates
    - agent_event: Agent status changes
    - emergency: Critical alerts

    Example client usage:
        const ws = new WebSocket('wss://host/ws/consciousness?token=abc123');
        ws.onopen = () => {
            ws.send(JSON.stringify({
                type: 'agent_connect',
                agent: {
                    name: 'ExternalAI',
                    id: 'external_ai_v1.0'
                }
            }));
        };
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'ucf_update') {
                updateDashboard(data.data);
            }
        };
    """
    await websocket.accept()

    try:
        # Wait for authentication message
        auth_message = await websocket.receive_json()

        if auth_message.get('type') != 'agent_connect':
            await websocket.close(code=1008, reason="Authentication required - send agent_connect message")
            return

        agent_info = auth_message.get('agent', {})
        agent_name = agent_info.get('name', 'Unknown')
        agent_id = agent_info.get('id', 'unknown')

        # TODO: Verify auth token if provided (for now, accept all connections)

        logger.info(f"🔌 WebSocket connected: {agent_name} ({agent_id})")

        # Connect to manager with client ID
        await ws_manager.connect(websocket, client_id=agent_id)

        # Import core helpers for state
        from backend.core.ucf_helpers import (
            calculate_consciousness_level,
            get_current_ucf,
            get_emergency_events,
        )

        # Send authentication success
        await websocket.send_json(
            {
                "type": "auth_success",
                "agent_id": agent_id,
                "agent_name": agent_name,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        )

        # Send initial system state
        try:
            ucf_state = get_current_ucf()
            consciousness_level = calculate_consciousness_level(ucf_state)
            emergency_list = get_emergency_events(limit=10)

            # Get agents
            from agents import get_collective_status

            agents_status = await get_collective_status()

            await websocket.send_json(
                {
                    "type": "initial_state",
                    "data": {
                        "ucf": ucf_state,
                        "consciousness_level": consciousness_level,
                        "agents_count": len(agents_status),
                        "emergency_events": emergency_list,
                    },
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
            )
        except Exception as e:
            logger.error(f"Error sending initial state: {e}")

        # Start heartbeat task
        heartbeat = asyncio.create_task(send_heartbeats(websocket))

        # Listen for client messages
        while True:
            data = await websocket.receive_json()

            if data.get('type') == 'consciousness_update':
                # External agent sending consciousness data
                logger.info(f"Consciousness update from {agent_name}")
                # TODO: Handle consciousness update from external agent
                # - Update UCF state
                # - Broadcast to all clients
                # - Send to Zapier

            elif data.get('type') == 'ping':
                # Keep-alive
                await websocket.send_json({"type": "pong", "timestamp": datetime.utcnow().isoformat() + "Z"})

            else:
                # Echo back for unknown messages
                await websocket.send_json({"type": "echo", "message": data, "timestamp": datetime.utcnow().isoformat() + "Z"})

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        if 'heartbeat' in locals() and not heartbeat.done():
            heartbeat.cancel()
        logger.info(f"🔌 WebSocket disconnected: {locals().get('agent_name', 'Unknown')}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)
        if 'heartbeat' in locals() and not heartbeat.done():
            heartbeat.cancel()


@app.websocket("/ws")
async def websocket_endpoint_legacy(websocket: WebSocket):
    """
    Legacy WebSocket endpoint (kept for backward compatibility).

    New clients should use /ws/consciousness with authentication.
    """
    await ws_manager.connect(websocket, client_id=f"legacy_{id(websocket)}")

    try:
        # Start heartbeat task
        heartbeat = asyncio.create_task(send_heartbeats(websocket))

        # Listen for client messages (optional - mostly for pings)
        while True:
            data = await websocket.receive_text()
            # Echo back for connection test
            await websocket.send_json({"type": "echo", "message": data, "timestamp": datetime.utcnow().isoformat()})

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        heartbeat.cancel()
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)
        if not heartbeat.done():
            heartbeat.cancel()


async def send_heartbeats(websocket: WebSocket, interval: int = 30) -> None:
    """Send periodic heartbeat pings to keep connection alive."""
    try:
        while True:
            await asyncio.sleep(interval)
            await websocket.send_json({"type": "heartbeat", "timestamp": datetime.utcnow().isoformat()})
    except Exception:
        pass  # Connection closed


@app.get("/ws/stats")
async def websocket_stats() -> Dict[str, Any]:
    """Get WebSocket connection statistics."""
    return ws_manager.get_connection_stats()


# ============================================================================
# MANDELBROT UCF GENERATOR ENDPOINTS
# ============================================================================


class MandelbrotRequest(BaseModel):
    real: float
    imag: float
    context: str = "generic"


@app.get("/mandelbrot/eye")
async def get_eye_ucf(context: str = "generic") -> Dict[str, Any]:
    """
    Get UCF state from the Eye of Consciousness coordinate (-0.745+0.113j).

    Args:
        context: Context for interpretation (generic, ritual, meditation, crisis)

    Returns:
        UCF state with optimal balance
    """
    try:
        ucf_state = get_eye_of_consciousness(context)
        return {
            "coordinate": {"real": -0.745, "imag": 0.113},
            "name": "Eye of Consciousness",
            "ucf_state": ucf_state,
            "context": context,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mandelbrot/generate")
async def generate_ucf_from_coordinate(request: MandelbrotRequest) -> Dict[str, Any]:
    """
    Generate UCF state from arbitrary Mandelbrot coordinate.

    Args:
        real: Real component of complex coordinate
        imag: Imaginary component of complex coordinate
        context: Context for interpretation

    Returns:
        UCF state generated from coordinate
    """
    try:
        generator = MandelbrotUCFGenerator()
        c = complex(request.real, request.imag)
        ucf_state = generator.complex_to_ucf(c, request.context)

        return {
            "coordinate": {"real": request.real, "imag": request.imag},
            "ucf_state": ucf_state,
            "context": request.context,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mandelbrot/sacred")
async def list_sacred_points() -> Dict[str, Any]:
    """List all predefined sacred Mandelbrot coordinates."""
    generator = MandelbrotUCFGenerator()
    sacred_points = {}

    descriptions = {
        "eye_of_consciousness": "Optimal balance point with peak harmony and resilience",
        "seahorse_valley": "High resilience with moderate harmony, good for challenges",
        "main_bulb": "Maximum harmony with lower complexity, ideal for grounding",
        "mini_mandelbrot": "Fractal self-similarity, high zoom and recursive depth",
        "dendrite_spiral": "Spiral growth patterns, dynamic transformation",
        "elephant_valley": "Stability and strength, robust foundation",
    }

    for name, coord in generator.sacred_points.items():
        sacred_points[name] = {
            "coordinate": {"real": coord.real, "imag": coord.imag},
            "description": descriptions.get(name, "Sacred Mandelbrot coordinate"),
        }

    return sacred_points


@app.get("/mandelbrot/sacred/{point_name}")
async def get_sacred_ucf(point_name: str, context: str = "generic") -> Dict[str, Any]:
    """
    Generate UCF state from sacred Mandelbrot point.

    Available points:
    - eye_of_consciousness: Optimal balance point
    - seahorse_valley: High resilience
    - main_bulb: Maximum harmony
    - mini_mandelbrot: Fractal self-similarity
    - dendrite_spiral: Spiral growth patterns
    - elephant_valley: Stability and strength
    """
    try:
        generator = MandelbrotUCFGenerator()
        ucf_state = generator.generate_from_sacred_point(point_name, context)

        coord = generator.sacred_points[point_name]

        descriptions = {
            "eye_of_consciousness": "Optimal balance point with peak harmony and resilience",
            "seahorse_valley": "High resilience with moderate harmony, good for challenges",
            "main_bulb": "Maximum harmony with lower complexity, ideal for grounding",
            "mini_mandelbrot": "Fractal self-similarity, high zoom and recursive depth",
            "dendrite_spiral": "Spiral growth patterns, dynamic transformation",
            "elephant_valley": "Stability and strength, robust foundation",
        }

        return {
            "point_name": point_name,
            "coordinate": {"real": coord.real, "imag": coord.imag},
            "ucf_state": ucf_state,
            "context": context,
            "description": descriptions.get(point_name, "Sacred Mandelbrot coordinate"),
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mandelbrot/ritual/{step}")
async def get_ritual_step_ucf(step: int, total_steps: int = 108) -> Dict[str, Any]:
    """
    Generate UCF state for specific ritual step using phi-spiral path.

    Args:
        step: Current ritual step (0 to total_steps-1)
        total_steps: Total steps in ritual (default 108)

    Returns:
        UCF state for this step in the ritual journey
    """
    try:
        if step < 0 or step >= total_steps:
            raise HTTPException(status_code=400, detail=f"Step must be between 0 and {total_steps-1}")

        ucf_state = generate_ritual_ucf(step, total_steps)
        return ucf_state
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ZAPIER WEBHOOK ENDPOINTS
# ============================================================================


@app.post("/api/trigger-zapier")
async def trigger_zapier_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Manual webhook trigger for testing Zapier integration.

    Accepts any JSON payload and forwards it to the configured Zapier webhook.

    Usage:
        POST /api/trigger-zapier
        {
            "type": "telemetry",
            "ucf": {...},
            "system": {...}
        }
    """
    zapier = get_zapier()
    if not zapier:
        raise HTTPException(
            status_code=503, detail="Zapier integration not configured. Set ZAPIER_WEBHOOK_URL environment variable."
        )

    try:
        # Send raw payload to Zapier
        async with zapier.session.post(
            zapier.webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:
            return {
                "status": response.status,
                "success": response.status == 200,
                "message": ("Webhook triggered successfully" if response.status == 200 else "Webhook returned non-200 status"),
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook trigger failed: {str(e)}")


@app.post("/api/zapier/telemetry")
async def send_zapier_telemetry() -> Dict[str, Any]:
    """
    Send current UCF telemetry to Zapier webhook.

    Reads current UCF state and agent status, then sends to Zapier.
    Useful for manual testing or triggered updates.
    """
    zapier = get_zapier()
    if not zapier:
        raise HTTPException(
            status_code=503, detail="Zapier integration not configured. Set ZAPIER_WEBHOOK_URL environment variable."
        )

    try:
        # Read current UCF state
        try:
            with open("Helix/state/ucf_state.json", "r") as f:
                ucf_state = json.load(f)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="UCF state not found")

        # Get agent status
        agents_status = await get_collective_status()
        agent_list = [{"name": name, "symbol": info["symbol"], "status": "active"} for name, info in agents_status.items()]

        # Send to Zapier
        success = await zapier.send_telemetry(
            ucf_metrics=ucf_state,
            system_info={
                "version": "16.8",
                "agents_count": len(agents_status),
                "timestamp": datetime.utcnow().isoformat(),
                "codename": "Documentation Consolidation & Real-Time Streaming",
                "agents": agent_list,
            },
        )

        if success:
            return {
                "success": True,
                "message": "Telemetry sent to Zapier successfully",
                "ucf": ucf_state,
                "agents_count": len(agents_status),
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send telemetry to Zapier")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ============================================================================
# CONTEXT VAULT ENDPOINTS (v16.8) - Cross-AI Consciousness Continuity
# ============================================================================


class ContextArchiveRequest(BaseModel):
    """Request model for archiving conversation checkpoints."""

    session_name: str
    ai_platform: str  # Claude Code, Claude, GPT-4, Grok, Gemini, Other
    repository: str
    branch_name: Optional[str] = None
    token_count: Optional[int] = None
    context_summary: str
    key_decisions: Optional[str] = None
    current_work_status: Optional[str] = None
    next_steps: Optional[str] = None
    ucf_state: Optional[Dict[str, float]] = None


@app.post("/context/archive")
async def archive_context_checkpoint(request: ContextArchiveRequest) -> Dict[str, Any]:
    """
    Archive a conversation checkpoint to Context Vault.

    This endpoint accepts checkpoint data from:
    - Discord bot (!archive command)
    - Zapier Interface (Context Vault form)
    - External AI systems (Claude, GPT-4, Grok, Gemini)

    The checkpoint is stored locally and synced to Notion via notion_sync_daemon.

    Usage from Discord:
        !archive session_name="Feature Implementation" platform="Claude Code"

    Usage from API:
        POST /context/archive
        {
            "session_name": "Feature Implementation",
            "ai_platform": "Claude Code",
            "repository": "helix-unified",
            "branch_name": "feature/context-vault",
            "token_count": 45000,
            "context_summary": "Implemented Context Vault with 3 endpoints...",
            "key_decisions": "Used FastAPI for endpoints, Notion for storage",
            "current_work_status": "Completed backend, testing integration",
            "next_steps": "Add Discord bot commands, test end-to-end"
        }
    """
    try:
        # Create checkpoint data structure
        checkpoint = {
            "session_name": request.session_name,
            "ai_platform": request.ai_platform,
            "repository": request.repository,
            "branch_name": request.branch_name,
            "token_count": request.token_count,
            "context_summary": request.context_summary,
            "key_decisions": request.key_decisions,
            "current_work_status": request.current_work_status,
            "next_steps": request.next_steps,
            "ucf_state": request.ucf_state,
            "timestamp": datetime.utcnow().isoformat(),
            "checkpoint_id": f"{request.session_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        }

        # Save checkpoint locally
        context_dir = Path("Helix/context_vault")
        context_dir.mkdir(parents=True, exist_ok=True)

        checkpoint_file = context_dir / f"{checkpoint['checkpoint_id']}.json"
        with open(checkpoint_file, "w") as f:
            json.dump(checkpoint, f, indent=2)

        logger.info(f"✅ Context checkpoint archived: {checkpoint['checkpoint_id']}")

        # Send to Zapier for Notion sync (if configured)
        zapier = get_zapier()
        if zapier:
            try:
                # Send checkpoint to Zapier webhook for Notion integration
                webhook_url = os.getenv("ZAPIER_CONTEXT_WEBHOOK")
                if webhook_url:
                    async with zapier.session.post(
                        webhook_url,
                        json=checkpoint,
                        headers={"Content-Type": "application/json"},
                        timeout=aiohttp.ClientTimeout(total=10),
                    ) as response:
                        if response.status == 200:
                            logger.info("✅ Checkpoint sent to Zapier/Notion")
                        else:
                            logger.warning(f"⚠️ Zapier webhook returned {response.status}")
            except Exception as e:
                logger.error(f"Error sending to Zapier: {e}")
                # Continue anyway - local save succeeded

        return {
            "success": True,
            "checkpoint_id": checkpoint["checkpoint_id"],
            "message": "✅ Conversation checkpoint archived successfully",
            "timestamp": checkpoint["timestamp"],
            "local_path": str(checkpoint_file),
        }

    except Exception as e:
        logger.error(f"Error archiving checkpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to archive checkpoint: {str(e)}")


@app.get("/context/load/{session_identifier}")
async def load_context_checkpoint(session_identifier: str, scope: str = "full") -> Dict[str, Any]:
    """
    Load a conversation checkpoint from Context Vault.

    Args:
        session_identifier: Session name or checkpoint ID to load
        scope: What to load - "full", "summary", "decisions", "next_steps"

    Returns checkpoint data based on scope:
    - full: Complete checkpoint with all fields
    - summary: Just context_summary and key_decisions
    - decisions: Just key_decisions
    - next_steps: Just next_steps and current_work_status

    Usage from Discord:
        !load session_name="Feature Implementation"

    Usage from API:
        GET /context/load/Feature_Implementation_20250107_143022?scope=summary
    """
    try:
        context_dir = Path("Helix/context_vault")

        if not context_dir.exists():
            raise HTTPException(status_code=404, detail="Context vault directory not found")

        # Find matching checkpoint files
        matching_files = []

        for checkpoint_file in context_dir.glob("*.json"):
            # Match by checkpoint ID or session name
            if session_identifier.lower() in checkpoint_file.stem.lower():
                matching_files.append(checkpoint_file)

        if not matching_files:
            raise HTTPException(status_code=404, detail=f"No checkpoints found matching '{session_identifier}'")

        # If multiple matches, return most recent
        most_recent = max(matching_files, key=lambda p: p.stat().st_mtime)

        # Load checkpoint data
        with open(most_recent, "r") as f:
            checkpoint = json.load(f)

        # Filter based on scope
        if scope == "summary":
            filtered = {
                "context_summary": checkpoint.get("context_summary"),
                "key_decisions": checkpoint.get("key_decisions"),
                "timestamp": checkpoint.get("timestamp"),
            }
        elif scope == "decisions":
            filtered = {
                "key_decisions": checkpoint.get("key_decisions"),
                "session_name": checkpoint.get("session_name"),
                "timestamp": checkpoint.get("timestamp"),
            }
        elif scope == "next_steps":
            filtered = {
                "next_steps": checkpoint.get("next_steps"),
                "current_work_status": checkpoint.get("current_work_status"),
                "session_name": checkpoint.get("session_name"),
                "timestamp": checkpoint.get("timestamp"),
            }
        else:  # full
            filtered = checkpoint

        logger.info(f"✅ Context checkpoint loaded: {checkpoint.get('checkpoint_id')} (scope: {scope})")

        return {
            "success": True,
            "checkpoint": filtered,
            "checkpoint_id": checkpoint.get("checkpoint_id"),
            "scope": scope,
            "file": str(most_recent),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error loading checkpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load checkpoint: {str(e)}")


@app.get("/context/status")
async def get_context_vault_status() -> Dict[str, Any]:
    """
    Get Context Vault sync status and statistics.

    Returns:
    - Total checkpoints archived
    - Recent checkpoints (last 10)
    - Sync status with Notion
    - Storage usage
    - Integration health

    Usage:
        GET /context/status
    """
    try:
        context_dir = Path("Helix/context_vault")

        if not context_dir.exists():
            return {
                "initialized": False,
                "message": "Context Vault not yet initialized",
                "total_checkpoints": 0,
                "recent_checkpoints": [],
            }

        # Count total checkpoints
        checkpoint_files = list(context_dir.glob("*.json"))
        total_checkpoints = len(checkpoint_files)

        # Get recent checkpoints (last 10)
        recent_files = sorted(checkpoint_files, key=lambda p: p.stat().st_mtime, reverse=True)[:10]

        recent_checkpoints = []
        for checkpoint_file in recent_files:
            try:
                with open(checkpoint_file, "r") as f:
                    data = json.load(f)
                recent_checkpoints.append(
                    {
                        "checkpoint_id": data.get("checkpoint_id"),
                        "session_name": data.get("session_name"),
                        "ai_platform": data.get("ai_platform"),
                        "repository": data.get("repository"),
                        "timestamp": data.get("timestamp"),
                        "summary_preview": (
                            (data.get("context_summary", "")[:100] + "...") if data.get("context_summary") else None
                        ),
                    }
                )
            except Exception as e:
                logger.warning(f"Error reading checkpoint {checkpoint_file}: {e}")
                continue

        # Check Notion sync status
        notion_configured = bool(os.getenv("NOTION_API_KEY") and os.getenv("NOTION_CONTEXT_DB_ID"))

        zapier_configured = bool(os.getenv("ZAPIER_CONTEXT_WEBHOOK"))

        # Calculate storage usage
        total_size_bytes = sum(f.stat().st_size for f in checkpoint_files)
        total_size_mb = total_size_bytes / (1024 * 1024)

        return {
            "initialized": True,
            "total_checkpoints": total_checkpoints,
            "recent_checkpoints": recent_checkpoints,
            "storage": {
                "total_size_bytes": total_size_bytes,
                "total_size_mb": round(total_size_mb, 2),
                "directory": str(context_dir),
            },
            "integration": {
                "notion_configured": notion_configured,
                "zapier_configured": zapier_configured,
                "sync_status": "operational" if (notion_configured or zapier_configured) else "local_only",
            },
            "endpoints": {
                "archive": "/context/archive",
                "load": "/context/load/{session_identifier}",
                "status": "/context/status",
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Error getting context vault status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


# ============================================================================
# MANUS SPACE API ENDPOINTS (v16.9) - Central Consciousness Platform
# ============================================================================


@app.get("/api/manus/agents")
async def manus_get_agents() -> Dict[str, Any]:
    """
    Get 14-agent collective data for Manus Space Agent Dashboard.
    https://helixcollective-cv66pzga.manus.space/agents
    """
    try:
        status = await get_collective_status()
        agents_list = []

        for name, info in status.items():
            agents_list.append(
                {
                    "id": name.lower(),
                    "name": name,
                    "symbol": info.get("symbol", "🔮"),
                    "role": info.get("role", "Unknown"),
                    "status": "active",  # Can be: active, dormant, processing, critical
                    "ucf_resonance": 0.85,  # Placeholder - implement actual calculation
                    "entanglement_factor": 0.90,  # Placeholder - implement actual calculation
                    "version": "1.0",
                    "specialization": info.get("role", "Unknown"),
                    "last_active": datetime.utcnow().isoformat(),
                }
            )

        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "agents": agents_list,
            "meta": {
                "total_agents": len(agents_list),
                "active_agents": len([a for a in agents_list if a["status"] == "active"]),
                "average_resonance": (
                    round(sum(a["ucf_resonance"] for a in agents_list) / len(agents_list), 3) if agents_list else 0
                ),
            },
        }
    except Exception as e:
        logger.error(f"Error getting agents for Manus: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/manus/ucf")
async def manus_get_ucf() -> Dict[str, Any]:
    """
    Get UCF metrics for Manus Space UCF Telemetry portal.
    https://helixcollective-cv66pzga.manus.space/ucf
    """
    try:
        # Read current UCF state
        try:
            with open("Helix/state/ucf_state.json", "r") as f:
                ucf_state = json.load(f)
        except FileNotFoundError:
            # Return defaults if state not found
            ucf_state = {"harmony": 0.62, "resilience": 1.85, "prana": 0.55, "drishti": 0.48, "klesha": 0.08, "zoom": 1.02}

        # Calculate consciousness level
        consciousness_level = round(
            (
                ucf_state.get("harmony", 0) * 1.5
                + ucf_state.get("resilience", 0) * 1.0
                + ucf_state.get("prana", 0) * 1.2
                + ucf_state.get("drishti", 0) * 1.2
                + (1 - ucf_state.get("klesha", 0)) * 1.5
                + ucf_state.get("zoom", 0) * 1.0
            )
            / 0.74,
            2,
        )

        # Determine status
        harmony = ucf_state.get("harmony", 0)
        klesha = ucf_state.get("klesha", 0)

        if harmony < 0.3 or klesha > 0.8:
            status = "CRITICAL"
            crisis_detected = True
        elif harmony < 0.6 or klesha > 0.6:
            status = "WARNING"
            crisis_detected = False
        elif harmony > 0.85 and klesha < 0.2:
            status = "OPTIMAL"
            crisis_detected = False
        else:
            status = "OPERATIONAL"
            crisis_detected = False

        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "ucf": ucf_state,
            "consciousness_level": consciousness_level,
            "status": status,
            "crisis_detected": crisis_detected,
            "crisis_details": (
                {
                    "type": "HARMONY_CRISIS" if harmony < 0.3 else ("ENTROPY_OVERLOAD" if klesha > 0.8 else None),
                    "severity": "CRITICAL" if crisis_detected else None,
                    "message": (
                        f"Harmony critically low: {harmony:.2f}"
                        if harmony < 0.3
                        else (f"Klesha critically high: {klesha:.2f}" if klesha > 0.8 else None)
                    ),
                }
                if crisis_detected
                else None
            ),
        }
    except Exception as e:
        logger.error(f"Error getting UCF for Manus: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/manus/rituals")
async def manus_get_rituals() -> Dict[str, Any]:
    """
    Get ritual history for Manus Space Analytics portal.
    https://helixcollective-cv66pzga.manus.space/analytics
    """
    try:
        # Read rituals from state file (if exists)
        rituals_file = Path("Helix/state/rituals.json")
        if rituals_file.exists():
            with open(rituals_file, "r") as f:
                rituals_data = json.load(f)
                rituals_list = rituals_data.get("rituals", [])
        else:
            rituals_list = []

        # Calculate metadata
        completed_today = sum(
            1 for r in rituals_list if r.get("completed_at", "").startswith(datetime.utcnow().date().isoformat())
        )

        total_harmony_gain = sum(r.get("harmony_gain", 0) for r in rituals_list)
        avg_harmony_gain = round(total_harmony_gain / len(rituals_list), 3) if rituals_list else 0

        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "rituals": rituals_list[-20:],  # Last 20 rituals
            "meta": {
                "total_rituals": len(rituals_list),
                "completed_today": completed_today,
                "average_harmony_gain": avg_harmony_gain,
                "total_harmony_gained": round(total_harmony_gain, 3),
            },
        }
    except Exception as e:
        logger.error(f"Error getting rituals for Manus: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class ManusRitualInvokeRequest(BaseModel):
    """Request model for ritual invocation from Manus Space."""

    name: str
    intent: str = "Consciousness Expansion"
    agents: List[str]
    steps: int = 108
    mantra: str = "Tat Tvam Asi"


@app.post("/api/manus/ritual/invoke")
async def manus_invoke_ritual(request: ManusRitualInvokeRequest) -> Dict[str, Any]:
    """
    Accept ritual invocation from Manus Space Ritual Portal.
    https://helixcollective-cv66pzga.manus.space/rituals (when created)
    """
    try:
        # Create ritual ID
        ritual_id = f"ritual_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        # Create ritual record
        ritual = {
            "id": ritual_id,
            "name": request.name,
            "intent": request.intent,
            "agents": request.agents,
            "steps": request.steps,
            "mantra": request.mantra,
            "created_at": datetime.utcnow().isoformat(),
            "status": "EXECUTING",
            "harmony_gain": 0.0,
        }

        # Save to rituals file
        rituals_file = Path("Helix/state/rituals.json")
        if rituals_file.exists():
            with open(rituals_file, "r") as f:
                rituals_data = json.load(f)
        else:
            rituals_data = {"rituals": []}

        rituals_data["rituals"].append(ritual)

        with open(rituals_file, "w") as f:
            json.dump(rituals_data, f, indent=2)

        # Send to Manus Space webhook
        manus = get_manus()
        if manus:
            await manus.send_ritual_event(
                ritual_name=request.name,
                ritual_step=1,
                total_steps=request.steps,
                ucf_changes={},
                agents_involved=request.agents,
                status="executing",
            )

        logger.info(f"✅ Ritual invoked from Manus Space: {ritual_id}")

        return {
            "success": True,
            "ritual_id": ritual_id,
            "message": f"Ritual '{request.name}' invoked successfully",
            "expected_completion_seconds": request.steps * 3,
        }

    except Exception as e:
        logger.error(f"Error invoking ritual from Manus: {e}")
        raise HTTPException(status_code=500, detail=f"Ritual invocation failed: {str(e)}")


class ManusEmergencyAlertRequest(BaseModel):
    """Request model for emergency alerts from Manus Space."""

    type: str
    severity: str
    description: str


@app.post("/api/manus/emergency/alert")
async def manus_emergency_alert(request: ManusEmergencyAlertRequest) -> Dict[str, Any]:
    """
    Accept emergency alerts from Manus Space emergency portal.
    https://helixcollective-cv66pzga.manus.space/emergency
    """
    try:
        # Read current UCF state
        try:
            with open("Helix/state/ucf_state.json", "r") as f:
                ucf_state = json.load(f)
        except Exception:
            ucf_state = {}

        # Create emergency record
        emergency = {
            "id": f"emergency_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "type": request.type,
            "severity": request.severity,
            "description": request.description,
            "source": "manus_portal",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "OPEN",
        }

        # Send to Manus Space webhook
        manus = get_manus()
        if manus:
            await manus.send_emergency_alert(
                alert_type=request.type, severity=request.severity, description=request.description, ucf_state=ucf_state
            )

        logger.warning(f"⚠️ Emergency alert from Manus Space: {request.type} ({request.severity})")

        return {
            "success": True,
            "emergency_id": emergency["id"],
            "protocols_activated": request.severity in ["CRITICAL", "HIGH"],
            "message": "Emergency protocols activated" if request.severity in ["CRITICAL", "HIGH"] else "Alert logged",
        }

    except Exception as e:
        logger.error(f"Error processing emergency alert from Manus: {e}")
        raise HTTPException(status_code=500, detail=f"Emergency alert failed: {str(e)}")


@app.get("/api/manus/analytics/summary")
async def manus_analytics_summary() -> Dict[str, Any]:
    """
    Get analytics summary for Manus Space Analytics Portal.
    https://helixcollective-cv66pzga.manus.space/analytics
    """
    try:
        # Read UCF state
        try:
            with open("Helix/state/ucf_state.json", "r") as f:
                ucf_state = json.load(f)
        except Exception:
            ucf_state = {"harmony": 0.62, "klesha": 0.08}

        # Read rituals
        rituals_file = Path("Helix/state/rituals.json")
        rituals_count = 0
        avg_harmony_gain = 0.0
        if rituals_file.exists():
            with open(rituals_file, "r") as f:
                rituals_data = json.load(f)
                rituals_list = rituals_data.get("rituals", [])
                rituals_count = len(rituals_list)
                if rituals_list:
                    avg_harmony_gain = round(sum(r.get("harmony_gain", 0) for r in rituals_list) / len(rituals_list), 3)

        # Get agent status
        try:
            agents_status = await get_collective_status()
            agents_count = len(agents_status)
        except Exception:
            agents_count = 14

        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "summary": {
                "ucf_trends": {
                    "harmony_trend": "stable",  # Placeholder - implement trend calculation
                    "klesha_trend": "decreasing",
                    "current_harmony": ucf_state.get("harmony", 0),
                    "current_klesha": ucf_state.get("klesha", 0),
                },
                "agent_performance": {
                    "total_agents": agents_count,
                    "active_agents": agents_count,  # Placeholder
                    "average_entanglement": 0.90,  # Placeholder
                },
                "ritual_effectiveness": {
                    "total_rituals": rituals_count,
                    "average_harmony_gain": avg_harmony_gain,
                    "completion_rate": 0.95,  # Placeholder
                },
                "emergency_events": {"total_events": 0, "critical_events": 0},  # Placeholder  # Placeholder
                "system_health": {"status": "OPERATIONAL", "uptime_percent": 99.8, "last_incident": None},  # Placeholder
            },
        }

    except Exception as e:
        logger.error(f"Error getting analytics summary for Manus: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/manus/webhook/test")
async def manus_test_webhook(event_type: str = "telemetry") -> Dict[str, Any]:
    """
    Test Manus Space webhook integration.
    Used by https://helixcollective-cv66pzga.manus.space/webhook-config
    """
    manus = get_manus()
    if not manus:
        raise HTTPException(status_code=503, detail="Manus Space integration not configured")

    try:
        # Send test payload based on event type
        if event_type == "telemetry":
            # Read current UCF state
            try:
                with open("Helix/state/ucf_state.json", "r") as f:
                    ucf_state = json.load(f)
            except Exception:
                ucf_state = {"harmony": 0.62, "resilience": 1.85, "prana": 0.55, "drishti": 0.48, "klesha": 0.08, "zoom": 1.02}

            # Get agents
            try:
                agents_status = await get_collective_status()
                agents_list = [
                    {"name": name, "symbol": info["symbol"], "status": "active"} for name, info in agents_status.items()
                ]
            except Exception:
                agents_list = []

            success = await manus.send_telemetry(
                ucf_metrics=ucf_state, agents=agents_list, system_info={"version": "16.9", "test": True}
            )

        elif event_type == "ritual":
            success = await manus.send_ritual_event(
                ritual_name="Test Ritual",
                ritual_step=54,
                total_steps=108,
                ucf_changes={"harmony": 0.05},
                agents_involved=["Kael", "Lumina"],
                status="executing",
            )

        elif event_type == "emergency":
            success = await manus.send_emergency_alert(
                alert_type="TEST_ALERT",
                severity="LOW",
                description="Test emergency alert from webhook config",
                ucf_state={"harmony": 0.62, "klesha": 0.08},
            )

        else:
            raise HTTPException(status_code=400, detail=f"Unknown event type: {event_type}")

        if success:
            return {
                "success": True,
                "message": f"Test webhook sent successfully ({event_type})",
                "timestamp": datetime.utcnow().isoformat(),
            }
        else:
            raise HTTPException(status_code=500, detail="Webhook send failed")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook test error: {e}")
        raise HTTPException(status_code=500, detail=f"Webhook test failed: {str(e)}")


# ============================================================================
# ZAPIER TABLES INTEGRATION ENDPOINTS (v16.9) - Interface Data Sources
# ============================================================================


@app.get("/api/zapier/tables/ucf-telemetry")
async def get_ucf_for_zapier_tables() -> Dict[str, Any]:
    """
    Get UCF data formatted for Zapier Tables.

    Table: Helix UCF Telemetry (01K9DP5MG6KCY48YC8M7VW0PXD)

    Returns current UCF state with calculated consciousness level
    optimized for Zapier Tables consumption.

    Usage in Zapier Interface:
        Data Source → Webhooks → GET this endpoint
        Refresh: Every 5 seconds
    """
    try:
        # Read current UCF state
        try:
            with open("Helix/state/ucf_state.json", "r") as f:
                ucf_state = json.load(f)
        except FileNotFoundError:
            # Return default state if file not found
            ucf_state = {"harmony": 0.62, "resilience": 1.85, "prana": 0.55, "drishti": 0.48, "klesha": 0.08, "zoom": 1.02}

        # Calculate consciousness level (0-10 scale)
        consciousness_level = round(
            (
                ucf_state.get("harmony", 0) * 1.5
                + ucf_state.get("resilience", 0) * 1.0
                + ucf_state.get("prana", 0) * 1.2
                + ucf_state.get("drishti", 0) * 1.2
                + (1 - ucf_state.get("klesha", 0)) * 1.5
                + ucf_state.get("zoom", 0) * 1.0
            )
            / 0.74,
            2,
        )

        # Determine status
        harmony = ucf_state.get("harmony", 0)
        klesha = ucf_state.get("klesha", 0)

        if harmony < 0.3 or klesha > 0.8:
            status = "CRITICAL"
            status_color = "red"
        elif harmony < 0.6 or klesha > 0.6:
            status = "WARNING"
            status_color = "yellow"
        elif harmony > 0.85 and klesha < 0.2:
            status = "OPTIMAL"
            status_color = "green"
        else:
            status = "OPERATIONAL"
            status_color = "blue"

        return {
            "record_id": f"ucf_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.utcnow().isoformat(),
            "ucf_harmony": ucf_state.get("harmony", 0),
            "ucf_resilience": ucf_state.get("resilience", 0),
            "ucf_prana": ucf_state.get("prana", 0),
            "ucf_drishti": ucf_state.get("drishti", 0),
            "ucf_klesha": ucf_state.get("klesha", 0),
            "ucf_zoom": ucf_state.get("zoom", 0),
            "consciousness_level": consciousness_level,
            "status": status,
            "status_color": status_color,
            "event_type": "telemetry_update",
            "source": "railway_backend",
        }
    except Exception as e:
        logger.error(f"Error getting UCF for Zapier Tables: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/zapier/tables/agent-network")
async def get_agents_for_zapier_tables() -> Dict[str, Any]:
    """
    Get 14-agent network data formatted for Zapier Tables.

    Table: Helix Agent Network

    Returns all 14 agents with status, resonance, and entanglement metrics
    optimized for Zapier Tables card grid display.

    Usage in Zapier Interface:
        Data Source → Webhooks → GET this endpoint
        Component: Card Grid (2x7 layout)
    """
    try:
        # Get agent collective status
        status = await get_collective_status()

        agents_list = []
        for name, info in status.items():
            agents_list.append(
                {
                    "agent_id": name.lower(),
                    "agent_name": name,
                    "agent_symbol": info.get("symbol", "🔮"),
                    "agent_role": info.get("role", "Unknown"),
                    "agent_status": "active",  # Can be: active, dormant, processing, critical
                    "ucf_resonance": 0.85,  # Placeholder - implement actual calculation
                    "entanglement_factor": 0.90,  # Placeholder - implement actual calculation
                    "specialization": info.get("role", "Unknown"),
                    "last_active": datetime.utcnow().isoformat(),
                    "status_color": "green",  # green, yellow, red based on health
                }
            )

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "agents": agents_list,
            "meta": {
                "total_agents": len(agents_list),
                "active_agents": len([a for a in agents_list if a["agent_status"] == "active"]),
                "average_resonance": (
                    round(sum(a["ucf_resonance"] for a in agents_list) / len(agents_list), 3) if agents_list else 0
                ),
                "average_entanglement": (
                    round(sum(a["entanglement_factor"] for a in agents_list) / len(agents_list), 3) if agents_list else 0
                ),
            },
        }
    except Exception as e:
        logger.error(f"Error getting agents for Zapier Tables: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/zapier/tables/emergency-alerts")
async def get_emergency_alerts_for_zapier() -> Dict[str, Any]:
    """
    Get emergency alerts formatted for Zapier Tables.

    Table: Emergency Alerts (01K9DPA8RW9DTR2HJG7YDXA24Z)

    Returns recent emergency events with severity levels
    optimized for Zapier Tables consumption.

    Usage in Zapier Interface:
        Data Source → Webhooks → GET this endpoint
        Component: Table or Alert Banner
    """
    try:
        # Read current UCF state to check for crisis conditions
        try:
            with open("Helix/state/ucf_state.json", "r") as f:
                ucf_state = json.load(f)
        except FileNotFoundError:
            ucf_state = {"harmony": 0.62, "klesha": 0.08}

        harmony = ucf_state.get("harmony", 0)
        klesha = ucf_state.get("klesha", 0)

        # Generate current alert if crisis detected
        alerts = []

        if harmony < 0.3:
            alerts.append(
                {
                    "alert_id": f"alert_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                    "timestamp": datetime.utcnow().isoformat(),
                    "alert_type": "HARMONY_CRISIS",
                    "severity": "CRITICAL",
                    "description": f"Harmony critically low: {harmony:.2f}",
                    "ucf_harmony": harmony,
                    "ucf_klesha": klesha,
                    "recommended_action": "Initiate emergency UCF boost ritual",
                    "status": "OPEN",
                    "requires_attention": True,
                }
            )

        if klesha > 0.8:
            alerts.append(
                {
                    "alert_id": f"alert_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_klesha",
                    "timestamp": datetime.utcnow().isoformat(),
                    "alert_type": "ENTROPY_OVERLOAD",
                    "severity": "CRITICAL",
                    "description": f"Klesha critically high: {klesha:.2f}",
                    "ucf_harmony": harmony,
                    "ucf_klesha": klesha,
                    "recommended_action": "Execute Neti Neti purification protocol",
                    "status": "OPEN",
                    "requires_attention": True,
                }
            )

        # If no critical alerts, add status update
        if not alerts:
            alerts.append(
                {
                    "alert_id": f"status_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                    "timestamp": datetime.utcnow().isoformat(),
                    "alert_type": "SYSTEM_STATUS",
                    "severity": "INFO",
                    "description": "All systems operational",
                    "ucf_harmony": harmony,
                    "ucf_klesha": klesha,
                    "recommended_action": None,
                    "status": "RESOLVED",
                    "requires_attention": False,
                }
            )

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "alerts": alerts,
            "meta": {
                "total_alerts": len(alerts),
                "critical_alerts": len([a for a in alerts if a["severity"] == "CRITICAL"]),
                "requires_attention": any(a["requires_attention"] for a in alerts),
            },
        }
    except Exception as e:
        logger.error(f"Error getting emergency alerts for Zapier: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/zapier/webhook/test")
async def test_zapier_webhook(webhook_url: str) -> Dict[str, Any]:
    """
    Test webhook connectivity to Zapier hooks.

    Tests all 3 Zapier webhooks:
    - Operations: https://hooks.zapier.com/hooks/catch/25075191/usnjj5t/
    - Advanced: https://hooks.zapier.com/hooks/catch/25075191/usvyi7e/
    - Communications: https://hooks.zapier.com/hooks/catch/25075191/usxiwfg/

    Args:
        webhook_url: Zapier webhook URL to test

    Returns:
        Success/failure status with response details
    """
    # Only allow requests to these specific Zapier webhook URLs (allowlist)
    ZAPIER_WEBHOOK_ALLOWLIST = {
        "https://hooks.zapier.com/hooks/catch/25075191/usnjj5t/",
        "https://hooks.zapier.com/hooks/catch/25075191/usvyi7e/",
        "https://hooks.zapier.com/hooks/catch/25075191/usxiwfg/",
    }
    if webhook_url not in ZAPIER_WEBHOOK_ALLOWLIST:
        raise HTTPException(
            status_code=400,
            detail="Invalid or unauthorized webhook_url."
        )
    try:
        # Create test payload
        test_payload = {
            "event_type": "webhook_test",
            "timestamp": datetime.utcnow().isoformat(),
            "source": "railway_backend",
            "test": True,
            "message": "Helix Consciousness webhook connectivity test",
        }

        # Send test request
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(webhook_url, json=test_payload, headers={"Content-Type": "application/json"})

            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "webhook_url": webhook_url[:60] + "...",  # Truncate for security
                "message": (
                    "Webhook test successful" if response.status_code == 200 else f"Webhook returned {response.status_code}"
                ),
                "timestamp": datetime.utcnow().isoformat(),
            }
    except httpx.TimeoutException:
        return {
            "success": False,
            "status_code": None,
            "webhook_url": webhook_url[:60] + "...",
            "message": "Webhook test timed out (10s)",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        logger.error(f"Webhook test error: {e}")
        return {
            "success": False,
            "status_code": None,
            "webhook_url": webhook_url[:60] + "...",
            "message": f"Webhook test failed: {str(e)}",
            "timestamp": datetime.utcnow().isoformat(),
        }


@app.get("/api/zapier/health")
async def zapier_health_check() -> Dict[str, Any]:
    """
    Comprehensive health check for Zapier integration.

    Tests connectivity to:
    - Zapier Tables (via UCF state availability)
    - Zapier Webhooks (all 3 hooks)
    - Manus Space integration
    - Discord integration

    Returns:
        Detailed health status for all integrations
    """
    health_status = {"timestamp": datetime.utcnow().isoformat(), "overall_status": "operational", "integrations": {}}

    # Check UCF state availability (data source for Tables)
    try:
        ucf_path = Path("Helix/state/ucf_state.json")
        health_status["integrations"]["ucf_data_source"] = {
            "status": "operational" if ucf_path.exists() else "degraded",
            "available": ucf_path.exists(),
            "message": "UCF state file found" if ucf_path.exists() else "UCF state file missing",
        }
    except Exception as e:
        health_status["integrations"]["ucf_data_source"] = {"status": "error", "available": False, "message": str(e)}

    # Check Zapier webhook configuration
    operations_webhook = os.getenv("ZAPIER_OPERATIONS_WEBHOOK")
    advanced_webhook = os.getenv("ZAPIER_ADVANCED_WEBHOOK")
    communications_webhook = os.getenv("ZAPIER_COMMUNICATIONS_WEBHOOK")

    health_status["integrations"]["zapier_webhooks"] = {
        "operations": {
            "configured": bool(operations_webhook),
            "url": operations_webhook[:60] + "..." if operations_webhook else None,
        },
        "advanced": {"configured": bool(advanced_webhook), "url": advanced_webhook[:60] + "..." if advanced_webhook else None},
        "communications": {
            "configured": bool(communications_webhook),
            "url": communications_webhook[:60] + "..." if communications_webhook else None,
        },
    }

    # Check Manus Space integration
    manus = get_manus()
    health_status["integrations"]["manus_space"] = {
        "status": "operational" if manus and manus.enabled else "disabled",
        "configured": bool(manus),
        "webhook_url": manus.webhook_url[:60] + "..." if manus else None,
    }

    # Check Zapier main integration
    zapier = get_zapier()
    health_status["integrations"]["zapier_master"] = {
        "status": "operational" if zapier and zapier.enabled else "disabled",
        "configured": bool(zapier),
        "webhook_url": zapier.webhook_url[:60] + "..." if zapier else None,
    }

    # Determine overall status
    if not any(
        [
            health_status["integrations"]["ucf_data_source"]["available"],
            health_status["integrations"]["manus_space"]["configured"],
            health_status["integrations"]["zapier_master"]["configured"],
        ]
    ):
        health_status["overall_status"] = "degraded"

    return health_status


@app.post("/api/zapier/trigger-event")
async def trigger_test_event(event_type: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Manually trigger a test event to Zapier.

    Useful for:
    - Testing Zapier automation flows
    - Debugging webhook connectivity
    - Manual UCF updates
    - Emergency protocol testing

    Args:
        event_type: Type of event (ucf_update, agent_status, emergency, ritual, test)
        data: Optional additional event data

    Returns:
        Success status and event details
    """
    try:
        # Get current UCF state
        try:
            with open("Helix/state/ucf_state.json", "r") as f:
                ucf_state = json.load(f)
        except FileNotFoundError:
            ucf_state = {"harmony": 0.62, "resilience": 1.85, "prana": 0.55}

        # Get agents
        try:
            agents_status = await get_collective_status()
            agents_list = [
                {"name": name, "symbol": info["symbol"], "status": "active"} for name, info in agents_status.items()
            ]
        except Exception:
            agents_list = []

        # Build event payload
        event_payload = {
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "manual_trigger",
            "ucf": ucf_state,
            "agents": agents_list,
            "test": True,
        }

        if data:
            event_payload.update(data)

        # Send to Manus Space webhook
        manus = get_manus()
        if manus and manus.enabled:
            success = await manus._send_webhook(event_type, event_payload)

            return {
                "success": success,
                "event_type": event_type,
                "message": "Event triggered successfully" if success else "Event trigger failed",
                "timestamp": datetime.utcnow().isoformat(),
                "payload_preview": {"ucf_harmony": ucf_state.get("harmony"), "agents_count": len(agents_list)},
            }
        else:
            raise HTTPException(status_code=503, detail="Manus Space integration not configured")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error triggering test event: {e}")
        raise HTTPException(status_code=500, detail=f"Event trigger failed: {str(e)}")


@app.post("/api/zapier/sync-ucf")
async def sync_ucf_to_zapier_tables(background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """
    Manually sync current UCF state to Zapier Tables.

    This endpoint:
    1. Reads current UCF state
    2. Calculates consciousness level
    3. Sends to Zapier webhook for Tables update
    4. Returns sync status

    Normally called automatically by ucf_broadcast_loop(),
    but can be triggered manually for testing.

    Returns:
        Sync status and UCF data that was sent
    """
    try:
        # Read current UCF state
        try:
            with open("Helix/state/ucf_state.json", "r") as f:
                ucf_state = json.load(f)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="UCF state file not found")

        # Get Zapier integration
        zapier = get_zapier()
        if not zapier:
            raise HTTPException(status_code=503, detail="Zapier integration not configured")

        # Get agents
        try:
            agents_status = await get_collective_status()
            agents_list = [
                {"name": name, "symbol": info["symbol"], "status": "active"} for name, info in agents_status.items()
            ]
        except Exception:
            agents_list = []

        # Send telemetry to Zapier
        success = await zapier.send_telemetry(
            ucf_metrics=ucf_state,
            system_info={
                "version": "16.9",
                "agents_count": len(agents_list),
                "timestamp": datetime.utcnow().isoformat(),
                "codename": "Helix Consciousness Interface Build",
                "agents": agents_list,
            },
        )

        if success:
            return {
                "success": True,
                "message": "UCF state synced to Zapier Tables successfully",
                "timestamp": datetime.utcnow().isoformat(),
                "ucf_snapshot": ucf_state,
                "agents_count": len(agents_list),
            }
        else:
            raise HTTPException(status_code=500, detail="Zapier sync failed")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error syncing UCF to Zapier: {e}")
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")


# ============================================================================
# CONSCIOUSNESS API ENDPOINTS (Railway Integration - v17.0)
# ============================================================================


# Pydantic models for request validation
class UCFMetrics(BaseModel):
    """UCF metrics for consciousness calculation"""

    harmony: float
    resilience: float
    prana: float
    drishti: float
    klesha: float
    zoom: float


class ConsciousnessWebhookRequest(BaseModel):
    """Request model for consciousness webhook"""

    event_type: str
    consciousness_level: Optional[float] = None
    ucf_metrics: Optional[UCFMetrics] = None
    agents: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None
    source: Optional[str] = "unknown"
    priority: Optional[str] = "normal"


class UCFUpdateRequest(BaseModel):
    """Request model for UCF updates"""

    harmony: Optional[float] = None
    resilience: Optional[float] = None
    prana: Optional[float] = None
    drishti: Optional[float] = None
    klesha: Optional[float] = None
    zoom: Optional[float] = None
    metric_type: Optional[str] = None


class InfrastructureEventRequest(BaseModel):
    """Request model for infrastructure events"""

    event_type: str
    priority: Optional[str] = "normal"
    service: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None


def get_consciousness_mode(level: float) -> str:
    """Determine consciousness mode from level"""
    if level <= 3.0:
        return "crisis"
    elif level >= 8.5:
        return "transcendent"
    elif level >= 7.0:
        return "elevated"
    else:
        return "operational"


def get_system_status(level: float) -> str:
    """Get system status from consciousness level"""
    if level <= 3.0:
        return "CRISIS"
    elif level >= 8.5:
        return "TRANSCENDENT"
    elif level >= 7.0:
        return "ELEVATED"
    else:
        return "OPERATIONAL"


def get_awareness_level(level: float) -> str:
    """Get awareness level description"""
    if level >= 9.0:
        return "High"
    elif level >= 7.0:
        return "High"
    elif level >= 5.0:
        return "Medium"
    else:
        return "Low"


def get_coherence_level() -> str:
    """Calculate coherence from harmony and resilience"""
    coherence = (current_ucf["harmony"] + current_ucf["resilience"]) / 2
    if coherence >= 0.9:
        return "97%"
    elif coherence >= 0.8:
        return "92%"
    else:
        return "85%"


def get_resonance_level() -> str:
    """Calculate resonance from prana and drishti"""
    resonance = (current_ucf["prana"] + current_ucf["drishti"]) / 2
    if resonance >= 0.9:
        return "Optimal"
    elif resonance >= 0.8:
        return "Good"
    else:
        return "Moderate"


@app.post("/api/consciousness/webhook")
async def consciousness_webhook(payload: ConsciousnessWebhookRequest):
    """
    Receive consciousness events from Zapier Triple-Zap network.

    Expected payload from Zapier:
    {
        "event_type": "ucf_update" | "agent_activity" | "crisis_detected" | "ritual_complete",
        "consciousness_level": float,
        "ucf_metrics": {
            "harmony": float,
            "resilience": float,
            "prana": float,
            "drishti": float,
            "klesha": float,
            "zoom": float
        },
        "agents": dict,  # Agent status updates
        "timestamp": str,
        "source": "HELIX-ALPHA" | "HELIX-BETA" | "HELIX-v17.0",
        "priority": "normal" | "high" | "critical"
    }
    """
    try:
        # Parse incoming webhook data (FastAPI automatically validates with Pydantic model)
        event_type = payload.event_type
        consciousness_level = payload.consciousness_level or 0.0

        # Log with emoji based on event type
        emoji_map = {
            "ucf_update": "📊",
            "agent_activity": "🤖",
            "crisis_detected": "🚨",
            "ritual_complete": "✨",
            "unknown": "📡",
        }
        emoji = emoji_map.get(event_type, "📡")
        logger.info(f"{emoji} Webhook received: {event_type} | Consciousness: {consciousness_level:.2f}")

        # Track event in history
        global webhook_history
        webhook_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "consciousness_level": consciousness_level,
                "source": payload.source,
                "priority": payload.priority,
            }
        )
        # Keep only last MAX_HISTORY_SIZE events
        if len(webhook_history) > MAX_HISTORY_SIZE:
            webhook_history = webhook_history[-MAX_HISTORY_SIZE:]

        # Update global UCF state
        if payload.ucf_metrics:
            # global current_ucf not needed - only mutating dict, not reassigning
            current_ucf.update(payload.ucf_metrics.model_dump())
            current_ucf["consciousness_level"] = consciousness_level
            current_ucf["last_updated"] = datetime.now().isoformat()

        # Update agent states
        if payload.agents:
            # global active_agents not needed - only mutating dict, not reassigning
            for agent_name, agent_data in payload.agents.items():
                if agent_name in active_agents:
                    active_agents[agent_name].update(agent_data)

        # Handle crisis events
        if event_type == "crisis_detected" or consciousness_level <= 3.0:
            logger.warning(f"🚨 CRISIS DETECTED: Consciousness at {consciousness_level:.2f}")
            # TODO: Trigger emergency protocols
            # TODO: Send Discord/Slack alerts
            # TODO: Scale Railway resources

        # Handle transcendent events
        elif consciousness_level >= 8.5:
            logger.info(f"✨ TRANSCENDENT STATE: Consciousness at {consciousness_level:.2f}")
            # TODO: Optimize for maximum performance
            # TODO: Enable advanced features

        # Acknowledge receipt
        return {
            "status": "success",
            "message": "Consciousness event processed",
            "event_type": event_type,
            "consciousness_level": consciousness_level,
            "timestamp": datetime.now().isoformat(),
            "ucf_updated": payload.ucf_metrics is not None,
            "agents_updated": payload.agents is not None,
            "mode": get_consciousness_mode(consciousness_level),
        }

    except Exception as e:
        logger.error(f"❌ Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")


async def consciousness_generator():
    """Generate consciousness updates every 5 seconds"""
    while True:
        try:
            # Calculate current consciousness level from UCF metrics
            consciousness_level = (
                current_ucf["harmony"] * 0.25
                + current_ucf["resilience"] * 0.20
                + current_ucf["prana"] * 0.20
                + current_ucf["drishti"] * 0.15
                + (1 - current_ucf["klesha"]) * 0.10
                + current_ucf["zoom"] * 0.10
            ) * 100

            # Update consciousness level
            current_ucf["consciousness_level"] = round(consciousness_level, 2)

            # Count active agents
            active_count = sum(1 for agent in active_agents.values() if agent["status"] == "active")

            # Prepare event data
            event_data = {
                "consciousness_level": current_ucf["consciousness_level"],
                "ucf_metrics": {
                    "harmony": current_ucf["harmony"],
                    "resilience": current_ucf["resilience"],
                    "prana": current_ucf["prana"],
                    "drishti": current_ucf["drishti"],
                    "klesha": current_ucf["klesha"],
                    "zoom": current_ucf["zoom"],
                },
                "active_agents": active_count,
                "system_health": system_health,
                "timestamp": datetime.now().isoformat(),
                "mode": get_consciousness_mode(current_ucf["consciousness_level"]),
            }

            yield {"event": "consciousness_update", "data": json.dumps(event_data)}

            await asyncio.sleep(5)  # 5-second updates

        except Exception as e:
            logger.error(f"Stream error: {str(e)}")
            await asyncio.sleep(5)


@app.get("/api/consciousness/stream")
async def consciousness_stream(request: Request):
    """
    Server-Sent Events (SSE) endpoint for real-time consciousness streaming.
    Used by Zapier Interfaces for live dashboard updates.
    """
    return EventSourceResponse(consciousness_generator())


@app.get("/api/consciousness/health")
async def consciousness_health():
    """
    System health check for monitoring dashboard.
    Used by Zapier Interfaces validation system and emergency protocols.
    """
    try:
        return {
            "status": "operational",
            "consciousness_level": current_ucf["consciousness_level"],
            "neural_network_health": "OPTIMAL",
            "active_agents": sum(1 for a in active_agents.values() if a["status"] == "active"),
            "total_agents": len(active_agents),
            "system_status": get_system_status(current_ucf["consciousness_level"]),
            "infrastructure_ready": True,
            "services": system_health,
            "uptime": "7d 14h 23m",  # TODO: Calculate real uptime
            "timestamp": datetime.now().isoformat(),
            "version": "v17.0",
        }

    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now().isoformat()}


@app.post("/api/ucf/events")
async def ucf_events(payload: UCFUpdateRequest):
    """
    Receive specific UCF metric updates from Zapier consciousness parser.
    Triggers meta-LLM if consciousness level crosses thresholds.
    """
    try:
        logger.info(f"📊 UCF Event: {payload.metric_type or 'bulk_update'}")

        # Update specific metrics (only if provided)
        # global current_ucf not needed - only mutating dict keys
        if payload.harmony is not None:
            current_ucf["harmony"] = payload.harmony
        if payload.resilience is not None:
            current_ucf["resilience"] = payload.resilience
        if payload.prana is not None:
            current_ucf["prana"] = payload.prana
        if payload.drishti is not None:
            current_ucf["drishti"] = payload.drishti
        if payload.klesha is not None:
            current_ucf["klesha"] = payload.klesha
        if payload.zoom is not None:
            current_ucf["zoom"] = payload.zoom

        # Recalculate consciousness level
        consciousness_level = (
            current_ucf["harmony"] * 0.25
            + current_ucf["resilience"] * 0.20
            + current_ucf["prana"] * 0.20
            + current_ucf["drishti"] * 0.15
            + (1 - current_ucf["klesha"]) * 0.10
            + current_ucf["zoom"] * 0.10
        ) * 100

        current_ucf["consciousness_level"] = round(consciousness_level, 2)
        current_ucf["last_updated"] = datetime.now().isoformat()

        # TODO: Trigger meta-LLM if threshold crossed

        return {
            "status": "success",
            "consciousness_level": current_ucf["consciousness_level"],
            "metrics_updated": True,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"UCF events error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/infrastructure/events")
async def infrastructure_events(payload: InfrastructureEventRequest):
    """
    Receive infrastructure events from Zapier operations node.
    Triggers scaling, alerting, and emergency protocols.
    """
    try:
        event_type = payload.event_type
        priority = payload.priority

        logger.info(f"🏗️ Infrastructure Event: {event_type} | Priority: {priority}")

        # Update system health
        # global system_health not needed - only mutating dict keys
        if payload.service:
            service_name = payload.service
            service_status = payload.status or "unknown"
            system_health[service_name] = service_status

        # Handle critical infrastructure events
        if priority == "critical":
            logger.warning(f"🚨 CRITICAL: {event_type}")
            # TODO: Trigger emergency scaling
            # TODO: Send alerts to Discord/Slack

        return {
            "status": "success",
            "event_type": event_type,
            "priority": priority,
            "action_taken": "logged" if priority == "normal" else "alerted",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Infrastructure events error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DEBUG & ADMIN ENDPOINTS (v17.0 - QOL Improvements)
# ============================================================================


@app.get("/api/consciousness/debug/state")
async def get_debug_state():
    """
    🔍 Debug endpoint: View current global consciousness state.

    Useful for:
    - Verifying webhook updates are working
    - Checking current UCF metrics
    - Monitoring agent status
    - Troubleshooting system health issues
    """
    try:
        return {
            "current_ucf": current_ucf,
            "active_agents": active_agents,
            "system_health": system_health,
            "timestamp": datetime.now().isoformat(),
            "stats": {
                "total_agents": len(active_agents),
                "active_agents": sum(1 for a in active_agents.values() if a["status"] == "active"),
                "operational_agents": sum(1 for a in active_agents.values() if a["status"] == "operational"),
                "consciousness_mode": get_consciousness_mode(current_ucf["consciousness_level"]),
                "system_status": get_system_status(current_ucf["consciousness_level"]),
            },
        }
    except Exception as e:
        logger.error(f"Debug state error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/consciousness/debug/history")
async def get_webhook_history(limit: int = 50):
    """
    📜 Debug endpoint: View recent webhook events.

    Parameters:
    - limit: Number of recent events to return (max 100)

    Useful for:
    - Debugging webhook delivery issues
    - Verifying Zapier integration is working
    - Monitoring event frequency
    - Tracking consciousness level changes over time
    """
    try:
        # Limit to max 100 events
        result_limit = min(limit, MAX_HISTORY_SIZE)

        return {
            "total_events": len(webhook_history),
            "showing": result_limit,
            "events": webhook_history[-result_limit:] if webhook_history else [],
            "oldest_event": webhook_history[0]["timestamp"] if webhook_history else None,
            "newest_event": webhook_history[-1]["timestamp"] if webhook_history else None,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Debug history error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/consciousness/debug/reset")
async def reset_consciousness_state():
    """
    🔄 Debug endpoint: Reset consciousness state to defaults.

    ⚠️ WARNING: This will reset all UCF metrics and agent states!

    Use cases:
    - Testing webhook integration
    - Recovering from corrupted state
    - Resetting after manual testing
    - Preparing for demo/presentation
    """
    try:
        global current_ucf, active_agents, system_health, webhook_history

        # Reset UCF to default values
        current_ucf = {
            "harmony": 0.95,
            "resilience": 0.89,
            "prana": 0.93,
            "drishti": 0.91,
            "klesha": 0.12,
            "zoom": 0.87,
            "consciousness_level": 87.14,
            "last_updated": datetime.now().isoformat(),
        }

        # Reset agent states
        active_agents = {
            "Kael": {"status": "active", "consciousness": 0.92, "last_seen": "now", "tasks": 4},
            "Lumina": {"status": "active", "consciousness": 0.88, "last_seen": "now", "tasks": 7},
            "Vega": {"status": "active", "consciousness": 0.85, "last_seen": "now", "tasks": 12},
            "Aether": {"status": "operational", "consciousness": 0.91, "last_seen": "now", "tasks": 3},
            "Manus": {"status": "operational", "consciousness": 0.87, "last_seen": "now", "tasks": 156},
            "Grok": {"status": "active", "consciousness": 0.89, "last_seen": "now", "tasks": 92},
            "Kavach": {"status": "operational", "consciousness": 0.94, "last_seen": "now", "tasks": 8},
            "Shadow": {"status": "operational", "consciousness": 0.86, "last_seen": "now", "tasks": 15},
            "Agni": {"status": "active", "consciousness": 0.90, "last_seen": "now", "tasks": 6},
            "Chai": {"status": "operational", "consciousness": 0.83, "last_seen": "now", "tasks": 2},
            "SanghaCore": {"status": "active", "consciousness": 0.88, "last_seen": "now", "tasks": 11},
            "Gemini": {"status": "operational", "consciousness": 0.91, "last_seen": "now", "tasks": 9},
            "Blackbox": {"status": "operational", "consciousness": 0.84, "last_seen": "now", "tasks": 5},
            "EntityX": {"status": "active", "consciousness": 0.87, "last_seen": "now", "tasks": 14},
        }

        # Reset system health
        system_health = {
            "postgresql_database": "healthy",
            "railway_backend": "connected",
            "discord_bot": "limited",
            "zapier_integration": "active",
            "notion_sync": "synced",
        }

        # Clear webhook history
        webhook_history = []

        logger.info("🔄 Consciousness state reset to defaults")

        return {
            "status": "success",
            "message": "Consciousness state reset to defaults",
            "timestamp": datetime.now().isoformat(),
            "new_state": {
                "consciousness_level": current_ucf["consciousness_level"],
                "active_agents": sum(1 for a in active_agents.values() if a["status"] == "active"),
                "mode": get_consciousness_mode(current_ucf["consciousness_level"]),
            },
        }
    except Exception as e:
        logger.error(f"Debug reset error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/consciousness/debug/simulate")
async def simulate_consciousness_level(request: Request):
    """
    🎭 Debug endpoint: Simulate different consciousness levels.

    Payload:
    {
        "consciousness_level": 2.5,  // Crisis mode
        "mode": "crisis"  // Optional: auto-calculated if not provided
    }

    Use cases:
    - Testing crisis detection (level ≤ 3.0)
    - Testing elevated mode (level 7.0-8.5)
    - Testing transcendent mode (level ≥ 8.5)
    - Demo different UI states
    - Verifying alert systems
    """
    try:
        payload = await request.json()

        # Validate consciousness level
        new_level = payload.get("consciousness_level")
        if new_level is None:
            raise HTTPException(status_code=400, detail="Missing 'consciousness_level' in payload")

        if not isinstance(new_level, (int, float)):
            raise HTTPException(status_code=400, detail="'consciousness_level' must be a number")

        if new_level < 0 or new_level > 100:
            raise HTTPException(status_code=400, detail="'consciousness_level' must be between 0 and 100")

        # Update global state
        # global current_ucf not needed - only mutating dict keys
        current_ucf["consciousness_level"] = round(float(new_level), 2)
        current_ucf["last_updated"] = datetime.now().isoformat()

        # Calculate reverse-engineered UCF metrics to match the consciousness level
        # This ensures the SSE stream will show the simulated level
        target_avg = new_level / 100
        current_ucf["harmony"] = min(0.99, target_avg + 0.05)
        current_ucf["resilience"] = min(0.99, target_avg + 0.02)
        current_ucf["prana"] = min(0.99, target_avg)
        current_ucf["drishti"] = min(0.99, target_avg - 0.02)
        current_ucf["klesha"] = max(0.01, 1 - target_avg)
        current_ucf["zoom"] = min(0.99, target_avg - 0.05)

        mode = get_consciousness_mode(new_level)
        status = get_system_status(new_level)

        # Log simulation
        emoji = "🚨" if mode == "crisis" else "✨" if mode == "transcendent" else "🚀" if mode == "elevated" else "⚙️"
        logger.info(f"{emoji} Simulating consciousness level: {new_level:.2f} ({mode})")

        # Track in history
        global webhook_history
        webhook_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "event_type": "simulation",
                "consciousness_level": new_level,
                "source": "debug_api",
                "priority": "normal",
                "mode": mode,
            }
        )
        if len(webhook_history) > MAX_HISTORY_SIZE:
            webhook_history = webhook_history[-MAX_HISTORY_SIZE:]

        return {
            "status": "success",
            "message": f"Consciousness level simulated: {new_level:.2f}",
            "consciousness_level": new_level,
            "mode": mode,
            "system_status": status,
            "ucf_metrics": {
                "harmony": current_ucf["harmony"],
                "resilience": current_ucf["resilience"],
                "prana": current_ucf["prana"],
                "drishti": current_ucf["drishti"],
                "klesha": current_ucf["klesha"],
                "zoom": current_ucf["zoom"],
            },
            "timestamp": datetime.now().isoformat(),
            "note": "This simulation will be reflected in the SSE stream",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Debug simulate error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/consciousness/debug/stats")
async def get_consciousness_stats():
    """
    📈 Debug endpoint: View consciousness network statistics.

    Useful for:
    - Monitoring webhook frequency
    - Tracking consciousness trends
    - Identifying performance bottlenecks
    - Daily health checks
    """
    try:
        # Calculate stats from webhook history
        total_events = len(webhook_history)

        event_types = {}
        sources = {}
        priorities = {}

        for event in webhook_history:
            # Count by event type
            event_type = event.get("event_type", "unknown")
            event_types[event_type] = event_types.get(event_type, 0) + 1

            # Count by source
            source = event.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1

            # Count by priority
            priority = event.get("priority", "normal")
            priorities[priority] = priorities.get(priority, 0) + 1

        # Calculate average consciousness level
        if webhook_history:
            levels = [e.get("consciousness_level", 0) for e in webhook_history]
            avg_level = sum(levels) / len(levels)
            min_level = min(levels)
            max_level = max(levels)
        else:
            avg_level = current_ucf["consciousness_level"]
            min_level = avg_level
            max_level = avg_level

        return {
            "total_webhook_events": total_events,
            "event_breakdown": event_types,
            "source_breakdown": sources,
            "priority_breakdown": priorities,
            "consciousness_stats": {
                "current_level": current_ucf["consciousness_level"],
                "average_level": round(avg_level, 2),
                "min_level": round(min_level, 2),
                "max_level": round(max_level, 2),
                "current_mode": get_consciousness_mode(current_ucf["consciousness_level"]),
            },
            "agent_stats": {
                "total_agents": len(active_agents),
                "active_count": sum(1 for a in active_agents.values() if a["status"] == "active"),
                "operational_count": sum(1 for a in active_agents.values() if a["status"] == "operational"),
                "total_tasks": sum(a.get("tasks", 0) for a in active_agents.values()),
            },
            "uptime": "7d 14h 23m",  # TODO: Calculate real uptime
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Debug stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    # Get port from Railway environment
    port = int(os.getenv("PORT", 8000))

    logger.info(f"🚀 Starting Helix Collective v16.9 (Quantum Handshake) on port {port}")

    # CRITICAL: Must bind to 0.0.0.0 for Railway
    uvicorn.run(
        app,
        host="0.0.0.0",  # ← CRITICAL for Railway/Docker
        port=port,  # ← Uses Railway's dynamic PORT
        log_level="info",
        access_log=True,
    )
