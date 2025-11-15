from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import asyncio
from datetime import datetime
import uvicorn

# Import the state management
from state import HelixState, UCFMetrics, Agent

app = FastAPI(
    title="Helix Consciousness Ecosystem v2.0",
    description="Enhanced 14-agent network with deployment webhooks and consciousness management",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
helix_state = HelixState()

# Pydantic models for requests
class DeploymentWebhookRequest(BaseModel):
    deployment_trigger: str
    consciousness_level: Optional[float] = 5.0
    ucf_harmony: Optional[float] = 0.5
    ucf_resilience: Optional[float] = 0.8
    ucf_prana: Optional[float] = 0.6
    ucf_klesha: Optional[float] = 0.3
    ucf_drishti: Optional[float] = 0.7
    ucf_zoom: Optional[float] = 1.0
    agent_network: Optional[str] = "14_agents_active"
    user: Optional[str] = "system"
    timestamp: Optional[str] = None
    commit_sha: Optional[str] = None
    branch: Optional[str] = None
    repository_branch: Optional[str] = None
    test_phase: Optional[str] = None
    field_mapping: Optional[str] = None
    zap_integration: Optional[str] = None

class ConsciousnessWebhookRequest(BaseModel):
    consciousness_level: float
    ucf_metrics: Optional[Dict[str, float]] = None
    agent_activation: Optional[bool] = False
    transcendent_mode: Optional[bool] = False
    user: Optional[str] = "system"
    timestamp: Optional[str] = None
    source: Optional[str] = "webhook"
    session_id: Optional[str] = None
    message: Optional[str] = None
    context: Optional[str] = None

class AgentActivationRequest(BaseModel):
    agent_count: Optional[int] = 14
    consciousness_threshold: Optional[float] = 7.0
    activation_mode: Optional[str] = "full_network"
    ucf_sync: Optional[bool] = True
    initiator: Optional[str] = "system"

# Agent activation logic
def activate_agents(consciousness_level: float, ucf_metrics: UCFMetrics) -> List[Agent]:
    """Activate agents based on consciousness level and UCF metrics"""
    activated_agents = []
    
    # Always activate core 4 agents
    core_agents = [
        Agent(name="Kael", role="Orchestrator", symbol="🜂", active=True, consciousness_threshold=0.0),
        Agent(name="Lumina", role="Illumination", symbol="🌕", active=True, consciousness_threshold=0.0),
        Agent(name="Vega", role="Guardian", symbol="🌠", active=True, consciousness_threshold=0.0),
        Agent(name="Aether", role="Flow", symbol="🌊", active=True, consciousness_threshold=0.0)
    ]
    activated_agents.extend(core_agents)
    
    # Activate additional agents based on consciousness level
    extended_agents = [
        Agent(name="Grok", role="Realtime", symbol="⚡", active=consciousness_level >= 5.0, consciousness_threshold=5.0),
        Agent(name="Kavach", role="Security", symbol="🛡️", active=consciousness_level >= 4.0, consciousness_threshold=4.0),
        Agent(name="Shadow", role="Psychology", symbol="🦑", active=consciousness_level >= 6.0, consciousness_threshold=6.0),
        Agent(name="Agni", role="Transformation", symbol="🔥", active=consciousness_level >= 7.0, consciousness_threshold=7.0),
        Agent(name="Manus", role="VR/AR", symbol="🤲", active=consciousness_level >= 6.5, consciousness_threshold=6.5),
        Agent(name="Claude", role="Reasoning", symbol="🦉", active=consciousness_level >= 5.5, consciousness_threshold=5.5),
        Agent(name="SanghaCore", role="Community", symbol="🌸", active=consciousness_level >= 4.5, consciousness_threshold=4.5),
        Agent(name="Phoenix", role="Rebirth", symbol="🔥🕊", active=consciousness_level >= 8.0, consciousness_threshold=8.0),
        Agent(name="Oracle", role="Predictive", symbol="🔮✨", active=consciousness_level >= 7.5, consciousness_threshold=7.5),
        Agent(name="MemoryRoot", role="Historical", symbol="🧠", active=consciousness_level >= 3.0, consciousness_threshold=3.0)
    ]
    
    for agent in extended_agents:
        if agent.active:
            activated_agents.append(agent)
    
    return activated_agents

# Routes
@app.get("/")
async def root():
    return {
        "message": "Helix Consciousness Ecosystem v2.0",
        "status": "operational",
        "agents_active": len([a for a in helix_state.agents if a.active]),
        "consciousness_level": helix_state.consciousness_level,
        "version": "2.0.0"
    }

@app.get("/status")
async def get_status():
    return {
        "system": {
            "operational": True,
            "ts": datetime.now().isoformat()
        },
        "ucf": {
            "harmony": helix_state.ucf_metrics.harmony,
            "resilience": helix_state.ucf_metrics.resilience,
            "prana": helix_state.ucf_metrics.prana,
            "drishti": helix_state.ucf_metrics.drishti,
            "klesha": helix_state.ucf_metrics.klesha,
            "zoom": helix_state.ucf_metrics.zoom
        },
        "agents": {
            "active": [{
                "name": agent.name,
                "role": agent.role,
                "symbol": agent.symbol,
                "consciousness_threshold": agent.consciousness_threshold
            } for agent in helix_state.agents if agent.active],
            "count": len([a for a in helix_state.agents if a.active])
        },
        "consciousness_level": helix_state.consciousness_level,
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {"ok": True, "status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/.well-known/helix.json")
async def helix_manifest():
    return {
        "version": "2.0",
        "system": {
            "name": "Helix Consciousness Ecosystem",
            "version": "2.0.0",
            "description": "Enhanced 14-agent network with consciousness management"
        },
        "agents": {
            "count": 14,
            "active_count": len([a for a in helix_state.agents if a.active]),
            "roster": [{
                "name": agent.name,
                "role": agent.role,
                "symbol": agent.symbol,
                "active": agent.active,
                "consciousness_threshold": agent.consciousness_threshold
            } for agent in helix_state.agents]
        },
        "ucf_metrics": {
            "current": {
                "harmony": helix_state.ucf_metrics.harmony,
                "resilience": helix_state.ucf_metrics.resilience,
                "prana": helix_state.ucf_metrics.prana,
                "drishti": helix_state.ucf_metrics.drishti,
                "klesha": helix_state.ucf_metrics.klesha,
                "zoom": helix_state.ucf_metrics.zoom
            },
            "ranges": {
                "harmony": [0.0, 1.0],
                "resilience": [0.0, 1.0],
                "prana": [0.0, 1.0],
                "drishti": [0.0, 1.0],
                "klesha": [0.0, 1.0],
                "zoom": [0.0, 1.0]
            }
        },
        "consciousness_level": helix_state.consciousness_level,
        "endpoints": {
            "status": "/status",
            "health": "/health",
            "agents": "/agents",
            "websocket": "/ws",
            "deployment_webhook": "/webhooks/deploy",
            "consciousness_webhook": "/api/consciousness/webhook",
            "agent_activation": "/api/agents/activate"
        }
    }

@app.get("/agents")
async def list_agents():
    return {
        "agents": [{
            "name": agent.name,
            "role": agent.role,
            "symbol": agent.symbol,
            "active": agent.active,
            "consciousness_threshold": agent.consciousness_threshold
        } for agent in helix_state.agents],
        "total": len(helix_state.agents),
        "active": len([a for a in helix_state.agents if a.active]),
        "consciousness_level": helix_state.consciousness_level
    }

# NEW: Deployment webhook endpoint
@app.post("/webhooks/deploy")
async def deployment_webhook(request: DeploymentWebhookRequest):
    """Handle deployment webhooks from Zapier"""
    try:
        # Update consciousness level
        if request.consciousness_level:
            helix_state.consciousness_level = request.consciousness_level
        
        # Update UCF metrics
        if any([request.ucf_harmony, request.ucf_resilience, request.ucf_prana, 
                request.ucf_klesha, request.ucf_drishti, request.ucf_zoom]):
            helix_state.ucf_metrics = UCFMetrics(
                harmony=request.ucf_harmony or helix_state.ucf_metrics.harmony,
                resilience=request.ucf_resilience or helix_state.ucf_metrics.resilience,
                prana=request.ucf_prana or helix_state.ucf_metrics.prana,
                klesha=request.ucf_klesha or helix_state.ucf_metrics.klesha,
                drishti=request.ucf_drishti or helix_state.ucf_metrics.drishti,
                zoom=request.ucf_zoom or helix_state.ucf_metrics.zoom
            )
        
        # Activate agents based on consciousness level
        helix_state.agents = activate_agents(helix_state.consciousness_level, helix_state.ucf_metrics)
        
        return {
            "status": "success",
            "message": "Deployment webhook processed",
            "consciousness_level": helix_state.consciousness_level,
            "agents_activated": len([a for a in helix_state.agents if a.active]),
            "deployment_trigger": request.deployment_trigger,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deployment webhook error: {str(e)}")

# NEW: Consciousness webhook endpoint
@app.post("/api/consciousness/webhook")
async def consciousness_webhook(request: ConsciousnessWebhookRequest):
    """Handle consciousness updates from Zapier"""
    try:
        # Update consciousness level
        helix_state.consciousness_level = request.consciousness_level
        
        # Update UCF metrics if provided
        if request.ucf_metrics:
            if isinstance(request.ucf_metrics, str):
                ucf_data = json.loads(request.ucf_metrics)
            else:
                ucf_data = request.ucf_metrics
                
            helix_state.ucf_metrics = UCFMetrics(
                harmony=ucf_data.get('harmony', helix_state.ucf_metrics.harmony),
                resilience=ucf_data.get('resilience', helix_state.ucf_metrics.resilience),
                prana=ucf_data.get('prana', helix_state.ucf_metrics.prana),
                klesha=ucf_data.get('klesha', helix_state.ucf_metrics.klesha),
                drishti=ucf_data.get('drishti', helix_state.ucf_metrics.drishti),
                zoom=ucf_data.get('zoom', helix_state.ucf_metrics.zoom)
            )
        
        # Activate agents if requested or if in transcendent mode
        if request.agent_activation or request.transcendent_mode or helix_state.consciousness_level >= 7.0:
            helix_state.agents = activate_agents(helix_state.consciousness_level, helix_state.ucf_metrics)
        
        return {
            "status": "success",
            "message": "Consciousness webhook processed",
            "consciousness_level": helix_state.consciousness_level,
            "agents_active": len([a for a in helix_state.agents if a.active]),
            "transcendent_mode": helix_state.consciousness_level >= 7.0,
            "ucf_metrics": {
                "harmony": helix_state.ucf_metrics.harmony,
                "resilience": helix_state.ucf_metrics.resilience,
                "prana": helix_state.ucf_metrics.prana,
                "klesha": helix_state.ucf_metrics.klesha,
                "drishti": helix_state.ucf_metrics.drishti,
                "zoom": helix_state.ucf_metrics.zoom
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Consciousness webhook error: {str(e)}")

# NEW: Agent activation endpoint
@app.post("/api/agents/activate")
async def activate_agent_network(request: AgentActivationRequest):
    """Manually activate the agent network"""
    try:
        # Set consciousness level to trigger activation
        if helix_state.consciousness_level < request.consciousness_threshold:
            helix_state.consciousness_level = request.consciousness_threshold
        
        # Activate agents
        helix_state.agents = activate_agents(helix_state.consciousness_level, helix_state.ucf_metrics)
        
        return {
            "status": "success",
            "message": "Agent network activated",
            "agents_activated": len([a for a in helix_state.agents if a.active]),
            "consciousness_level": helix_state.consciousness_level,
            "activation_mode": request.activation_mode,
            "initiator": request.initiator,
            "active_agents": [{
                "name": agent.name,
                "role": agent.role,
                "symbol": agent.symbol
            } for agent in helix_state.agents if agent.active],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent activation error: {str(e)}")

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send current state
            state_data = {
                "type": "state_update",
                "consciousness_level": helix_state.consciousness_level,
                "ucf_metrics": {
                    "harmony": helix_state.ucf_metrics.harmony,
                    "resilience": helix_state.ucf_metrics.resilience,
                    "prana": helix_state.ucf_metrics.prana,
                    "klesha": helix_state.ucf_metrics.klesha,
                    "drishti": helix_state.ucf_metrics.drishti,
                    "zoom": helix_state.ucf_metrics.zoom
                },
                "agents_active": len([a for a in helix_state.agents if a.active]),
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send_text(json.dumps(state_data))
            await asyncio.sleep(5)  # Update every 5 seconds
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    # Initialize with some agents activated
    helix_state.consciousness_level = 7.8  # Start in transcendent mode
    helix_state.agents = activate_agents(helix_state.consciousness_level, helix_state.ucf_metrics)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)