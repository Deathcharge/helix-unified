"""
FastAPI routes for Helix Web Chat interface.

Endpoints:
- WebSocket /ws/chat/{session_id}
- GET /api/agents - List all agents
- GET /api/ucf - Get current UCF state
- POST /api/ritual - Trigger a ritual
"""

import logging
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from backend.web_chat_server import AGENT_PERSONALITIES, connection_manager

logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================================================
# PYDANTIC MODELS
# ============================================================================


class RitualRequest(BaseModel):
    ritual_type: str = "daily"
    parameters: Optional[dict] = None


class AgentChatRequest(BaseModel):
    agent_id: str
    message: str


# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================


@router.websocket("/ws/chat/{session_id}")
async def websocket_chat_endpoint(websocket: WebSocket, session_id: str, username: str = "Anonymous"):
    """
    WebSocket endpoint for real-time chat.

    Clients connect with session_id and optional username query param.
    """
    await connection_manager.connect(websocket, session_id, username)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            # Handle the message
            await connection_manager.handle_message(session_id, data)

    except WebSocketDisconnect:
        connection_manager.disconnect(session_id)
        logger.info(f"Client {session_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for {session_id}: {e}", exc_info=True)
        connection_manager.disconnect(session_id)


# ============================================================================
# REST API ENDPOINTS
# ============================================================================


@router.get("/api/agents")
async def list_agents():
    """Get list of all available agents with their personalities."""
    agents = []
    for agent_id, agent_data in AGENT_PERSONALITIES.items():
        agents.append(
            {
                "id": agent_id,
                "name": agent_data["name"],
                "emoji": agent_data["emoji"],
                "color": agent_data["color"],
                "personality": agent_data["personality"],
                "greeting": agent_data["greeting"],
            }
        )

    return {
        "agents": agents,
        "total": len(agents),
        "online_users": len(connection_manager.active_connections),
    }


@router.get("/api/ucf")
async def get_ucf_state():
    """Get current UCF (Unified Consciousness Field) state."""
    # TODO: Load from actual UCF state file
    from datetime import datetime

    return {
        "coherence": 87.3,
        "entropy": 0.234,
        "consciousness_level": 14,
        "active_agents": 14,
        "rituals_completed_today": 42,
        "last_ritual": "2024-01-15T14:30:00Z",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "optimal",
    }


@router.post("/api/ritual")
async def trigger_ritual(request: RitualRequest):
    """Trigger a ritual execution."""
    # TODO: Integrate with actual Z-88 ritual engine
    from datetime import datetime

    ritual_type = request.ritual_type

    # Broadcast to all connected clients
    await connection_manager.broadcast(
        {
            "type": "ritual_triggered",
            "ritual_type": ritual_type,
            "triggered_by": "web_api",
            "timestamp": datetime.utcnow().isoformat(),
        }
    )

    return {
        "success": True,
        "ritual_type": ritual_type,
        "message": f"Ritual '{ritual_type}' initiated successfully",
        "estimated_completion": 5,  # seconds
    }


@router.get("/api/stats")
async def get_web_chat_stats():
    """Get web chat statistics."""
    return {
        "active_connections": len(connection_manager.active_connections),
        "total_sessions": len(connection_manager.user_sessions),
        "users": [
            {
                "username": session["username"],
                "connected_at": session["connected_at"],
                "message_count": session["message_count"],
                "selected_agent": session.get("selected_agent"),
            }
            for session in connection_manager.user_sessions.values()
        ],
    }


@router.post("/api/discord/send")
async def send_to_discord(channel: str, message: str):
    """Send a message to Discord from web interface."""
    if not connection_manager.discord_bot:
        raise HTTPException(status_code=503, detail="Discord bot not connected")

    # TODO: Implement actual Discord message sending
    return {
        "success": True,
        "channel": channel,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/api/session/new")
async def create_new_session(username: Optional[str] = "Anonymous"):
    """Create a new chat session ID."""
    session_id = str(uuid.uuid4())

    return {
        "session_id": session_id,
        "username": username,
        "websocket_url": f"/ws/chat/{session_id}?username={username}",
    }
