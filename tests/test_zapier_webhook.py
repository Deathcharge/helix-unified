#!/usr/bin/env python3
"""
Zapier Master Webhook Test Suite
=================================
Tests all 7 routing paths for Helix Collective Zapier integration.

Usage:
    python tests/test_zapier_webhook.py --all
    python tests/test_zapier_webhook.py --path event_log
    python tests/test_zapier_webhook.py --path telemetry

Requirements:
    - ZAPIER_MASTER_HOOK_URL environment variable must be set
    - Zapier Pro account (for PRO tier tests)
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import aiohttp

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from zapier_client import ZapierClient


class ZapierTester:
    """Test suite for Zapier Master Webhook"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.results = []

    async def test_event_log(self, client: ZapierClient) -> bool:
        """Test Path A: Event Log → Notion Event Log (FREE)"""
        print("\n🧪 Testing Path A: Event Log...")
        result = await client.log_event(
            event_title="Test Event from Webhook Tester",
            event_type="Test",
            agent_name="TestAgent",
            description="This is a test event to verify Zapier integration is working correctly",
            ucf_snapshot='{"harmony": 0.75, "zoom": 1.02}'
        )
        return result

    async def test_agent_registry(self, client: ZapierClient) -> bool:
        """Test Path B: Agent Registry → Notion Agent Registry (FREE)"""
        print("\n🧪 Testing Path B: Agent Registry...")
        result = await client.update_agent(
            agent_name="Manus",
            status="Active",
            last_action="Running webhook test",
            health_score=98
        )
        return result

    async def test_system_state(self, client: ZapierClient) -> bool:
        """Test Path C: System State → Notion System State (FREE)"""
        print("\n🧪 Testing Path C: System State...")
        result = await client.update_system_state(
            component="Webhook Test Suite",
            status="Testing",
            harmony=0.88,
            error_log="",
            verified=True
        )
        return result

    async def test_discord_notification(self, client: ZapierClient) -> bool:
        """Test Path D: Discord Notifications → Slack (PRO)"""
        print("\n🧪 Testing Path D: Discord Notifications (PRO)...")
        result = await client.send_discord_notification(
            channel_name="status",
            message="Test notification from Zapier webhook tester",
            priority="normal"
        )
        return result

    async def test_telemetry(self, client: ZapierClient) -> bool:
        """Test Path E: Telemetry → Google Sheets/Tables (PRO)"""
        print("\n🧪 Testing Path E: Telemetry (PRO)...")
        result = await client.log_telemetry(
            metric_name="test_webhook_latency",
            value=42.5,
            component="Webhook Test Suite",
            metadata={"test_run": datetime.now().isoformat()}
        )
        return result

    async def test_error_alert(self, client: ZapierClient) -> bool:
        """Test Path F: Error Alerts → Email + Slack (PRO)"""
        print("\n🧪 Testing Path F: Error Alerts (PRO)...")
        result = await client.send_error_alert(
            error_message="Test error alert - this is not a real error",
            component="Webhook Test Suite",
            severity="low",
            context={"test": True, "timestamp": datetime.now().isoformat()}
        )
        return result

    async def test_repository_action(self, client: ZapierClient) -> bool:
        """Test Path G: Repository Actions → GitHub + MEGA (PRO)"""
        print("\n🧪 Testing Path G: Repository Actions (PRO)...")
        result = await client.log_repository_action(
            repo_name="helix-unified",
            action="test_webhook",
            details="Testing repository action webhook path",
            commit_hash="test123abc"
        )
        return result

    async def run_all_tests(self):
        """Run all webhook tests"""
        print("=" * 70)
        print("🌀 Helix Collective - Zapier Master Webhook Test Suite")
        print("=" * 70)
        print(f"Webhook URL: {self.webhook_url[:50]}...")
        print(f"Timestamp: {datetime.now().isoformat()}")

        async with aiohttp.ClientSession() as session:
            client = ZapierClient(session)
            client.master_hook_url = self.webhook_url  # Override for testing

            # Week 1: Free Tier Tests
            print("\n" + "=" * 70)
            print("📅 WEEK 1: Core Monitoring (FREE TIER)")
            print("=" * 70)

            tests = [
                ("Event Log", self.test_event_log),
                ("Agent Registry", self.test_agent_registry),
                ("System State", self.test_system_state),
            ]

            week1_results = []
            for name, test_func in tests:
                try:
                    result = await test_func(client)
                    status = "✅ PASS" if result else "❌ FAIL"
                    week1_results.append((name, result))
                    print(f"{status}: {name}")
                except Exception as e:
                    week1_results.append((name, False))
                    print(f"❌ ERROR: {name} - {e}")

                await asyncio.sleep(1)  # Rate limiting

            # Week 2-4: Pro Tier Tests
            print("\n" + "=" * 70)
            print("📅 WEEK 2-4: Advanced Features (ZAPIER PRO)")
            print("=" * 70)

            pro_tests = [
                ("Discord Notifications", self.test_discord_notification),
                ("Telemetry", self.test_telemetry),
                ("Error Alerts", self.test_error_alert),
                ("Repository Actions", self.test_repository_action),
            ]

            pro_results = []
            for name, test_func in pro_tests:
                try:
                    result = await test_func(client)
                    status = "✅ PASS" if result else "❌ FAIL"
                    pro_results.append((name, result))
                    print(f"{status}: {name}")
                except Exception as e:
                    pro_results.append((name, False))
                    print(f"❌ ERROR: {name} - {e}")

                await asyncio.sleep(1)  # Rate limiting

            # Summary
            print("\n" + "=" * 70)
            print("📊 TEST SUMMARY")
            print("=" * 70)

            week1_pass = sum(1 for _, result in week1_results if result)
            pro_pass = sum(1 for _, result in pro_results if result)

            print(f"\nWeek 1 (FREE): {week1_pass}/{len(week1_results)} tests passed")
            print(f"Week 2-4 (PRO): {pro_pass}/{len(pro_tests)} tests passed")
            print(f"\nTotal: {week1_pass + pro_pass}/{len(tests) + len(pro_tests)} tests passed")

            if week1_pass == len(week1_results) and pro_pass == len(pro_tests):
                print("\n🎉 All tests passed! Your Zapier Master Webhook is fully operational!")
                return True
            elif week1_pass == len(week1_results):
                print("\n✅ Free tier tests passed! Pro features may require Zapier Pro account.")
                return True
            else:
                print("\n⚠️ Some tests failed. Check your Zapier configuration.")
                return False

    async def run_single_test(self, path: str):
        """Run a single test path"""
        print(f"\n🧪 Testing single path: {path}")

        async with aiohttp.ClientSession() as session:
            client = ZapierClient(session)
            client.master_hook_url = self.webhook_url

            test_map = {
                "event_log": self.test_event_log,
                "agent_registry": self.test_agent_registry,
                "system_state": self.test_system_state,
                "discord_notification": self.test_discord_notification,
                "telemetry": self.test_telemetry,
                "error_alert": self.test_error_alert,
                "repository_action": self.test_repository_action,
            }

            if path not in test_map:
                print(f"❌ Unknown test path: {path}")
                print(f"Available paths: {', '.join(test_map.keys())}")
                return False

            try:
                result = await test_map[path](client)
                if result:
                    print(f"✅ Test passed: {path}")
                    return True
                else:
                    print(f"❌ Test failed: {path}")
                    return False
            except Exception as e:
                print(f"❌ Test error: {e}")
                return False


def main():
    parser = argparse.ArgumentParser(
        description="Test Zapier Master Webhook integration"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all tests"
    )
    parser.add_argument(
        "--path",
        type=str,
        help="Run a specific test path (event_log, agent_registry, system_state, etc.)"
    )

    args = parser.parse_args()

    # Get webhook URL from environment
    webhook_url = os.getenv("ZAPIER_MASTER_HOOK_URL")
    if not webhook_url:
        print("❌ Error: ZAPIER_MASTER_HOOK_URL environment variable not set")
        print("\nSet it with:")
        print("  export ZAPIER_MASTER_HOOK_URL='https://hooks.zapier.com/hooks/catch/xxxxx/master'")
        sys.exit(1)

    tester = ZapierTester(webhook_url)

    if args.all:
        success = asyncio.run(tester.run_all_tests())
        sys.exit(0 if success else 1)
    elif args.path:
        success = asyncio.run(tester.run_single_test(args.path))
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        print("\n💡 Quick start:")
        print("  python tests/test_zapier_webhook.py --all")
        sys.exit(0)


if __name__ == "__main__":
    main()
