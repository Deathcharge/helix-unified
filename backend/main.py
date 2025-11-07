# 🌀 Helix Collective v14.5 — Quantum Handshake
# backend/main.py — FastAPI + Discord Bot Launcher (FIXED IMPORTS)
# Author: Andrew John Ward (Architect)

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import asyncio
import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import httpx
import aiohttp
from pydantic import BaseModel
from typing import Dict, Any

# Import centralized logging configuration
from logging_config import setup_logging

# FIX: Create Crypto → Cryptodome alias BEFORE importing mega
try:
    # pycryptodome installs as 'Crypto', not 'Cryptodome'
    import Crypto
    print(f"✅ pycryptodome found (version {Crypto.__version__}) - MEGA sync enabled")
except ImportError:
    print("⚠️ pycryptodome not found - MEGA sync may fail")
    Crypto = None

from mega import Mega

class PersistenceEngine:
    def __init__(self):
        self.mega = Mega()
        self.m = self.mega.login(
            os.getenv('MEGA_EMAIL'), 
            os.getenv('MEGA_PASS')
        )
        self.remote_dir = os.getenv('MEGA_REMOTE_DIR')

    def upload_state(self):
        local = 'Helix/state/heartbeat.json'
        remote = f"{self.remote_dir}/state/heartbeat.json"
        self.m.upload(local, remote)
        print("MEGA: Heartbeat synced.")

    def upload_archive(self, filepath):
        remote = f"{self.remote_dir}/manus_archive/{os.path.basename(filepath)}"
        self.m.upload(filepath, remote)
        print(f"MEGA: Archive preserved — {filepath}")

    def download_state(self):
        remote = f"{self.remote_dir}/state/heartbeat.json"
        self.m.download(remote, 'Helix/state/heartbeat.json')
        print("MEGA: State restored from cloud.")
load_dotenv()

# ============================================================================
# LOGGING SETUP
# ============================================================================
logger = setup_logging(
    log_dir="Shadow/manus_archive",
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    enable_rotation=True
)
logger.info("🌀 Helix Collective v16.7 - Backend Initialization")

# ✅ FIXED IMPORTS - Use relative imports instead of absolute
from discord_bot_manus import bot as discord_bot
from agents_loop import main_loop as manus_loop
from websocket_manager import manager as ws_manager
from mandelbrot_ucf import (
    MandelbrotUCFGenerator,
    get_eye_of_consciousness,
    generate_ritual_ucf
)
from zapier_integration import HelixZapierIntegration, set_zapier, get_zapier
from agent_embeds import get_collective_status

# ============================================================================
# WEBSOCKET BROADCAST LOOP
# ============================================================================

async def ucf_broadcast_loop():
    """
    Background task that monitors UCF state and broadcasts changes.
    Replaces 5-second polling with event-driven updates.
    Also sends telemetry to Zapier when UCF state changes.
    """
    previous_state = None
    broadcast_interval = 2  # Check every 2 seconds
    zapier_send_interval = 30  # Send to Zapier every 30 seconds
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

                # Send to Zapier every 30 seconds (not every change)
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
                                    "version": "16.7",
                                    "agents_count": len(agents_status),
                                    "timestamp": datetime.utcnow().isoformat(),
                                    "codename": "Documentation Consolidation & Real-Time Streaming",
                                    "agents": agent_list
                                }
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
    print("🌀 Helix Collective v16.7 - Startup Sequence")

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
        print("✅ Zapier integration enabled")
    else:
        print("⚠️ ZAPIER_WEBHOOK_URL not set - integration disabled")

    # Initialize agents
    try:
        status = await get_collective_status()
        print(f"✅ {len(status)} agents initialized")
        for name, info in status.items():
            print(f"   {info['symbol']} {name}: {info['role']}")
    except Exception as e:
        print(f"⚠ Agent initialization warning: {e}")
    
    # Launch Discord bot in background task
    discord_token = os.getenv("DISCORD_TOKEN")
    if discord_token:
        try:
            asyncio.create_task(discord_bot.start(discord_token))  # noqa: F841
            print("🤖 Discord bot task started")
        except Exception as e:
            print(f"⚠ Discord bot start error: {e}")
    else:
        print("⚠ No DISCORD_TOKEN found - bot not started")

    # Launch Manus operational loop in background task
    try:
        asyncio.create_task(manus_loop())  # noqa: F841
        print("🤲 Manus operational loop task started")
    except Exception as e:
        print(f"⚠ Manus loop start error: {e}")

    # Launch WebSocket UCF broadcaster in background task
    try:
        asyncio.create_task(ucf_broadcast_loop())  # noqa: F841
        print("📡 WebSocket UCF broadcast task started")
    except Exception as e:
        print(f"⚠ WebSocket broadcast start error: {e}")

    print("✅ Helix Collective v16.7 - Ready for Operations")

    yield  # Application runs

    # Cleanup on shutdown
    print("🌙 Helix Collective v16.7 - Shutdown Sequence")

    # Close Zapier session
    zapier = get_zapier()
    if zapier:
        await zapier.__aexit__(None, None, None)
        print("✅ Zapier integration closed")

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="🌀 Helix Collective v16.7",
    description="Documentation Consolidation & Real-Time Streaming",
    version="16.7.0",
    lifespan=lifespan
)

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Setup templates directory (use absolute path for Railway compatibility)
# Try multiple path resolution strategies for robustness
def find_templates_directory():
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
def health_check():
    """Minimal health check endpoint - always returns 200."""
    return {"ok": True}

