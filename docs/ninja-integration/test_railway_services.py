#!/usr/bin/env python3

import requests
import json
import time
import os
import jwt
from datetime import datetime, timedelta

# Configuration
RAILWAY_SELF_MANAGEMENT_URL = os.getenv("RAILWAY_SELF_MANAGEMENT_URL", "http://localhost:3000")
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")

# Generate test JWT token
def generate_test_token():
    payload = {
        "sub": "test-user",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# Test headers
TEST_HEADERS = {
    "Authorization": f"Bearer {generate_test_token()}",
    "Content-Type": "application/json"
}

def test_railway_self_management():
    """Test Railway self-management system"""
    print("Testing Railway Self-Management System...")
    
    # Test health check
    try:
        response = requests.get(f"{RAILWAY_SELF_MANAGEMENT_URL}/api/services")
        if response.status_code == 200:
            print("✅ Railway self-management system is healthy")
            return True
        else:
            print(f"❌ Railway self-management system health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Railway self-management system health check failed: {e}")
        return False

def test_websocket_service():
    """Test WebSocket Consciousness Streaming Service"""
    print("Testing WebSocket Consciousness Streaming Service...")
    
    # Test health check
    try:
        response = requests.get(f"{RAILWAY_SELF_MANAGEMENT_URL}/../websocket-service/health")
        if response.status_code == 200:
            print("✅ WebSocket service is healthy")
        else:
            print(f"❌ WebSocket service health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ WebSocket service health check failed: {e}")
        return False
    
    # Test consciousness metrics endpoint
    try:
        response = requests.get(f"{RAILWAY_SELF_MANAGEMENT_URL}/../websocket-service/api/consciousness/metrics", headers=TEST_HEADERS)
        if response.status_code == 200:
            print("✅ WebSocket consciousness metrics endpoint working")
        else:
            print(f"❌ WebSocket consciousness metrics endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ WebSocket consciousness metrics endpoint failed: {e}")
        return False
    
    return True

def test_agent_orchestration_service():
    """Test Agent Orchestration Service"""
    print("Testing Agent Orchestration Service...")
    
    # Test health check
    try:
        response = requests.get(f"{RAILWAY_SELF_MANAGEMENT_URL}/../agent-orchestration/health")
        if response.status_code == 200:
            print("✅ Agent orchestration service is healthy")
        else:
            print(f"❌ Agent orchestration service health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Agent orchestration service health check failed: {e}")
        return False
    
    # Test agent profile creation
    agent_data = {
        "agent_id": f"test-agent-{int(time.time())}",
        "name": "Test Agent",
        "role": "testing",
        "capabilities": ["test", "validation"]
    }
    
    try:
        response = requests.post(
            f"{RAILWAY_SELF_MANAGEMENT_URL}/../agent-orchestration/api/agents",
            headers=TEST_HEADERS,
            data=json.dumps(agent_data)
        )
        if response.status_code == 200:
            agent_response = response.json()
            print("✅ Agent profile created successfully")
            agent_id = agent_response["agent_id"]
        else:
            print(f"❌ Agent profile creation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Agent profile creation failed: {e}")
        return False
    
    # Test agent listing
    try:
        response = requests.get(
            f"{RAILWAY_SELF_MANAGEMENT_URL}/../agent-orchestration/api/agents",
            headers=TEST_HEADERS
        )
        if response.status_code == 200:
            print("✅ Agent listing working")
        else:
            print(f"❌ Agent listing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Agent listing failed: {e}")
        return False
    
    # Test agent deletion
    try:
        response = requests.delete(
            f"{RAILWAY_SELF_MANAGEMENT_URL}/../agent-orchestration/api/agents/{agent_id}",
            headers=TEST_HEADERS
        )
        if response.status_code == 200:
            print("✅ Agent profile deleted successfully")
        else:
            print(f"❌ Agent profile deletion failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Agent profile deletion failed: {e}")
        return False
    
    return True

def test_voice_processing_service():
    """Test Voice Processing Service"""
    print("Testing Voice Processing Service...")
    
    # Test health check
    try:
        response = requests.get(f"{RAILWAY_SELF_MANAGEMENT_URL}/../voice-processor/health")
        if response.status_code == 200:
            print("✅ Voice processing service is healthy")
        else:
            print(f"❌ Voice processing service health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Voice processing service health check failed: {e}")
        return False
    
    # Test transcription endpoint
    try:
        response = requests.get(f"{RAILWAY_SELF_MANAGEMENT_URL}/../voice-processor/api/transcribe/test", headers=TEST_HEADERS)
        if response.status_code == 200:
            print("✅ Voice transcription test endpoint working")
        else:
            print(f"❌ Voice transcription test endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Voice transcription test endpoint failed: {e}")
        return False
    
    return True

def test_zapier_integration_service():
    """Test Zapier Integration Service"""
    print("Testing Zapier Integration Service...")
    
    # Test health check
    try:
        response = requests.get(f"{RAILWAY_SELF_MANAGEMENT_URL}/../zapier-service/health")
        if response.status_code == 200:
            print("✅ Zapier integration service is healthy")
        else:
            print(f"❌ Zapier integration service health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Zapier integration service health check failed: {e}")
        return False
    
    # Test Zapier integration endpoint
    try:
        response = requests.get(f"{RAILWAY_SELF_MANAGEMENT_URL}/../zapier-service/api/test", headers=TEST_HEADERS)
        if response.status_code == 200:
            print("✅ Zapier integration test endpoint working")
        else:
            print(f"❌ Zapier integration test endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Zapier integration test endpoint failed: {e}")
        return False
    
    # Test webhook status
    try:
        response = requests.get(f"{RAILWAY_SELF_MANAGEMENT_URL}/../zapier-service/api/webhooks/status", headers=TEST_HEADERS)
        if response.status_code == 200:
            print("✅ Zapier webhook status endpoint working")
        else:
            print(f"❌ Zapier webhook status endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Zapier webhook status endpoint failed: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("Starting Helix Unified Discord Bot Service Testing...")
    print("=" * 50)
    
    # Test each service
    tests = [
        test_railway_self_management,
        test_websocket_service,
        test_agent_orchestration_service,
        test_voice_processing_service,
        test_zapier_integration_service
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
            print()
    
    # Summary
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())