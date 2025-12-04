"""
🌀 Helix Collective v17.0 - Zapier Integration Test Suite
tests/test_zapier_integration_v17.py

Comprehensive test suite for v17.0 Zapier and Interface integration endpoints.

Tests:
- GET /api/zapier/tables/ucf-telemetry
- GET /api/zapier/tables/agent-network
- GET /api/zapier/tables/emergency-alerts
- POST /api/zapier/trigger-event
- POST /api/interface/consciousness/update
- POST /api/interface/command

Author: Andrew John Ward (Architect)
Version: 17.0.0
"""

from datetime import datetime

import httpx
import pytest

BASE_URL = "https://helix-unified-production.up.railway.app"
LOCAL_URL = "http://localhost:8000"

# Use local URL for testing if available, fallback to production
TEST_URL = LOCAL_URL


# Helper to check if server is running
async def _is_server_available():
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            await client.get(f"{TEST_URL}/health")
            return True
    except (httpx.ConnectError, httpx.TimeoutException):
        return False


# Skip all integration tests if server is not available
pytestmark = [
    pytest.mark.integration,
    pytest.mark.asyncio,
    pytest.mark.skipif(
        "not config.getoption('--run-integration')",
        reason="Integration tests require --run-integration flag or running API server"
    )
]


async def test_ucf_telemetry_endpoint():
    """Test GET /api/zapier/tables/ucf-telemetry"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TEST_URL}/api/zapier/tables/ucf-telemetry")

        assert response.status_code == 200
        data = response.json()

        assert data['success'] == True
        assert 'records' in data
        assert len(data['records']) > 0

        # Verify record structure
        record = data['records'][0]
        assert 'timestamp' in record
        assert 'consciousness_level' in record
        assert 'harmony' in record
        assert 'resilience' in record
        assert 'prana' in record
        assert 'drishti' in record
        assert 'klesha' in record
        assert 'zoom' in record
        assert 'system_version' in record
        assert 'source' in record

        # Verify table ID
        assert data['table_id'] == "01K9DP5MG6KCY48YC8M7VW0PXD"

        print(f"✅ UCF Telemetry endpoint test passed")
        print(f"   Consciousness Level: {record['consciousness_level']}")
        print(f"   System Status: {record.get('system_status', 'N/A')}")


async def test_agent_network_endpoint():
    """Test GET /api/zapier/tables/agent-network"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TEST_URL}/api/zapier/tables/agent-network")

        assert response.status_code == 200
        data = response.json()

        assert data['success'] == True
        assert 'agents' in data
        assert data['total_agents'] >= 14  # Should have at least 14 agents

        # Verify agent structure
        if len(data['agents']) > 0:
            agent = data['agents'][0]
            assert 'agent_name' in agent
            assert 'agent_id' in agent
            assert 'symbol' in agent
            assert 'status' in agent
            assert 'consciousness' in agent
            assert 'specialization' in agent
            assert 'ucf_resonance' in agent
            assert 'entanglement_factor' in agent

        # Verify table ID
        assert data['table_id'] == "01K9GT5YGZ1Y82K4VZF9YXHTMH"

        print(f"✅ Agent Network endpoint test passed")
        print(f"   Total Agents: {data['total_agents']}")
        print(f"   Active Agents: {data['active_agents']}")


