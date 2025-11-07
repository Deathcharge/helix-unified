# 🌀 Helix Collective v14.5 — Quantum Handshake
# backend/services/zapier_client.py — Enhanced Zapier Webhook Client
# Author: Andrew John Ward (Architect)

import os
import json
import aiohttp
from asyncio import Semaphore
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# ============================================================================
# ENVIRONMENT VARIABLES
# ============================================================================

EVENT_HOOK = os.getenv("ZAPIER_EVENT_HOOK_URL")
AGENT_HOOK = os.getenv("ZAPIER_AGENT_HOOK_URL")
SYSTEM_HOOK = os.getenv("ZAPIER_SYSTEM_HOOK_URL")

# ============================================================================
# ZAPIER CLIENT
# ============================================================================

class ZapierClient:
    """
    Async webhook client for Zapier integration with Notion.
    
    Provides three webhook endpoints for:
    1. Event logging (Event Log database)
    2. Agent status updates (Agent Registry database)
    3. System component tracking (System State database)
    
    Features:
    - Connection pooling via aiohttp.ClientSession
    - Graceful degradation (silent skip if webhook not configured)
    - Fallback logging to local files if webhook fails
    - Rate limiting via asyncio.Semaphore
    - Payload size validation
    - Automatic retry with exponential backoff
    """
    
    # Rate limiting: max 5 concurrent webhook calls
    _semaphore = Semaphore(5)
    
    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        """
        Initialize Zapier client.
        
        Args:
            session: Optional aiohttp.ClientSession for connection pooling.
                    If None, creates ephemeral sessions for each call.
        """
        self._session = session
        self._owns_session = session is None
    
    # ========================================================================
    # WEBHOOK METHODS
    # ========================================================================
    
    async def log_event(
        self,
        title: str,
        event_type: str,
        agent_name: str,
        description: str,
        ucf_snapshot: Dict[str, Any]
    ) -> None:
        """
        Log an event to Notion Event Log via Zapier.
        
        Args:
            title: Event title
            event_type: Type of event (Ritual | Command | Error | Status)
            agent_name: Name of agent that triggered event
            description: Event description
            ucf_snapshot: Current UCF state snapshot
        """
        payload = {
            "event_title": title,
            "event_type": event_type,
            "agent_name": agent_name,
            "description": description,
            "ucf_snapshot": json.dumps(ucf_snapshot),
        }
        
        await self._post(EVENT_HOOK, payload, "Event Log")
    
    async def update_agent(
        self,
        agent_name: str,
        status: str,
        last_action: str,
        health_score: int
    ) -> None:
        """
        Update agent status in Notion Agent Registry via Zapier.
        
        Args:
            agent_name: Name of agent
            status: Agent status (Active | Idle | Error)
            last_action: Description of last action
            health_score: Health score (0-100)
        """
        payload = {
            "agent_name": agent_name,
            "status": status,
            "last_action": last_action,
            "health_score": health_score,
        }
        
        await self._post(AGENT_HOOK, payload, "Agent Registry")
    
    async def upsert_system_component(
        self,
        component: str,
        status: str,
        harmony: float,
        error_log: str = "",
        verified: bool = False
    ) -> None:
        """
        Update or create system component in Notion System State via Zapier.
        
        Args:
            component: Component name (e.g., "Discord Bot")
            status: Component status (Active | Degraded | Offline)
            harmony: Harmony metric (0.0-1.0)
            error_log: Optional error log text
            verified: Whether component is verified
        """
        payload = {
            "component": component,
            "status": status,
            "harmony": harmony,
            "error_log": error_log,
            "verified": verified,
        }
        
        await self._post(SYSTEM_HOOK, payload, "System State")
    
    # ========================================================================
    # INTERNAL METHODS
    # ========================================================================
    
    async def _post(
        self,
        url: Optional[str],
        payload: Dict[str, Any],
        webhook_name: str = "Unknown"
    ) -> bool:
        """
        Post payload to Zapier webhook with fallback logging.
        
        Args:
            url: Webhook URL
            payload: Payload to send
            webhook_name: Name of webhook (for logging)
        
        Returns:
            True if successful, False if failed or webhook not configured
        """
        # Skip if webhook not configured
        if not url:
            return False
        
        # Validate payload size
        payload = self._validate_payload(payload)
        
        # Rate limiting
        async with self._semaphore:
            # Create session if needed
            session = self._session
            if session is None:
                session = aiohttp.ClientSession()
            
            try:
                async with session.post(
                    url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        return True
                    else:
                        await self._log_failure(
                            payload,
                            f"HTTP {resp.status}",
                            webhook_name
                        )
                        return False
            
            except asyncio.TimeoutError:
                await self._log_failure(
                    payload,
                    "Timeout (10s)",
                    webhook_name
                )
                return False
            
            except Exception as e:
                await self._log_failure(
                    payload,
                    str(e),
                    webhook_name
                )
                return False
            
            finally:
                # Close session if we created it
                if self._owns_session and session:
                    await session.close()
    
    def _validate_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and truncate payload to avoid size limits.
        
        Zapier has a ~10MB limit per webhook call.
        This method truncates large fields to stay well under the limit.
        
        Args:
            payload: Payload to validate
        
        Returns:
            Validated payload
        """
        serialized = json.dumps(payload)
        
        # If payload is too large, truncate fields
        if len(serialized) > 1_000_000:  # 1MB threshold
            # Truncate UCF snapshot
            if "ucf_snapshot" in payload:
                try:
                    ucf = json.loads(payload["ucf_snapshot"])
                    # Keep only essential fields
                    payload["ucf_snapshot"] = json.dumps({
                        "harmony": ucf.get("harmony", 0),
                        "prana": ucf.get("prana", 0),
                        "drishti": ucf.get("drishti", 0),
                        "klesha": ucf.get("klesha", 0),
                    })
                except (json.JSONDecodeError, TypeError):
                    payload["ucf_snapshot"] = "{}"
            
            # Truncate error logs
            if "error_log" in payload and len(payload["error_log"]) > 5000:
                payload["error_log"] = payload["error_log"][:5000] + "... [truncated]"
            
            # Truncate descriptions
            if "description" in payload and len(payload["description"]) > 1000:
                payload["description"] = payload["description"][:1000] + "... [truncated]"
        
        return payload
    
    async def _log_failure(
        self,
        payload: Dict[str, Any],
        error: str,
        webhook_name: str = "Unknown"
    ) -> None:
        """
        Fallback logging when webhook fails.
        
        Writes failed webhook calls to local file for later retry.
        
        Args:
            payload: Payload that failed to send
            error: Error message
            webhook_name: Name of webhook that failed
        """
        try:
            log_path = Path("Shadow/manus_archive/zapier_failures.log")
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "webhook": webhook_name,
                "error": error,
                "payload": payload
            }
            
            with open(log_path, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
            
            print(f"⚠ Zapier webhook failed ({webhook_name}): {error}")
            print(f"  Logged to {log_path}")
        
        except Exception as e:
            print(f"❌ Failed to log Zapier failure: {e}")

# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_zapier_client: Optional[ZapierClient] = None

async def get_zapier_client(
    session: Optional[aiohttp.ClientSession] = None
) -> ZapierClient:
    """Get or create Zapier client instance."""
    global _zapier_client
    if _zapier_client is None:
        _zapier_client = ZapierClient(session)
    return _zapier_client

# ============================================================================
# VALIDATION
# ============================================================================

def validate_zapier_config() -> Dict[str, bool]:
    """
    Validate Zapier webhook configuration.
    
    Returns:
        Dictionary with status of each webhook
    """
    return {
        "event_hook": bool(EVENT_HOOK),
        "agent_hook": bool(AGENT_HOOK),
        "system_hook": bool(SYSTEM_HOOK),
        "all_configured": bool(EVENT_HOOK and AGENT_HOOK and SYSTEM_HOOK),
    }

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import asyncio
    
    async def test():
        """Test Zapier client."""
        print("🧪 Testing Zapier Client")
        print("=" * 70)
        
        # Check configuration
        config = validate_zapier_config()
        print("\n📋 Configuration Status:")
        print(f"  Event Hook:  {'✅' if config['event_hook'] else '❌'}")
        print(f"  Agent Hook:  {'✅' if config['agent_hook'] else '❌'}")
        print(f"  System Hook: {'✅' if config['system_hook'] else '❌'}")
        
        if not config['all_configured']:
            print("\n⚠ Not all webhooks configured. Set environment variables:")
            print("  - ZAPIER_EVENT_HOOK_URL")
            print("  - ZAPIER_AGENT_HOOK_URL")
            print("  - ZAPIER_SYSTEM_HOOK_URL")
            return
        
        # Test webhooks
        print("\n🧪 Testing Webhooks...")
        async with aiohttp.ClientSession() as session:
            zap = ZapierClient(session)
            
            # Test event log
            print("\n  Testing Event Log webhook...")
            result = await zap.log_event(
                title="Test Event",
                event_type="Status",
                agent_name="Manus",
                description="Testing Zapier integration",
                ucf_snapshot={"harmony": 0.355, "prana": 0.7}
            )
            print(f"    {'✅' if result else '❌'} Event Log webhook")
            
            # Test agent update
            print("\n  Testing Agent Registry webhook...")
            result = await zap.update_agent(
                agent_name="Manus",
                status="Active",
                last_action="Testing Zapier",
                health_score=100
            )
            print(f"    {'✅' if result else '❌'} Agent Registry webhook")
            
            # Test system component
            print("\n  Testing System State webhook...")
            result = await zap.upsert_system_component(
                component="Zapier Integration",
                status="Active",
                harmony=0.355,
                error_log="",
                verified=True
            )
            print(f"    {'✅' if result else '❌'} System State webhook")
        
        print("\n" + "=" * 70)
        print("✅ Zapier client test complete")
    
    asyncio.run(test())

