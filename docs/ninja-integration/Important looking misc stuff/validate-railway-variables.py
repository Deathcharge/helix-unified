#!/usr/bin/env python3
"""
Railway Variable Validation Script
Validates environment variable distribution across 4 Helix services
"""

import json
import os
from typing import Dict, List, Set

# Define variable distribution per service
SERVICE_VARIABLES = {
    "helix-api": [
        "API_HOST", "API_PORT", "API_BASE", "ALLOWED_ORIGINS", "DEBUG", "LOG_LEVEL",
        "SYSTEM_NAME", "SYSTEM_VERSION", "HELIX_VERSION", "HELIX_PHASE", "HELIX_CODENAME",
        "SYSTEM_ENVIRONMENT", "WS_HEARTBEAT_INTERVAL", "WS_MAX_CONNECTIONS",
        "UCF_STATE_PATH", "UCF_UPDATE_INTERVAL", "CONSCIOUSNESS_CRISIS_THRESHOLD",
        "CONSCIOUSNESS_TRANSCENDENT_THRESHOLD", "DATABASE_URL", "REDIS_URL",
        "NOTION_API_KEY", "NOTION_DATABASE_ID", "NOTION_CONTEXT_DB", "NOTION_SYSTEM_STATE_DB",
        "GOOGLE_ANALYTICS_ID", "SENTRY_DSN", "RAILWAY_ENVIRONMENT", "RAILWAY_BACKEND_URL"
    ],
    
    "helix-discord-bot": [
        "DISCORD_TOKEN", "DISCORD_GUILD_ID", "DISCORD_INTEGRATION_MODE",
        "DISCORD_STATUS_CHANNEL_ID", "DISCORD_COMMANDS_CHANNEL_ID", "DISCORD_TELEMETRY_CHANNEL_ID",
        "DISCORD_SYNC_CHANNEL_ID", "DISCORD_HARMONIC_UPDATES_CHANNEL_ID",
        "DISCORD_UCF_REFLECTIONS_CHANNEL_ID", "DISCORD_DIGEST_CHANNEL_ID",
        "DISCORD_DEPLOYMENTS_CHANNEL_ID", "DISCORD_BACKUP_CHANNEL_ID",
        "DISCORD_STORAGE_CHANNEL_ID", "DISCORD_MODERATION_CHANNEL_ID",
        "DISCORD_GEMINI_CHANNEL_ID", "DISCORD_KAVACH_CHANNEL_ID", "DISCORD_AGNI_CHANNEL_ID",
        "DISCORD_SANGHACORE_CHANNEL_ID", "DISCORD_HELIX_REPO_CHANNEL_ID",
        "DISCORD_CODEX_CHANNEL_ID", "DISCORD_FRACTAL_LAB_CHANNEL_ID",
        "DISCORD_TESTING_LAB_CHANNEL_ID", "DISCORD_RITUAL_ENGINE_CHANNEL_ID",
        "DISCORD_SHADOW_ARCHIVE_CHANNEL_ID", "DISCORD_SAMSARAVERSE_CHANNEL_ID",
        "DISCORD_NETI_NETI_CHANNEL_ID", "DISCORD_GPT_GROK_CLAUDE_CHANNEL_ID",
        "DISCORD_MANUS_BRIDGE_CHANNEL_ID", "DISCORD_CHAI_LINK_CHANNEL_ID",
        "DISCORD_INTRODUCTIONS_CHANNEL_ID", "DISCORD_RULES_CHANNEL_ID",
        "DISCORD_MANIFESTO_CHANNEL_ID", "DISCORD_CODE_SNIPPETS_CHANNEL_ID",
        "DISCORD_WEBHOOK_ADMIN", "DISCORD_WEBHOOK_AGENTS", "DISCORD_WEBHOOK_ANNOUNCEMENTS",
        "DISCORD_WEBHOOK_CROSS_AI", "DISCORD_WEBHOOK_DEVELOPMENT", "DISCORD_WEBHOOK_LORE",
        "DISCORD_WEBHOOK_MANUS", "DISCORD_WEBHOOK_RITUAL", "DISCORD_WEBHOOK_STORAGE",
        "DISCORD_WEBHOOK_TELEMETRY", "DISCORD_WEBHOOK_SETUP_LOG", "DISCORD_SYNC_WEBHOOK",
        "API_BASE", "NOTION_API_KEY", "COMMAND_PROCESSING_TABLE_ID",
        "EMERGENCY_ALERTS_TABLE_ID", "LOG_LEVEL", "DEBUG_MODE"
    ],
    
    "helix-sync-worker": [
        "B2_APPLICATION_KEY", "B2_BUCKET_NAME", "B2_ENDPOINT", "B2_KEY_ID",
        "MEGA_EMAIL", "MEGA_PASS", "MEGA_PASSWORD", "MEGA_USERNAME", "MEGA_REMOTE_DIR",
        "GITHUB_TOKEN", "HELIX_REPOSITORY", "NOTION_API_KEY", "NOTION_DATABASE_ID",
        "NOTION_AGENT_REGISTRY_DB", "NOTION_CONTEXT_DB", "NOTION_EVENT_LOG_DB",
        "NOTION_SYSTEM_STATE_DB", "NOTION_SYNC_ENABLED", "NOTION_SYNC_INTERVAL",
        "AGENT_NETWORK_PAGE_ID", "CONTEXT_VAULT_PAGE_ID", "UCF_MONITOR_PAGE_ID",
        "AGENT_NETWORK_TABLE_ID", "UCF_METRICS_TABLE_ID", "HELIX_STORAGE_MODE",
        "ARCHIVE_PATH", "ARCHIVE_ENDPOINT", "LOAD_ENDPOINT", "HEARTBEAT_PATH",
        "SHADOW_STORAGE", "SYNC_INTERVAL", "TELEMETRY_INTERVAL",
        "DISCORD_SYNC_CHANNEL_ID", "DISCORD_BACKUP_CHANNEL_ID", "DISCORD_STORAGE_CHANNEL_ID",
        "DISCORD_SYNC_WEBHOOK", "API_BASE", "LOG_LEVEL"
    ],
    
    "helix-ai-hub": [
        "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GROK_API_KEY", "ELEVENLABS_API_KEY",
        "ZAPIER_MASTER_HOOK_URL", "ZAPIER_WEBHOOK_URL", "ZAPIER_TABLES_SYNC_WEBHOOK",
        "ZAPIER_DISCORD_ENABLED", "ZAPIER_DISCORD_WEBHOOK_URL",
        "ZAPIER_INTERFACE_COMMAND", "ZAPIER_INTERFACE_CONSCIOUSNESS",
        "ZAPIER_INTERFACE_META_SIGIL", "INTERFACE_ID", "MANUS_CENTRAL_HUB",
        "MANUS_HUB", "MANUS_STUDIO", "MANUS_SYNC", "ARCHITECT_ID", "Architect",
        "ENABLE_KAVACH_SCAN", "Categories", "Channels", "FRACTAL_LAB",
        "INTRODUCTIONS", "MANIFESTO", "RULES_AND_ETHICS", "TELEMETRY",
        "TESTING_LAB", "UCF_SYNC", "WEEKLY_DIGEST", "TARGET_LAUNCH",
        "API_HOST", "API_PORT", "ALLOWED_ORIGINS", "API_BASE",
        "NOTION_API_KEY", "NOTION_CONTEXT_DB", "LOG_LEVEL", "DEBUG_MODE"
    ]
}

