#!/usr/bin/env python3
"""
Example 4: Subscription Management
===================================

Create, upgrade, and manage Stripe subscriptions.
"""

import os
import requests
import json

API_URL = os.getenv("HELIX_API_URL", "http://localhost:8000")
ACCESS_TOKEN = os.getenv("HELIX_ACCESS_TOKEN", "")


def create_subscription(tier="pro", billing_cycle="monthly"):
    """Create a new subscription"""
    print("\n💳 Creating subscription...")
    print("-" * 50)

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    try:
        response = requests.post(
            f"{API_URL}/stripe/create-subscription",
            headers=headers,
            json={
                "tier": tier,
                "billing_cycle": billing_cycle
            },
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Subscription created!")
            print(f"Subscription ID: {data.get('subscription_id')}")
            print(f"Status: {data.get('status')}")
            print(f"Current Period End: {data.get('current_period_end')}")
            return data
        else:
            print(f"❌ Failed: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def get_subscription():
    """Get current subscription"""
    print("\n📊 Getting current subscription...")
    print("-" * 50)

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    try:
        response = requests.get(
            f"{API_URL}/stripe/subscription",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Subscription info:")
            print(json.dumps(data, indent=2))
            return data
        elif response.status_code == 404:
            print("⚠️  No active subscription")
            return None
        else:
            print(f"❌ Failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def upgrade_subscription(new_tier="workflow"):
    """Upgrade subscription to higher tier"""
    print(f"\n⬆️  Upgrading to {new_tier}...")
    print("-" * 50)

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    try:
        response = requests.put(
            f"{API_URL}/stripe/update-subscription",
            headers=headers,
            json={"tier": new_tier},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Subscription upgraded!")
            print(f"New Tier: {data.get('tier')}")
            return data
        else:
            print(f"❌ Failed: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def cancel_subscription():
    """Cancel subscription"""
    print("\n🚫 Cancelling subscription...")
    print("-" * 50)

    confirm = input("Are you sure? (yes/no): ")
    if confirm.lower() != "yes":
        print("Cancelled.")
        return None

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    try:
        response = requests.delete(
            f"{API_URL}/stripe/cancel-subscription",
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Subscription cancelled")
            print(f"Cancel at period end: {data.get('cancel_at_period_end')}")
            return data
        else:
            print(f"❌ Failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """Main function"""
    print("\n" + "=" * 50)
    print("🌀 Helix Unified - Subscription Management")
    print("=" * 50)

    if not ACCESS_TOKEN:
        print("\n❌ Access token required!")
        print("Run: export HELIX_ACCESS_TOKEN=your-token")
        print("Get token from: python examples/02_auth_flow.py")
        return

    # Check current subscription
    current = get_subscription()

    if not current:
        # Create new subscription
        print("\nNo subscription found. Let's create one!")
        tier = input("Choose tier (free/pro/workflow/enterprise) [pro]: ") or "pro"
        cycle = input("Billing cycle (monthly/yearly) [monthly]: ") or "monthly"

        subscription = create_subscription(tier, cycle)

        if subscription:
            print("\n🎉 Subscription created successfully!")
    else:
        # Manage existing subscription
        print("\nManage subscription:")
        print("1. View details (already shown)")
        print("2. Upgrade tier")
        print("3. Cancel subscription")
        choice = input("\nChoice (1/2/3): ")

        if choice == "2":
            upgrade_subscription("workflow")
        elif choice == "3":
            cancel_subscription()

    print("\n" + "=" * 50)
    print("Done!")
    print("=" * 50)


if __name__ == "__main__":
    main()