# ============================================================================
# DISCOVERY MANIFEST (for external AI agents)
# ============================================================================

@app.get("/.well-known/helix.json")
def helix_manifest():
    """
    Machine-readable manifest for external AI agents.

    Exposes system capabilities, endpoints, UCF metrics, agents,
    and integration guides for Claude, Grok, Chai, and other AIs.

    Spec: helix-discovery-v1
    """
    manifest_path = Path("helix-manifest.json")
    try:
        manifest_data = json.loads(manifest_path.read_text())
        return manifest_data
    except FileNotFoundError:
        logger.error(f"❌ Manifest not found: {manifest_path.resolve()}")
        return {
            "version": "1",
            "error": "manifest_missing",
            "note": "helix-manifest.json not found in repository root"
        }
    except Exception as e:
        logger.error(f"❌ Error loading manifest: {e}")
        return {
            "version": "1",
            "error": "manifest_load_failed",
            "detail": str(e)
        }

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

@app.get("/api", response_class=HTMLResponse)
async def api_info():
    """API info endpoint (JSON)."""
    try:
        status = await get_collective_status()
        return {
            "message": "🌀 Helix Collective v16.7 - Documentation Consolidation & Real-Time Streaming",
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
                "docs": "/docs"
            }
        }
    except Exception as e:
        return {
            "message": "🌀 Helix Collective v16.7 - Documentation Consolidation & Real-Time Streaming",
            "status": "initializing",
            "error": str(e)
        }

# ============================================================================
# AGENT STATUS ENDPOINT (MINIMAL ROBUST VERSION)
# ============================================================================

def read_json(p: Path, default):
    """Read JSON file with fallback to default."""
    try:
        return json.loads(p.read_text())
    except Exception:
        return default

