# 🌀 Helix Collective v14.5 — Quantum Handshake
# backend/main.py — FastAPI + Discord Bot Launcher (FIXED IMPORTS)
# Author: Andrew John Ward (Architect)

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
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
logger.info("🌀 Helix Collective v16.7 - Backend Initialization")

# ✅ FIXED IMPORTS - Use relative imports instead of absolute
from discord_bot_manus import bot as discord_bot
from agents_loop import main_loop as manus_loop
from agents import AGENTS, get_collective_status

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
    
    print("✅ Helix Collective v16.7 - Ready for Operations")

    yield  # Application runs

    # Cleanup on shutdown
    print("🌙 Helix Collective v16.7 - Shutdown Sequence")

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
def health_check():
    """Minimal health check endpoint - always returns 200."""
    return {"ok": True}

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
                except:
                    pass

                # Read heartbeat
                heartbeat = {}
                try:
                    with open("Helix/state/heartbeat.json", "r") as f:
                        heartbeat = json.load(f)
                except:
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
