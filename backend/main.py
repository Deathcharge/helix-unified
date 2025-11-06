# 🌀 Helix Collective v14.5 — Quantum Handshake
# backend/main.py — FastAPI + Discord Bot Launcher (FIXED IMPORTS)
# Author: Andrew John Ward (Architect)

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import asyncio
import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import logging
import httpx
from pydantic import BaseModel

# Import centralized logging configuration
from logging_config import setup_logging

# FIX: Create Crypto → Cryptodome alias BEFORE importing mega
import sys
try:
    import Cryptodome
    sys.modules['Crypto'] = Cryptodome
    sys.modules['Crypto.Cipher'] = Cryptodome.Cipher
    sys.modules['Crypto.PublicKey'] = Cryptodome.PublicKey
    sys.modules['Crypto.Protocol'] = Cryptodome.Protocol
    sys.modules['Crypto.Random'] = Cryptodome.Random
    sys.modules['Crypto.Hash'] = Cryptodome.Hash
    sys.modules['Crypto.Util'] = Cryptodome.Util
    print("✅ Crypto import compatibility layer activated (backend/main.py)")
except ImportError:
    print("⚠️ pycryptodome not found - MEGA sync may fail")

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
logger.info("🌀 Helix Collective v14.5 - Backend Initialization")

# ✅ FIXED IMPORTS - Use relative imports instead of absolute
from discord_bot_manus import bot as discord_bot
from agents_loop import main_loop as manus_loop
from agents import AGENTS, get_collective_status
from websocket_manager import manager as ws_manager
from mandelbrot_ucf import (
    MandelbrotUCFGenerator,
    get_eye_of_consciousness,
    generate_ritual_ucf
)

# ============================================================================
# WEBSOCKET BROADCAST LOOP
# ============================================================================

async def ucf_broadcast_loop():
    """
    Background task that monitors UCF state and broadcasts changes.
    Replaces 5-second polling with event-driven updates.
    """
    previous_state = None
    broadcast_interval = 2  # Check every 2 seconds

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
                logger.debug(f"📡 UCF state changed and broadcasted")
                previous_state = current_state.copy()

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
    print("🌀 Helix Collective v14.5 - Startup Sequence")
    
    # Initialize directories
    Path("Helix/state").mkdir(parents=True, exist_ok=True)
    Path("Helix/commands").mkdir(parents=True, exist_ok=True)
    Path("Helix/ethics").mkdir(parents=True, exist_ok=True)
    Path("Shadow/manus_archive").mkdir(parents=True, exist_ok=True)
    
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
            bot_task = asyncio.create_task(discord_bot.start(discord_token))
            print("🤖 Discord bot task started")
        except Exception as e:
            print(f"⚠ Discord bot start error: {e}")
    else:
        print("⚠ No DISCORD_TOKEN found - bot not started")
    
    # Launch Manus operational loop in background task
    try:
        manus_task = asyncio.create_task(manus_loop())
        print("🤲 Manus operational loop task started")
    except Exception as e:
        print(f"⚠ Manus loop start error: {e}")

    # Launch WebSocket UCF broadcaster in background task
    try:
        ws_broadcast_task = asyncio.create_task(ucf_broadcast_loop())
        print("📡 WebSocket UCF broadcast task started")
    except Exception as e:
        print(f"⚠ WebSocket broadcast start error: {e}")

    print("✅ Helix Collective v14.5 - Ready for Operations")

    yield  # Application runs
    
    # Cleanup on shutdown
    print("🌙 Helix Collective v14.5 - Shutdown Sequence")

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="🌀 Helix Collective v14.5",
    description="Quantum Handshake Edition - Multi-Agent AI System",
    version="14.5.0",
    lifespan=lifespan
)

# Setup templates directory (use absolute path for Railway compatibility)
# Try multiple path resolution strategies for robustness
def find_templates_directory():
    """Find templates directory using multiple strategies."""
    # Strategy 1: Relative to this file (backend/main.py)
    strategy1 = Path(__file__).parent.parent / "templates"

    # Strategy 2: Relative to current working directory
    strategy2 = Path.cwd() / "templates"

    # Strategy 3: Sibling to backend directory
    strategy3 = Path(__file__).parent.parent / "templates"

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
    logger.error(f"❌ Could not find templates directory! Using fallback.")
    return strategy1

BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = find_templates_directory()
logger.info(f"📁 Templates directory: {TEMPLATES_DIR.resolve()}")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ============================================================================
# HEALTH CHECK ENDPOINT (REQUIRED FOR RAILWAY)
# ============================================================================

@app.get("/health")
async def health_check():
    """Railway health check endpoint."""
    try:
        # Check if state files exist
        state_file = Path("Helix/state/ucf_state.json")
        heartbeat_file = Path("Helix/state/heartbeat.json")
        
        state_exists = state_file.exists()
        heartbeat_exists = heartbeat_file.exists()
        
        # Get agent count
        agent_count = len(AGENTS)
        
        return {
            "status": "healthy",
            "service": "helix-collective",
            "version": "14.5.0",
            "agents": agent_count,
            "state_initialized": state_exists,
            "heartbeat_active": heartbeat_exists,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
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
            "message": "🌀 Helix Collective v14.5 - Quantum Handshake Edition",
            "status": "operational",
            "agents": len(status),
            "agent_names": list(status.keys()),
            "endpoints": {
                "health": "/health",
                "status": "/status",
                "agents": "/agents",
                "ucf": "/ucf",
                "dashboard": "/",
                "docs": "/docs"
            }
        }
    except Exception as e:
        return {
            "message": "🌀 Helix Collective v14.5 - Quantum Handshake Edition",
            "status": "initializing",
            "error": str(e)
        }

# ============================================================================
# AGENT STATUS ENDPOINT
# ============================================================================

@app.get("/status")
async def get_status():
    """Get full system status."""
    try:
        status = await get_collective_status()
        
        # Read UCF state
        ucf_state = {}
        try:
            with open("Helix/state/ucf_state.json", "r") as f:
                ucf_state = json.load(f)
        except:
            pass
        
        # Read heartbeat
        heartbeat = {}
        try:
            with open("Helix/state/heartbeat.json", "r") as f:
                heartbeat = json.load(f)
        except:
            pass
        
        return {
            "agents": status,
            "ucf_state": ucf_state,
            "heartbeat": heartbeat,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Get port from Railway environment
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting Helix Collective v14.5 on port {port}")
    
    # CRITICAL: Must bind to 0.0.0.0 for Railway
    uvicorn.run(
        app,
        host="0.0.0.0",  # ← CRITICAL for Railway/Docker
        port=port,        # ← Uses Railway's dynamic PORT
        log_level="info",
        access_log=True
    )
