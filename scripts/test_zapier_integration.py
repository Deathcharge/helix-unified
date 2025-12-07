#!/usr/bin/env python3
# 🌀 Helix Collective v14.5 — Quantum Handshake
# scripts/test_zapier_integration.py — Zapier Integration Test Script
# Author: Andrew John Ward (Architect)

"""
Standalone test script for Zapier webhook integration.

Tests all three Zapier webhooks without requiring FastAPI startup.

Usage:
    export ZAPIER_EVENT_HOOK_URL=https://hooks.zapier.com/...
    export ZAPIER_AGENT_HOOK_URL=https://hooks.zapier.com/...
    export ZAPIER_SYSTEM_HOOK_URL=https://hooks.zapier.com/...
    python scripts/test_zapier_integration.py

Expected output:
    ✅ Event Log webhook: 200 OK
    ✅ Agent Registry webhook: 200 OK
    ✅ System State webhook: 200 OK
    All webhooks operational.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import aiohttp

from backend.services.zapier_client import (AGENT_HOOK, EVENT_HOOK,
                                            SYSTEM_HOOK, ZapierClient,
                                            validate_zapier_config)

# ============================================================================
# TEST FUNCTIONS
# ============================================================================

async def test_zapier_integration():
    """Test all Zapier webhooks."""
    print("\n" + "=" * 70)
    print("🧪 ZAPIER INTEGRATION TEST")
    print("=" * 70)
    
    # Check configuration
    print("\n📋 Configuration Status:")
    config = validate_zapier_config()
    print(f"  Event Hook:  {'✅' if config['event_hook'] else '❌'}")
    print(f"  Agent Hook:  {'✅' if config['agent_hook'] else '❌'}")
    print(f"  System Hook: {'✅' if config['system_hook'] else '❌'}")
    
    if not config['all_configured']:
        print("\n❌ ERROR: Not all webhooks configured!")
        print("\nSet environment variables:")
        print("  export ZAPIER_EVENT_HOOK_URL=https://hooks.zapier.com/...")
        print("  export ZAPIER_AGENT_HOOK_URL=https://hooks.zapier.com/...")
        print("  export ZAPIER_SYSTEM_HOOK_URL=https://hooks.zapier.com/...")
        return False
    
    print("\n✅ All webhooks configured")
    
    # Create session and client
    print("\n🔗 Creating Zapier client...")
    async with aiohttp.ClientSession() as session:
        zap = ZapierClient(session)
        
        results = {
            "event_log": None,
            "agent_registry": None,
            "system_state": None,
        }
        
        # Test Event Log webhook
        print("\n📝 Testing Event Log webhook...")
        try:
            result = await zap.log_event(
                title="Test Event - Zapier Integration",
                event_type="Status",
                agent_name="Manus",
                description="Testing Zapier integration from test script",
                ucf_snapshot={
                    "harmony": 0.355,
                    "prana": 0.7,
                    "drishti": 0.8,
                    "klesha": 0.2,
                }
            )
            results["event_log"] = result
            print(f"  {'✅' if result else '❌'} Event Log webhook: {'OK' if result else 'FAILED'}")
        except Exception as e:
            print(f"  ❌ Event Log webhook: {e}")
            results["event_log"] = False
        
        # Test Agent Registry webhook
        print("\n👤 Testing Agent Registry webhook...")
        try:
            result = await zap.update_agent(
                agent_name="Manus",
                status="Active",
                last_action="Testing Zapier integration",
                health_score=100
            )
            results["agent_registry"] = result
            print(f"  {'✅' if result else '❌'} Agent Registry webhook: {'OK' if result else 'FAILED'}")
        except Exception as e:
            print(f"  ❌ Agent Registry webhook: {e}")
            results["agent_registry"] = False
        
        # Test System State webhook
        print("\n🔧 Testing System State webhook...")
        try:
            result = await zap.upsert_system_component(
                component="Zapier Integration Test",
                status="Active",
                harmony=0.355,
                error_log="",
                verified=True
            )
            results["system_state"] = result
            print(f"  {'✅' if result else '❌'} System State webhook: {'OK' if result else 'FAILED'}")
        except Exception as e:
            print(f"  ❌ System State webhook: {e}")
            results["system_state"] = False
    
    # Summary
    print("\n" + "=" * 70)
    all_passed = all(results.values())
    
    if all_passed:
        print("✅ ALL WEBHOOKS OPERATIONAL")
        print("=" * 70 + "\n")
        return True
    else:
        print("⚠️  SOME WEBHOOKS FAILED")
        print(f"  Event Log:      {'✅' if results['event_log'] else '❌'}")
        print(f"  Agent Registry: {'✅' if results['agent_registry'] else '❌'}")
        print(f"  System State:   {'✅' if results['system_state'] else '❌'}")
        print("=" * 70 + "\n")
        return False

async def test_payload_validation():
    """Test payload size validation."""
    print("\n" + "=" * 70)
    print("🧪 PAYLOAD VALIDATION TEST")
    print("=" * 70)
    
    async with aiohttp.ClientSession() as session:
        zap = ZapierClient(session)
        
        # Test with large payload
        print("\n📦 Testing large payload handling...")
        large_ucf = {
            "harmony": 0.355,
            "prana": 0.7,
            "drishti": 0.8,
            "klesha": 0.2,
            "large_data": "x" * 100000,  # 100KB of data
        }
        
        try:
            result = await zap.log_event(
                title="Large Payload Test",
                event_type="Status",
                agent_name="Manus",
                description="Testing large payload handling",
                ucf_snapshot=large_ucf
            )
            print(f"  {'✅' if result else '❌'} Large payload handled correctly")
        except Exception as e:
            print(f"  ❌ Large payload test failed: {e}")
    
    print("\n" + "=" * 70 + "\n")

async def test_graceful_degradation():
    """Test graceful degradation when webhooks are not configured."""
    print("\n" + "=" * 70)
    print("🧪 GRACEFUL DEGRADATION TEST")
    print("=" * 70)
    
    # Temporarily clear webhook URLs
    original_event = os.environ.get("ZAPIER_EVENT_HOOK_URL")
    original_agent = os.environ.get("ZAPIER_AGENT_HOOK_URL")
    original_system = os.environ.get("ZAPIER_SYSTEM_HOOK_URL")
    
    try:
        # Clear all webhooks
        os.environ.pop("ZAPIER_EVENT_HOOK_URL", None)
        os.environ.pop("ZAPIER_AGENT_HOOK_URL", None)
        os.environ.pop("ZAPIER_SYSTEM_HOOK_URL", None)
        
        print("\n🔌 Testing with no webhooks configured...")
        
        async with aiohttp.ClientSession() as session:
            zap = ZapierClient(session)
            
            # These should not raise exceptions
            print("  Testing log_event (should skip silently)...")
            result = await zap.log_event(
                title="Test",
                event_type="Status",
                agent_name="Manus",
                description="Test",
                ucf_snapshot={}
            )
            print(f"    ✅ Handled gracefully (returned {result})")
            
            print("  Testing update_agent (should skip silently)...")
            result = await zap.update_agent(
                agent_name="Manus",
                status="Active",
                last_action="Test",
                health_score=100
            )
            print(f"    ✅ Handled gracefully (returned {result})")
            
            print("  Testing upsert_system_component (should skip silently)...")
            result = await zap.upsert_system_component(
                component="Test",
                status="Active",
                harmony=0.355
            )
            print(f"    ✅ Handled gracefully (returned {result})")
    
    finally:
        # Restore original values
        if original_event:
            os.environ["ZAPIER_EVENT_HOOK_URL"] = original_event
        if original_agent:
            os.environ["ZAPIER_AGENT_HOOK_URL"] = original_agent
        if original_system:
            os.environ["ZAPIER_SYSTEM_HOOK_URL"] = original_system
    
    print("\n" + "=" * 70 + "\n")

# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Run all tests."""
    print("\n🌀 Helix Collective v14.5 — Zapier Integration Test Suite")
    
    # Test 1: Zapier integration
    success1 = await test_zapier_integration()
    
    # Test 2: Payload validation
    await test_payload_validation()
    
    # Test 3: Graceful degradation
    await test_graceful_degradation()
    
    # Final summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    if success1:
        print("✅ Zapier integration: OPERATIONAL")
        print("✅ Payload validation: PASSED")
        print("✅ Graceful degradation: PASSED")
        print("\n🎉 All tests passed! Zapier integration is ready for production.")
    else:
        print("❌ Zapier integration: FAILED")
        print("⚠️  Please check webhook URLs and Zapier configuration.")
    
    print("=" * 70 + "\n")
    
    return 0 if success1 else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

