#!/usr/bin/env python3
"""
Enhanced Telemetry Emitter for Helix v16.6
Wraps the v16.5 ZapierClient for convenient one-line telemetry
"""
import asyncio
import aiohttp
import os
from backend.zapier_client import ZapierClient

class EnhancedEmitter:
    """Simplified wrapper for common telemetry patterns"""

    def __init__(self):
        self.session = None
        self.client = None

    async def initialize(self):
        """Initialize async HTTP session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            self.client = ZapierClient(self.session)

    async def emit_event(self, title: str, event_type: str, agent: str, description: str):
        """Quick event emission"""
        await self.initialize()
        return await self.client.log_event(title, event_type, agent, description)

    async def emit_telemetry(self, metric: str, value: float, component: str = "System"):
        """Quick telemetry emission"""
        await self.initialize()
        return await self.client.log_telemetry(metric, value, component)

    async def emit_heartbeat(self, agent: str, status: str, health: int):
        """Quick heartbeat emission"""
        await self.initialize()
        return await self.client.update_agent(agent, status, "Heartbeat", health)

    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

# Global emitter instance
_emitter = EnhancedEmitter()

# Convenience functions
async def quick_event(title: str, agent: str = "System", desc: str = ""):
    """Fire and forget event logging"""
    await _emitter.emit_event(title, "Status", agent, desc)

async def quick_metric(name: str, value: float, component: str = "System"):
    """Fire and forget metric logging"""
    await _emitter.emit_telemetry(name, value, component)

async def quick_heartbeat(agent: str, health: int = 100):
    """Fire and forget heartbeat"""
    await _emitter.emit_heartbeat(agent, "Active", health)
