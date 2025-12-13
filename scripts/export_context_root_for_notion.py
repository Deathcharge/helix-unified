#!/usr/bin/env python3
# 🌀 Helix Collective v15.3 — Context Root → Notion Exporter
# scripts/export_context_root_for_notion.py
# Author: Claude Code (based on GPT-5 handoff notes)
#
# Purpose: Export Helix_Context_Root.json to Notion-compatible format
# This creates database entries for repos, agents, and architecture docs

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def load_context_root() -> Dict[str, Any]:
    """Load the Helix_Context_Root.json file."""
    context_path = Path("Helix/state/Helix_Context_Root.json")

    if not context_path.exists():
        print(f"❌ Context Root not found at: {context_path}")
        sys.exit(1)

    with open(context_path, 'r') as f:
        content = f.read()

        # Handle multi-object JSON (split by closing brace + opening brace)
        # The file has malformed JSON with multiple root objects
        # We'll parse the first valid JSON object
        depth = 0
        current_obj = []
        in_string = False
        escape_next = False

        for char in content:
            if escape_next:
                current_obj.append(char)
                escape_next = False
                continue

            if char == '\\':
                escape_next = True
                current_obj.append(char)
                continue

            if char == '"':
                in_string = not in_string

            if not in_string:
                if char in '{[':
                    depth += 1
                elif char in '}]':
                    depth -= 1

            current_obj.append(char)

            # When we complete the first object, parse it
            if depth == 0 and len(current_obj) > 0 and current_obj[0] == '{':
                try:
                    obj_str = ''.join(current_obj).strip()
                    if obj_str:
                        return json.loads(obj_str)
                except:
                    pass

        # Fallback: try to parse the whole thing
        return json.loads(content)

