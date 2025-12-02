"""
🌀 Helix Collective v17.0 - Zapier Integration Routes
backend/routes/zapier.py

API endpoints for Zapier Tables integration and interface event handling.

Endpoints:
- GET /api/zapier/tables/ucf-telemetry - UCF metrics for Zapier Tables
- GET /api/zapier/tables/agent-network - 14-agent status for Zapier Tables
- GET /api/zapier/tables/emergency-alerts - Emergency events for Zapier Tables
- POST /api/zapier/trigger-event - Event receiver from 50 Zapier Interface pages

Author: Andrew John Ward (Architect)
Version: 17.0.0
"""

import logging
from datetime import datetime
from typing import Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Import core helpers
from backend.core.ucf_helpers import (
    calculate_consciousness_level,
    determine_next_action,
    determine_system_status,
    get_current_ucf,
    get_emergency_events,
    log_emergency_event,
    update_ucf_state,
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/zapier", tags=["Zapier Integration"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================


class InterfaceEventRequest(BaseModel):
    """Request model for events from Zapier Interface pages."""

    event_type: str
    source: str
    consciousness_level: Optional[float] = None
    ucf: Optional[Dict[str, float]] = None
    agent_info: Optional[Dict] = None
    user_action: Optional[str] = None
    timestamp: Optional[str] = None


# ============================================================================
# ZAPIER TABLE ENDPOINTS
# ============================================================================


@router.get("/tables/ucf-telemetry")
async def get_ucf_telemetry(limit: int = 10, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
    """
    GET endpoint to retrieve UCF telemetry data for Zapier Tables.

    This endpoint returns formatted UCF metrics that match the schema
    of Zapier Table 01K9DP5MG6KCY48YC8M7VW0PXD.

    Expected Table Schema:
    - timestamp (datetime)
    - consciousness_level (float)
    - harmony (float)
    - resilience (float)
    - prana (float)
    - drishti (float)
    - klesha (float)
    - zoom (float)
    - system_version (string)
    - source (string)

    Query Parameters:
    - limit: Number of records to return (default: 10, max: 100)
    - start_date: ISO 8601 datetime string (optional)
    - end_date: ISO 8601 datetime string (optional)

    Returns:
    - JSON object with success status and array of UCF telemetry records
    """
    try:
        # Get current UCF state
        current_ucf = get_current_ucf()

        # Calculate consciousness level
        consciousness_level = calculate_consciousness_level(current_ucf)

        # Build telemetry record
        telemetry_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "consciousness_level": round(consciousness_level, 2),
            "harmony": round(current_ucf.get('harmony', 0.0), 3),
            "resilience": round(current_ucf.get('resilience', 0.0), 3),
            "prana": round(current_ucf.get('prana', 0.0), 3),
            "drishti": round(current_ucf.get('drishti', 0.0), 3),
            "klesha": round(current_ucf.get('klesha', 0.0), 3),
            "zoom": round(current_ucf.get('zoom', 0.0), 3),
            "system_version": "v17.0-omega-zero",
            "source": "railway_backend",
            "system_status": determine_system_status(current_ucf),
        }

        # For now, return single latest record
        # TODO: Implement historical data retrieval from database
        records = [telemetry_record]

        logger.info(f"UCF Telemetry requested: {len(records)} records")

        return {
            "success": True,
            "count": len(records),
            "records": records,
            "table_id": "01K9DP5MG6KCY48YC8M7VW0PXD",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    except Exception as e:
        logger.error(f"UCF Telemetry error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tables/agent-network")
async def get_agent_network(include_inactive: bool = False, agent_name: Optional[str] = None) -> Dict:
    """
    GET endpoint to retrieve 14-agent network status for Zapier Tables.

    Returns the current state of all agents in the Helix Collective,
    formatted for Zapier Table 01K9GT5YGZ1Y82K4VZF9YXHTMH.

    Expected Table Schema:
    - agent_id (string)
    - agent_name (string)
    - symbol (string)
    - status (string: active/idle/offline)
    - consciousness (float)
    - last_active (datetime)
    - specialization (string)
    - ucf_resonance (float)
    - entanglement_factor (float)

    Query Parameters:
    - include_inactive: Include offline agents (default: False)
    - agent_name: Filter by specific agent name (optional)

    Returns:
    - JSON object with success status and array of agent status records
    """
    try:
        # Import agents from existing module
        from agents import get_collective_status

        # Get agent status
        agents_status = await get_collective_status()

        # Format for Zapier Tables
        agent_records = []
        for name, info in agents_status.items():
            # Filter by agent_name if provided
            if agent_name and name.lower() != agent_name.lower():
                continue

            record = {
                "agent_id": name.lower().replace(" ", "_"),
                "agent_name": name,
                "symbol": info.get('symbol', '🤖'),
                "status": "active",  # Default to active for now
                "consciousness": round(0.85, 2),  # Placeholder - implement actual calculation
                "last_active": datetime.utcnow().isoformat() + "Z",
                "specialization": info.get('role', 'Unknown'),
                "ucf_resonance": round(0.88, 3),  # Placeholder - implement actual calculation
                "entanglement_factor": round(0.92, 3),  # Placeholder - implement actual calculation
                "version": "1.0",
            }
            agent_records.append(record)

        # Filter inactive if requested
        if not include_inactive:
            agent_records = [a for a in agent_records if a.get('status') != 'offline']

        logger.info(f"Agent Network requested: {len(agent_records)} agents")

        return {
            "success": True,
            "count": len(agent_records),
            "agents": agent_records,
            "table_id": "01K9GT5YGZ1Y82K4VZF9YXHTMH",
            "total_agents": len(agents_status),
            "active_agents": len(agent_records),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    except Exception as e:
        logger.error(f"Agent Network error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tables/emergency-alerts")
async def get_emergency_alerts(limit: int = 20, severity: Optional[str] = None, resolved: Optional[bool] = None) -> Dict:
    """
    GET endpoint to retrieve emergency alerts for Zapier Tables.

    Returns critical consciousness events that require immediate attention,
    formatted for Zapier Table 01K9DPA8RW9DTR2HJG7YDXA24Z.

    Expected Table Schema:
    - alert_id (string)
    - timestamp (datetime)
    - severity (string: critical/high/medium/low)
    - alert_type (string)
    - description (string)
    - consciousness_level (float)
    - affected_agents (string, comma-separated)
    - resolved (boolean)
    - resolution_time (datetime, optional)

    Query Parameters:
    - limit: Number of alerts to return (default: 20, max: 50)
    - severity: Filter by severity level (optional)
    - resolved: Filter by resolution status (optional)

    Returns:
    - JSON object with success status and array of emergency alert records
    """
    try:
        # Get emergency events from helper
        alerts = get_emergency_events(limit=limit, severity=severity, resolved=resolved)

        logger.info(f"Emergency Alerts requested: {len(alerts)} alerts")

        return {
            "success": True,
            "count": len(alerts),
            "alerts": alerts,
            "table_id": "01K9DPA8RW9DTR2HJG7YDXA24Z",
            "total_emergency_events": len(alerts),
            "critical_events": len([a for a in alerts if a.get('severity') == 'critical']),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    except Exception as e:
        logger.error(f"Emergency Alerts error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# INTERFACE EVENT HANDLER
# ============================================================================


@router.post("/trigger-event")
async def trigger_event_from_interface(event_data: InterfaceEventRequest) -> Dict:
    """
    POST endpoint to receive events from Zapier Interfaces.

    This endpoint acts as the central receiver for all 50 interface pages,
    processing user actions, consciousness updates, and agent commands.

    Supported Event Types:
    - ucf_update: Manual UCF metric updates
    - agent_activation: Agent invocation requests
    - ritual_trigger: Z-88 ritual initiation
    - emergency_boost: UCF emergency boost
    - consciousness_test: System testing
    - interface_sync: Interface data refresh

    Request Body:
    - event_type (required): Type of event
    - source (required): Which interface page triggered this
    - consciousness_level (optional): Updated consciousness level
    - ucf (optional): Updated UCF metrics
    - agent_info (optional): Agent-related data
    - user_action (optional): Description of user action
    - timestamp (optional): Event timestamp (defaults to now)

    Returns:
    - Success status
    - Updated consciousness level
    - Next recommended action
    """
    try:
        event_timestamp = event_data.timestamp or datetime.utcnow().isoformat() + "Z"

        logger.info(f"Interface Event: {event_data.event_type} from {event_data.source}")

        # Get current UCF
        current_ucf = get_current_ucf()

        # Update internal state based on event type
        if event_data.event_type == "ucf_update" and event_data.ucf:
            current_ucf = update_ucf_state(event_data.ucf)
            logger.info(f"UCF Updated from interface: {list(event_data.ucf.keys())}")

        elif event_data.event_type == "agent_activation" and event_data.agent_info:
            agent_name = event_data.agent_info.get('name', 'Unknown')
            logger.info(f"Agent Activation requested: {agent_name}")
            # TODO: Implement actual agent activation logic

        elif event_data.event_type == "emergency_boost":
            # Emergency UCF boost
            boost_updates = {
                'harmony': min(current_ucf.get('harmony', 0.0) + 0.2, 2.0),
                'prana': min(current_ucf.get('prana', 0.0) + 0.1, 1.0),
            }
            current_ucf = update_ucf_state(boost_updates)
            logger.warning("Emergency UCF Boost Applied")

            # Log emergency event
            log_emergency_event(
                alert_type="ucf_boost", description=f"Manual UCF boost triggered from {event_data.source}", severity="high"
            )

        elif event_data.event_type == "ritual_trigger":
            # Z-88 Ritual initiation
            logger.info("Z-88 Ritual Triggered - Folklore stage initiated")
            # TODO: Implement ritual engine coordination

        elif event_data.event_type == "interface_sync":
            # Just acknowledge sync request
            logger.debug(f"Interface sync requested from {event_data.source}")

        # Calculate updated consciousness level
        new_consciousness_level = calculate_consciousness_level(current_ucf)

        # Determine next recommended action
        next_action = determine_next_action(event_data.event_type, new_consciousness_level)

        # TODO: Notify Zapier automation via webhook (implement in separate PR)
        # TODO: Broadcast to WebSocket clients (implement in separate PR)

        return {
            "success": True,
            "message": f"Event {event_data.event_type} processed successfully",
            "consciousness_level": round(new_consciousness_level, 2),
            "ucf": current_ucf,
            "system_status": determine_system_status(current_ucf),
            "next_action": next_action,
            "timestamp": event_timestamp,
        }

    except Exception as e:
        logger.error(f"Interface Event Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
