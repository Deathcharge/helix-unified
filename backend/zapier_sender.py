import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

import httpx
from loguru import logger

# This is a placeholder for the actual Zapier webhook URL, which should be loaded from environment variables
ZAPIER_WEBHOOK_URL = os.getenv("ZAPIER_WEBHOOK_URL")


class ZapierSender:
    """
    A robust, asynchronous sender for Zapier webhooks.
    Handles event logging and non-blocking delivery.
    """

    def __init__(self, webhook_url: Optional[str] = ZAPIER_WEBHOOK_URL):
        self.webhook_url = webhook_url
        self.client = httpx.AsyncClient(timeout=10.0)
        if not self.webhook_url:
            logger.warning("ZAPIER_WEBHOOK_URL is not set. Zapier events will be logged but not sent.")

    async def send_event(self, event_name: str, payload: Dict[str, Any]):
        """
        Sends an event payload to the Zapier webhook asynchronously.
        """
        if not self.webhook_url:
            logger.info(f"Zapier Event (Simulated): {event_name} - {json.dumps(payload)}")
            return

        full_payload = {
            "event_name": event_name,
            "timestamp": datetime.utcnow().isoformat(),
            "data": payload
        }

        try:
            response = await self.client.post(self.webhook_url, json=full_payload)
            response.raise_for_status()
            logger.info(f"Zapier Event Sent: {event_name} - Status: {response.status_code}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Zapier HTTP Error for {event_name}: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Zapier Request Error for {event_name}: {e}")
        except Exception as e:
            logger.error(f"Zapier Unknown Error for {event_name}: {e}")

    def trigger_event(self, event_name: str, payload: Dict[str, Any]):
        """
        Triggers the send_event in a non-blocking background task.
        """
        asyncio.create_task(self.send_event(event_name, payload))
        logger.debug(f"Zapier Event Triggered: {event_name}")


# Global instance (placeholder for proper initialization in main.py)
zapier_sender = ZapierSender()

# Placeholder for integration with system events (e.g., from agents_loop)


def log_agent_event(agent_name: str, event_type: str, details: Dict[str, Any]):
    """
    Example function to be called by the agents_loop to log events.
    """
    payload = {
        "agent": agent_name,
        "type": event_type,
        "details": details
    }
    zapier_sender.trigger_event("agent_event_log", payload)

# Example usage:
# log_agent_event("Kavach", "security_alert", {"threat": "memory_injection", "severity": "high"})