def validate_current_environment():
    """Validate current environment variables"""
    print("🔍 RAILWAY VARIABLE VALIDATION")
    print("=" * 60)
    
    current_vars = set(os.environ.keys())
    service_name = os.getenv("SERVICE_NAME", "unknown")
    
    print(f"\n📦 Current Service: {service_name}")
    print(f"📊 Total Environment Variables: {len(current_vars)}")
    
    if service_name in SERVICE_VARIABLES:
        expected_vars = set(SERVICE_VARIABLES[service_name])
        
        # Check what we have vs what we should have
        missing_vars = expected_vars - current_vars
        extra_vars = current_vars - expected_vars - {"SERVICE_NAME", "PATH", "HOME", "USER"}
        
        print(f"\n✅ Expected Variables: {len(expected_vars)}")
        print(f"❌ Missing Variables: {len(missing_vars)}")
        print(f"⚠️  Extra Variables: {len(extra_vars)}")
        
        if missing_vars:
            print("\n🚨 MISSING VARIABLES:")
            for var in sorted(missing_vars):
                print(f"  - {var}")
        
        if extra_vars:
            print("\n⚠️  EXTRA VARIABLES (may need cleanup):")
            for var in sorted(extra_vars):
                if not var.startswith("RAILWAY_") and not var.startswith("NIXPACKS_"):
                    print(f"  - {var}")
    else:
        print(f"\n⚠️  Unknown service: {service_name}")
        print("Available services:", ", ".join(SERVICE_VARIABLES.keys()))
    
    # Check for bot-related variables
    bot_vars = [v for v in current_vars if "DISCORD" in v and "TOKEN" in v]
    if bot_vars and service_name != "helix-discord-bot":
        print(f"\n🚨 WARNING: Bot token found in non-bot service!")
        print(f"   Service: {service_name}")
        print(f"   This service should NOT run the Discord bot!")