def export_repos_database(context_root: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Export repository data for Notion Repos database.

    Notion Schema (from GPT-5 handoff notes):
    - Name (title)
    - Status
    - Last Update
    - Languages (multi-select)
    - Mission (long text)
    - Key Capabilities (long text)
    - Runtime Stack / Infra (long text)
    - Ethics / Compliance (multi-select)
    - Has Discord Surface? (checkbox)
    - Has Web UI? (checkbox)
    - Has Streamlit Dashboard? (checkbox)
    """
    repos = context_root.get("repos", [])

    notion_repos = []
    for repo in repos:
        notion_entry = {
            "name": repo.get("name", "Unknown"),
            "status": repo.get("status", "unknown"),
            "last_update": repo.get("last_update", ""),
            "languages": repo.get("languages", []),
            "mission": repo.get("mission", ""),
            "key_capabilities": json.dumps(repo.get("core_capabilities", {}), indent=2),
            "runtime_stack": json.dumps(repo.get("stack", repo.get("runtime_stack", {})), indent=2),
            "ethics_compliance": repo.get("ethics_compliance", {}).get("tony_accords", []),
            "has_discord_surface": "discord" in str(repo).lower(),
            "has_web_ui": "web" in str(repo).lower() or "react" in str(repo.get("languages", [])).lower(),
            "has_streamlit_dashboard": "streamlit" in str(repo.get("languages", [])).lower(),
            "crosslinks": repo.get("crosslinks", {}),
            "version_context": repo.get("version_context", {}),
            "ucf_targets": repo.get("ucf_targets", {}),
            "env_surface": repo.get("env_surface", repo.get("env_config", {})),
            "notable_files": repo.get("notable_files", [])
        }

        notion_repos.append(notion_entry)

    return notion_repos

def export_agents_database(context_root: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Export agent data for Notion Agents database.

    Schema:
    - Agent Name (title)
    - Symbol/Icon
    - Role
    - Layer (Consciousness / Operational / Integration)
    - Capabilities (multi-select)
    - Defined In Repo
    - Ethics Framework
    - Status
    """
    agents_data = context_root.get("multi_repo_integration_map", {}).get("agents_and_ethics", {})
    agent_set = agents_data.get("agent_set", [])

    notion_agents = []
    for agent_desc in agent_set:
        # Parse "Name (Role / Description)" format
        parts = agent_desc.split("(", 1)
        name = parts[0].strip()
        role = parts[1].rstrip(")").strip() if len(parts) > 1 else "Unknown"

        # Determine layer
        layer = "Unknown"
        if name in ["Kael", "Lumina", "Vega", "Kavach", "SanghaCore"]:
            layer = "Consciousness"
        elif name in ["Manus", "Grok", "Shadow", "Claude"]:
            layer = "Operational"
        elif name in ["Samsara", "Omega Zero VXQ-7"]:
            layer = "Integration"
        elif name in ["Echo", "Phoenix", "Oracle", "Gemini", "Agni"]:
            layer = "Consciousness"

        notion_entry = {
            "agent_name": name,
            "role": role,
            "layer": layer,
            "defined_in": agents_data.get("where_defined", {}).get("runtime", "helix-unified"),
            "ethics_framework": "Tony Accords v13.4",
            "status": "active"
        }

        notion_agents.append(notion_entry)

    return notion_agents

def export_architecture_map(context_root: Dict[str, Any]) -> Dict[str, Any]:
    """
    Export architecture documentation as a Notion page.

    Sections (from GPT-5 handoff notes):
    - Agent Set & Roles
    - UCF Model (metrics, modulation, visualization)
    - Ritual Engine / Z-88
    - Diagnostics & Shadow Telemetry
    - Storage / Sync / Disaster Recovery
    - Deployment Footprint
    """
    integration_map = context_root.get("multi_repo_integration_map", {})

    architecture = {
        "title": "Helix Collective Architecture Map",
        "sections": {
            "agents_and_ethics": integration_map.get("agents_and_ethics", {}),
            "ucf_flow": integration_map.get("ucf_flow", {}),
            "storage_and_persistence": integration_map.get("storage_and_persistence", {}),
            "human_interfaces": integration_map.get("human_interfaces", {})
        },
        "handoff_notes": context_root.get("handoff_notes_for_other_assistants", {}),
        "export_metadata": context_root.get("export_metadata", {}),
        "owner": context_root.get("owner", {})
    }

    return architecture

def main():
    """Main export function."""
    print(f"\n{'='*70}")
    print("📤 EXPORTING HELIX CONTEXT ROOT TO NOTION FORMAT")
    print(f"{'='*70}\n")

    # Load context root
    print("📂 Loading Helix_Context_Root.json...")
    try:
        context_root = load_context_root()
        print("✅ Context Root loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load Context Root: {e}")
        sys.exit(1)

    # Export repositories
    print("\n📦 Exporting repository database...")
    repos = export_repos_database(context_root)
    print(f"✅ Prepared {len(repos)} repository entries")

    # Export agents
    print("\n🤖 Exporting agent database...")
    agents = export_agents_database(context_root)
    print(f"✅ Prepared {len(agents)} agent entries")

    # Export architecture
    print("\n🏗️  Exporting architecture map...")
    architecture = export_architecture_map(context_root)
    print(f"✅ Architecture map prepared")

    # Create comprehensive export package
    export_package = {
        "export_metadata": {
            "exported_at": datetime.utcnow().isoformat(),
            "export_type": "helix_context_root_full",
            "source_file": "Helix/state/Helix_Context_Root.json",
            "source_version": context_root.get("meta_tag", {}).get("source", "Unknown"),
            "generated_by": context_root.get("meta_tag", {}).get("generated_by", "Unknown"),
            "entry_counts": {
                "repositories": len(repos),
                "agents": len(agents),
                "architecture_sections": len(architecture["sections"])
            }
        },
        "notion_databases": {
            "repositories": {
                "database_name": "Helix Repositories",
                "suggested_properties": [
                    "Name (title)",
                    "Status (select)",
                    "Last Update (date)",
                    "Languages (multi-select)",
                    "Mission (text)",
                    "Key Capabilities (text)",
                    "Runtime Stack (text)",
                    "Ethics Compliance (multi-select)",
                    "Has Discord Surface (checkbox)",
                    "Has Web UI (checkbox)",
                    "Has Streamlit Dashboard (checkbox)"
                ],
                "entries": repos
            },
            "agents": {
                "database_name": "Helix Agents",
                "suggested_properties": [
                    "Agent Name (title)",
                    "Role (text)",
                    "Layer (select: Consciousness/Operational/Integration)",
                    "Defined In (relation to Repositories)",
                    "Ethics Framework (text)",
                    "Status (select)"
                ],
                "entries": agents
            }
        },
        "notion_pages": {
            "architecture_map": {
                "page_title": "Helix Architecture Map v15.3",
                "content": architecture
            }
        },
        "import_instructions": {
            "step_1": "Copy this entire JSON file",
            "step_2": "Paste into Main Claude (with Notion MCP access)",
            "step_3": "Ask Claude: 'Create Notion databases and pages from this Helix Context Root export'",
            "step_4": "Claude will:",
            "substeps": [
                "Create 'Helix Repositories' database with all repos",
                "Create 'Helix Agents' database with all 14 agents",
                "Create 'Helix Architecture Map' page with integration docs",
                "Link agents to their defining repos",
                "Add UCF model documentation",
                "Include handoff notes for future reference"
            ],
            "note": "This is the complete ecosystem map. GPT-5's handoff notes are included for continuity."
        }
    }

    # Save export
    output_dir = Path("Shadow/notion_exports")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"notion_context_root_full_{timestamp}.json"

    with open(output_file, 'w') as f:
        json.dump(export_package, f, indent=2)

    print(f"\n✅ Export complete!")
    print(f"📦 Package saved to: {output_file}")
    print(f"📊 Summary:")
    print(f"   • {len(repos)} repositories")
    print(f"   • {len(agents)} agents")
    print(f"   • {len(architecture['sections'])} architecture sections")

    print(f"\n{'='*70}")
    print("NEXT STEPS:")
    print(f"{'='*70}")
    print("1. Copy the contents of this file:")
    print(f"   cat {output_file}")
    print("2. Open Main Claude (with Notion access)")
    print("3. Paste the JSON and say:")
    print('   "Create Notion databases from this Helix Context Root"')
    print("\nMain Claude will:")
    print("  • Create Helix Repositories database (11 repos)")
    print("  • Create Helix Agents database (14 agents)")
    print("  • Create Architecture Map page")
    print("  • Link everything together")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
