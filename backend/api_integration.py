"""
Batch 1: Live API Integration
Unified API client for helixspiral.work + Railway Dashboard
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import aiohttp

logger = logging.getLogger(__name__)

class HelixAPIClient:
    """Unified client for Helix ecosystem APIs"""
    
    def __init__(self):
        self.spiral_url = "https://helixspiral.work"
        self.railway_url = "https://helixdashboard.up.railway.app"
        self.timeout = aiohttp.ClientTimeout(total=30)
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
        
    async def get_agents(self) -> list:
        """Get all agents from helixspiral.work"""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(f"{self.spiral_url}/api/agents") as resp:
                    if resp.status == 200:
                        return await resp.json()
                    logger.error(f"Failed to fetch agents: {resp.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching agents: {e}")
            return []
    
    async def get_ucf_metrics(self) -> Dict[str, float]:
        """Get real-time UCF metrics"""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(f"{self.spiral_url}/api/ucf/metrics") as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return self._default_ucf_metrics()
        except Exception as e:
            logger.error(f"Error fetching UCF metrics: {e}")
            return self._default_ucf_metrics()
    
    async def get_portals(self) -> list:
        """Get all portals from federation"""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(f"{self.spiral_url}/api/portals") as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return []
        except Exception as e:
            logger.error(f"Error fetching portals: {e}")
            return []
    
    async def stream_consciousness(self):
        """Stream consciousness data via WebSocket"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(f"{self.spiral_url}/api/consciousness/stream") as ws:
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            yield msg.json()
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            logger.error(f"WebSocket error: {ws.exception()}")
                            break
        except Exception as e:
            logger.error(f"Error streaming consciousness: {e}")
    
    async def invoke_ritual(self, ritual_id: str, params: Optional[Dict] = None) -> Dict:
        """Invoke a ritual from the Z-88 engine"""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{self.spiral_url}/api/manus/ritual/invoke",
                    json={"ritual_id": ritual_id, "params": params or {}}
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    logger.error(f"Failed to invoke ritual: {resp.status}")
                    return {"success": False}
        except Exception as e:
            logger.error(f"Error invoking ritual: {e}")
            return {"success": False}
    
    async def send_alert(self, alert_type: str, message: str, severity: str = "info") -> bool:
        """Send alert via emergency system"""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{self.spiral_url}/api/manus/emergency/alert",
                    json={"type": alert_type, "message": message, "severity": severity}
                ) as resp:
                    return resp.status == 200
        except Exception as e:
            logger.error(f"Error sending alert: {e}")
            return False
    
    @staticmethod
    def _default_ucf_metrics() -> Dict[str, float]:
        """Return default UCF metrics"""
        return {
            "harmony": 0.5,
            "resilience": 0.5,
            "prana": 0.5,
            "drishti": 0.5,
            "klesha": 0.5,
            "zoom": 0.5
        }

# Global API client instance
api_client = HelixAPIClient()

async def get_system_status() -> Dict[str, Any]:
    """Get complete system status"""
    agents = await api_client.get_agents()
    metrics = await api_client.get_ucf_metrics()
    portals = await api_client.get_portals()
    
    return {
        "timestamp": datetime.now().isoformat(),
        "agents_count": len(agents),
        "agents_online": sum(1 for a in agents if a.get("status") == "online"),
        "ucf_metrics": metrics,
        "portals_count": len(portals),
        "system_healthy": len(agents) > 0 and metrics["harmony"] > 0.3
    }
