"""
Agent Orchestration API Routes
"""

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.agent_orchestrator import Z88Stage, get_orchestrator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/agents", tags=["agents"])


class HandshakeRequest(BaseModel):
    session_id: Optional[str] = None
    context: Dict[str, Any] = {}


class Z88Request(BaseModel):
    stage: str
    context: Dict[str, Any] = {}


class MCPToolRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any] = {}


@router.get("/status")
async def get_agent_status():
    """Get current status of all agents"""
    try:
        orchestrator = get_orchestrator()
        return orchestrator.get_agent_status()
    except Exception as e:
        logger.error(f"Failed to get agent status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/handshake")
async def execute_handshake(request: HandshakeRequest):
    """Execute Quantum Handshake protocol"""
    try:
        orchestrator = get_orchestrator()
        result = await orchestrator.quantum_handshake(request.context)
        return result
    except Exception as e:
        logger.error(f"Handshake failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/z88")
async def execute_z88_stage(request: Z88Request):
    """Execute Z-88 Ritual Engine stage"""
    try:
        stage = Z88Stage(request.stage)
        orchestrator = get_orchestrator()
        result = await orchestrator.execute_z88_stage(stage, request.context)
        return result
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid Z-88 stage: {request.stage}")
    except Exception as e:
        logger.error(f"Z-88 stage failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mcp/tool")
async def call_mcp_tool(request: MCPToolRequest):
    """Route MCP tool call"""
    try:
        orchestrator = get_orchestrator()
        result = await orchestrator.route_mcp_tool(request.tool_name, request.arguments)
        return result
    except Exception as e:
        logger.error(f"MCP tool call failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}")
async def get_agent_details(agent_id: str):
    """Get details for a specific agent"""
    try:
        orchestrator = get_orchestrator()
        agent = orchestrator.agents.get(agent_id)

        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent not found: {agent_id}")

        return {
            "id": agent.id,
            "emoji": agent.emoji,
            "archetype": agent.archetype,
            "tier": agent.tier.value,
            "roles": agent.primary_roles,
            "active": agent.active,
            "last_activation": agent.last_activation.isoformat() if agent.last_activation else None,
            "execution_count": agent.execution_count,
            "discord_channels": agent.get_discord_channels(),
            "mcp_tools": agent.get_mcp_tools(),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent details: {e}")
        raise HTTPException(status_code=500, detail=str(e))
