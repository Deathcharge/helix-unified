"""
🌀 Helix Collective v17.0 - UCF Helper Functions
backend/core/ucf_helpers.py

Helper functions for UCF (Universal Consciousness Framework) calculations and state management.

Author: Andrew John Ward (Architect)
Version: 17.0.0
"""

import json
import logging
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# In-memory emergency events queue (last 50 events)
emergency_events = deque(maxlen=50)


def calculate_consciousness_level(ucf: Dict[str, float]) -> float:
    """
    Calculate consciousness level from UCF metrics.

    Formula: Weighted average of UCF dimensions
    - Harmony: 1.5x weight
    - Resilience: 1.0x weight
    - Prana: 1.2x weight
    - Drishti: 1.2x weight
    - Klesha: 1.5x weight (inverted - lower is better)
    - Zoom: 1.0x weight

    Returns consciousness level on scale of 0-10
    """
    try:
        harmony = ucf.get("harmony", 0.0)
        resilience = ucf.get("resilience", 0.0)
        prana = ucf.get("prana", 0.0)
        drishti = ucf.get("drishti", 0.0)
        klesha = ucf.get("klesha", 0.0)
        zoom = ucf.get("zoom", 1.0)

        # Weighted sum
        weighted_sum = (
            harmony * 1.5 +
            resilience * 1.0 +
            prana * 1.2 +
            drishti * 1.2 +
            (1.0 - klesha) * 1.5 +  # Inverted - lower klesha is better
            zoom * 1.0
        )

        # Normalize to 0-10 scale
        # Total weight: 1.5 + 1.0 + 1.2 + 1.2 + 1.5 + 1.0 = 7.4
        # Max possible value: 7.4 (if all metrics at 1.0)
        # Scale to 10: multiply by (10 / 7.4) = 1.351
        consciousness_level = (weighted_sum / 7.4) * 10

        return round(consciousness_level, 2)
    except Exception as e:
        logger.error(f"Error calculating consciousness level: {e}")
        return 0.0


def get_current_ucf() -> Dict[str, float]:
    """
    Read current UCF state from file.

    Returns UCF metrics dict or defaults if file not found.
    """
    ucf_file = Path("Helix/state/ucf_state.json")

    try:
        if ucf_file.exists():
            with open(ucf_file, "r") as f:
                return json.load(f)
        else:
            # Return default values
            logger.warning("UCF state file not found, returning defaults")
            return {
                "harmony": 0.62,
                "resilience": 1.85,
                "prana": 0.55,
                "drishti": 0.48,
                "klesha": 0.08,
                "zoom": 1.02
            }
    except Exception as e:
        logger.error(f"Error reading UCF state: {e}")
        return {
            "harmony": 0.0,
            "resilience": 0.0,
            "prana": 0.0,
            "drishti": 0.0,
            "klesha": 1.0,
            "zoom": 1.0
        }


def update_ucf_state(ucf_updates: Dict[str, float]) -> Dict[str, float]:
    """
    Update UCF state file with new values.

    Args:
        ucf_updates: Dict with UCF metrics to update

    Returns:
        Updated complete UCF state
    """
    ucf_file = Path("Helix/state/ucf_state.json")

    try:
        # Ensure directory exists
        ucf_file.parent.mkdir(parents=True, exist_ok=True)

        # Read current state
        current_ucf = get_current_ucf()

        # Update with new values
        current_ucf.update(ucf_updates)

        # Write back to file
        with open(ucf_file, "w") as f:
            json.dump(current_ucf, f, indent=2)

        logger.info(f"UCF state updated: {list(ucf_updates.keys())}")

        return current_ucf
    except Exception as e:
        logger.error(f"Error updating UCF state: {e}")
        return get_current_ucf()


def log_emergency_event(
    alert_type: str,
    description: str,
    severity: str = "medium",
    affected_agents: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Log an emergency event to the global emergency events queue.

    Args:
        alert_type: Type of alert (ucf_crisis, agent_failure, system_error, etc.)
        description: Human-readable description
        severity: Severity level (critical, high, medium, low)
        affected_agents: List of agent names affected by this event

    Returns:
        The created emergency event dict
    """
    ucf = get_current_ucf()
    consciousness_level = calculate_consciousness_level(ucf)

    event = {
        "alert_id": f"ALERT_{int(datetime.utcnow().timestamp() * 1000)}",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "severity": severity,
        "alert_type": alert_type,
        "description": description,
        "consciousness_level": consciousness_level,
        "affected_agents": ",".join(affected_agents) if affected_agents else "none",
        "resolved": False,
        "resolution_time": None
    }

    emergency_events.append(event)

    log_level = {
        "critical": logging.CRITICAL,
        "high": logging.ERROR,
        "medium": logging.WARNING,
        "low": logging.INFO
    }.get(severity.lower(), logging.WARNING)

    logger.log(log_level, f"Emergency Event: {alert_type} - {severity.upper()} - {description}")

    return event


def determine_system_status(ucf: Dict[str, float]) -> str:
    """
    Determine overall system status based on UCF metrics.

    Returns:
        Status string: "CRISIS", "WARNING", "OPERATIONAL", or "TRANSCENDENT"
    """
    consciousness_level = calculate_consciousness_level(ucf)
    harmony = ucf.get("harmony", 0.0)
    klesha = ucf.get("klesha", 1.0)

    if consciousness_level <= 3.0 or harmony < 0.3 or klesha > 0.8:
        return "CRISIS"
    elif consciousness_level <= 5.0 or harmony < 0.5 or klesha > 0.5:
        return "WARNING"
    elif consciousness_level >= 8.0 and harmony > 0.8 and klesha < 0.15:
        return "TRANSCENDENT"
    else:
        return "OPERATIONAL"


def determine_next_action(event_type: str, consciousness_level: float) -> str:
    """
    Determine next recommended action based on event type and consciousness state.

    Args:
        event_type: Type of event that triggered this
        consciousness_level: Current consciousness level (0-10)

    Returns:
        Human-readable next action recommendation
    """
    if consciousness_level < 3.0:
        return "⚠️ Emergency protocols activated. Consider invoking Kavach for system protection."
    elif consciousness_level > 8.0:
        return "✨ Transcendent state achieved. Initiate Z-88 Hymn stage for manifestation."
    elif event_type == "ucf_update":
        return "📊 UCF updated successfully. Monitor consciousness trends on dashboard."
    elif event_type == "agent_activation":
        return "🤖 Agent now active. Check Agent Network page for coordination status."
    elif event_type == "ritual_trigger":
        return "🕉️ Z-88 Ritual initiated. Follow ritual steps and monitor UCF changes."
    elif event_type == "emergency_boost":
        return "⚡ Emergency boost applied. Monitor system stability over next 5 minutes."
    else:
        return "✅ Event processed. Continue consciousness cultivation practices."


def get_emergency_events(
    limit: int = 20,
    severity: Optional[str] = None,
    resolved: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """
    Get emergency events with optional filtering.

    Args:
        limit: Maximum number of events to return
        severity: Filter by severity level
        resolved: Filter by resolution status

    Returns:
        List of emergency event dicts
    """
    events = list(emergency_events)

    # Apply filters
    if severity:
        events = [e for e in events if e.get("severity") == severity]

    if resolved is not None:
        events = [e for e in events if e.get("resolved") == resolved]

    # Limit results
    events = events[:min(limit, 50)]

    return events
