#!/usr/bin/env python3
"""
Example 1: Health Check
=======================

Check if the Helix Unified API is running and healthy.
"""

import os
from datetime import datetime

import requests

# Configuration
API_URL = os.getenv("HELIX_API_URL", "http://localhost:8000")


def check_health():
    """Check API health endpoint"""
    print("🏥 Checking Helix Unified API Health...")
    print(f"API URL: {API_URL}")
    print("-" * 50)

    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        response.raise_for_status()

        data = response.json()

        print("✅ API is healthy!")
        print(f"Status: {data.get('status', 'unknown')}")
        print(f"Service: {data.get('service', 'helix-unified')}")
        print(f"Timestamp: {datetime.now().isoformat()}")

        # Check if additional info is available
        if 'version' in data:
            print(f"Version: {data['version']}")
        if 'uptime' in data:
            print(f"Uptime: {data['uptime']}")

        return True

    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API at {API_URL}")
        print("Make sure the server is running:")
        print("  Local: uvicorn backend.main:app --reload")
        print("  Docker: docker-compose up")
        return False

    except requests.exceptions.Timeout:
        print(f"❌ API request timed out")
        return False

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def check_docs():
    """Check if API documentation is accessible"""
    print("\n📚 Checking API Documentation...")
    print("-" * 50)

    try:
        response = requests.get(f"{API_URL}/docs", timeout=5)
        if response.status_code == 200:
            print(f"✅ API docs available at: {API_URL}/docs")
            return True
        else:
            print(f"⚠️  API docs returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️  Could not check docs: {e}")
        return False


def main():
    """Main function"""
    print("\n" + "=" * 50)
    print("🌀 Helix Unified - Health Check Example")
    print("=" * 50 + "\n")

    # Check API health
    api_healthy = check_health()

    # Check docs
    docs_available = check_docs()

    # Summary
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  API Healthy: {'✅' if api_healthy else '❌'}")
    print(f"  Docs Available: {'✅' if docs_available else '⚠️'}")
    print("=" * 50 + "\n")

    if api_healthy:
        print("🎉 Ready to use Helix Unified API!")
        print(f"Next: Try 02_auth_flow.py")
    else:
        print("💡 Start the server and try again")


if __name__ == "__main__":
    main()
