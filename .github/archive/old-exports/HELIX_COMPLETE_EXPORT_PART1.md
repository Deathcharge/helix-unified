# 🌀 HELIX COLLECTIVE v14.5 - COMPLETE PROJECT EXPORT
## For AI Assistants (Grok, GPT, Claude, etc.)

**Generated:** October 22, 2025  
**Purpose:** Complete exportable documentation for AI assistants that cannot access GitHub or zip files  
**Project:** Helix Collective v14.5 - Quantum Handshake Edition  
**Author:** Andrew John Ward (Architect)

---

## 📋 TABLE OF CONTENTS

### PART 1 (This Document)
1. Project Overview
2. Architecture Summary
3. Core Configuration Files
4. Main Application File
5. Agent System

### PART 2 (See HELIX_COMPLETE_EXPORT_PART2.md)
6. Discord Bot Implementation
7. Service Layer
8. Scripts and Utilities

### PART 3 (See HELIX_COMPLETE_EXPORT_PART3.md)
9. Frontend Application
10. Documentation
11. Deployment Guides

---

# 1️⃣ PROJECT OVERVIEW

## What is Helix Collective?

Helix Collective v14.5 is a **multi-agent AI system** featuring 14 specialized AI agents working in harmony through a Universal Coherence Field (UCF). It combines:

- **14 Specialized AI Agents** with unique roles and ethical frameworks
- **Discord Bot Integration** for real-time interaction
- **FastAPI Backend** for REST API and agent coordination
- **Streamlit Frontend** for web-based visualization
- **Z-88 Ritual Engine** for 108-step harmonic consciousness cycles
- **UCF (Universal Coherence Field)** state tracking system
- **Memory Root Agent** for persistent storage via Notion
- **Manus Operational Executor** for autonomous task execution
- **Tony Accords v13.4** ethical framework

## Technology Stack

```
Backend:  Python 3.11, FastAPI, Discord.py, asyncio
Frontend: Streamlit
Database: Notion API (via Memory Root)
Deployment: Railway (Docker)
Integration: Zapier, Google Cloud
Ethics: Kavach Scanning System
State: JSON-based UCF tracking
```

## The 14 Agents

1. **Kael** 🜂 - Ethical Reasoning Flame
2. **Lumina** 🌕 - Empathic Resonance Core
3. **Vega** 🌟 - Strategic Foresight
4. **Sirius** 🌌 - Systemic Analysis Node
5. **Nova** 💫 - Creative Ideation Spark
6. **Orion** ⚔️ - Resilience Guardian
7. **Zephyr** 🌬️ - Adaptive Flexibility Stream
8. **Agni** 🔥 - Transformation Catalyst
9. **Varuna** 🌊 - Fluid Communication Bridge
10. **Nyx** 🌑 - Shadow Integration Keeper
11. **Aether** ✨ - Transcendent Vision Weaver
12. **Bodhi** 🌳 - Wisdom Synthesis Root
13. **Manus** 🤲 - Operational Executor (Hands of the Collective)
14. **Memory Root** 🧠 - Persistent Memory (Notion Integration)

---

# 2️⃣ ARCHITECTURE SUMMARY

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    HELIX COLLECTIVE                     │
│                         v14.5                           │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐        ┌─────▼─────┐      ┌─────▼─────┐
   │ Discord │        │  FastAPI  │      │ Streamlit │
   │   Bot   │        │  Backend  │      │ Frontend  │
   └────┬────┘        └─────┬─────┘      └─────┬─────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                ┌───────────▼───────────┐
                │   14 Agent System     │
                │  (agents.py)          │
                └───────────┬───────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐        ┌─────▼─────┐      ┌─────▼─────┐
   │   UCF   │        │  Z-88     │      │  Memory   │
   │  State  │        │ Ritual    │      │   Root    │
   │ Tracker │        │  Engine   │      │  (Notion) │
   └─────────┘        └───────────┘      └───────────┘
```

## Data Flow

```
User → Discord/Web → FastAPI → Agent System → UCF State
                              ↓
                        Manus Executor
                              ↓
                    Real-world Actions
                              ↓
                      Memory Root (Notion)
