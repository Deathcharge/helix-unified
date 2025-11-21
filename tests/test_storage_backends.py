#!/usr/bin/env python3
"""
🧪 Helix Storage Backend Test Suite
tests/test_storage_backends.py

Tests for multi-backend storage (Nextcloud + MEGA + Local)
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from helix_storage_adapter_async import HelixStorageAdapterAsync, upload_samsara_asset


async def test_nextcloud_connection():
    """Test Nextcloud WebDAV connection."""
    print("\n🧪 Testing Nextcloud Connection...")

    # Check environment variables
    required_vars = ["NEXTCLOUD_URL", "NEXTCLOUD_USER", "NEXTCLOUD_PASS"]
    missing = [v for v in required_vars if not os.getenv(v)]

    if missing:
        print(f"⚠️  Missing environment variables: {', '.join(missing)}")
        print("   Set these in Railway or local .env file")
        return False

    # Try to import webdav client
    try:
        from services.nextcloud_client import get_nextcloud_client
        client = get_nextcloud_client()

        if client and client.enabled:
            print("✅ Nextcloud client initialized!")

            # Test connection
            storage_info = client.get_storage_info()
            if 'error' not in storage_info:
                print(f"📊 Storage: {storage_info.get('quota_used', 0) / (1024**3):.2f} GB used")
                print(f"   Free: {storage_info.get('quota_available', 0) / (1024**3):.2f} GB")
                return True
            else:
                print(f"❌ Connection failed: {storage_info['error']}")
                return False
        else:
            print("❌ Nextcloud client not enabled")
            return False

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Install: pip install webdavclient3")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False


async def test_storage_adapter():
    """Test HelixStorageAdapterAsync with all backends."""
    print("\n🧪 Testing Storage Adapter...")

    storage = HelixStorageAdapterAsync()
    print(f"📦 Storage mode: {storage.mode}")

    # Test 1: Archive JSON
    test_data = {
        "test": "multi-backend storage",
        "timestamp": datetime.utcnow().isoformat(),
        "backends": ["nextcloud", "mega", "local"],
        "ucf_harmony": 0.618,
    }

    print("\n📝 Test 1: Archive JSON...")
    try:
        archive_path = await storage.archive_json(test_data, "test_storage_backend")
        print(f"✅ Archived to: {archive_path}")

        # Wait for background upload
        await asyncio.sleep(2)

    except Exception as e:
        print(f"❌ Archive failed: {e}")
        return False

    # Test 2: List archives
    print("\n📂 Test 2: List Archives...")
    try:
        archives = await storage.list_archives()
        print(f"✅ Found {len(archives)} archives")
        for arch in archives[:5]:
            print(f"   - {arch}")
    except Exception as e:
        print(f"❌ List failed: {e}")

    # Test 3: Get storage stats
    print("\n📊 Test 3: Storage Stats...")
    try:
        stats = await storage.get_storage_stats()
        print(f"✅ Mode: {stats['mode']}")
        print(f"   Archives: {stats['archive_count']}")
        print(f"   Size: {stats['total_size_mb']} MB")
        print(f"   Free: {stats['free_gb']} GB")
    except Exception as e:
        print(f"❌ Stats failed: {e}")

    # Test 4: Search archives
    print("\n🔍 Test 4: Search Archives...")
    try:
        results = await storage.search_archives("test_storage_*", limit=5)
        print(f"✅ Found {len(results)} matching archives")
        for res in results:
            print(f"   - {res['filename']} ({res['size_kb']} KB)")
    except Exception as e:
        print(f"❌ Search failed: {e}")

    return True


async def test_samsara_upload():
    """Test Samsara asset upload to Nextcloud."""
    print("\n🧪 Testing Samsara Asset Upload...")

    if os.getenv("HELIX_STORAGE_MODE") != "nextcloud":
        print("⚠️  Skipping (HELIX_STORAGE_MODE != nextcloud)")
        return True

    # Create test asset
    test_file = Path("Shadow/manus_archive/test_ritual_frame.json")
    test_file.parent.mkdir(parents=True, exist_ok=True)

    test_data = {
        "type": "ritual_frame",
        "timestamp": datetime.utcnow().isoformat(),
        "ucf_state": {
            "harmony": 0.62,
            "resilience": 1.85,
            "prana": 0.55,
        }
    }

    test_file.write_text(json.dumps(test_data, indent=2))

    # Upload
    try:
        success = await upload_samsara_asset(test_file, test_data)
        if success:
            print("✅ Samsara asset uploaded to Nextcloud!")
        else:
            print("⚠️  Upload failed (check logs)")
        return success
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False


async def main():
    """Run all tests."""
    print("=" * 60)
    print("🌀 HELIX STORAGE BACKEND TEST SUITE")
    print("=" * 60)

    results = {
        "nextcloud_connection": await test_nextcloud_connection(),
        "storage_adapter": await test_storage_adapter(),
        "samsara_upload": await test_samsara_upload(),
    }

    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)

    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test}")

    all_passed = all(results.values())

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED - Check configuration")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
