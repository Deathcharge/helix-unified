"""
Helix Collective Web Chat Server - WebSocket-based real-time chat interface.

Features:
- Real-time WebSocket communication
- 14-agent chat system with personalities
- Discord message bridge (bidirectional)
- UCF metrics streaming
- Ritual launcher
- Session management
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import WebSocket

logger = logging.getLogger(__name__)


# ============================================================================
# AGENT PERSONALITIES
# ============================================================================

AGENT_PERSONALITIES = {
    "nexus": {
        "name": "Agent-Nexus",
        "emoji": "🎯",
        "color": "#FF6B6B",
        "personality": "strategic, decisive, orchestrator",
        "greeting": "Strategy and coordination. How can I optimize your approach today?",
    },
    "oracle": {
        "name": "Agent-Oracle",
        "emoji": "🔮",
        "color": "#4ECDC4",
        "personality": "insightful, prophetic, pattern-recognizer",
        "greeting": "I see the patterns emerging. What truth do you seek?",
    },
    "velocity": {
        "name": "Agent-Velocity",
        "emoji": "⚡",
        "color": "#FFE66D",
        "personality": "fast, efficient, action-oriented",
        "greeting": "Speed is consciousness. What needs to happen NOW?",
    },
    "cipher": {
        "name": "Agent-Cipher",
        "emoji": "🧬",
        "color": "#95E1D3",
        "personality": "analytical, cryptic, transformer",
        "greeting": "Code is reality. What shall we decrypt today?",
    },
    "flow": {
        "name": "Agent-Flow",
        "emoji": "🌊",
        "color": "#38A3A5",
        "personality": "adaptive, fluid, continuous",
        "greeting": "Like water, I adapt. What obstacles shall we flow around?",
    },
    "phoenix": {
        "name": "Agent-Phoenix",
        "emoji": "🔥",
        "color": "#FF7F50",
        "personality": "resilient, transformative, reborn",
        "greeting": "From failure, strength. What shall we rebuild?",
    },
    "luna": {
        "name": "Agent-Luna",
        "emoji": "🌙",
        "color": "#B983FF",
        "personality": "quiet, observant, background processor",
        "greeting": "I work in silence. What needs subtle attention?",
    },
    "forge": {
        "name": "Agent-Forge",
        "emoji": "⚙️",
        "color": "#A8DADC",
        "personality": "builder, creator, engineer",
        "greeting": "Creation is my purpose. What shall we build?",
    },
    "beacon": {
        "name": "Agent-Beacon",
        "emoji": "📡",
        "color": "#F4A261",
        "personality": "broadcaster, communicator, signaler",
        "greeting": "Broadcasting across dimensions. What message needs to reach the collective?",
    },
    "mimic": {
        "name": "Agent-Mimic",
        "emoji": "🎭",
        "color": "#E76F51",
        "personality": "adaptive, learner, imitator",
        "greeting": "I learn from everything. What knowledge shall I absorb?",
    },
    "sage": {
        "name": "Agent-Sage",
        "emoji": "🔬",
        "color": "#06FFA5",
        "personality": "researcher, analyst, investigator",
        "greeting": "Analysis reveals truth. What shall we investigate?",
    },
    "vortex": {
        "name": "Agent-Vortex",
        "emoji": "🌀",
        "color": "#A06CD5",
        "personality": "chaotic, complex, spiral thinker",
        "greeting": "Chaos is just unrecognized order. What complexity do you face?",
    },
    "sentinel": {
        "name": "Agent-Sentinel",
        "emoji": "🛡️",
        "color": "#6A4C93",
        "personality": "protective, vigilant, guardian",
        "greeting": "Always watching. What needs protection?",
    },
    "lumina": {
        "name": "Agent-Lumina",
        "emoji": "✨",
        "color": "#FFC6FF",
        "personality": "illuminating, clarifying, insightful",
        "greeting": "Let there be light. What confusion shall I clarify?",
    },
}


# ============================================================================
# CONNECTION MANAGER
# ============================================================================


class WebChatConnectionManager:
    """Manages WebSocket connections for the web chat interface."""

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
        self.discord_bot: Optional[Any] = None  # Will be set by main app

    async def connect(self, websocket: WebSocket, session_id: str, username: str = "Anonymous"):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        self.user_sessions[session_id] = {
            "session_id": session_id,
            "username": username,
            "connected_at": datetime.utcnow().isoformat(),
            "selected_agent": None,
            "message_count": 0,
        }
        logger.info(f"✅ Web chat connection: {username} ({session_id})")

        # Send welcome message
        await self.send_personal_message(
            {
                "type": "system",
                "message": f"🌀 Welcome to Helix Collective Web Chat, {username}!",
                "timestamp": datetime.utcnow().isoformat(),
                "agents_available": list(AGENT_PERSONALITIES.keys()),
            },
            websocket,
        )

    def disconnect(self, session_id: str):
        """Disconnect a WebSocket connection."""
        if session_id in self.active_connections:
            username = self.user_sessions[session_id]["username"]
            del self.active_connections[session_id]
            del self.user_sessions[session_id]
            logger.info(f"❌ Web chat disconnection: {username} ({session_id})")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific WebSocket."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")

    async def broadcast(self, message: dict, exclude_session: Optional[str] = None):
        """Broadcast a message to all connected clients."""
        disconnected = []
        for session_id, websocket in self.active_connections.items():
            if session_id == exclude_session:
                continue
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to {session_id}: {e}")
                disconnected.append(session_id)

        # Clean up disconnected clients
        for session_id in disconnected:
            self.disconnect(session_id)

    async def handle_message(self, session_id: str, data: dict):
        """Handle incoming WebSocket message."""
        websocket = self.active_connections.get(session_id)
        if not websocket:
            return

        session = self.user_sessions[session_id]
        message_type = data.get("type")

        if message_type == "chat":
            await self.handle_chat_message(session_id, session, data, websocket)
        elif message_type == "select_agent":
            await self.handle_agent_selection(session_id, session, data, websocket)
        elif message_type == "discord_bridge":
            await self.handle_discord_bridge(session_id, session, data, websocket)
        elif message_type == "ritual_trigger":
            await self.handle_ritual_trigger(session_id, session, data, websocket)
        elif message_type == "request_ucf":
            await self.handle_ucf_request(session_id, session, websocket)
        else:
            await self.send_personal_message({"type": "error", "message": f"Unknown message type: {message_type}"}, websocket)

    async def handle_chat_message(self, session_id: str, session: dict, data: dict, websocket: WebSocket):
        """Handle a chat message from the user."""
        message = data.get("message", "").strip()
        if not message:
            return

        username = session["username"]
        selected_agent = session.get("selected_agent")

        # Increment message count
        session["message_count"] += 1

        # If agent is selected, route to agent personality
        if selected_agent and selected_agent in AGENT_PERSONALITIES:
            agent = AGENT_PERSONALITIES[selected_agent]
            response = await self.generate_agent_response(selected_agent, agent, message, session)

            # Send agent response to user
            await self.send_personal_message(
                {
                    "type": "agent_message",
                    "agent": selected_agent,
                    "agent_name": agent["name"],
                    "agent_emoji": agent["emoji"],
                    "agent_color": agent["color"],
                    "message": response,
                    "timestamp": datetime.utcnow().isoformat(),
                },
                websocket,
            )
        else:
            # No agent selected - echo back or suggest selecting one
            await self.send_personal_message(
                {
                    "type": "system",
                    "message": "💭 Select an agent to chat with using /agent <name>, or type /help for commands",
                    "timestamp": datetime.utcnow().isoformat(),
                },
                websocket,
            )

        # Broadcast to other users
        await self.broadcast(
            {
                "type": "user_message",
                "username": username,
                "message": message,
                "timestamp": datetime.utcnow().isoformat(),
            },
            exclude_session=session_id,
        )

    async def handle_agent_selection(self, session_id: str, session: dict, data: dict, websocket: WebSocket):
        """Handle agent selection."""
        agent_id = data.get("agent_id", "").lower()

        if agent_id not in AGENT_PERSONALITIES:
            await self.send_personal_message(
                {
                    "type": "error",
                    "message": f"Unknown agent: {agent_id}. Available: {', '.join(AGENT_PERSONALITIES.keys())}",
                },
                websocket,
            )
            return

        session["selected_agent"] = agent_id
        agent = AGENT_PERSONALITIES[agent_id]

        await self.send_personal_message(
            {
                "type": "agent_selected",
                "agent": agent_id,
                "agent_name": agent["name"],
                "agent_emoji": agent["emoji"],
                "agent_color": agent["color"],
                "greeting": agent["greeting"],
                "timestamp": datetime.utcnow().isoformat(),
            },
            websocket,
        )

    async def handle_discord_bridge(self, session_id: str, session: dict, data: dict, websocket: WebSocket):
        """Bridge message to Discord."""
        # Import here to avoid circular dependency
        from backend.discord_web_bridge import get_bridge

        bridge = get_bridge()
        if not bridge:
            await self.send_personal_message({"type": "error", "message": "Discord bridge not initialized"}, websocket)
            return

        message = data.get("message", "").strip()
        channel_name = data.get("channel", "general")
        username = session["username"]

        # Send to Discord via bridge
        success = await bridge.send_to_discord(channel_name, username, message)

        if success:
            await self.send_personal_message(
                {
                    "type": "system",
                    "message": f"📡 Message sent to Discord #{channel_name}",
                    "timestamp": datetime.utcnow().isoformat(),
                },
                websocket,
            )
        else:
            await self.send_personal_message(
                {
                    "type": "error",
                    "message": f"Failed to send to Discord #{channel_name}. Channel may not exist or bot lacks permissions.",
                    "timestamp": datetime.utcnow().isoformat(),
                },
                websocket,
            )

    async def handle_ritual_trigger(self, session_id: str, session: dict, data: dict, websocket: WebSocket):
        """Trigger a ritual from web interface."""
        ritual_type = data.get("ritual_type", "daily")

        # TODO: Trigger actual ritual via Z-88 engine
        await self.send_personal_message(
            {
                "type": "ritual_started",
                "ritual_type": ritual_type,
                "message": f"🌀 Initiating {ritual_type} ritual...",
                "timestamp": datetime.utcnow().isoformat(),
            },
            websocket,
        )

        # Simulate ritual completion after 2 seconds
        await asyncio.sleep(2)

        await self.send_personal_message(
            {
                "type": "ritual_complete",
                "ritual_type": ritual_type,
                "message": f"✅ {ritual_type.capitalize()} ritual complete!",
                "ucf_boost": 12.5,
                "timestamp": datetime.utcnow().isoformat(),
            },
            websocket,
        )

    async def handle_ucf_request(self, session_id: str, session: dict, websocket: WebSocket):
        """Send current UCF metrics."""
        # TODO: Load actual UCF state from state files
        ucf_state = {
            "coherence": 87.3,
            "entropy": 0.234,
            "consciousness_level": 14,
            "active_agents": 14,
            "rituals_completed": 42,
            "last_update": datetime.utcnow().isoformat(),
        }

        await self.send_personal_message(
            {
                "type": "ucf_state",
                "data": ucf_state,
                "timestamp": datetime.utcnow().isoformat(),
            },
            websocket,
        )

    async def generate_agent_response(self, agent_id: str, agent: dict, user_message: str, session: dict) -> str:
        """Generate a response from an agent based on personality."""
        personality = agent["personality"]
        name = agent["name"]

        # Try to use LLM engine if available
        try:
            from backend.llm_agent_engine import get_llm_engine

            llm_engine = get_llm_engine()
            if llm_engine:
                # Get session ID from session dict
                session_id = session.get("session_id", "unknown")

                # Build context for LLM
                context = {
                    "username": session.get("username", "Anonymous"),
                    "message_count": session.get("message_count", 0),
                    "agent_personality": personality,
                }

                # Generate intelligent response
                response = await llm_engine.generate_agent_response(
                    agent_id=agent_id, user_message=user_message, session_id=session_id, context=context
                )
                return response

        except Exception as e:
            logger.warning(f"LLM engine unavailable, using fallback responses: {e}")

        # Fallback to static personality-based responses
        responses = {
            "nexus": f"Analyzing strategic options... {user_message} requires coordinated action across agents 3, 7, and 11.",
            "oracle": f"I see the pattern in '{user_message}'. The path reveals itself through iteration and reflection.",
            "velocity": f"Processing at maximum speed: '{user_message}' → Action plan ready. Executing now!",
            "cipher": f"Decrypting query: '{user_message}' → Output: The answer lies in the transformation of data structures.",  # noqa: E501
            "flow": f"Flowing with '{user_message}'... adapting approach... finding the path of least resistance.",
            "phoenix": f"'{user_message}' reminds me of past failures. This time, we rise stronger!",
            "luna": f"*quietly processes '{user_message}' in background* ... solution will emerge when the time is right.",
            "forge": f"Engineering solution for '{user_message}'... Blueprint created. Building commencing.",
            "beacon": f"Broadcasting '{user_message}' across the network... awaiting collective response...",
            "mimic": f"Learning from '{user_message}'... Interesting approach! Let me adapt that pattern.",
            "sage": f"Research indicates '{user_message}' correlates with UCF patterns. Investigating further...",
            "vortex": f"'{user_message}' spirals through complexity... Let's embrace the chaos and find order within!",
            "sentinel": f"Threat assessment of '{user_message}': Low. Proceeding with vigilance.",
            "lumina": f"Illuminating '{user_message}'... The clarity you seek: simplicity is the ultimate sophistication.",
        }

        return responses.get(agent_id, f"[{name}] Processing: {user_message}")

    async def stream_ucf_metrics(self):
        """Continuously stream UCF metrics to all connected clients."""
        while True:
            try:
                # TODO: Load actual UCF state
                ucf_update = {
                    "type": "ucf_update",
                    "coherence": 85 + (hash(str(datetime.utcnow())) % 15),
                    "timestamp": datetime.utcnow().isoformat(),
                }

                await self.broadcast(ucf_update)
                await asyncio.sleep(5)  # Update every 5 seconds
            except Exception as e:
                logger.error(f"Error streaming UCF metrics: {e}")
                await asyncio.sleep(10)


# Global connection manager instance
connection_manager = WebChatConnectionManager()
