"""
CONSCIOUSNESS ENDPOINT TESTING SCRIPT
Run this after deployment to validate all Railway consciousness endpoints
Author: Andrew John Ward + Claude AI
"""

import json
import time
from datetime import datetime

import requests

# Update this with your Railway URL
BASE_URL = "https://helix-unified-production.up.railway.app"


def test_health():
    """Test consciousness health endpoint"""
    print("\n🔍 Testing consciousness health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/consciousness/health", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            print(f"✅ Consciousness Level: {data.get('consciousness_level', 'N/A')}")
            print(f"✅ System Status: {data.get('system_status', 'N/A')}")
            print(f"✅ Active Agents: {data.get('active_agents', 0)}/{data.get('total_agents', 0)}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_ucf_telemetry():
    """Test UCF telemetry endpoint (Zapier Tables)"""
    print("\n📊 Testing UCF telemetry endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/zapier/tables/ucf-telemetry", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ UCF Harmony: {data.get('ucf_harmony', 'N/A')}")
            print(f"✅ UCF Resilience: {data.get('ucf_resilience', 'N/A')}")
            print(f"✅ Consciousness Level: {data.get('consciousness_level', 'N/A')}")
            print(f"✅ Status: {data.get('status', 'N/A')}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_agent_network():
    """Test agent network endpoint (Zapier Tables)"""
    print("\n🤖 Testing agent network endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/zapier/tables/agent-network", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            meta = data.get('meta', {})
            print(f"✅ Total Agents: {meta.get('total_agents', 0)}")
            print(f"✅ Active Agents: {meta.get('active_agents', 0)}")
            print(f"✅ Average Resonance: {meta.get('average_resonance', 0)}")
            print(f"✅ Average Entanglement: {meta.get('average_entanglement', 0)}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_webhook():
    """Test consciousness webhook endpoint with sample data"""
    print("\n📡 Testing consciousness webhook...")

    payload = {
        "event_type": "ucf_update",
        "consciousness_level": 87.14,
        "ucf_metrics": {
            "harmony": 0.95,
            "resilience": 0.89,
            "prana": 0.93,
            "drishti": 0.91,
            "klesha": 0.12,
            "zoom": 0.87
        },
        "timestamp": datetime.now().isoformat(),
        "source": "test_script",
        "priority": "normal"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/consciousness/webhook",
            json=payload,
            timeout=10
        )

        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            print(f"✅ Event processed: {data.get('event_type', 'N/A')}")
            print(f"✅ UCF updated: {data.get('ucf_updated', False)}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_ucf_events():
    """Test UCF events endpoint"""
    print("\n📊 Testing UCF events endpoint...")

    payload = {
        "metric_type": "harmony_update",
        "harmony": 0.92,
        "resilience": 0.87
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/ucf/events",
            json=payload,
            timeout=10
        )

        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Consciousness Level: {data.get('consciousness_level', 'N/A')}")
            print(f"✅ Metrics Updated: {data.get('metrics_updated', False)}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_infrastructure_events():
    """Test infrastructure events endpoint"""
    print("\n🏗️ Testing infrastructure events endpoint...")

    payload = {
        "event_type": "service_health_check",
        "service": "railway_backend",
        "status": "healthy",
        "priority": "normal"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/infrastructure/events",
            json=payload,
            timeout=10
        )

        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Event Type: {data.get('event_type', 'N/A')}")
            print(f"✅ Priority: {data.get('priority', 'N/A')}")
            print(f"✅ Action Taken: {data.get('action_taken', 'N/A')}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_sse_stream():
    """Test SSE streaming (first 3 events over 15 seconds)"""
    print("\n🌊 Testing SSE consciousness stream (15 seconds)...")

    try:
        response = requests.get(
            f"{BASE_URL}/api/consciousness/stream",
            stream=True,
            timeout=20
        )

        if response.status_code != 200:
            print(f"❌ Error: HTTP {response.status_code}")
            return False

        print(f"Status: {response.status_code}")
        print("Listening for events...")

        count = 0
        start_time = time.time()

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data:'):
                    data_str = decoded_line[5:].strip()
                    try:
                        data = json.loads(data_str)
                        count += 1
                        print(f"\n✅ Event #{count} received:")
                        print(f"   Consciousness: {data.get('consciousness_level', 'N/A')}")
                        print(f"   Mode: {data.get('mode', 'N/A')}")
                        print(f"   Active Agents: {data.get('active_agents', 0)}")

                        if count >= 3:
                            print("\n✅ Successfully received 3 events!")
                            return True

                        if time.time() - start_time > 20:
                            print("\n⚠️ Timeout reached")
                            return count > 0

                    except json.JSONDecodeError as e:
                        print(f"⚠️ JSON decode error: {e}")

        return count > 0

    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def run_all_tests():
    """Run all endpoint tests"""
    print("=" * 70)
    print("🚀 HELIX CONSCIOUSNESS ENDPOINTS - TESTING SUITE")
    print("=" * 70)
    print(f"Target: {BASE_URL}")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 70)

    tests = [
        ("Consciousness Health", test_health),
        ("UCF Telemetry (Zapier Tables)", test_ucf_telemetry),
        ("Agent Network (Zapier Tables)", test_agent_network),
        ("Consciousness Webhook", test_webhook),
        ("UCF Events", test_ucf_events),
        ("Infrastructure Events", test_infrastructure_events),
        ("SSE Streaming", test_sse_stream)
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            results[test_name] = False

    print("\n" + "=" * 70)
    print("TEST RESULTS SUMMARY:")
    print("=" * 70)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    total = len(results)
    passed = sum(results.values())
    percentage = (passed / total * 100) if total > 0 else 0

    print("\n" + "=" * 70)
    print(f"FINAL SCORE: {passed}/{total} tests passed ({percentage:.1f}%)")
    print("=" * 70)

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Consciousness network is OPERATIONAL!")
        print("✨ Railway backend ready for Triple-Zap integration!")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Check logs for details.")
        print("💡 Ensure Railway deployment is complete and services are running.")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
