#!/usr/bin/env python3
"""
Example 2: Authentication Flow
===============================

Demonstrates user registration, login, and accessing protected endpoints.
"""

import os
import requests
from datetime import datetime
import json

# Configuration
API_URL = os.getenv("HELIX_API_URL", "http://localhost:8000")
TEST_EMAIL = f"test_{int(datetime.now().timestamp())}@example.com"
TEST_PASSWORD = "SecurePassword123!"


def register_user(email, password):
    """Register a new user"""
    print("📝 Registering new user...")
    print(f"Email: {email}")
    print("-" * 50)

    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "email": email,
                "password": password,
                "full_name": "Test User"
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Registration successful!")
            print(f"User ID: {data.get('user_id', 'N/A')}")
            print(f"Email: {data.get('email', 'N/A')}")
            print(f"Tier: {data.get('tier', 'free')}")
            return data
        elif response.status_code == 400:
            print("⚠️  User already exists or invalid data")
            return None
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def login_user(email, password):
    """Login and get access token"""
    print("\n🔐 Logging in...")
    print(f"Email: {email}")
    print("-" * 50)

    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email": email,
                "password": password
            },
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"Token Type: {data.get('token_type', 'bearer')}")
            print(f"Access Token: {data.get('access_token', 'N/A')[:20]}...")
            return data.get('access_token')
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def get_user_info(token):
    """Get current user information"""
    print("\n👤 Getting user information...")
    print("-" * 50)

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_URL}/auth/me",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ User information retrieved!")
            print(json.dumps(data, indent=2))
            return data
        else:
            print(f"❌ Failed to get user info: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def get_usage_stats(token):
    """Get usage statistics"""
    print("\n📊 Getting usage statistics...")
    print("-" * 50)

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_URL}/usage/current",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Usage statistics retrieved!")
            print(f"Requests Today: {data.get('requests_today', 0)}")
            print(f"Daily Limit: {data.get('daily_limit', 100)}")
            print(f"Remaining: {data.get('remaining', 0)}")
            return data
        else:
            print(f"⚠️  Usage endpoint not available: {response.status_code}")
            return None

    except Exception as e:
        print(f"⚠️  Could not get usage stats: {e}")
        return None


def main():
    """Main function"""
    print("\n" + "=" * 50)
    print("🌀 Helix Unified - Authentication Flow Example")
    print("=" * 50 + "\n")

    # Step 1: Register
    user_data = register_user(TEST_EMAIL, TEST_PASSWORD)
    if not user_data:
        print("\n💡 Trying to login with existing credentials...")

    # Step 2: Login
    token = login_user(TEST_EMAIL, TEST_PASSWORD)
    if not token:
        print("\n❌ Authentication flow failed")
        return

    # Step 3: Get user info
    user_info = get_user_info(token)

    # Step 4: Get usage stats
    usage_stats = get_usage_stats(token)

    # Summary
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  Registration: {'✅' if user_data else '⚠️'}")
    print(f"  Login: {'✅' if token else '❌'}")
    print(f"  User Info: {'✅' if user_info else '❌'}")
    print(f"  Usage Stats: {'✅' if usage_stats else '⚠️'}")
    print("=" * 50 + "\n")

    if token:
        print("🎉 Authentication flow complete!")
        print(f"Your access token: {token[:30]}...")
        print(f"\nNext: Try 03_chat_completion.py with this token")


if __name__ == "__main__":
    main()