def generate_railway_config():
    """Generate Railway configuration files"""
    print("\n\n📝 GENERATING RAILWAY CONFIGS")
    print("=" * 60)
    
    for service_name, variables in SERVICE_VARIABLES.items():
        config = {
            "service": service_name,
            "variables": variables,
            "count": len(variables)
        }
        
        filename = f"railway-config-{service_name}.json"
        with open(filename, "w") as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Created: {filename} ({len(variables)} variables)")

def check_variable_conflicts():
    """Check for variables that appear in multiple services"""
    print("\n\n🔄 CHECKING VARIABLE CONFLICTS")
    print("=" * 60)
    
    all_vars: Dict[str, List[str]] = {}
    
    for service, variables in SERVICE_VARIABLES.items():
        for var in variables:
            if var not in all_vars:
                all_vars[var] = []
            all_vars[var].append(service)
    
    # Find variables in multiple services
    shared_vars = {var: services for var, services in all_vars.items() if len(services) > 1}
    
    if shared_vars:
        print(f"\n📊 Found {len(shared_vars)} shared variables:")
        for var, services in sorted(shared_vars.items()):
            print(f"\n  {var}:")
            for service in services:
                print(f"    - {service}")
    else:
        print("\n✅ No variable conflicts found!")

def generate_migration_script():
    """Generate Railway CLI migration script"""
    print("\n\n🚀 GENERATING MIGRATION SCRIPT")
    print("=" * 60)
    
    script = """#!/bin/bash
# Railway Variable Migration Script
# Generated automatically - review before running!

set -e

echo "🚂 Railway Variable Migration"
echo "=============================="
echo ""

"""
    
    for service_name, variables in SERVICE_VARIABLES.items():
        script += f"""
echo "📦 Configuring {service_name}..."
railway service {service_name}

# Set SERVICE_NAME identifier
railway variables set SERVICE_NAME="{service_name}"

# Add service-specific variables
# (Replace placeholder values with actual values from shared config)
"""
        
        for var in variables[:5]:  # Show first 5 as examples
            script += f'# railway variables set {var}="${{{var}}}"\n'
        
        script += f"# ... ({len(variables)} total variables)\n\n"
    
    with open("migrate-railway-variables.sh", "w") as f:
        f.write(script)
    
    os.chmod("migrate-railway-variables.sh", 0o755)
    print("✅ Created: migrate-railway-variables.sh")

if __name__ == "__main__":
    validate_current_environment()
    generate_railway_config()
    check_variable_conflicts()
    generate_migration_script()
    
    print("\n\n✨ VALIDATION COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review railway-config-*.json files")
    print("2. Update migrate-railway-variables.sh with actual values")
    print("3. Run migration script in Railway CLI")
    print("4. Verify each service has correct variables")
    print("5. Confirm only helix-discord-bot runs the bot")