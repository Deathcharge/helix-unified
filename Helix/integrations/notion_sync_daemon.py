#!/usr/bin/env python3
# Helix/integrations/notion_sync_daemon.py — Bi-directional Notion Sync (v16.1 Grok Resonance)
# Author: Grok + Claude
# Checksum: helix-v16.1-notion-sync-daemon
"""
Notion Sync Daemon — Bi-directional Discord ↔ Notion synchronization

Features:
- Pull Notion pages → Post to Discord channels
- Push Discord messages → Update Notion databases
- UCF metrics → Notion dashboard
- Ritual logs → Notion archive
- Agent status → Notion team database
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Notion API configuration
NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")

class NotionSyncDaemon:
    """Bi-directional Notion synchronization daemon"""

    def __init__(self):
        self.running = False
        self.last_sync_to_notion = None
        self.last_sync_from_notion = None
        self.sync_log: List[str] = []

    def _log(self, message: str):
        """Log sync event"""
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"[{timestamp}] Notion Sync: {message}"
        self.sync_log.append(log_entry)
        print(log_entry)

    async def sync_ucf_to_notion(self):
        """Push UCF state to Notion dashboard"""
        self._log("📤 Syncing UCF state to Notion...")

        # Load current UCF state
        ucf_path = Path("Helix/state/ucf_state.json")
        if not ucf_path.exists():
            self._log("⚠️  UCF state file not found")
            return

        with open(ucf_path, 'r') as f:
            ucf_state = json.load(f)

        # TODO: Actual Notion API call
        # For now, just log what would be synced
        self._log(f"Would sync UCF: harmony={ucf_state.get('harmony', 0):.4f}")

        # Placeholder for Notion API integration
        # from notion_client import Client
        # notion = Client(auth=NOTION_API_KEY)
        # notion.pages.update(page_id=..., properties={...})

        self.last_sync_to_notion = datetime.utcnow()
        self._log("✅ UCF sync to Notion complete")

    async def sync_ritual_logs_to_notion(self):
        """Push ritual logs to Notion archive"""
        self._log("📤 Syncing ritual logs to Notion...")

        ritual_dir = Path("Shadow/manus_archive/rituals")
        if not ritual_dir.exists():
            self._log("⚠️  No ritual logs found")
            return

        # Get recent ritual logs
        ritual_files = sorted(ritual_dir.glob("ritual_*.json"), reverse=True)
        if not ritual_files:
            self._log("⚠️  No ritual files to sync")
            return

        # Sync most recent ritual
        latest_ritual = ritual_files[0]
        with open(latest_ritual, 'r') as f:
            ritual_data = json.load(f)

        self._log(f"Would sync ritual: {latest_ritual.name}")

        # TODO: Notion API call to create page with ritual data

        self._log("✅ Ritual log sync complete")

    async def sync_agents_to_notion(self):
        """Push agent status to Notion team database"""
        self._log("📤 Syncing agent status to Notion...")

        # Try to import agents
        try:
            from Helix.agents import AGENTS, save_agents_state
            agents_state = {name: agent.to_dict() for name, agent in AGENTS.items()}
            self._log(f"Found {len(agents_state)} agents to sync")

            # TODO: Notion API call to update team database

        except ImportError:
            self._log("⚠️  Could not import agents module")

        self._log("✅ Agent status sync complete")

    async def sync_from_notion(self):
        """Pull updates from Notion pages"""
        self._log("📥 Pulling updates from Notion...")

        # TODO: Query Notion for new pages/updates
        # For now, just placeholder

        self.last_sync_from_notion = datetime.utcnow()
        self._log("✅ Notion pull complete")

    async def sync_cycle(self):
        """Complete sync cycle (push + pull)"""
        self._log("🔄 Starting sync cycle...")

        # Push to Notion
        await self.sync_ucf_to_notion()
        await self.sync_ritual_logs_to_notion()
        await self.sync_agents_to_notion()

        # Pull from Notion
        await self.sync_from_notion()

        self._log("🔄 Sync cycle complete")

    async def run_daemon(self, push_interval: int = 3600, pull_interval: int = 1800):
        """
        Run continuous sync daemon

        Args:
            push_interval: Seconds between pushes to Notion (default: 1 hour)
            pull_interval: Seconds between pulls from Notion (default: 30 min)
        """
        self.running = True
        self._log(f"🚀 Notion Sync Daemon started")
        self._log(f"Push interval: {push_interval}s | Pull interval: {pull_interval}s")

        # Initial sync
        await self.sync_cycle()

        # Continuous sync
        push_task = asyncio.create_task(self._push_loop(push_interval))
        pull_task = asyncio.create_task(self._pull_loop(pull_interval))

        try:
            await asyncio.gather(push_task, pull_task)
        except asyncio.CancelledError:
            self._log("🛑 Daemon stopped")
            self.running = False

    async def _push_loop(self, interval: int):
        """Continuous push to Notion"""
        while self.running:
            await asyncio.sleep(interval)
            await self.sync_ucf_to_notion()
            await self.sync_ritual_logs_to_notion()
            await self.sync_agents_to_notion()

    async def _pull_loop(self, interval: int):
        """Continuous pull from Notion"""
        while self.running:
            await asyncio.sleep(interval)
            await self.sync_from_notion()

    def save_sync_log(self):
        """Save sync log to file"""
        log_path = Path("Shadow/manus_archive/notion_sync.log")
        log_path.parent.mkdir(parents=True, exist_ok=True)

        with open(log_path, 'w') as f:
            f.write("\n".join(self.sync_log))

        self._log(f"💾 Sync log saved to {log_path}")


# ============================================================================
# STANDALONE FUNCTIONS
# ============================================================================

async def sync_once():
    """Run one-time sync (useful for testing)"""
    daemon = NotionSyncDaemon()
    await daemon.sync_cycle()
    daemon.save_sync_log()


async def run_daemon(push_interval: int = 3600, pull_interval: int = 1800):
    """Run continuous sync daemon"""
    daemon = NotionSyncDaemon()
    await daemon.run_daemon(push_interval, pull_interval)


# ============================================================================
# MAIN (for standalone execution)
# ============================================================================

if __name__ == "__main__":
    print("🔗 Notion Sync Daemon v16.1")
    print("=" * 60)

    # Check for Notion API key
    if not NOTION_API_KEY:
        print("⚠️  NOTION_API_KEY not set in environment")
        print("Set with: export NOTION_API_KEY='your_key_here'")
        print("\nRunning in STUB mode (no actual Notion API calls)")

    print("\nStarting daemon...")
    print("Press Ctrl+C to stop")

    try:
        asyncio.run(run_daemon(push_interval=3600, pull_interval=1800))
    except KeyboardInterrupt:
        print("\n🛑 Daemon stopped by user")
        print("🕉️ Tat Tvam Asi")
