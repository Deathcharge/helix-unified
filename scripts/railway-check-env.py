#!/usr/bin/env python3
"""
Railway Environment Variables Manager
======================================

Manages environment variables across Railway services.
"""

import os
import sys
import json
import subprocess
from typing import Dict, List, Optional

# Required environment variables by service
SERVICE_ENV_VARS = {
    "helix-backend-api": [
        "DATABASE_URL",
        "REDIS_URL",
        "JWT_SECRET",
        "ANTHROPIC_API_KEY",
        "OPENAI_API_KEY",
        "STRIPE_SECRET_KEY",
        "STRIPE_PUBLISHABLE_KEY",
    ],
    "helix-discord-bot": [
        "DISCORD_BOT_TOKEN",
        "DISCORD_CLIENT_ID",
        "REDIS_URL",
    ],
    "helix-claude-api": [
        "ANTHROPIC_API_KEY",
        "REDIS_URL",
    ],
    "helix-dashboard": [
        "DATABASE_URL",
        "REDIS_URL",
    ],
}


def run_railway_command(cmd: List[str]) -> Optional[str]:
    """Run railway CLI command"""
    try:
        result = subprocess.run(
            ["railway"] + cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return None
    except FileNotFoundError:
        print("❌ Railway CLI not found. Install: curl -fsSL https://railway.app/install.sh | sh")
        sys.exit(1)


def list_services() -> List[str]:
    """List all services in project"""
    output = run_railway_command(["status", "--json"])
    if not output:
        return []

    try:
        data = json.loads(output)
        return [svc["name"] for svc in data.get("services", [])]
    except (json.JSONDecodeError, KeyError):
        return []


def get_service_vars(service: str) -> Dict[str, str]:
    """Get environment variables for a service"""
    output = run_railway_command(["variables", "--service", service, "--json"])
    if not output:
        return {}

    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return {}


def set_service_var(service: str, key: str, value: str) -> bool:
    """Set environment variable for a service"""
    result = run_railway_command(["variables", "set", f"{key}={value}", "--service", service])
    return result is not None


def check_service_vars(service: str) -> tuple[List[str], List[str]]:
    """Check which required vars are missing"""
    required = SERVICE_ENV_VARS.get(service, [])
    current = get_service_vars(service)

    present = [var for var in required if var in current]
    missing = [var for var in required if var not in current]

    return present, missing


def main():
    """Main function"""
    print("🚂 Helix Unified - Railway Environment Manager")
    print("=" * 50)
    print()

    # List services
    print("📦 Fetching services...")
    services = list_services()

    if not services:
        print("❌ No services found. Make sure you're in a Railway project.")
        sys.exit(1)

    print(f"✓ Found {len(services)} services")
    print()

    # Check each service
    all_good = True
    for service in services:
        print(f"🔍 Checking {service}...")
        present, missing = check_service_vars(service)

        if missing:
            all_good = False
            print(f"  ⚠️  Missing {len(missing)} required variables:")
            for var in missing:
                print(f"     - {var}")
        else:
            print(f"  ✅ All required variables present ({len(present)})")
        print()

    # Summary
    print("=" * 50)
    if all_good:
        print("✅ All services properly configured!")
    else:
        print("⚠️  Some services need configuration")
        print()
        print("Set variables with:")
        print("  railway variables set KEY=value --service SERVICE_NAME")
    print("=" * 50)


if __name__ == "__main__":
    main()