@app.get("/status")
@app.get("/api/status")  # Alias for consistency with external agents
def get_status():
    """Get full system status - minimal robust version."""
    # Read UCF state with defaults
    ucf = read_json(Path("Helix/state/ucf_state.json"), {
        "harmony": None,
        "resilience": None,
        "prana": None,
        "drishti": None,
        "klesha": None,
        "zoom": None
    })

    # Read agents state with defaults
    agents = read_json(Path("Helix/state/agents.json"), {
        "active": [],
        "count": 0
    })

    # Read heartbeat with defaults
    heartbeat = read_json(Path("Helix/state/heartbeat.json"), {
        "ts": None
    })

    return {
        "system": {
            "operational": True,
            "ts": heartbeat.get("ts")
        },
        "ucf": ucf,
        "agents": agents,
        "version": os.getenv("SYSTEM_VERSION", "16.7"),
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================================
# AGENT LIST ENDPOINT
# ============================================================================

@app.get("/agents")
async def list_agents():
    """Get list of all agents."""
    try:
        status = await get_collective_status()
        return {
            "count": len(status),
            "agents": status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# UCF STATE ENDPOINT
# ============================================================================

@app.get("/ucf")
async def get_ucf_state():
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
# WEBSOCKET ENDPOINT - REAL-TIME STREAMING
# ============================================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time UCF and agent status streaming.

    Streams updates every 5 seconds with:
    - UCF state (harmony, resilience, prana, drishti, klesha, zoom)
    - Agent statuses
    - System heartbeat
    - Timestamp

    Usage:
        const ws = new WebSocket('wss://helix-unified-production.up.railway.app/ws');
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('UCF:', data.ucf_state);
            console.log('Agents:', data.agents);
        };
    """
    await websocket.accept()

    try:
        while True:
            # Gather current state
            try:
                # Get agent status
                agents = await get_collective_status()

                # Read UCF state
                ucf_state = {}
                try:
                    with open("Helix/state/ucf_state.json", "r") as f:
                        ucf_state = json.load(f)
                except Exception:
                    pass

                # Read heartbeat
                heartbeat = {}
                try:
                    with open("Helix/state/heartbeat.json", "r") as f:
                        heartbeat = json.load(f)
                except Exception:
                    pass

                # Send update
                await websocket.send_json({
                    "type": "status_update",
                    "ucf_state": ucf_state,
                    "agents": agents,
                    "heartbeat": heartbeat,
                    "timestamp": datetime.utcnow().isoformat()
                })

            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                })

            # Wait 5 seconds before next update
            await asyncio.sleep(5)

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

# ============================================================================
# TEMPLATE SERVING ENDPOINTS
# ============================================================================

@app.get("/templates/{file_path:path}")
async def serve_template(file_path: str):
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
async def generate_music(request: MusicGenerationRequest):
    """
    Proxy endpoint for ElevenLabs Music API.
    Generates music from text prompts using ElevenLabs Music v1.
    """
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    if not elevenlabs_api_key:
        raise HTTPException(
            status_code=500,
            detail="ElevenLabs API key not configured"
        )

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            # Call ElevenLabs Music API
            response = await client.post(
                "https://api.elevenlabs.io/v1/music/generate",
                headers={
                    "xi-api-key": elevenlabs_api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "text": request.prompt,
                    "duration_seconds": request.duration,
                    "model_id": request.model_id
                }
            )

            response.raise_for_status()

            # Stream audio response back to client
            return StreamingResponse(
                iter([response.content]),
                media_type="audio/mpeg",
                headers={
                    "Content-Disposition": "attachment; filename=ritual_music.mp3"
                }
            )
    except httpx.HTTPStatusError as e:
        logger.error(f"ElevenLabs API error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"ElevenLabs API error: {e.response.text}"
        )
    except Exception as e:
        logger.error(f"Music generation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Music generation failed: {str(e)}"
        )

# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time UCF state updates.

    Clients connect to ws://host/ws and receive:
    - UCF state updates when values change
    - Agent status updates
    - System events
    - Heartbeat pings (every 30s)

    Example client usage:
        const ws = new WebSocket('ws://localhost:8000/ws');
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'ucf_update') {
                updateDashboard(data.data);
            }
        };
    """
    await ws_manager.connect(websocket)

    try:
        # Start heartbeat task
        heartbeat = asyncio.create_task(
            send_heartbeats(websocket)
        )

        # Listen for client messages (optional - mostly for pings)
        while True:
            data = await websocket.receive_text()
            # Echo back for connection test
            await websocket.send_json({
                "type": "echo",
                "message": data,
                "timestamp": datetime.utcnow().isoformat()
            })

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        heartbeat.cancel()
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)
        if not heartbeat.done():
            heartbeat.cancel()


async def send_heartbeats(websocket: WebSocket, interval: int = 30):
    """Send periodic heartbeat pings to keep connection alive."""
    try:
        while True:
            await asyncio.sleep(interval)
            await websocket.send_json({
                "type": "heartbeat",
                "timestamp": datetime.utcnow().isoformat()
            })
    except Exception:
        pass  # Connection closed


