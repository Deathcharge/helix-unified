# 🌀 Helix Collective v14.5 — Quantum Handshake
# backend/services/zapier_handler.py — Zapier Webhook Handler
# Author: Andrew John Ward (Architect)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
import json
from pathlib import Path

from backend.services.notion_client import get_notion_client

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class EventPayload(BaseModel):
    """Payload for event logging via Zapier."""
    event_title: str
    event_type: str
    agent_name: str
    description: str
    ucf_snapshot: Dict[str, Any]

class AgentStatusPayload(BaseModel):
    """Payload for agent status updates via Zapier."""
    agent_name: str
    status: str
    last_action: str
    health_score: int

class ComponentStatusPayload(BaseModel):
    """Payload for system component updates via Zapier."""
    component_name: str
    status: str
    harmony: float
    error_log: str = ""
    verified: bool = False

class ContextSnapshotPayload(BaseModel):
    """Payload for context snapshot via Zapier."""
    session_id: str
    ai_system: str
    summary: str
    key_decisions: str
    next_steps: str
    full_context: Dict[str, Any]

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(prefix="/zapier", tags=["zapier"])

# ============================================================================
# WEBHOOK ENDPOINTS
# ============================================================================

@router.post("/event")
async def webhook_log_event(payload: EventPayload):
    """
    Zapier webhook to log events to Notion.
    
    Trigger: When Manus completes a task
    Action: Create page in Event Log
    """
    try:
        notion = await get_notion_client()
        if not notion:
            raise HTTPException(status_code=503, detail="Notion client unavailable")
        
        # Log to Notion
        page_id = await notion.log_event(
            event_title=payload.event_title,
            event_type=payload.event_type,
            agent_name=payload.agent_name,
            description=payload.description,
            ucf_snapshot=payload.ucf_snapshot
        )
        
        # Also log locally for audit trail
        log_path = Path("Shadow/manus_archive/zapier_events.log")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "type": "event",
                "payload": payload.dict(),
                "notion_page_id": page_id
            }) + "\n")
        
        return {
            "status": "success",
            "message": f"Event logged: {payload.event_title}",
            "notion_page_id": page_id
        }
    except Exception as e:
        print(f"❌ Error in webhook_log_event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agent-status")
async def webhook_update_agent_status(payload: AgentStatusPayload):
    """
    Zapier webhook to update agent status in Notion.
    
    Trigger: When Manus starts/stops
    Action: Update page in Agent Registry
    """
    try:
        notion = await get_notion_client()
        if not notion:
            raise HTTPException(status_code=503, detail="Notion client unavailable")
        
        # Update in Notion
        success = await notion.update_agent_status(
            agent_name=payload.agent_name,
            status=payload.status,
            last_action=payload.last_action,
            health_score=payload.health_score
        )
        
        # Log locally
        log_path = Path("Shadow/manus_archive/zapier_events.log")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "type": "agent_status",
                "payload": payload.dict(),
                "success": success
            }) + "\n")
        
        return {
            "status": "success" if success else "failed",
            "message": f"Agent {payload.agent_name} status updated",
            "agent_name": payload.agent_name
        }
    except Exception as e:
        print(f"❌ Error in webhook_update_agent_status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/component-status")
async def webhook_update_component_status(payload: ComponentStatusPayload):
    """
    Zapier webhook to update system component status in Notion.
    
    Trigger: When component status changes
    Action: Update page in System State
    """
    try:
        notion = await get_notion_client()
        if not notion:
            raise HTTPException(status_code=503, detail="Notion client unavailable")
        
        # Update in Notion
        success = await notion.update_system_component(
            component_name=payload.component_name,
            status=payload.status,
            harmony=payload.harmony,
            error_log=payload.error_log,
            verified=payload.verified
        )
        
        # Log locally
        log_path = Path("Shadow/manus_archive/zapier_events.log")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "type": "component_status",
                "payload": payload.dict(),
                "success": success
            }) + "\n")
        
        return {
            "status": "success" if success else "failed",
            "message": f"Component {payload.component_name} status updated",
            "component_name": payload.component_name
        }
    except Exception as e:
        print(f"❌ Error in webhook_update_component_status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/context-snapshot")
async def webhook_save_context_snapshot(payload: ContextSnapshotPayload):
    """
    Zapier webhook to save context snapshot to Notion.
    
    Trigger: At end of session
    Action: Create page in Context Snapshots
    """
    try:
        notion = await get_notion_client()
        if not notion:
            raise HTTPException(status_code=503, detail="Notion client unavailable")
        
        # Save to Notion
        page_id = await notion.save_context_snapshot(
            session_id=payload.session_id,
            ai_system=payload.ai_system,
            summary=payload.summary,
            key_decisions=payload.key_decisions,
            next_steps=payload.next_steps,
            full_context=payload.full_context
        )
        
        # Log locally
        log_path = Path("Shadow/manus_archive/zapier_events.log")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "type": "context_snapshot",
                "payload": payload.dict(),
                "notion_page_id": page_id
            }) + "\n")
        
        return {
            "status": "success",
            "message": f"Context snapshot saved: {payload.session_id}",
            "notion_page_id": page_id
        }
    except Exception as e:
        print(f"❌ Error in webhook_save_context_snapshot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def zapier_health():
    """Check Zapier webhook health."""
    try:
        notion = await get_notion_client()
        if not notion:
            return {"status": "degraded", "notion": "unavailable"}
        
        health = await notion.health_check()
        return {
            "status": "healthy" if health else "degraded",
            "notion": "available" if health else "unavailable"
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# ============================================================================
# ENTRY POINT
# ============================================================================

# Include this router in main.py:
# from backend.services.zapier_handler import router as zapier_router
# app.include_router(zapier_router)

