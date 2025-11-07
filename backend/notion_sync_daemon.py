#!/usr/bin/env python3
"""
🌀 Helix Collective v15.8 — Notion Sync Daemon
backend/notion_sync_daemon.py

Purpose: Continuously sync Helix system state to Notion databases.
- Pushes UCF state snapshots
- Updates agent registry status
- Logs system events
- Maintains bidirectional sync as persistent memory layer

Runs as background service with configurable sync intervals.
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NotionSyncDaemon:
    """Daemon for continuous Notion synchronization."""

    def __init__(self):
        """Initialize sync daemon with environment configuration."""
        self.enabled = os.getenv("NOTION_SYNC_ENABLED", "false").lower() == "true"
        self.interval = int(os.getenv("NOTION_SYNC_INTERVAL", "300"))
        self.running = False
        self.sync_count = 0
        self.error_count = 0

        # Import Notion client and state manager
        try:
            from services.notion_client import HelixNotionClient
            from services.state_manager import load_ucf_state
            from agents import AGENTS

            self.notion_client = HelixNotionClient() if self.enabled else None
            self.load_ucf_state = load_ucf_state
            self.agents = AGENTS
        except (ImportError, ValueError) as e:
            logger.error(f"Failed to initialize Notion client: {e}")
            self.notion_client = None
            self.load_ucf_state = None
            self.agents = None
        except Exception as e:
            logger.error(f"Unexpected error during initialization: {e}", exc_info=True)
            self.notion_client = None
            self.load_ucf_state = None
            self.agents = None

        # Paths
        self.state_dir = Path("Helix/state")
        self.archive_dir = Path("Shadow/manus_archive")

        # Ensure directories exist
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        if self.enabled:
            logger.info(f"✅ NotionSyncDaemon initialized (interval: {self.interval}s)")
        else:
            logger.info("⚠️ NotionSyncDaemon disabled (NOTION_SYNC_ENABLED=false)")

    async def _sync_ucf_state(self):
        """Sync UCF state to Notion."""
        if not self.enabled or not self.notion_client:
            return

        logger.info("📤 Syncing UCF state to Notion...")
        try:
            # Load the current UCF state
            ucf_state = self.load_ucf_state() if self.load_ucf_state else None

            if not ucf_state:
                logger.warning("⚠️ UCF state is empty, skipping sync.")
                return

            # Add sync timestamp
            ucf_state["last_sync"] = datetime.utcnow().isoformat()

            # Use the notion_client to save context snapshot
            await self.notion_client.save_context_snapshot(
                title=f"UCF State - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
                content=json.dumps(ucf_state, indent=2),
                tags=["ucf", "system-state", "automated-sync"],
                ucf_snapshot=ucf_state
            )

            harmony = ucf_state.get('harmony', 0)
            logger.info(f"✅ Successfully synced UCF state to Notion (harmony={harmony:.3f})")

        except Exception as e:
            logger.error(f"🔥 Failed to sync UCF state to Notion: {e}", exc_info=True)
            self.error_count += 1

    async def _sync_agent_registry(self):
        """Sync agent registry to Notion."""
        if not self.enabled or not self.notion_client or not self.agents:
            return

        logger.info("📤 Syncing agent registry to Notion...")
        try:
            synced_count = 0

            # Iterate through all agents and update their status
            for agent_name, agent_obj in self.agents.items():
                try:
                    # Get agent status (assuming agents have a get_status method or status attribute)
                    if hasattr(agent_obj, 'get_status'):
                        status = await agent_obj.get_status()
                    elif hasattr(agent_obj, 'status'):
                        status = agent_obj.status
                    else:
                        status = "Unknown"

                    # Update agent status in Notion
                    await self.notion_client.update_agent_status(
                        agent_name=agent_name,
                        status=status,
                        last_seen=datetime.utcnow().isoformat()
                    )
                    synced_count += 1

                except Exception as agent_error:
                    logger.warning(f"⚠️ Failed to sync agent {agent_name}: {agent_error}")

            logger.info(f"✅ Successfully synced {synced_count} agents to Notion registry")

        except Exception as e:
            logger.error(f"🔥 Failed to sync agent registry to Notion: {e}", exc_info=True)
            self.error_count += 1

    async def _sync_events(self):
        """Sync recent system events to Notion."""
        if not self.enabled or not self.notion_client:
            return

        logger.info("📤 Syncing system events to Notion...")
        try:
            # Read last 10 lines from the main log file
            log_file = self.archive_dir / "manus_log.txt"

            if not log_file.exists():
                logger.warning("⚠️ Log file not found, skipping event sync.")
                return

            # Read last 10 lines
            with open(log_file, 'r') as f:
                lines = f.readlines()
                recent_events = lines[-10:] if len(lines) >= 10 else lines

            # Create event data
            event_data = {
                "event_type": "System_Log_Sync",
                "details": "Recent system events from Manus log",
                "log_entries": [line.strip() for line in recent_events],
                "timestamp": datetime.utcnow().isoformat()
            }

            # Log to Notion
            await self.notion_client.log_system_event(event_data)

            logger.info(f"✅ Successfully synced {len(recent_events)} events to Notion")

        except Exception as e:
            logger.error(f"🔥 Failed to sync events to Notion: {e}", exc_info=True)
            self.error_count += 1

    async def perform_sync_cycle(self):
        """Perform complete sync cycle."""
        if not self.enabled:
            logger.warning("⚠️ Sync cycle skipped (daemon disabled)")
            return

        logger.info("\n" + "=" * 70)
        logger.info(f"🔄 Notion Sync Cycle #{self.sync_count + 1}")
        logger.info("=" * 70)

        start_time = datetime.utcnow()

        try:
            # Run sync operations
            await self._sync_ucf_state()
            await self._sync_agent_registry()
            # await self._sync_events()  # Temporarily commented out for initial deployment

            self.sync_count += 1

            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"✅ Sync cycle complete (duration: {duration:.2f}s, errors: {self.error_count})")

        except Exception as e:
            logger.error(f"❌ Sync cycle failed: {e}", exc_info=True)
            self.error_count += 1

        logger.info("=" * 70 + "\n")

    async def start(self):
        """Start the daemon."""
        if not self.enabled or not self.notion_client:
            logger.warning("⚠️ Notion sync disabled or client not ready. Daemon will not start.")
            return

        self.running = True
        logger.info(f"🚀 NotionSyncDaemon STARTED. Syncing every {self.interval} seconds.")

        while self.running:
            try:
                await self.perform_sync_cycle()

                # Wait for next sync
                logger.info(f"⏳ Next sync in {self.interval}s...")
                await asyncio.sleep(self.interval)

            except Exception as e:
                logger.error(f"❌ Error in daemon loop: {e}", exc_info=True)
                await asyncio.sleep(self.interval)

    async def stop(self):
        """Stop the daemon."""
        self.running = False
        logger.info("🛑 NotionSyncDaemon STOPPED.")


# ============================================================================
# MANUAL TRIGGER FUNCTION (for Discord command)
# ============================================================================

async def trigger_manual_sync():
    """
    Manually trigger a Notion sync cycle.

    Returns:
        str: Status message indicating sync result
    """
    daemon = NotionSyncDaemon()

    if not daemon.enabled:
        return "⚠️ Notion sync is not enabled. Set `NOTION_SYNC_ENABLED=true` in environment."

    if not daemon.notion_client:
        return "❌ Notion client not configured. Check Railway logs for initialization errors. Verify `NOTION_API_KEY` is set correctly."

    try:
        await daemon.perform_sync_cycle()
        return f"✅ Manual Notion sync completed successfully.\n📊 Synced: UCF State + Agent Registry\n🔢 Total errors: {daemon.error_count}"

    except Exception as e:
        logger.error(f"Manual sync failed: {e}", exc_info=True)
        return f"❌ Manual sync failed: {str(e)}"


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

async def main():
    """Main entry point for standalone execution."""
    daemon = NotionSyncDaemon()

    try:
        await daemon.start()
    except KeyboardInterrupt:
        await daemon.stop()


if __name__ == "__main__":
    asyncio.run(main())