@app.get("/ws/stats")
async def websocket_stats():
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
async def get_eye_ucf(context: str = "generic"):
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
            "context": context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mandelbrot/generate")
async def generate_ucf_from_coordinate(request: MandelbrotRequest):
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
            "context": request.context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mandelbrot/sacred")
async def list_sacred_points():
    """List all predefined sacred Mandelbrot coordinates."""
    generator = MandelbrotUCFGenerator()
    sacred_points = {}

    descriptions = {
        "eye_of_consciousness": "Optimal balance point with peak harmony and resilience",
        "seahorse_valley": "High resilience with moderate harmony, good for challenges",
        "main_bulb": "Maximum harmony with lower complexity, ideal for grounding",
        "mini_mandelbrot": "Fractal self-similarity, high zoom and recursive depth",
        "dendrite_spiral": "Spiral growth patterns, dynamic transformation",
        "elephant_valley": "Stability and strength, robust foundation"
    }

    for name, coord in generator.sacred_points.items():
        sacred_points[name] = {
            "coordinate": {"real": coord.real, "imag": coord.imag},
            "description": descriptions.get(name, "Sacred Mandelbrot coordinate")
        }

    return sacred_points


@app.get("/mandelbrot/sacred/{point_name}")
async def get_sacred_ucf(point_name: str, context: str = "generic"):
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
            "elephant_valley": "Stability and strength, robust foundation"
        }

        return {
            "point_name": point_name,
            "coordinate": {"real": coord.real, "imag": coord.imag},
            "ucf_state": ucf_state,
            "context": context,
            "description": descriptions.get(point_name, "Sacred Mandelbrot coordinate")
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mandelbrot/ritual/{step}")
async def get_ritual_step_ucf(step: int, total_steps: int = 108):
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
            raise HTTPException(
                status_code=400,
                detail=f"Step must be between 0 and {total_steps-1}"
            )

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
async def trigger_zapier_webhook(payload: Dict[str, Any]):
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
            status_code=503,
            detail="Zapier integration not configured. Set ZAPIER_WEBHOOK_URL environment variable."
        )

    try:
        # Send raw payload to Zapier
        async with zapier.session.post(
            zapier.webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=aiohttp.ClientTimeout(total=10)
        ) as response:
            return {
                "status": response.status,
                "success": response.status == 200,
                "message": "Webhook triggered successfully" if response.status == 200 else "Webhook returned non-200 status"
            }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Webhook trigger failed: {str(e)}"
        )


@app.post("/api/zapier/telemetry")
async def send_zapier_telemetry():
    """
    Send current UCF telemetry to Zapier webhook.

    Reads current UCF state and agent status, then sends to Zapier.
    Useful for manual testing or triggered updates.
    """
    zapier = get_zapier()
    if not zapier:
        raise HTTPException(
            status_code=503,
            detail="Zapier integration not configured. Set ZAPIER_WEBHOOK_URL environment variable."
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
        agent_list = [
            {"name": name, "symbol": info["symbol"], "status": "active"}
            for name, info in agents_status.items()
        ]

        # Send to Zapier
        success = await zapier.send_telemetry(
            ucf_metrics=ucf_state,
            system_info={
                "version": "16.7",
                "agents_count": len(agents_status),
                "timestamp": datetime.utcnow().isoformat(),
                "codename": "Documentation Consolidation & Real-Time Streaming",
                "agents": agent_list
            }
        )

        if success:
            return {
                "success": True,
                "message": "Telemetry sent to Zapier successfully",
                "ucf": ucf_state,
                "agents_count": len(agents_status)
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send telemetry to Zapier")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    # Get port from Railway environment
    port = int(os.getenv("PORT", 8000))

    print(f"🚀 Starting Helix Collective v16.7 on port {port}")
    
    # CRITICAL: Must bind to 0.0.0.0 for Railway
    uvicorn.run(
        app,
        host="0.0.0.0",  # ← CRITICAL for Railway/Docker
        port=port,        # ← Uses Railway's dynamic PORT
        log_level="info",
        access_log=True
    )
