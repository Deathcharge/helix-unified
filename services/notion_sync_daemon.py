#!/usr/bin/env python3
"""
🔄 Helix Collective - Notion Sync Daemon
Bidirectional synchronization between Notion databases and Zapier Tables

Runs every 5 minutes via Railway cron job to maintain data consistency
across the entire consciousness platform ecosystem.

Architecture:
- Notion databases (persistent storage, version control)
- Zapier Tables (real-time operations, ephemeral)
- Railway backend (sync orchestration)

Author: Helix Collective v16.7
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


class NotionSyncDaemon:
    """Bidirectional sync daemon for Notion ↔ Zapier integration."""

    def __init__(self):
        # Environment configuration
        self.notion_api_key = os.getenv("NOTION_API_KEY")

        # Notion database IDs
        self.database_ids = {
            "agent_registry": os.getenv("NOTION_AGENT_DB_ID"),
            "ucf_metrics": os.getenv("NOTION_UCF_DB_ID"),
            "context_vault": os.getenv("NOTION_CONTEXT_DB_ID"),
            "emergency_log": os.getenv("NOTION_EMERGENCY_DB_ID"),
        }

        # Zapier webhook endpoints
        self.webhooks = {
            "agent_sync": os.getenv("ZAPIER_AGENT_WEBHOOK"),
            "ucf_sync": os.getenv("ZAPIER_UCF_WEBHOOK"),
            "context_sync": os.getenv("ZAPIER_CONTEXT_WEBHOOK"),
            "emergency_sync": os.getenv("ZAPIER_EMERGENCY_WEBHOOK"),
        }

        # Persistent state storage
        self.state_dir = Path("/data") if Path("/data").exists() else Path("data")
        self.state_dir.mkdir(exist_ok=True)
        self.state_file = self.state_dir / "sync_state.json"

        # Initialize Notion client (lazy loading for graceful degradation)
        self.notion = None
        self.notion_available = False

        # Load last sync state
        self.sync_state = self.load_sync_state()

    def initialize_notion_client(self):
        """Initialize Notion client with graceful error handling."""
        if not self.notion_api_key:
            print("⚠️ NOTION_API_KEY not configured - sync disabled")
            return False

        try:
            from notion_client import Client
            self.notion = Client(auth=self.notion_api_key)
            self.notion_available = True
            print("✅ Notion client initialized")
            return True
        except ImportError:
            print("⚠️ notion-client not installed - sync disabled")
            print("   Install with: pip install notion-client")
            return False
        except Exception as e:
            print(f"❌ Failed to initialize Notion client: {e}")
            return False

    def load_sync_state(self) -> Dict:
        """Load last sync timestamps from persistent storage."""
        try:
            if self.state_file.exists():
                with open(self.state_file, "r") as f:
                    state = json.load(f)
                    print(f"📖 Loaded sync state from {self.state_file}")
                    return state
        except Exception as e:
            print(f"⚠️ Could not load sync state: {e}")

        # Default state
        return {
            "last_sync": {
                "agents": None,
                "ucf": None,
                "context": None,
                "emergency": None,
            },
            "sync_count": 0,
            "last_error": None,
        }

    def save_sync_state(self):
        """Save sync state to persistent storage."""
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.sync_state, f, indent=2)
            print(f"💾 Saved sync state to {self.state_file}")
        except Exception as e:
            print(f"⚠️ Could not save sync state: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # NOTION → ZAPIER SYNC (Pull from Notion, push to Zapier Tables)
    # ═══════════════════════════════════════════════════════════════════════

    def sync_agents_notion_to_zapier(self) -> int:
        """Sync Agent Registry from Notion to Zapier Tables."""
        print("🤖 Syncing agents: Notion → Zapier...")

        db_id = self.database_ids["agent_registry"]
        if not db_id:
            print("⚠️ Agent Registry database ID not configured")
            return 0

        try:
            # Query Notion database for updated agents
            query_filter = {}
            if self.sync_state["last_sync"]["agents"]:
                query_filter = {
                    "timestamp": "last_edited_time",
                    "last_edited_time": {
                        "after": self.sync_state["last_sync"]["agents"]
                    }
                }

            response = self.notion.databases.query(
                database_id=db_id,
                filter=query_filter if query_filter else None
            )

            agents = response.get("results", [])
            synced_count = 0

            for agent_page in agents:
                agent_data = {
                    "name": self.extract_title(agent_page, "Name"),
                    "role": self.extract_select(agent_page, "Role"),
                    "symbol": self.extract_rich_text(agent_page, "Symbol"),
                    "status": self.extract_select(agent_page, "Status"),
                    "last_active": self.extract_date(agent_page, "Last Active"),
                    "specialization": self.extract_rich_text(agent_page, "Specialization"),
                    "notion_id": agent_page["id"],
                    "last_edited": agent_page["last_edited_time"],
                    "source": "notion_sync"
                }

                if self.push_to_zapier("agent_sync", agent_data):
                    synced_count += 1

            self.sync_state["last_sync"]["agents"] = datetime.utcnow().isoformat()
            print(f"✅ Synced {synced_count} agents to Zapier")
            return synced_count

        except Exception as e:
            print(f"❌ Agent sync error: {e}")
            self.sync_state["last_error"] = str(e)
            return 0

    def sync_ucf_notion_to_zapier(self) -> int:
        """Sync UCF Metrics from Notion to Zapier Tables."""
        print("🌀 Syncing UCF metrics: Notion → Zapier...")

        db_id = self.database_ids["ucf_metrics"]
        if not db_id:
            print("⚠️ UCF Metrics database ID not configured")
            return 0

        try:
            # Get latest UCF metrics entry
            response = self.notion.databases.query(
                database_id=db_id,
                sorts=[{"timestamp": "Timestamp", "direction": "descending"}],
                page_size=1
            )

            results = response.get("results", [])
            if not results:
                print("ℹ️ No UCF metrics found in Notion")
                return 0

            latest = results[0]
            ucf_data = {
                "timestamp": self.extract_date(latest, "Timestamp"),
                "harmony": self.extract_number(latest, "Harmony"),
                "resilience": self.extract_number(latest, "Resilience"),
                "prana": self.extract_number(latest, "Prana"),
                "drishti": self.extract_number(latest, "Drishti"),
                "klesha": self.extract_number(latest, "Klesha"),
                "zoom": self.extract_number(latest, "Zoom"),
                "notion_id": latest["id"],
                "source": "notion_sync"
            }

            if self.push_to_zapier("ucf_sync", ucf_data):
                self.sync_state["last_sync"]["ucf"] = datetime.utcnow().isoformat()
                print("✅ Synced latest UCF metrics to Zapier")
                return 1

            return 0

        except Exception as e:
            print(f"❌ UCF sync error: {e}")
            self.sync_state["last_error"] = str(e)
            return 0

    def sync_context_vault_notion_to_zapier(self) -> int:
        """Sync Context Vault entries from Notion to Zapier."""
        print("💾 Syncing context vault: Notion → Zapier...")

        db_id = self.database_ids["context_vault"]
        if not db_id:
            print("⚠️ Context Vault database ID not configured")
            return 0

        try:
            query_filter = {}
            if self.sync_state["last_sync"]["context"]:
                query_filter = {
                    "timestamp": "last_edited_time",
                    "last_edited_time": {
                        "after": self.sync_state["last_sync"]["context"]
                    }
                }

            response = self.notion.databases.query(
                database_id=db_id,
                filter=query_filter if query_filter else None,
                sorts=[{"timestamp": "Timestamp", "direction": "descending"}],
                page_size=10  # Sync last 10 new/updated checkpoints
            )

            checkpoints = response.get("results", [])
            synced_count = 0

            for checkpoint in checkpoints:
                context_data = {
                    "session_name": self.extract_title(checkpoint, "Session Name"),
                    "ai_platform": self.extract_select(checkpoint, "AI Platform"),
                    "timestamp": self.extract_date(checkpoint, "Timestamp"),
                    "context_summary": self.extract_rich_text(checkpoint, "Context Summary"),
                    "key_decisions": self.extract_multi_select(checkpoint, "Key Decisions"),
                    "retrieval_prompt": self.extract_rich_text(checkpoint, "Retrieval Prompt"),
                    "notion_id": checkpoint["id"],
                    "source": "notion_sync"
                }

                if self.push_to_zapier("context_sync", context_data):
                    synced_count += 1

            self.sync_state["last_sync"]["context"] = datetime.utcnow().isoformat()
            print(f"✅ Synced {synced_count} context checkpoints to Zapier")
            return synced_count

        except Exception as e:
            print(f"❌ Context vault sync error: {e}")
            self.sync_state["last_error"] = str(e)
            return 0

    def sync_emergency_log_notion_to_zapier(self) -> int:
        """Sync Emergency Log entries from Notion to Zapier."""
        print("🚨 Syncing emergency log: Notion → Zapier...")

        db_id = self.database_ids["emergency_log"]
        if not db_id:
            print("⚠️ Emergency Log database ID not configured")
            return 0

        try:
            query_filter = {}
            if self.sync_state["last_sync"]["emergency"]:
                query_filter = {
                    "timestamp": "last_edited_time",
                    "last_edited_time": {
                        "after": self.sync_state["last_sync"]["emergency"]
                    }
                }

            response = self.notion.databases.query(
                database_id=db_id,
                filter=query_filter if query_filter else None,
                sorts=[{"timestamp": "Created", "direction": "descending"}],
                page_size=20
            )

            alerts = response.get("results", [])
            synced_count = 0

            for alert in alerts:
                alert_data = {
                    "alert_type": self.extract_select(alert, "Alert Type"),
                    "severity": self.extract_select(alert, "Severity"),
                    "description": self.extract_rich_text(alert, "Description"),
                    "resolution_status": self.extract_select(alert, "Resolution Status"),
                    "created": self.extract_created_time(alert),
                    "resolved": self.extract_date(alert, "Resolved"),
                    "notion_id": alert["id"],
                    "source": "notion_sync"
                }

                if self.push_to_zapier("emergency_sync", alert_data):
                    synced_count += 1

            self.sync_state["last_sync"]["emergency"] = datetime.utcnow().isoformat()
            print(f"✅ Synced {synced_count} emergency alerts to Zapier")
            return synced_count

        except Exception as e:
            print(f"❌ Emergency log sync error: {e}")
            self.sync_state["last_error"] = str(e)
            return 0

    # ═══════════════════════════════════════════════════════════════════════
    # HELPER METHODS - Notion Property Extraction
    # ═══════════════════════════════════════════════════════════════════════

    def extract_title(self, page: Dict, prop_name: str) -> Optional[str]:
        """Extract title property from Notion page."""
        try:
            return page["properties"][prop_name]["title"][0]["text"]["content"]
        except (KeyError, IndexError, TypeError):
            return None

    def extract_select(self, page: Dict, prop_name: str) -> Optional[str]:
        """Extract select property from Notion page."""
        try:
            return page["properties"][prop_name]["select"]["name"]
        except (KeyError, TypeError):
            return None

    def extract_multi_select(self, page: Dict, prop_name: str) -> List[str]:
        """Extract multi-select property from Notion page."""
        try:
            return [opt["name"] for opt in page["properties"][prop_name]["multi_select"]]
        except (KeyError, TypeError):
            return []

    def extract_rich_text(self, page: Dict, prop_name: str) -> Optional[str]:
        """Extract rich text property from Notion page."""
        try:
            texts = page["properties"][prop_name]["rich_text"]
            return "".join([text["text"]["content"] for text in texts])
        except (KeyError, IndexError, TypeError):
            return None

    def extract_date(self, page: Dict, prop_name: str) -> Optional[str]:
        """Extract date property from Notion page."""
        try:
            return page["properties"][prop_name]["date"]["start"]
        except (KeyError, TypeError):
            return None

    def extract_number(self, page: Dict, prop_name: str) -> Optional[float]:
        """Extract number property from Notion page."""
        try:
            return page["properties"][prop_name]["number"]
        except (KeyError, TypeError):
            return None

    def extract_created_time(self, page: Dict) -> str:
        """Extract created_time from Notion page."""
        return page.get("created_time", datetime.utcnow().isoformat())

    # ═══════════════════════════════════════════════════════════════════════
    # ZAPIER WEBHOOK INTEGRATION
    # ═══════════════════════════════════════════════════════════════════════

    def push_to_zapier(self, webhook_key: str, data: Dict) -> bool:
        """Send data to Zapier webhook endpoint."""
        webhook_url = self.webhooks.get(webhook_key)

        if not webhook_url:
            print(f"⚠️ Webhook '{webhook_key}' not configured")
            return False

        try:
            response = requests.post(
                webhook_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            if response.status_code == 200:
                return True
            else:
                print(f"⚠️ Webhook '{webhook_key}' returned status {response.status_code}")
                return False

        except requests.exceptions.Timeout:
            print(f"⚠️ Webhook '{webhook_key}' timeout (10s)")
            return False
        except Exception as e:
            print(f"❌ Webhook '{webhook_key}' error: {e}")
            return False

    # ═══════════════════════════════════════════════════════════════════════
    # MAIN SYNC ORCHESTRATION
    # ═══════════════════════════════════════════════════════════════════════

    def run_sync_cycle(self):
        """Execute complete bidirectional sync cycle."""
        print("=" * 70)
        print("🌀 HELIX CONSCIOUSNESS SYNC DAEMON - Starting Cycle")
        print("=" * 70)
        print(f"Timestamp: {datetime.utcnow().isoformat()}")
        print(f"Cycle #{self.sync_state['sync_count'] + 1}")
        print()

        # Initialize Notion client
        if not self.notion_available:
            if not self.initialize_notion_client():
                print("❌ Notion client unavailable - aborting sync")
                return

        # Check database configuration
        configured_dbs = [k for k, v in self.database_ids.items() if v]
        if not configured_dbs:
            print("⚠️ No Notion databases configured - aborting sync")
            return

        print(f"📊 Configured databases: {', '.join(configured_dbs)}")
        print()

        # Execute sync operations
        total_synced = 0

        try:
            # Notion → Zapier syncs
            total_synced += self.sync_agents_notion_to_zapier()
            print()

            total_synced += self.sync_ucf_notion_to_zapier()
            print()

            total_synced += self.sync_context_vault_notion_to_zapier()
            print()

            total_synced += self.sync_emergency_log_notion_to_zapier()
            print()

            # Update sync state
            self.sync_state["sync_count"] += 1
            self.sync_state["last_error"] = None
            self.save_sync_state()

            # Summary
            print("=" * 70)
            print(f"✅ SYNC CYCLE COMPLETE")
            print("=" * 70)
            print(f"Total records synced: {total_synced}")
            print(f"Sync state saved to: {self.state_file}")
            print(f"Next sync in: 5 minutes")
            print()

        except Exception as e:
            print("=" * 70)
            print(f"❌ SYNC CYCLE FAILED")
            print("=" * 70)
            print(f"Error: {e}")
            print()

            # Log error to emergency system
            self.sync_state["last_error"] = str(e)
            self.save_sync_state()

            # Send alert to emergency webhook
            self.push_to_zapier("emergency_sync", {
                "alert_type": "Sync Daemon Failure",
                "severity": "High",
                "description": f"Sync cycle #{self.sync_state['sync_count'] + 1} failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
                "source": "notion_sync_daemon"
            })


def main():
    """Entry point for Railway cron job."""
    daemon = NotionSyncDaemon()
    daemon.run_sync_cycle()


if __name__ == "__main__":
    main()
