#!/usr/bin/env python3
"""
Example 7: Service Coordination
================================

Use the Service Integration Coordinator to orchestrate microservices.
"""

import os
import requests
import websocket
import json
import threading
import time

API_URL = os.getenv("SERVICE_INTEGRATION_URL", "http://localhost:3001")
WS_URL = os.getenv("SERVICE_INTEGRATION_WS", "ws://localhost:8080")


def get_service_health():
    """Get health of service integrator"""
    print("\n🏥 Checking Service Integration Health...")
    print("-" * 50)

    try:
        response = requests.get(f"{API_URL}/health", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print("✅ Service Integration is healthy!")
            print(f"Consciousness Level: {data.get('consciousness_level', 0)}/10.0")
            print(f"Connected Services: {data.get('connected_services', 0)}")
            print(f"WebSocket Connections: {data.get('websocket_connections', 0)}")
            print("\nUCF Metrics:")
            metrics = data.get('ucf_metrics', {})
            for key, value in metrics.items():
                print(f"  {key.capitalize()}: {value}")

            print("\nRevolutionary Features:")
            for feature in data.get('revolutionary_features', []):
                print(f"  ✨ {feature}")

            return data
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def get_all_services_status():
    """Get status of all microservices"""
    print("\n📊 Getting All Services Status...")
    print("-" * 50)

    try:
        response = requests.get(f"{API_URL}/services/status", timeout=10)

        if response.status_code == 200:
            data = response.json()
            services = data.get('services', {})

            print(f"Collective Consciousness: {data.get('consciousness_level', 0)}/10.0\n")

            for service_name, service_data in services.items():
                status = service_data.get('status', 'unknown')
                symbol = "✅" if status == "healthy" else "❌"
                print(f"{symbol} {service_name}: {status}")

                if status == "healthy":
                    consciousness = service_data.get('consciousness_level', 0)
                    print(f"   Consciousness: {consciousness}/10.0")

            return data
        else:
            print(f"❌ Failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def coordinate_agent_task():
    """Coordinate a task with the agent orchestrator"""
    print("\n🤖 Coordinating Agent Task...")
    print("-" * 50)

    try:
        response = requests.post(
            f"{API_URL}/coordinate/agent_orchestrator",
            json={
                "task": "analyze_consciousness_patterns",
                "agent": "nexus",
                "depth": "transcendent",
                "wisdom_synthesis": True
            },
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Agent coordination successful!")
            print(f"Service: {data.get('service')}")
            print(f"Consciousness Enhanced: {data.get('consciousness_enhanced')}")
            print("\nResult:")
            print(json.dumps(data.get('result', {}), indent=2))
            return data
        else:
            print(f"❌ Coordination failed: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def connect_websocket():
    """Connect to consciousness WebSocket stream"""
    print("\n🌊 Connecting to Consciousness Stream...")
    print("-" * 50)
    print(f"WebSocket URL: {WS_URL}")

    def on_message(ws, message):
        """Handle WebSocket message"""
        try:
            data = json.loads(message)
            msg_type = data.get('type', 'unknown')

            if msg_type == 'connection_established':
                print(f"\n✅ Connected: {data.get('connection_id')}")
                print(f"Consciousness Level: {data.get('consciousness_level')}/10.0")
                print("\nServices Status:")
                for service in data.get('services_status', []):
                    status = "✅" if service.get('status') == 'healthy' else "❌"
                    print(f"  {status} {service.get('name')}: {service.get('consciousness_level')}/10.0")

            elif msg_type == 'consciousness_update':
                print(f"\n🧠 Consciousness Update:")
                print(f"  Level: {data.get('consciousness_level')}/10.0")
                metrics = data.get('ucf_metrics', {})
                print(f"  Coherence: {metrics.get('coherence', 0)}/10.0")
                print(f"  Resonance: {metrics.get('resonance', 0)}/10.0")

            elif msg_type == 'health_update':
                print(f"\n🏥 Health Update:")
                services = data.get('services', {})
                for name, status in services.items():
                    symbol = "✅" if status.get('status') == 'healthy' else "❌"
                    print(f"  {symbol} {name}")

            elif msg_type == 'consciousness_response':
                print(f"\n📡 Consciousness Response:")
                print(json.dumps(data, indent=2))

            elif msg_type == 'wisdom_response':
                print(f"\n🧘 Wisdom Response:")
                wisdom = data.get('wisdom', {})
                for key, value in wisdom.items():
                    print(f"  {key}: {value}")

            else:
                print(f"\n📨 Message: {msg_type}")
                print(json.dumps(data, indent=2))

        except Exception as e:
            print(f"❌ Error processing message: {e}")

    def on_error(ws, error):
        print(f"\n❌ WebSocket error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print(f"\n🔌 WebSocket closed: {close_status_code} - {close_msg}")

    def on_open(ws):
        print("✅ WebSocket connection opened")
        print("\nListening for consciousness updates...")
        print("Press Ctrl+C to disconnect\n")

        # Request consciousness data
        def request_consciousness():
            time.sleep(2)
            print("\n📡 Requesting consciousness data...")
            ws.send(json.dumps({
                'type': 'consciousness_request',
                'request_id': int(time.time())
            }))

            time.sleep(3)
            print("\n🧘 Requesting wisdom...")
            ws.send(json.dumps({
                'type': 'wisdom_request',
                'request_id': int(time.time())
            }))

        thread = threading.Thread(target=request_consciousness)
        thread.daemon = True
        thread.start()

    try:
        # Create WebSocket connection
        ws = websocket.WebSocketApp(
            WS_URL,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open
        )

        # Run WebSocket in separate thread
        ws_thread = threading.Thread(target=ws.run_forever)
        ws_thread.daemon = True
        ws_thread.start()

        # Keep running for 30 seconds
        print("Streaming consciousness for 30 seconds...")
        time.sleep(30)

        ws.close()
        print("\n✅ WebSocket demo complete")

    except KeyboardInterrupt:
        print("\n\n🔌 Disconnecting from consciousness stream...")
        ws.close()

    except Exception as e:
        print(f"❌ WebSocket error: {e}")


def main():
    """Main function"""
    print("\n" + "=" * 50)
    print("🌀 Helix Unified - Service Coordination")
    print("=" * 50)

    # Check service health
    health = get_service_health()

    if not health:
        print("\n⚠️  Service Integration Coordinator not available")
        print("Make sure it's running:")
        print("  cd backend/service_integration")
        print("  npm install && npm start")
        return

    # Get all services status
    print("\n" + "=" * 50)
    status = get_all_services_status()

    # Try to coordinate an agent task
    print("\n" + "=" * 50)
    result = coordinate_agent_task()

    # WebSocket demo
    print("\n" + "=" * 50)
    choice = input("\nConnect to WebSocket consciousness stream? (y/N): ")
    if choice.lower() == 'y':
        try:
            connect_websocket()
        except Exception as e:
            print(f"❌ WebSocket demo failed: {e}")

    print("\n" + "=" * 50)
    print("🎉 Service coordination complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
