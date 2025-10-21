# 🌀 Helix Collective v14.5 — Quantum Handshake
# backend/services/notion_client.py — Notion Integration Client
# Author: Andrew John Ward (Architect)

import os
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List
from notion_client import Client

# ============================================================================
# NOTION CLIENT
# ============================================================================

class HelixNotionClient:
    """Client for Notion integration with Helix Collective databases."""
    
    def __init__(self):
        """Initialize Notion client with database IDs."""
        notion_token = os.getenv("NOTION_API_KEY")
        if not notion_token:
            raise ValueError("NOTION_API_KEY environment variable not set")
        
        self.notion = Client(auth=notion_token)
        
        # Database IDs (from Notion workspace)
        self.system_state_db = os.getenv("NOTION_SYSTEM_STATE_DB", "009a946d04fb46aa83e4481be86f09ef")
        self.agent_registry_db = os.getenv("NOTION_AGENT_REGISTRY_DB", "2f65aab794a64ec48bcc46bf760f128f")
        self.event_log_db = os.getenv("NOTION_EVENT_LOG_DB", "acb01d4a955d4775aaeb2310d1da1102")
        self.context_db = os.getenv("NOTION_CONTEXT_DB", "d704854868474666b4b774750f8b134a")
        
        # Cache for agent page IDs
        self._agent_cache: Dict[str, str] = {}
    
    # ========================================================================
    # AGENT REGISTRY OPERATIONS
    # ========================================================================
    
    async def _get_agent_page_id(self, agent_name: str) -> Optional[str]:
        """Get page ID for an agent from cache or database."""
        if agent_name in self._agent_cache:
            return self._agent_cache[agent_name]
        
        try:
            results = self.notion.databases.query(
                database_id=self.agent_registry_db,
                filter={
                    "property": "Agent Name",
                    "title": {"equals": agent_name}
                }
            )
            
            if results["results"]:
                page_id = results["results"][0]["id"]
                self._agent_cache[agent_name] = page_id
                return page_id
        except Exception as e:
            print(f"⚠ Error getting agent page ID for {agent_name}: {e}")
        
        return None
    
    async def create_agent(
        self,
        agent_name: str,
        symbol: str,
        role: str,
        status: str = "Active",
        health_score: int = 100
    ) -> Optional[str]:
        """Create a new agent in the Agent Registry."""
        try:
            response = self.notion.pages.create(
                parent={"database_id": self.agent_registry_db},
                properties={
                    "Agent Name": {
                        "title": [{"text": {"content": agent_name}}]
                    },
                    "Symbol": {
                        "rich_text": [{"text": {"content": symbol}}]
                    },
                    "Role": {
                        "rich_text": [{"text": {"content": role}}]
                    },
                    "Status": {
                        "select": {"name": status}
                    },
                    "Last Action": {
                        "rich_text": [{"text": {"content": "Initialized"}}]
                    },
                    "Health Score": {
                        "number": health_score
                    },
                    "Last Updated": {
                        "date": {"start": datetime.utcnow().isoformat()}
                    }
                }
            )
            
            page_id = response["id"]
            self._agent_cache[agent_name] = page_id
            print(f"✅ Created agent {agent_name} in Notion")
            return page_id
        except Exception as e:
            print(f"❌ Error creating agent {agent_name}: {e}")
            return None
    
    async def update_agent_status(
        self,
        agent_name: str,
        status: str,
        last_action: str,
        health_score: int
    ) -> bool:
        """Update agent status in the Agent Registry."""
        try:
            agent_page_id = await self._get_agent_page_id(agent_name)
            if not agent_page_id:
                print(f"⚠ Agent {agent_name} not found in Notion")
                return False
            
            self.notion.pages.update(
                page_id=agent_page_id,
                properties={
                    "Status": {"select": {"name": status}},
                    "Last Action": {
                        "rich_text": [{"text": {"content": last_action[:100]}}]
                    },
                    "Health Score": {"number": health_score},
                    "Last Updated": {
                        "date": {"start": datetime.utcnow().isoformat()}
                    }
                }
            )
            print(f"✅ Updated agent {agent_name} status to {status}")
            return True
        except Exception as e:
            print(f"❌ Error updating agent {agent_name}: {e}")
            return False
    
    # ========================================================================
    # EVENT LOG OPERATIONS
    # ========================================================================
    
    async def log_event(
        self,
        event_title: str,
        event_type: str,
        agent_name: str,
        description: str,
        ucf_snapshot: Dict[str, Any]
    ) -> Optional[str]:
        """Write event to the Event Log."""
        try:
            agent_page_id = await self._get_agent_page_id(agent_name)
            
            response = self.notion.pages.create(
                parent={"database_id": self.event_log_db},
                properties={
                    "Event": {
                        "title": [{"text": {"content": event_title[:100]}}]
                    },
                    "Timestamp": {
                        "date": {"start": datetime.utcnow().isoformat()}
                    },
                    "Event Type": {
                        "select": {"name": event_type}
                    },
                    "Agent": {
                        "relation": [{"id": agent_page_id}] if agent_page_id else []
                    },
                    "Description": {
                        "rich_text": [{"text": {"content": description[:2000]}}]
                    },
                    "UCF Snapshot": {
                        "rich_text": [{"text": {"content": str(ucf_snapshot)[:2000]}}]
                    }
                }
            )
            
            print(f"✅ Logged event: {event_title}")
            return response["id"]
        except Exception as e:
            print(f"❌ Error logging event {event_title}: {e}")
            return None
    
    # ========================================================================
    # SYSTEM STATE OPERATIONS
    # ========================================================================
    
    async def update_system_component(
        self,
        component_name: str,
        status: str,
        harmony: float,
        error_log: str = "",
        verified: bool = False
    ) -> bool:
        """Update or create system component in System State."""
        try:
            # Query for existing component
            results = self.notion.databases.query(
                database_id=self.system_state_db,
                filter={
                    "property": "Component",
                    "title": {"equals": component_name}
                }
            )
            
            properties = {
                "Status": {"select": {"name": status}},
                "Harmony": {"number": harmony},
                "Last Updated": {
                    "date": {"start": datetime.utcnow().isoformat()}
                },
                "Error Log": {
                    "rich_text": [{"text": {"content": error_log[:2000]}}]
                },
                "Verification": {"checkbox": verified}
            }
            
            if results["results"]:
                # Update existing
                page_id = results["results"][0]["id"]
                self.notion.pages.update(page_id=page_id, properties=properties)
                print(f"✅ Updated component {component_name}")
            else:
                # Create new
                properties["Component"] = {
                    "title": [{"text": {"content": component_name}}]
                }
                self.notion.pages.create(
                    parent={"database_id": self.system_state_db},
                    properties=properties
                )
                print(f"✅ Created component {component_name}")
            
            return True
        except Exception as e:
            print(f"❌ Error updating component {component_name}: {e}")
            return False
    
    # ========================================================================
    # CONTEXT SNAPSHOT OPERATIONS
    # ========================================================================
    
    async def save_context_snapshot(
        self,
        session_id: str,
        ai_system: str,
        summary: str,
        key_decisions: str,
        next_steps: str,
        full_context: Dict[str, Any]
    ) -> Optional[str]:
        """Save context snapshot for session continuity."""
        try:
            response = self.notion.pages.create(
                parent={"database_id": self.context_db},
                properties={
                    "Session ID": {
                        "title": [{"text": {"content": session_id}}]
                    },
                    "AI System": {
                        "select": {"name": ai_system}
                    },
                    "Created": {
                        "date": {"start": datetime.utcnow().isoformat()}
                    },
                    "Summary": {
                        "rich_text": [{"text": {"content": summary[:2000]}}]
                    },
                    "Key Decisions": {
                        "rich_text": [{"text": {"content": key_decisions[:2000]}}]
                    },
                    "Next Steps": {
                        "rich_text": [{"text": {"content": next_steps[:2000]}}]
                    },
                    "Full Context": {
                        "rich_text": [{"text": {"content": str(full_context)[:2000]}}]
                    }
                }
            )
            
            print(f"✅ Saved context snapshot: {session_id}")
            return response["id"]
        except Exception as e:
            print(f"❌ Error saving context snapshot: {e}")
            return None
    
    # ========================================================================
    # HEALTH CHECK & UTILITIES
    # ========================================================================
    
    async def health_check(self) -> bool:
        """Check if Notion connection is working."""
        try:
            self.notion.users.me()
            print("✅ Notion connection healthy")
            return True
        except Exception as e:
            print(f"❌ Notion connection failed: {e}")
            return False
    
    async def clear_agent_cache(self):
        """Clear the agent page ID cache."""
        self._agent_cache.clear()
        print("✅ Agent cache cleared")
    
    async def get_context_snapshot(self, session_id: str):
        """Retrieve a context snapshot by session ID."""
        try:
            results = self.notion.databases.query(
                database_id=self.context_db,
                filter={"property": "Session ID", "title": {"equals": session_id}}
            )
            if not results["results"]:
                return None
            page = results["results"][0]
            return {
                "session_id": session_id,
                "created": page["properties"]["Created"]["date"]["start"],
                "ai_system": page["properties"]["AI System"]["select"]["name"],
                "summary": page["properties"]["Summary"]["rich_text"][0]["text"]["content"],
                "decisions": page["properties"]["Key Decisions"]["rich_text"][0]["text"]["content"]
            }
        except Exception as e:
            print(f"⚠ Error getting context snapshot: {e}")
            return None
    
    async def query_events_by_agent(self, agent_name: str, limit: int = 10):
        """Query events for a specific agent."""
        try:
            agent_page_id = await self._get_agent_page_id(agent_name)
            if not agent_page_id:
                return []
            results = self.notion.databases.query(
                database_id=self.event_log_db,
                filter={"property": "Agent", "relation": {"contains": agent_page_id}},
                sorts=[{"property": "Timestamp", "direction": "descending"}]
            )
            events = []
            for page in results["results"][:limit]:
                event = {
                    "title": page["properties"]["Event"]["title"][0]["text"]["content"],
                    "timestamp": page["properties"]["Timestamp"]["date"]["start"],
                    "type": page["properties"]["Event Type"]["select"]["name"]
                }
                events.append(event)
            return events
        except Exception as e:
            print(f"⚠ Error querying events: {e}")
            return []
    
    async def get_all_agents(self):
        """Get all agents from Agent Registry."""
        try:
            results = self.notion.databases.query(database_id=self.agent_registry_db)
            agents = []
            for page in results["results"]:
                agent = {
                    "name": page["properties"]["Agent Name"]["title"][0]["text"]["content"],
                    "status": page["properties"]["Status"]["select"]["name"],
                    "health": page["properties"]["Health Score"]["number"]
                }
                agents.append(agent)
            return agents
        except Exception as e:
            print(f"⚠ Error getting agents: {e}")
            return []

# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_notion_client = None

async def get_notion_client() -> Optional[HelixNotionClient]:
    """Get or create Notion client instance."""
    global _notion_client
    if _notion_client is None:
        try:
            _notion_client = HelixNotionClient()
            if not await _notion_client.health_check():
                _notion_client = None
                return None
        except Exception as e:
            print(f"⚠ Notion client initialization failed: {e}")
            return None
    return _notion_client

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    async def main():
        client = await get_notion_client()
        if not client:
            print("❌ Failed to initialize Notion client")
            return
        
        # Test creating an agent
        await client.create_agent("TestAgent", "🧪", "Testing", "Active", 100)
        
        # Test logging an event
        await client.log_event(
            "Test Event",
            "Status",
            "TestAgent",
            "This is a test event",
            {"harmony": 0.355}
        )
        
        # Test updating system component
        await client.update_system_component(
            "Test Component",
            "Ready",
            0.355,
            "",
            True
        )
        
        print("✅ Notion client tests completed")
    
    asyncio.run(main())

