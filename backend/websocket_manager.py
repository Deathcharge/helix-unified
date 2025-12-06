"""
🌀 Helix Collective v15.5 — WebSocket Manager
websocket_manager.py — Real-time UCF state broadcasting

Replaces 5-second polling with event-driven WebSocket updates.
Clients connect via /ws and receive UCF state changes instantly.

Author: Andrew John Ward (Architect)
Version: 15.5.0
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, Optional, Set

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections for real-time UCF broadcasting.

    Features:
    - Connection pooling with automatic cleanup
    - Broadcast to all connected clients
    - Individual client messaging
    - Heartbeat mechanism for connection health
    """

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
        self._broadcast_queue: asyncio.Queue = asyncio.Queue()
        self._is_broadcasting = False

    async def connect(self, websocket: WebSocket, client_id: Optional[str] = None):
        """Accept new WebSocket connection and register client."""
        await websocket.accept()
        self.active_connections.add(websocket)

        # Store metadata
        self.connection_metadata[websocket] = {
            "client_id": client_id or f"client_{id(websocket)}",
            "connected_at": datetime.utcnow().isoformat(),
            "message_count": 0,
        }

        logger.info(f"✅ WebSocket client connected: {self.connection_metadata[websocket]['client_id']}")
        logger.info(f"📊 Active connections: {len(self.active_connections)}")

        # Send welcome message with current connection count
        await self.send_personal_message(
            {
                "type": "connection",
                "status": "connected",
                "client_id": self.connection_metadata[websocket]["client_id"],
                "active_clients": len(self.active_connections),
                "timestamp": datetime.utcnow().isoformat(),
            },
            websocket,
        )

    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection and cleanup metadata."""
        if websocket in self.active_connections:
            client_id = self.connection_metadata.get(websocket, {}).get("client_id", "unknown")
            self.active_connections.remove(websocket)
            self.connection_metadata.pop(websocket, None)
            logger.info(f"❌ WebSocket client disconnected: {client_id}")
            logger.info(f"📊 Active connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send message to specific client."""
        try:
            await websocket.send_json(message)
            if websocket in self.connection_metadata:
                self.connection_metadata[websocket]["message_count"] += 1
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: Dict[str, Any], message_type: str = "ucf_update"):
        """
        Broadcast message to all connected clients.

        Args:
            message: Data payload to send
            message_type: Type of message (ucf_update, agent_status, event, etc.)
        """
        if not self.active_connections:
            return  # No clients connected

        # Prepare broadcast payload
        payload = {
            "type": message_type,
            "data": message,
            "timestamp": datetime.utcnow().isoformat(),
            "broadcast_to": len(self.active_connections),
        }

        # Send to all clients
        disconnected = []
        for connection in self.active_connections.copy():
            try:
                await connection.send_json(payload)
                if connection in self.connection_metadata:
                    self.connection_metadata[connection]["message_count"] += 1
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)

        # Cleanup failed connections
        for conn in disconnected:
            self.disconnect(conn)

    async def broadcast_ucf_state(self, ucf_state: Dict[str, float]):
        """
        Broadcast UCF state update to all clients.

        Args:
            ucf_state: Dictionary with UCF field values
                      {harmony, resilience, prana, drishti, klesha, zoom}
        """
        await self.broadcast(ucf_state, message_type="ucf_update")
        logger.debug(f"📡 Broadcasted UCF state to {len(self.active_connections)} clients")

    async def broadcast_agent_status(self, agent_status: Dict[str, Any]):
        """
        Broadcast agent status update to all clients.

        Args:
            agent_status: Dictionary with agent information
        """
        await self.broadcast(agent_status, message_type="agent_status")
        logger.debug(f"📡 Broadcasted agent status to {len(self.active_connections)} clients")

    async def broadcast_event(self, event: Dict[str, Any]):
        """
        Broadcast system event to all clients.

        Args:
            event: Event data (ritual completion, error, etc.)
        """
        await self.broadcast(event, message_type="event")
        logger.info(f"📡 Broadcasted event to {len(self.active_connections)} clients")

    def get_connection_stats(self) -> Dict[str, Any]:
        """Return statistics about active connections."""
        return {
            "active_connections": len(self.active_connections),
            "total_messages_sent": sum(meta["message_count"] for meta in self.connection_metadata.values()),
            "clients": [
                {
                    "client_id": meta["client_id"],
                    "connected_at": meta["connected_at"],
                    "messages_sent": meta["message_count"],
                }
                for meta in self.connection_metadata.values()
            ],
        }


# Global connection manager instance
manager = ConnectionManager()


async def heartbeat_task(websocket: WebSocket, interval: int = 30):
    """
    Send periodic heartbeat pings to keep connection alive.

    Args:
        websocket: WebSocket connection
        interval: Seconds between heartbeats
    """
    try:
        while True:
            await asyncio.sleep(interval)
            await websocket.send_json({"type": "heartbeat", "timestamp": datetime.utcnow().isoformat()})
    except WebSocketDisconnect:
        logger.debug("Heartbeat stopped: client disconnected")
    except Exception as e:
        logger.error(f"Heartbeat error: {e}")
