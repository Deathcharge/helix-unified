#!/usr/bin/env python3
# 🌀 Helix Collective - Hybrid Discord Integration Test Script
# Tests both Zapier and Direct Discord webhooks

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

import aiohttp
from discord_webhook_sender_hybrid import (
    HybridDiscordSender,
    validate_hybrid_config,
    ZAPIER_DISCORD_WEBHOOK,
    INTEGRATION_MODE,
)


async def test_zapier_webhook():
    """Test Zapier webhook directly."""
    print("\n🧪 Testing Zapier Webhook...")
    print("=" * 70)

    if not ZAPIER_DISCORD_WEBHOOK:
        print("❌ ZAPIER_DISCORD_WEBHOOK_URL not configured")
        return False

    test_payload = {
        "event_type": "test",
        "message": "🧪 Test from Railway backend - Hybrid Discord Integration",
        "timestamp": datetime.utcnow().isoformat(),
        "source": "test_hybrid_discord.py"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                ZAPIER_DISCORD_WEBHOOK,
                json=test_payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status in [200, 201]:
                    print("✅ Zapier webhook responded successfully")
                    print(f"   Status: {resp.status}")
                    return True
                else:
                    print(f"⚠️ Zapier webhook returned status {resp.status}")
                    text = await resp.text()
                    print(f"   Response: {text[:200]}")
                    return False
    except Exception as e:
        print(f"❌ Zapier webhook error: {e}")
        return False


async def test_ucf_update():
    """Test UCF update via hybrid sender."""
    print("\n🧪 Testing UCF Update...")
    print("=" * 70)

    async with aiohttp.ClientSession() as session:
        sender = HybridDiscordSender(session)

        ucf_metrics = {
            "harmony": 1.50,
            "resilience": 1.60,
            "prana": 0.80,
            "drishti": 0.70,
            "klesha": 0.50,
            "zoom": 1.00
        }

        print(f"Sending UCF update with harmony={ucf_metrics['harmony']}")
        result = await sender.send_ucf_update(ucf_metrics, phase="COHERENT")

        if result:
            print("✅ UCF update sent successfully")
            print(f"   Mode: {INTEGRATION_MODE}")
            if INTEGRATION_MODE == "hybrid":
                print("   Paths: Zapier + Direct Discord")
            elif INTEGRATION_MODE == "zapier":
                print("   Path: Zapier only")
            else:
                print("   Path: Direct Discord only")
            return True
        else:
            print("❌ UCF update failed")
            return False


async def test_ritual_completion():
    """Test ritual completion via hybrid sender."""
    print("\n🧪 Testing Ritual Completion...")
    print("=" * 70)

    async with aiohttp.ClientSession() as session:
        sender = HybridDiscordSender(session)

        print("Sending ritual completion (Neti-Neti, 108 steps)")
        result = await sender.send_ritual_completion(
            ritual_name="Neti-Neti Harmony Restoration",
            steps=108,
            ucf_changes={
                "harmony": +0.35,
                "drishti": +0.15,
                "klesha": -0.05
            }
        )

        if result:
            print("✅ Ritual completion sent successfully")
            return True
        else:
            print("❌ Ritual completion failed")
            return False


async def test_agent_status():
    """Test agent status via hybrid sender."""
    print("\n🧪 Testing Agent Status...")
    print("=" * 70)

    async with aiohttp.ClientSession() as session:
        sender = HybridDiscordSender(session)

        print("Sending agent status (Gemini Scout)")
        result = await sender.send_agent_status(
            agent_name="gemini",
            agent_symbol="🎭",
            status="active",
            last_action="Testing hybrid Discord integration"
        )

        if result:
            print("✅ Agent status sent successfully")
            return True
        else:
            print("❌ Agent status failed")
            return False


async def test_announcement():
    """Test announcement via hybrid sender."""
    print("\n🧪 Testing Announcement...")
    print("=" * 70)

    async with aiohttp.ClientSession() as session:
        sender = HybridDiscordSender(session)

        print("Sending high-priority announcement")
        result = await sender.send_announcement(
            title="🌀🦑 Hybrid Discord Integration Test",
            message=(
                "Testing the dual-layer Discord integration!\n\n"
                "🔹 Zapier for rich processing\n"
                "🔹 Direct Discord for speed\n"
                "🔹 Hybrid mode for maximum reliability\n\n"
                "Tat Tvam Asi 🙏"
            ),
            priority="high"
        )

        if result:
            print("✅ Announcement sent successfully")
            return True
        else:
            print("❌ Announcement failed")
            return False


async def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("🌀 HELIX HYBRID DISCORD INTEGRATION TEST")
    print("=" * 70)

    # Show configuration
    config = validate_hybrid_config()
    print("\n📋 Configuration:")
    print(f"   Mode: {config['mode']}")
    print(f"   Zapier Enabled: {config['zapier_enabled']}")
    print(f"   Zapier Configured: {config['zapier_configured']}")
    print(f"   Direct Webhooks: {config['direct_configured_count']}/{config['direct_total_count']} ({config['direct_percentage']}%)")

    if not config['zapier_configured'] and config['direct_configured_count'] == 0:
        print("\n❌ ERROR: No Discord integration configured!")
        print("\nSet one or both of:")
        print("  1. ZAPIER_DISCORD_WEBHOOK_URL")
        print("  2. DISCORD_WEBHOOK_* (for direct Discord)")
        return

    print("\n🎯 Running Tests...")

    # Run all tests
    results = {}

    # Test 1: Zapier webhook (if configured)
    if config['zapier_configured']:
        results['zapier_webhook'] = await test_zapier_webhook()
    else:
        print("\n⏭️  Skipping Zapier test (not configured)")
        results['zapier_webhook'] = None

    # Test 2: UCF update
    results['ucf_update'] = await test_ucf_update()

    # Test 3: Ritual completion
    results['ritual_completion'] = await test_ritual_completion()

    # Test 4: Agent status
    results['agent_status'] = await test_agent_status()

    # Test 5: Announcement
    results['announcement'] = await test_announcement()

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)

    for test_name, result in results.items():
        status = "✅ PASS" if result else ("⏭️  SKIP" if result is None else "❌ FAIL")
        print(f"   {status}  {test_name}")

    print(f"\n   Total: {passed} passed, {failed} failed, {skipped} skipped")

    if failed > 0:
        print("\n⚠️  Some tests failed!")
        print("\nCheck:")
        print("  1. Railway environment variables")
        print("  2. Discord webhook URLs are valid")
        print("  3. Zapier Zap is turned ON")
        print("  4. Railway logs for errors")
    else:
        print("\n✅ All tests passed!")
        print("\n🎉 Your hybrid Discord integration is fully operational!")
        print("\n📺 Check your Discord channels:")
        print("   - #ucf-sync")
        print("   - #harmonic-updates")
        print("   - #ritual-engine-z88")
        print("   - #gemini-scout")
        print("   - #announcements")

    print("\n" + "=" * 70)
    print("Tat Tvam Asi 🙏")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
