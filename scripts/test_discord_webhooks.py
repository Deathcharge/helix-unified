#!/usr/bin/env python3
"""
Discord Webhook Test Script
Tests all configured webhooks for Helix Collective v15.3

Usage:
    python scripts/test_discord_webhooks.py
"""

import os
import sys
import json
import asyncio
import aiohttp
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Webhook configuration
WEBHOOKS = {
    "DISCORD_WEBHOOK_MANUS": {
        "name": "Manus Ops Hook",
        "channel": "#helix-ops",
        "color": 0x00BFFF,  # Blue
        "emoji": "🤲"
    },
    "DISCORD_SYNC_WEBHOOK": {
        "name": "Helix Sync Service",
        "channel": "#sync-reports",
        "color": 0x9932CC,  # Purple
        "emoji": "🔄"
    },
    "DISCORD_WEBHOOK_GITHUB": {
        "name": "GitHub Notifier",
        "channel": "#github-activity",
        "color": 0x00FF7F,  # Green
        "emoji": "📦"
    },
    "DISCORD_WEBHOOK_CONSCIOUSNESS": {
        "name": "Consciousness Monitor",
        "channel": "#consciousness",
        "color": 0x8A2BE2,  # Blue Violet
        "emoji": "🧠"
    }
}


async def test_webhook(webhook_url: str, config: dict) -> dict:
    """
    Test a single webhook by sending a test message.
    
    Args:
        webhook_url: The webhook URL to test
        config: Configuration dict with name, channel, color, emoji
        
    Returns:
        Dict with test results
    """
    result = {
        "name": config["name"],
        "channel": config["channel"],
        "success": False,
        "error": None,
        "response_time": None
    }
    
    try:
        start_time = datetime.now()
        
        # Create test embed
        embed = {
            "title": f"{config['emoji']} Webhook Test - {config['name']}",
            "description": f"Testing webhook connection to {config['channel']}",
            "color": config["color"],
            "fields": [
                {
                    "name": "Status",
                    "value": "✅ Connection successful",
                    "inline": True
                },
                {
                    "name": "Timestamp",
                    "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "inline": True
                },
                {
                    "name": "Test Info",
                    "value": "This is an automated webhook test from Helix Collective v15.3",
                    "inline": False
                }
            ],
            "footer": {
                "text": "Helix Collective v15.3 - Webhook Test"
            }
        }
        
        # Send test message
        async with aiohttp.ClientSession() as session:
            async with session.post(
                webhook_url,
                json={
                    "content": f"🔔 **Webhook Test** - {config['name']}",
                    "embeds": [embed]
                }
            ) as response:
                end_time = datetime.now()
                result["response_time"] = (end_time - start_time).total_seconds()
                
                if response.status in [200, 204]:
                    result["success"] = True
                else:
                    result["error"] = f"HTTP {response.status}: {await response.text()}"
                    
    except Exception as e:
        result["error"] = str(e)
    
    return result


async def test_all_webhooks():
    """
    Test all configured webhooks and display results.
    """
    print("=" * 70)
    print("🌀 Helix Collective - Discord Webhook Test")
    print("=" * 70)
    print()
    
    results = []
    configured_count = 0
    success_count = 0
    
    for env_var, config in WEBHOOKS.items():
        webhook_url = os.getenv(env_var)
        
        if not webhook_url:
            print(f"⚠️  {config['name']}")
            print(f"   Channel: {config['channel']}")
            print(f"   Status: ❌ NOT CONFIGURED")
            print(f"   Env Var: {env_var}")
            print()
            results.append({
                "name": config["name"],
                "channel": config["channel"],
                "configured": False
            })
            continue
        
        configured_count += 1
        
        print(f"🔍 Testing {config['name']}...")
        print(f"   Channel: {config['channel']}")
        print(f"   Env Var: {env_var}")
        
        result = await test_webhook(webhook_url, config)
        results.append({**result, "configured": True})
        
        if result["success"]:
            success_count += 1
            print(f"   Status: ✅ SUCCESS")
            print(f"   Response Time: {result['response_time']:.3f}s")
        else:
            print(f"   Status: ❌ FAILED")
            print(f"   Error: {result['error']}")
        
        print()
        
        # Rate limit protection
        await asyncio.sleep(1)
    
    # Summary
    print("=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    print(f"Total Webhooks: {len(WEBHOOKS)}")
    print(f"Configured: {configured_count}/{len(WEBHOOKS)}")
    print(f"Successful: {success_count}/{configured_count if configured_count > 0 else 0}")
    print()
    
    if success_count == configured_count and configured_count > 0:
        print("✅ All configured webhooks are working!")
    elif success_count > 0:
        print("⚠️  Some webhooks failed - check errors above")
    else:
        print("❌ No webhooks are working - check configuration")
    
    print()
    
    # Configuration guide
    if configured_count < len(WEBHOOKS):
        print("=" * 70)
        print("🔧 Missing Webhooks - Configuration Guide")
        print("=" * 70)
        print()
        print("To configure missing webhooks:")
        print("1. Open Discord and go to your Helix server")
        print("2. Right-click the target channel → Edit Channel")
        print("3. Go to Integrations → Create Webhook")
        print("4. Copy the webhook URL")
        print("5. Add to your environment:")
        print()
        
        for env_var, config in WEBHOOKS.items():
            if not os.getenv(env_var):
                print(f"   export {env_var}=\"https://discord.com/api/webhooks/...\"")
                print(f"   # For {config['name']} in {config['channel']}")
                print()
    
    # Save results to file
    results_file = Path("logs/webhook_test_results.json")
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total": len(WEBHOOKS),
            "configured": configured_count,
            "successful": success_count,
            "results": results
        }, f, indent=2)
    
    print(f"📄 Results saved to: {results_file}")
    print()
    
    return success_count == configured_count and configured_count > 0


def main():
    """Main entry point."""
    try:
        success = asyncio.run(test_all_webhooks())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

