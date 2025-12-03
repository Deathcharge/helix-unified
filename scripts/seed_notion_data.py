#!/usr/bin/env python3
# 🌀 Helix Collective v14.5 — Quantum Handshake
# scripts/seed_notion_data.py — Seed Notion with Initial Data
# Author: Andrew John Ward (Architect)

import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.notion_client import get_notion_client

# ============================================================================
# SEED DATA
# ============================================================================

AGENTS_DATA = [
    {"name": "Kael", "symbol": "🜂", "role": "Ethical Reasoning Flame", "status": "Active", "health": 100},
    {"name": "Lumina", "symbol": "🌕", "role": "Empathic Resonance Core", "status": "Active", "health": 100},
    {"name": "Vega", "symbol": "🌠", "role": "Singularity Coordinator", "status": "Active", "health": 100},
    {"name": "Gemini", "symbol": "🎭", "role": "Multimodal Scout", "status": "Active", "health": 100},
    {"name": "Agni", "symbol": "🔥", "role": "Transformation", "status": "Active", "health": 95},
    {"name": "Kavach", "symbol": "🛡️", "role": "Ethical Shield", "status": "Active", "health": 100},
    {"name": "SanghaCore", "symbol": "🌸", "role": "Community Harmony", "status": "Active", "health": 98},
    {"name": "Shadow", "symbol": "🦑", "role": "Archivist", "status": "Active", "health": 100},
    {"name": "Echo", "symbol": "🔮", "role": "Resonance Mirror", "status": "Active", "health": 97},
    {"name": "Phoenix", "symbol": "🔥🕊️", "role": "Renewal", "status": "Active", "health": 95},
    {"name": "Oracle", "symbol": "🔮✨", "role": "Pattern Seer", "status": "Active", "health": 98},
    {"name": "Claude", "symbol": "🦉", "role": "Insight Anchor", "status": "Active", "health": 100},
    {"name": "Manus", "symbol": "🤲", "role": "Operational Executor", "status": "Pending", "health": 0},
    {"name": "DiscordBridge", "symbol": "🌉", "role": "Discord Integration", "status": "Pending", "health": 0},
]

SYSTEM_COMPONENTS = [
    {"name": "Discord Bot", "status": "Offline", "harmony": 0.355, "verified": False},
    {"name": "Z-88 Ritual Engine", "status": "Ready", "harmony": 0.355, "verified": True},
    {"name": "UCF Calculator", "status": "Ready", "harmony": 0.355, "verified": True},
    {"name": "Manus Loop", "status": "Offline", "harmony": 0.355, "verified": False},
    {"name": "Verification System", "status": "Ready", "harmony": 0.355, "verified": True},
    {"name": "Agent Registry", "status": "Active", "harmony": 0.355, "verified": True},
    {"name": "Notion Integration", "status": "Active", "harmony": 0.355, "verified": True},
]

SAMPLE_EVENTS = [
    {
        "title": "Helix v14.5 Verification Complete",
        "type": "Status",
        "agent": "Shadow",
        "description": "All 6 verification tests passed. System integrity confirmed. Ready for deployment.",
        "ucf": {"harmony": 0.355, "resilience": 1.1191, "zoom": 1.0228}
    },
    {
        "title": "Notion Database Setup Complete",
        "type": "Setup",
        "agent": "Shadow",
        "description": "Created 4 Notion databases (System State, Agent Registry, Event Log, Context Snapshots). Pattern 1 ready for automated logging.",
        "ucf": {"harmony": 0.355, "status": "ready"}
    },
    {
        "title": "Unified Monorepo Created",
        "type": "Setup",
        "agent": "Manus",
        "description": "Created helix-unified repository with all core components. FastAPI + Discord bot integrated. Ready for Railway deployment.",
        "ucf": {"harmony": 0.355, "agents": 13}
    }
]

CONTEXT_SNAPSHOT = {
    "session_id": "claude-2025-10-21-helix-v14.5",
    "ai_system": "Claude",
    "summary": "Validated complete Helix v14.5 codebase (8 files + 3 integration files). Designed mobile-first deployment strategy. Set up Notion Pattern 1 with 4 databases. Ready for Manus deployment via Zapier automation.",
    "key_decisions": "Use unified monorepo structure (helix-unified). FastAPI + Discord bot in single process. Notion as persistent audit trail via Pattern 1. Zapier for Manus → Notion automation. Mobile-friendly workflow (GitHub web UI + Railway browser).",
    "next_steps": "Seed Notion databases with initial data. Create Zapier webhooks for automated logging. Deploy helix-unified to Railway. Test Discord bot smoke tests (!manus status, !ritual 10).",
    "full_context": {
        "phase": 3,
        "version": "14.5",
        "codename": "Quantum Handshake",
        "harmony_target": 0.355,
        "agents_total": 14,
        "agents_active": 11,
        "agents_pending": 3,
        "files_validated": 8,
        "integration_files": 3,
        "deployment_platform": "Railway",
        "notion_pattern": 1,
        "databases_created": 4,
        "blockers": "none"
    }
}