async def test_emergency_alerts_endpoint():
    """Test GET /api/zapier/tables/emergency-alerts"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TEST_URL}/api/zapier/tables/emergency-alerts")

        assert response.status_code == 200
        data = response.json()

        assert data['success'] == True
        assert 'alerts' in data
        assert 'table_id' in data

        # Verify table ID
        assert data['table_id'] == "01K9DPA8RW9DTR2HJG7YDXA24Z"

        # If alerts exist, verify structure
        if len(data['alerts']) > 0:
            alert = data['alerts'][0]
            assert 'alert_id' in alert
            assert 'timestamp' in alert
            assert 'severity' in alert
            assert 'alert_type' in alert
            assert 'description' in alert
            assert 'consciousness_level' in alert
            assert 'affected_agents' in alert
            assert 'resolved' in alert

        print(f"✅ Emergency Alerts endpoint test passed")
        print(f"   Total Events: {data['total_emergency_events']}")
        print(f"   Critical Events: {data['critical_events']}")


async def test_trigger_event_endpoint():
    """Test POST /api/zapier/trigger-event"""
    async with httpx.AsyncClient() as client:
        payload = {
            "event_type": "interface_test",
            "source": "automated_test_suite",
            "consciousness_level": 7.5,
            "ucf": {
                "harmony": 0.85,
                "resilience": 1.90,
                "prana": 0.75,
                "drishti": 0.88,
                "klesha": 0.12,
                "zoom": 1.05
            }
        }

        response = await client.post(
            f"{TEST_URL}/api/zapier/trigger-event",
            json=payload,
            timeout=10.0
        )

        assert response.status_code == 200
        data = response.json()

        assert data['success'] == True
        assert 'consciousness_level' in data
        assert 'system_status' in data
        assert 'next_action' in data
        assert 'ucf' in data

        print(f"✅ Trigger Event endpoint test passed")
        print(f"   Consciousness Level: {data['consciousness_level']}")
        print(f"   System Status: {data['system_status']}")
        print(f"   Next Action: {data['next_action']}")


async def test_consciousness_update_endpoint():
    """Test POST /api/interface/consciousness/update"""
    async with httpx.AsyncClient() as client:
        payload = {
            "ucf": {
                "harmony": 0.87,
                "resilience": 1.92,
                "prana": 0.78,
                "drishti": 0.89,
                "klesha": 0.10,
                "zoom": 1.08
            },
            "source": "automated_test_suite"
        }

        response = await client.post(
            f"{TEST_URL}/api/interface/consciousness/update",
            json=payload,
            timeout=10.0
        )

        assert response.status_code == 200
        data = response.json()

        assert data['success'] == True
        assert 'consciousness_level' in data
        assert 'system_status' in data
        assert data['system_status'] in ['OPERATIONAL', 'CRISIS', 'WARNING', 'TRANSCENDENT']
        assert 'ucf' in data

        print(f"✅ Consciousness Update endpoint test passed")
        print(f"   Consciousness Level: {data['consciousness_level']}")
        print(f"   System Status: {data['system_status']}")


async def test_command_endpoint_ucf_boost():
    """Test POST /api/interface/command (ucf_boost)"""
    async with httpx.AsyncClient() as client:
        payload = {
            "command_type": "ucf_boost",
            "source": "automated_test_suite",
            "parameters": {
                "boost_amount": 0.15
            }
        }

        response = await client.post(
            f"{TEST_URL}/api/interface/command",
            json=payload,
            timeout=10.0
        )

        assert response.status_code == 200
        data = response.json()

        assert data['success'] == True
        assert 'result' in data
        assert data['command_type'] == 'ucf_boost'
        assert 'new_consciousness_level' in data['result']

        print(f"✅ Command endpoint (UCF Boost) test passed")
        print(f"   New Consciousness Level: {data['result']['new_consciousness_level']}")


async def test_command_endpoint_system_reset():
    """Test POST /api/interface/command (system_reset)"""
    async with httpx.AsyncClient() as client:
        payload = {
            "command_type": "system_reset",
            "source": "automated_test_suite"
        }

        response = await client.post(
            f"{TEST_URL}/api/interface/command",
            json=payload,
            timeout=10.0
        )

        assert response.status_code == 200
        data = response.json()

        assert data['success'] == True
        assert 'result' in data
        assert data['command_type'] == 'system_reset'
        assert 'new_consciousness_level' in data['result']
        assert 'ucf' in data['result']

        print(f"✅ Command endpoint (System Reset) test passed")
        print(f"   UCF reset to defaults")


async def test_health_endpoint():
    """Test GET /health (verify system is operational)"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TEST_URL}/health")

        assert response.status_code == 200
        data = response.json()

        assert data['ok'] == True
        assert 'version' in data
        assert 'timestamp' in data

        print(f"✅ Health endpoint test passed")
        print(f"   Version: {data['version']}")
        print(f"   System OK: {data['ok']}")


if __name__ == "__main__":
    import asyncio

    async def run_all_tests():
        """Run all tests sequentially"""
        print("\n🌀 Helix Collective v17.0 - Integration Test Suite")
        print("=" * 60)

        tests = [
            ("Health Check", test_health_endpoint),
            ("UCF Telemetry", test_ucf_telemetry_endpoint),
            ("Agent Network", test_agent_network_endpoint),
            ("Emergency Alerts", test_emergency_alerts_endpoint),
            ("Trigger Event", test_trigger_event_endpoint),
            ("Consciousness Update", test_consciousness_update_endpoint),
            ("Command: UCF Boost", test_command_endpoint_ucf_boost),
            ("Command: System Reset", test_command_endpoint_system_reset),
        ]

        passed = 0
        failed = 0

        for test_name, test_func in tests:
            try:
                print(f"\n📝 Testing: {test_name}")
                await test_func()
                passed += 1
            except Exception as e:
                print(f"❌ {test_name} FAILED: {e}")
                failed += 1

        print("\n" + "=" * 60)
        print(f"✅ Tests Passed: {passed}/{len(tests)}")
        print(f"❌ Tests Failed: {failed}/{len(tests)}")
        print("=" * 60)

    asyncio.run(run_all_tests())
