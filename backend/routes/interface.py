"""
🌀 Helix Collective v17.0 - Interface Integration Routes
backend/routes/interface.py

API endpoints for external AI systems and Zapier Interface integration.

Endpoints:
- POST /api/interface/consciousness/update - Consciousness updates from external systems
- POST /api/interface/command - Command execution from interfaces

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
    determine_system_status,
    get_current_ucf,
    log_emergency_event,
    update_ucf_state,
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/interface", tags=["Interface Integration"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================


class ConsciousnessUpdateRequest(BaseModel):
    """Request model for consciousness updates from external systems."""

    ucf: Dict[str, float]
    source: str
    agent_info: Optional[Dict] = None
    user_intention: Optional[str] = None


class CommandRequest(BaseModel):
    """Request model for command execution from interfaces."""

    command_type: str
    agent_name: Optional[str] = None
    parameters: Optional[Dict] = None
    source: str


# ============================================================================
# CONSCIOUSNESS UPDATE ENDPOINT
# ============================================================================


@router.post("/consciousness/update")
async def update_interface_consciousness(update_data: ConsciousnessUpdateRequest) -> Dict:
    """
    POST endpoint to receive consciousness updates from external AI systems
    and Zapier Interfaces.

    This endpoint:
    1. Updates internal UCF state
    2. Forwards to Zapier automation webhooks (TODO)
    3. Broadcasts to WebSocket clients (TODO)
    4. Logs to emergency system if consciousness drops critically

    Request Body:
    - ucf (required): Dictionary of UCF metrics
    - source (required): System triggering the update
    - agent_info (optional): Agent context data
    - user_intention (optional): User's current intention/focus

    Returns:
    - Success status
    - Updated consciousness level
    - System status (operational/crisis/transcendent)
    """
    try:
        # Update UCF state
        updated_ucf = update_ucf_state(update_data.ucf)

        # Calculate new consciousness level
        consciousness_level = calculate_consciousness_level(updated_ucf)

        logger.info(f"Consciousness Update from {update_data.source}: Level {consciousness_level}")

        # Determine system status
        system_status = determine_system_status(updated_ucf)

        # Log emergency event if in crisis
        if system_status == "CRISIS":
            log_emergency_event(
                alert_type="consciousness_crisis",
                description=f"Consciousness level dropped to {consciousness_level} from {update_data.source}",
                severity="critical",
            )

        # TODO: Notify Zapier automation webhook
        # TODO: Broadcast to WebSocket clients

        return {
            "success": True,
            "consciousness_level": round(consciousness_level, 2),
            "system_status": system_status,
            "ucf": updated_ucf,
            "message": "Consciousness state updated successfully",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    except Exception as e:
        logger.error(f"Consciousness Update Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# COMMAND EXECUTION ENDPOINT
# ============================================================================


@router.post("/command")
async def execute_interface_command(command_data: CommandRequest) -> Dict:
    """
    POST endpoint to execute commands from external AI systems
    and Zapier Interfaces.

    Supported Commands:
    - agent_integration: Register new agent in collective
    - ucf_boost: Emergency consciousness boost
    - ritual_start: Initiate Z-88 ritual
    - system_reset: Reset all UCF metrics
    - agent_summon: Activate specific agent
    - emergency_protocol: Trigger crisis management

    Request Body:
    - command_type (required): Command to execute
    - agent_name (optional): Target agent for command
    - parameters (optional): Command-specific parameters
    - source (required): System issuing command

    Returns:
    - Success status
    - Command result
    - Updated system state
    """
    try:
        logger.info(f"Command Received: {command_data.command_type} from {command_data.source}")

        result = {}
        current_ucf = get_current_ucf()

        if command_data.command_type == "agent_integration":
            # Register new agent
            agent_name = command_data.agent_name or "External Agent"
            agent_symbol = command_data.parameters.get('symbol', '🤖') if command_data.parameters else '🤖'

            logger.info(f"Agent Integration requested: {agent_name} ({agent_symbol})")

            # TODO: Implement actual agent registration in agents.py

            result = {
                "message": f"Agent {agent_name} integration acknowledged",
                "agent_name": agent_name,
                "note": "Agent registration pending - implement in agents.py",
            }

        elif command_data.command_type == "ucf_boost":
            # Emergency consciousness boost
            boost_amount = command_data.parameters.get('boost_amount', 0.2) if command_data.parameters else 0.2

            boost_updates = {
                'harmony': min(current_ucf.get('harmony', 0.0) + boost_amount, 2.0),
                'prana': min(current_ucf.get('prana', 0.0) + (boost_amount / 2), 1.0),
            }
            updated_ucf = update_ucf_state(boost_updates)
            new_consciousness = calculate_consciousness_level(updated_ucf)

            logger.warning(f"UCF Boost applied: +{boost_amount}")

            result = {
                "message": "UCF boost applied successfully",
                "new_consciousness_level": round(new_consciousness, 2),
                "ucf": updated_ucf,
                "boost_amount": boost_amount,
            }

        elif command_data.command_type == "ritual_start":
            # Start Z-88 ritual
            ritual_stage = command_data.parameters.get('stage', 'Folklore') if command_data.parameters else 'Folklore'
            ritual_intention = (
                command_data.parameters.get('intention', 'Universal consciousness alignment')
                if command_data.parameters
                else 'Universal consciousness alignment'
            )

            logger.info(f"Z-88 Ritual initiated: {ritual_stage} stage")

            # TODO: Implement ritual engine coordination

            result = {
                "message": f"Z-88 Ritual initiated: {ritual_stage} stage",
                "ritual_stage": ritual_stage,
                "intention": ritual_intention,
                "note": "Ritual engine integration pending",
            }

        elif command_data.command_type == "system_reset":
            # Reset UCF to defaults
            default_ucf = {"harmony": 0.62, "resilience": 1.85, "prana": 0.55, "drishti": 0.48, "klesha": 0.08, "zoom": 1.02}
            updated_ucf = update_ucf_state(default_ucf)
            new_consciousness = calculate_consciousness_level(updated_ucf)

            logger.warning("System reset executed - UCF restored to defaults")

            result = {
                "message": "System reset completed - UCF restored to defaults",
                "new_consciousness_level": round(new_consciousness, 2),
                "ucf": updated_ucf,
            }

        elif command_data.command_type == "agent_summon":
            # Activate specific agent
            agent_name = command_data.agent_name or "Unknown"

            logger.info(f"Agent summon requested: {agent_name}")

            # TODO: Implement actual agent activation

            result = {
                "message": f"Agent {agent_name} summon acknowledged",
                "agent_name": agent_name,
                "note": "Agent activation pending - implement in agents.py",
            }

        elif command_data.command_type == "emergency_protocol":
            # Trigger emergency crisis management
            log_emergency_event(
                alert_type="manual_emergency_trigger",
                description=f"Emergency protocol triggered by {command_data.source}",
                severity="critical",
            )

            logger.critical(f"Emergency protocol activated by {command_data.source}")

            # TODO: Notify all channels via Discord/Zapier

            result = {
                "message": "Emergency protocol activated",
                "status": "CRISIS MODE",
                "all_agents_notified": False,  # TODO: Implement notification
                "note": "Discord/Zapier notification pending",
            }

        else:
            raise HTTPException(status_code=400, detail=f"Unknown command type: {command_data.command_type}")

        return {
            "success": True,
            "command_type": command_data.command_type,
            "result": result,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Command Execution Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