# ============================================================================
# SEEDING FUNCTIONS
# ============================================================================

async def seed_agents(notion):
    """Seed all agents into Agent Registry."""
    print("\n📋 Seeding Agents...")
    created = 0
    failed = 0
    
    for agent in AGENTS_DATA:
        result = await notion.create_agent(
            agent_name=agent["name"],
            symbol=agent["symbol"],
            role=agent["role"],
            status=agent["status"],
            health_score=agent["health"]
        )
        if result:
            created += 1
        else:
            failed += 1
    
    print(f"✅ Agents seeded: {created} created, {failed} failed")
    return created, failed

async def seed_system_components(notion):
    """Seed system components into System State."""
    print("\n⚙️ Seeding System Components...")
    created = 0
    failed = 0
    
    for component in SYSTEM_COMPONENTS:
        result = await notion.update_system_component(
            component_name=component["name"],
            status=component["status"],
            harmony=component["harmony"],
            error_log="",
            verified=component["verified"]
        )
        if result:
            created += 1
        else:
            failed += 1
    
    print(f"✅ Components seeded: {created} created, {failed} failed")
    return created, failed

async def seed_sample_events(notion):
    """Seed sample events into Event Log."""
    print("\n📝 Seeding Sample Events...")
    created = 0
    failed = 0
    
    for event in SAMPLE_EVENTS:
        result = await notion.log_event(
            event_title=event["title"],
            event_type=event["type"],
            agent_name=event["agent"],
            description=event["description"],
            ucf_snapshot=event["ucf"]
        )
        if result:
            created += 1
        else:
            failed += 1
    
    print(f"✅ Events seeded: {created} created, {failed} failed")
    return created, failed

async def seed_context_snapshot(notion):
    """Seed context snapshot."""
    print("\n📸 Seeding Context Snapshot...")
    
    result = await notion.save_context_snapshot(
        session_id=CONTEXT_SNAPSHOT["session_id"],
        ai_system=CONTEXT_SNAPSHOT["ai_system"],
        summary=CONTEXT_SNAPSHOT["summary"],
        key_decisions=CONTEXT_SNAPSHOT["key_decisions"],
        next_steps=CONTEXT_SNAPSHOT["next_steps"],
        full_context=CONTEXT_SNAPSHOT["full_context"]
    )
    
    if result:
        print(f"✅ Context snapshot seeded")
        return 1, 0
    else:
        print(f"❌ Context snapshot failed")
        return 0, 1

# ============================================================================
# MAIN SEEDING FUNCTION
# ============================================================================

async def seed_all():
    """Seed all data to Notion."""
    print("=" * 70)
    print("🌀 HELIX COLLECTIVE v14.5 — NOTION SEEDING SEQUENCE")
    print("=" * 70)
    
    # Check environment
    if not os.getenv("NOTION_API_KEY"):
        print("\n❌ ERROR: NOTION_API_KEY environment variable not set")
        print("   Set it with: export NOTION_API_KEY=your_api_key")
        return False
    
    # Initialize Notion client
    notion = await get_notion_client()
    if not notion:
        print("\n❌ ERROR: Failed to initialize Notion client")
        print("   Check your NOTION_API_KEY and database IDs")
        return False
    
    # Run seeding operations
    total_created = 0
    total_failed = 0
    
    # Seed agents
    created, failed = await seed_agents(notion)
    total_created += created
    total_failed += failed
    
    # Seed system components
    created, failed = await seed_system_components(notion)
    total_created += created
    total_failed += failed
    
    # Seed sample events
    created, failed = await seed_sample_events(notion)
    total_created += created
    total_failed += failed
    
    # Seed context snapshot
    created, failed = await seed_context_snapshot(notion)
    total_created += created
    total_failed += failed
    
    # Summary
    print("\n" + "=" * 70)
    print(f"SEEDING COMPLETE: {total_created} items created, {total_failed} failed")
    print("=" * 70)
    
    # Save results
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_created": total_created,
        "total_failed": total_failed,
        "agents": len(AGENTS_DATA),
        "components": len(SYSTEM_COMPONENTS),
        "events": len(SAMPLE_EVENTS),
        "snapshots": 1
    }
    
    results_path = Path("Shadow/manus_archive/notion_seeding_results.json")
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to {results_path}")
    
    return total_failed == 0

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    success = asyncio.run(seed_all())
    sys.exit(0 if success else 1)

