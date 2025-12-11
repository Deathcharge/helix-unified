#!/usr/bin/env python3
"""
Quick environment validation script for Helix services.
Run before deployment to catch missing variables early.
"""
import os
import sys

# Required variables for core services
REQUIRED_VARS = {
    "core": [
        "DISCORD_BOT_TOKEN",
        "ANTHROPIC_API_KEY",
        "DATABASE_URL",
    ],
    "microservices": [
        "JWT_SECRET",
        "REDIS_URL",
    ],
    "optional": [
        "OPENAI_API_KEY",
        "PERPLEXITY_API_KEY",
        "GOOGLE_CLOUD_TTS_API_KEY",
        "RAILWAY_TOKEN",
    ]
}

def validate_env():
    """Validate environment variables."""
    missing = []
    optional_missing = []

    print("🔍 Validating Helix Environment Variables...\n")

    # Check required core vars
    print("📋 Core Services:")
    for var in REQUIRED_VARS["core"]:
        if os.getenv(var):
            print(f"  ✅ {var}")
        else:
            print(f"  ❌ {var} - MISSING")
            missing.append(var)

    # Check microservice vars
    print("\n📋 Microservices:")
    for var in REQUIRED_VARS["microservices"]:
        if os.getenv(var):
            print(f"  ✅ {var}")
        else:
            print(f"  ❌ {var} - MISSING")
            missing.append(var)

    # Check optional vars
    print("\n📋 Optional (Recommended):")
    for var in REQUIRED_VARS["optional"]:
        if os.getenv(var):
            print(f"  ✅ {var}")
        else:
            print(f"  ⚠️  {var} - Not set (optional)")
            optional_missing.append(var)

    # Security checks
    print("\n🔒 Security Checks:")
    jwt_secret = os.getenv("JWT_SECRET")
    if jwt_secret:
        if len(jwt_secret) < 32:
            print(f"  ⚠️  JWT_SECRET is too short ({len(jwt_secret)} chars, min 32 recommended)")
        else:
            print(f"  ✅ JWT_SECRET length OK ({len(jwt_secret)} chars)")

    # Summary
    print("\n" + "="*60)
    if missing:
        print(f"❌ FAILED: {len(missing)} required variables missing")
        print(f"\nMissing variables:")
        for var in missing:
            print(f"  - {var}")
        print(f"\n⚠️  Set these in Railway or your .env file before deployment!")
        return False
    else:
        print("✅ PASSED: All required variables set")
        if optional_missing:
            print(f"\n⚠️  {len(optional_missing)} optional variables not set")
            print("   Some features may be disabled")
        return True

if __name__ == "__main__":
    success = validate_env()
    sys.exit(0 if success else 1)
