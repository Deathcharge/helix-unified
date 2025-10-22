# 🌀 Helix Collective v14.5 — Quantum Handshake
# backend/main.py — FastAPI + Discord Bot Launcher (CORRECTED)
# Author: Andrew John Ward (Architect)

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import asyncio
import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Import core components
from backend.discord_bot_manus import bot as discord_bot
from backend.agents_loop import main_loop as manus_loop
from backend.agents import AGENTS, get_collective_status

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
            print(f"⚠ Discord bot startup warning: {e}")
            bot_task = None
    else:
        print("⚠ DISCORD_TOKEN not set - Discord bot disabled")
        bot_task = None
    
    # Launch Manus operational loop in background task
    try:
        manus_task = asyncio.create_task(manus_loop())
        print("🤲 Manus operational loop task started")
    except Exception as e:
        print(f"⚠ Manus loop startup warning: {e}")
        manus_task = None
    
    print("✅ Helix Collective v14.5 - Ready for Operations")
    
    yield  # App runs here
    
    # Cleanup on shutdown
    print("🛑 Helix Collective v14.5 - Shutdown Sequence")
    if bot_task:
        try:
            await discord_bot.close()
            bot_task.cancel()
        except:
            pass
    if manus_task:
        try:
            manus_task.cancel()
        except:
            pass

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Helix Collective API",
    version="14.5",
    description="Unified multi-agent system with Discord integration and autonomous operations",
    lifespan=lifespan
)

# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        ucf_state = {}
        state_path = Path("Helix/state/ucf_state.json")
        if state_path.exists():
            with open(state_path) as f:
                ucf_state = json.load(f)
        
        return {
            "status": "healthy",
            "version": "14.5",
            "codename": "Quantum Handshake",
            "discord_bot": discord_bot.user is not None if hasattr(discord_bot, 'user') else False,
            "harmony": ucf_state.get("harmony", 0.355),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ucf/current")
async def get_ucf_state():
    """Get current UCF state."""
    try:
        state_path = Path("Helix/state/ucf_state.json")
        if not state_path.exists():
            return {
                "zoom": 1.0228,
                "harmony": 0.355,
                "resilience": 1.1191,
                "prana": 0.5175,
                "drishti": 0.5023,
                "klesha": 0.010
            }
        with open(state_path) as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def system_status():
    """Get current system status including UCF state."""
    try:
        state_path = Path("Helix/state/ucf_state.json")
        heartbeat_path = Path("Helix/state/heartbeat.json")
        
        ucf_state = {}
        heartbeat = {}
        
        if state_path.exists():
            with open(state_path) as f:
                ucf_state = json.load(f)
        
        if heartbeat_path.exists():
            with open(heartbeat_path) as f:
                heartbeat = json.load(f)
        
        return {
            "system": "Helix Collective v14.5",
            "ucf_state": ucf_state,
            "heartbeat": heartbeat,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents")
async def list_agents():
    """List all active agents in the collective."""
    try:
        agents_info = []
        for name, agent in AGENTS.items():
            agents_info.append({
                "name": name,
                "symbol": agent.symbol,
                "role": agent.role,
                "active": agent.active,
                "memory_size": len(agent.memory)
            })
        return {"agents": agents_info, "total": len(agents_info)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# DIRECTIVE ENDPOINTS
# ============================================================================

@app.post("/directive")
async def issue_directive(action: str, parameters: dict = None):
    """Issue a directive to Manus for execution."""
    if parameters is None:
        parameters = {}
    
    try:
        vega = AGENTS.get("Vega")
        if not vega:
            raise HTTPException(status_code=500, detail="Vega agent not initialized")
        
        directive = await vega.issue_directive(action, parameters)
        return {
            "status": "directive_issued",
            "directive": directive,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ritual")
async def execute_ritual(steps: int = 108):
    """Execute Z-88 ritual."""
    try:
        from backend.z88_ritual_engine import RitualManager
        manager = RitualManager(steps=steps)
        final_state = await manager.run_async()
        return {
            "status": "ritual_complete",
            "steps": steps,
            "final_state": final_state,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# LOGS ENDPOINTS
# ============================================================================

@app.get("/logs/operations")
async def get_operation_logs(limit: int = 20):
    """Get recent operation logs from Manus archive."""
    try:
        log_path = Path("Shadow/manus_archive/operations.log")
        if not log_path.exists():
            return {"logs": [], "total": 0}
        
        with open(log_path) as f:
            lines = f.readlines()
        
        logs = []
        for line in lines[-limit:]:
            try:
                logs.append(json.loads(line))
            except:
                pass
        
        return {"logs": logs, "total": len(logs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs/discord")
async def get_discord_logs(limit: int = 20):
    """Get recent Discord bot logs."""
    try:
        log_path = Path("Shadow/manus_archive/discord_bridge_log.json")
        if not log_path.exists():
            return {"logs": [], "total": 0}
        
        with open(log_path) as f:
            logs = json.load(f)
        
        return {"logs": logs[-limit:], "total": len(logs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs/ritual")
async def get_ritual_logs(limit: int = 20):
    """Get recent ritual execution logs."""
    try:
        log_path = Path("Shadow/manus_archive/z88_log.json")
        if not log_path.exists():
            return {"logs": [], "total": 0}
        
        with open(log_path) as f:
            logs = json.load(f)
        
        return {"logs": logs[-limit:], "total": len(logs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with system info."""
    return {
        "system": "Helix Collective v14.5 - Quantum Handshake Edition",
        "description": "Unified multi-agent system with Discord integration and autonomous operations",
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "agents": "/agents",
            "ucf": "/api/ucf/current",
            "directive": "/directive",
            "ritual": "/ritual",
            "logs": {
                "operations": "/logs/operations",
                "discord": "/logs/discord",
                "ritual": "/logs/ritual"
            }
        },
        "documentation": "/docs"
    }

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    # Get port from environment (Railway sets this)
    port = int(os.getenv("PORT", 8000))

    # MUST bind to 0.0.0.0, not localhost/127.0.0.1
    uvicorn.run(
        app,
        host="0.0.0.0",  # ← CRITICAL for Railway
        port=port,        # ← CRITICAL: Use Railway's PORT
        log_level="info",
        access_log=True
    )

