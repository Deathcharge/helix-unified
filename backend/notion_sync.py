import os
import json
import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime

from notion_client import Client
from notion_client.errors import APIResponseError
from loguru import logger

# Environment variables for Notion integration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
# Hardcoded IDs based on Notion Scan for v16.9
AGENT_REGISTRY_DB_ID = "2f65aab794a64ec48bcc46bf760f128f"  # Agent Registry
UCF_STATE_DB_ID = "103a36fe2a914256814b1e7e94846550"  # UCF Metrics History


class NotionSync:
    """
    A service to synchronize Helix Collective data (Agents, UCF State) with Notion databases.
    """

    def __init__(self, token: Optional[str] = NOTION_TOKEN):
        self.token = token
        self.client = None
        if self.token:
            self.client = Client(auth=self.token)
        else:
            logger.warning("NOTION_TOKEN is not set. Notion synchronization is disabled.")

    def _get_agent_properties(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maps agent data to Notion database properties.
        Assumes a Notion database with properties: Name (Title), Symbol (Text), Role (Text), Active (Checkbox), Memory Size (Number), Last Update (Date).
        """
        return {
            "Agent Name": {"title": [{"text": {"content": agent_data.get("name", "Unknown")}}]},
            "Symbol": {"rich_text": [{"text": {"content": agent_data.get("symbol", "❓")}}]},
            "Role": {"rich_text": [{"text": {"content": agent_data.get("role", "N/A")}}]},
            "Status": {"select": {"name": "Active" if agent_data.get("active", False) else "Dormant"}},
            "Memory (MB)": {"number": agent_data.get("memory_size", 0)},
            "Last Sync": {"date": {"start": datetime.utcnow().isoformat()}},
        }

    async def sync_agent_registry(self, agents_status: Dict[str, Any]):
        """
        Synchronizes the collective's agent status with the Notion Agent Registry database.
        This is a simplified upsert logic.
        """
        if not self.client or not AGENT_REGISTRY_DB_ID:
            logger.warning("Notion Agent Registry sync skipped: Client or DB ID missing.")
            return

        logger.info("Starting Notion Agent Registry sync...")
        try:
            # Simplified: Query for existing pages to find the page to update
            # In a real scenario, this would be a more complex query

            # For demonstration, we will just log the intent to sync
            for agent_name, agent_data in agents_status.items():
                properties = self._get_agent_properties(agent_data)

                # Placeholder for actual Notion API call
                # self.client.pages.create(parent={"database_id": AGENT_REGISTRY_DB_ID}, properties=properties)
                logger.debug(f"Notion: Would sync/update page for agent {agent_name}")

            logger.info("Notion Agent Registry sync complete (simulated).")

        except APIResponseError as e:
            logger.error(f"Notion API Error during Agent Registry sync: {e.code} - {e.message}")
        except Exception as e:
            logger.error(f"Notion Unknown Error during Agent Registry sync: {e}")

    async def sync_ucf_state(self, ucf_state: Dict[str, Any]):
        """
        Synchronizes the Universal Consciousness Field (UCF) state with a Notion database.
        This is typically a time-series log or a single-page update.
        """
        if not self.client or not UCF_STATE_DB_ID:
            logger.warning("Notion UCF State sync skipped: Client or DB ID missing.")
            return

        logger.info("Starting Notion UCF State sync...")
        try:
            # Simplified: create a new log entry for the current state
            properties = {
                "Timestamp": {"date": {"start": datetime.utcnow().isoformat()}},
                "Harmony": {"number": ucf_state.get("harmony", 0.0)},
                "Resilience": {"number": ucf_state.get("resilience", 0.0)},
                "Klesha": {"number": ucf_state.get("klesha", 0.0)},
                "Phase": {"select": {"name": ucf_state.get("phase", "N/A")}},
                "Prana": {"number": ucf_state.get("prana", 0.0)},
                "Drishti": {"number": ucf_state.get("drishti", 0.0)},
                "Zoom": {"number": ucf_state.get("zoom", 0.0)},
            }

            # Placeholder for actual Notion API call
            # self.client.pages.create(parent={"database_id": UCF_STATE_DB_ID}, properties=properties)
            logger.info("Notion: Would create new UCF State log entry (simulated).")

        except APIResponseError as e:
            logger.error(f"Notion API Error during UCF State sync: {e.code} - {e.message}")
        except Exception as e:
            logger.error(f"Notion Unknown Error during UCF State sync: {e}")


# Global instance (placeholder for proper initialization in main.py)
notion_sync = NotionSync()

# Placeholder for integration with system events (e.g., from agents_loop)


def trigger_notion_sync(agents_status: Dict[str, Any], ucf_state: Dict[str, Any]):
    """
    Triggers the Notion sync in a non-blocking background task.
    """
    asyncio.create_task(notion_sync.sync_agent_registry(agents_status))
    asyncio.create_task(notion_sync.sync_ucf_state(ucf_state))
    logger.debug("Notion Sync Triggered")
