#!/usr/bin/env python3
# backend/agents/verify_blueprints.py
# Helix v15.2 Blueprint Verification & Combination Tool

import glob
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path("Helix/agents/blueprints")
STATE = Path("Helix/state")


def checksum(data: dict) -> str:
    """Generate SHA256 checksum of blueprint data."""
    return hashlib.sha256(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()[:12]


def verify():
    """Verify all agent blueprints and create combined file."""
    print("🌀 Helix v15.2 Blueprint Verification")
    print("=" * 50)

    # Load manifest
    manifest_path = STATE / "blueprints_manifest.json"
    if not manifest_path.exists():
        print("❌ blueprints_manifest.json not found!")
        sys.exit(1)

    manifest = json.load(open(manifest_path))
    expected = set(manifest["agents"])

    # Find all blueprint files (excluding combined file)
    found_files = {
        Path(f).name for f in glob.glob(str(ROOT / "*.json"))
        if "all" not in f and "combined" not in f
    }

    # Check for missing files
    missing = expected - found_files
    extra = found_files - expected

    if missing:
        print(f"❌ Missing blueprint files: {', '.join(missing)}")
        sys.exit(1)

    if extra:
        print(f"⚠️  Extra files (not in manifest): {', '.join(extra)}")

    # Verify each blueprint has required fields
    all_ok = True
    agent_data = {}

    for filename in found_files:
        filepath = ROOT / filename
        try:
            data = json.load(open(filepath))

            # Check required fields
            required = ["agent", "version", "role", "ethics_compliance", "status"]
            missing_fields = [f for f in required if f not in data]

            if missing_fields:
                print(f"⚠️  {filename}: missing fields {missing_fields}")
                all_ok = False

            # Verify ethics compliance
            if "ethics_compliance" not in data:
                print(f"⚠️  {filename}: no ethics_compliance key")
                all_ok = False
            elif "Tony Accords" not in data["ethics_compliance"]:
                print(f"⚠️  {filename}: ethics_compliance doesn't reference Tony Accords")
                all_ok = False

            # Store for combined file (use agent name as key)
            agent_name = data.get("agent", Path(filename).stem)
            agent_data[agent_name] = data

            print(f"✅ {filename}: {data.get('agent', 'Unknown')} v{data.get('version', '?')}")

        except json.JSONDecodeError as e:
            print(f"❌ {filename}: Invalid JSON - {e}")
            all_ok = False
        except Exception as e:
            print(f"❌ {filename}: Error - {e}")
            all_ok = False

    if not all_ok:
        print("\n⚠️  Some blueprints have issues - review above")
        sys.exit(1)

    # Create combined blueprints file
    combined = {
        "version": manifest.get("version", "15.2"),
        "ethics": {
            "framework": manifest.get("ethics", "Tony Accords v13.4"),
            "pillars": [
                "Non-Maleficence",
                "Autonomy",
                "Reciprocal Freedom",
                "Perfect State"
            ],
            "verification": "pass"
        },
        "agents": agent_data,
        "checksum": checksum(agent_data),
        "generated_on": datetime.utcnow().isoformat() + "Z",
        "manifest": manifest
    }

    # Write combined file
    combined_path = ROOT / "blueprints_all.json"
    with open(combined_path, "w") as out:
        json.dump(combined, out, indent=2)

    print("=" * 50)
    print(f"✅ All {len(agent_data)} agent blueprints verified!")
    print(f"✅ Combined file created: {combined_path}")
    print(f"📋 Checksum: {combined['checksum']}")
    print(f"🔐 Ethics: {combined['ethics']['framework']}")
    print("\n🌀 Helix v15.2 Blueprint Archive Ready!")
    print("   Tat Tvam Asi 🙏")


if __name__ == "__main__":
    verify()