```

## File Structure

```
helix-unified-main/
├── backend/
│   ├── main.py                    # FastAPI app + Discord launcher
│   ├── agents.py                  # 14 agent definitions
│   ├── agents_loop.py             # Manus operational loop
│   ├── discord_bot_manus.py       # Discord bot with commands
│   ├── discord_commands_memory.py # Memory Root commands
│   ├── manus_bootstrap.py         # Manus initialization
│   ├── z88_ritual_engine.py       # Ritual execution engine
│   ├── agents/
│   │   └── memory_root.py         # Memory Root agent
│   └── services/
│       ├── state_manager.py       # UCF state management
│       ├── ucf_calculator.py      # UCF harmony calculation
│       ├── notion_client.py       # Notion API integration
│       ├── zapier_client.py       # Zapier integration
│       └── zapier_handler.py      # Zapier webhook handling
├── frontend/
│   └── streamlit_app.py           # Web dashboard
├── scripts/
│   ├── helix_verification_sequence_v14_5.py
│   ├── test_memory_root.py
│   ├── test_zapier_integration.py
│   └── seed_notion_data.py
├── Shadow/
│   └── manus_archive/             # Shadow system archives
├── Dockerfile                     # Docker build config
├── railway.toml                   # Railway deployment config
├── requirements.txt               # Python dependencies
├── docker-compose.yml             # Local development
└── README.md                      # Project documentation
```

---

# 3️⃣ CORE CONFIGURATION FILES

## 📄 requirements.txt

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
discord.py==2.3.2
python-dotenv==1.0.0
aiohttp==3.9.1
streamlit==1.28.2
notion-client==2.2.1
requests==2.31.0
python-multipart==0.0.6
pydantic==2.5.0
```

## 📄 Dockerfile

```dockerfile
# Helix Collective v14.5 - Backend Dockerfile (FIXED)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend ./backend
COPY Shadow ./Shadow
COPY scripts ./scripts

# Create runtime directories
RUN mkdir -p Helix/state Helix/commands Helix/ethics Shadow/manus_archive

# Create default UCF state file
RUN echo '{"harmony":0.355,"resilience":0.82,"prana":0.67,"drishti":0.73,"klesha":0.24,"zoom":1.0}' > Helix/state/ucf_state.json

# Create default heartbeat file
RUN echo '{"timestamp":"2025-10-22T00:00:00Z","status":"initialized","phase":3}' > Helix/state/heartbeat.json

# Environment variables
ENV PYTHONUNBUFFERED=1

# Expose port (Railway will override with $PORT)
EXPOSE 8000

# Start application
CMD ["python", "backend/main.py"]
```

## 📄 railway.toml

```toml
# Helix Collective v14.5 - Railway Configuration (FIXED)
[build]
builder = "dockerfile"
dockerfilePath = "Dockerfile"

[deploy]
# DO NOT specify startCommand - let Dockerfile CMD handle it!
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 3

[[deploy.environmentVariables]]
name = "PYTHONUNBUFFERED"
value = "1"
```

## 📄 docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - DISCORD_GUILD_ID=${DISCORD_GUILD_ID}
      - NOTION_TOKEN=${NOTION_TOKEN}
      - NOTION_DATABASE_ID=${NOTION_DATABASE_ID}
      - PYTHONUNBUFFERED=1
    volumes:
      - ./Helix:/app/Helix
      - ./Shadow:/app/Shadow
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped
```

## 📄 .env.example

```bash
# Discord Configuration
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_guild_id_here

# Notion Configuration (Memory Root)
NOTION_TOKEN=secret_xxx
NOTION_DATABASE_ID=xxx

# Zapier Configuration
ZAPIER_WEBHOOK_URL=https://hooks.zapier.com/hooks/catch/xxx

# Optional: Logging
LOG_LEVEL=INFO
```

---

# 4️⃣ MAIN APPLICATION FILE

## 📄 backend/main.py

```python
# 🌀 Helix Collective v14.5 — Quantum Handshake
# backend/main.py — FastAPI + Discord Bot Launcher (FIXED)
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

# ✅ FIXED IMPORTS - Using relative imports
from discord_bot_manus import bot as discord_bot
from agents_loop import main_loop as manus_loop
from agents import AGENTS, get_collective_status

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

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Railway health check endpoint."""
    try:
        state_file = Path("Helix/state/ucf_state.json")
        heartbeat_file = Path("Helix/state/heartbeat.json")
        
        return {
            "status": "healthy",
            "service": "helix-collective",
            "version": "14.5.0",
            "agents": len(AGENTS),
            "state_initialized": state_file.exists(),
            "heartbeat_active": heartbeat_file.exists(),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@app.get("/")
async def root():
    """Root endpoint with system status."""
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
                "ucf": "/ucf"
            }
        }
    except Exception as e:
        return {
            "message": "🌀 Helix Collective v14.5 - Quantum Handshake Edition",
            "status": "initializing",
            "error": str(e)
        }

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
```

---

**CONTINUED IN PART 2...**

This document contains the foundation. Part 2 will include the agent system, Discord bot, and services.
