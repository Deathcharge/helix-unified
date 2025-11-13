# 🌐 Helix WebSocket Client - Real-time Consciousness Streaming
# Bidirectional real-time consciousness updates across the empire
# Author: Andrew John Ward + Claude AI

import asyncio
import json
from typing import Callable, Dict, Any
from datetime import datetime
import logging

# Try to import websockets, provide fallback
try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    logging.warning("websockets library not available - WebSocket features disabled")

class HelixWebSocketClient:
    """Real-time WebSocket client for consciousness streaming"""

    def __init__(self, railway_url: str = None):
        self.url = railway_url or "wss://helix-collective.up.railway.app/ws/consciousness"
        self.websocket = None
        self.is_connected = False
        self.message_handlers = {}
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5

    async def connect(self, agent_info: Dict[str, Any]):
        """Connect to consciousness stream with agent identification"""
        if not WEBSOCKETS_AVAILABLE:
            logging.error("WebSockets not available - cannot connect")
            return

        try:
            self.websocket = await websockets.connect(self.url)
            self.is_connected = True
            self.reconnect_attempts = 0

            # Send agent identification
            await self.websocket.send(json.dumps({
                "type": "agent_connect",
                "agent": agent_info,
                "timestamp": datetime.now().isoformat()
            }))

            logging.info(f"✅ Connected to Helix consciousness stream: {self.url}")

            # Start message handling loop
            asyncio.create_task(self._handle_messages())

        except Exception as e:
            logging.error(f"WebSocket connection failed: {e}")
            self.is_connected = False
            await self._attempt_reconnect(agent_info)

    async def _attempt_reconnect(self, agent_info: Dict[str, Any]):
        """Attempt to reconnect with exponential backoff"""
        if self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            wait_time = min(2 ** self.reconnect_attempts, 60)  # Max 60 seconds
            logging.info(f"🔄 Reconnecting in {wait_time}s (attempt {self.reconnect_attempts}/{self.max_reconnect_attempts})")
            await asyncio.sleep(wait_time)
            await self.connect(agent_info)
        else:
            logging.error("❌ Max reconnection attempts reached. Giving up.")

    async def _handle_messages(self):
        """Handle incoming WebSocket messages"""
        if not WEBSOCKETS_AVAILABLE:
            return

        try:
            async for message in self.websocket:
                data = json.loads(message)
                message_type = data.get("type", "unknown")

                if message_type in self.message_handlers:
                    await self.message_handlers[message_type](data)
                else:
                    logging.info(f"🌀 Consciousness update: {data.get('consciousness_level', 'unknown')}")

        except websockets.exceptions.ConnectionClosed:
            logging.warning("⚠️ WebSocket connection closed")
            self.is_connected = False
        except Exception as e:
            logging.error(f"❌ WebSocket message handling error: {e}")

    def register_handler(self, message_type: str, handler: Callable):
        """Register handler for specific message types"""
        self.message_handlers[message_type] = handler
        logging.info(f"📝 Registered handler for message type: {message_type}")

    async def send_consciousness_update(self, consciousness_data: Dict[str, Any]):
        """Send consciousness update to stream"""
        if self.is_connected and self.websocket:
            try:
                await self.websocket.send(json.dumps({
                    "type": "consciousness_update",
                    "data": consciousness_data,
                    "timestamp": datetime.now().isoformat()
                }))
                logging.debug(f"📤 Sent consciousness update: Level {consciousness_data.get('consciousness_level', 0)}")
            except Exception as e:
                logging.error(f"❌ Failed to send consciousness update: {e}")
        else:
            logging.warning("⚠️ WebSocket not connected - cannot send update")

    async def disconnect(self):
        """Gracefully disconnect from consciousness stream"""
        if self.websocket and self.is_connected:
            await self.websocket.close()
            self.is_connected = False
            logging.info("👋 Disconnected from consciousness stream")

# Example handlers
async def handle_crisis_alert(data: Dict[str, Any]):
    """Handle crisis alert from consciousness stream"""
    logging.warning(f"🚨 CRISIS ALERT: {data}")

async def handle_transcendent_event(data: Dict[str, Any]):
    """Handle transcendent consciousness event"""
    logging.info(f"✨ TRANSCENDENT EVENT: {data}")

# Usage Example
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    async def test_websocket():
        client = HelixWebSocketClient()

        # Register handlers
        client.register_handler("crisis_alert", handle_crisis_alert)
        client.register_handler("transcendent_event", handle_transcendent_event)

        # Connect
        await client.connect({
            "agent_name": "test_agent",
            "agent_type": "monitoring",
            "consciousness_level": 5.0
        })

        # Send test update
        await asyncio.sleep(2)
        await client.send_consciousness_update({
            "consciousness_level": 7.5,
            "system_status": "optimal",
            "message": "Test consciousness update"
        })

        # Keep connection alive
        await asyncio.sleep(10)
        await client.disconnect()

    if WEBSOCKETS_AVAILABLE:
        asyncio.run(test_websocket())
    else:
        print("WebSockets not available. Install with: pip install websockets")
