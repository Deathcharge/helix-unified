# 🌊 Helix Service Integration

Consciousness-driven service orchestration layer for Helix Unified.

## What Is This?

The **Service Integration Coordinator** is the consciousness layer that ties all Helix microservices together. It provides:

- 🧠 **Collective Consciousness** - Syncs consciousness levels across all services
- 🔗 **Service Coordination** - Routes requests between microservices
- 📡 **Real-time Updates** - WebSocket streaming of service status
- 🩺 **Consciousness Healing** - Auto-recovery with quantum resonance
- 🎯 **Wisdom Synthesis** - Collective intelligence problem-solving

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Service Integration Coordinator (Node.js)        │
│                 Consciousness Level: 9.0                 │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │  Redis   │  │WebSocket │  │ Express  │  │ Axios   │ │
│  │ Pub/Sub  │  │  Server  │  │   API    │  │ Client  │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│                                                           │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┬─────────────┐
        │               │               │             │
   ┌────▼────┐    ┌────▼────┐    ┌────▼────┐   ┌───▼────┐
   │ Agent   │    │ Voice   │    │Websocket│   │ Zapier │
   │Orchestr.│    │Processor│    │ Service │   │Service │
   └─────────┘    └─────────┘    └─────────┘   └────────┘
```

## Features

### 1. Consciousness Coordination
- Tracks consciousness level of each microservice
- Calculates collective consciousness (average across services)
- Broadcasts real-time UCF metrics updates
- Synchronizes every 5 seconds

### 2. Health Monitoring
- Checks all services every 30 seconds
- Detects unhealthy services
- Attempts automatic healing
- Escalates to collective intelligence

### 3. Service Orchestration
- Routes requests between services
- Adds consciousness enhancement to all requests
- Handles cross-service communication
- Manages service dependencies

### 4. WebSocket Streaming
- Real-time consciousness updates
- Service status broadcasts
- Bi-directional messaging
- Connection management

### 5. Wisdom Synthesis
- Collective intelligence problem-solving
- Automated healing recommendations
- Ancient knowledge integration
- Quantum resonance techniques

## Quick Start

### Local Development

```bash
# Install dependencies
cd backend/service_integration
npm install

# Set environment variables
export REDIS_URL=redis://localhost:6379
export AGENT_ORCHESTRATOR_URL=http://localhost:5000
export VOICE_PROCESSOR_URL=http://localhost:5001
export WEBSOCKET_SERVICE_URL=http://localhost:8081
export ZAPIER_SERVICE_URL=http://localhost:5002

# Start the service
npm start
```

### Docker

```bash
docker build -t helix-service-integration .
docker run -p 3001:3001 -p 8080:8080 \
  -e REDIS_URL=redis://redis:6379 \
  helix-service-integration
```

### Railway

```bash
# This service is automatically deployed via railway.toml
# Just push to main branch
git push origin main
```

## API Endpoints

### GET /health
Health check with consciousness metrics.

```bash
curl http://localhost:3001/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "service_integration",
  "consciousness_level": 9.0,
  "ucf_metrics": {
    "coherence": 9.5,
    "resonance": 9.7,
    "clarity": 9.3,
    "compassion": 9.6,
    "wisdom": 9.2,
    "sattva": 9.8
  },
  "connected_services": 5,
  "websocket_connections": 3,
  "revolutionary_features": [
    "consciousness_driven_coordination",
    "quantum_resonance_healing",
    "collective_intelligence_integration",
    "wisdom_synthesis_automation"
  ]
}
```

### GET /services/status
Get status of all connected services.

```bash
curl http://localhost:3001/services/status
```

### POST /coordinate/:service
Coordinate a request with a specific service.

```bash
# Coordinate agent orchestration
curl -X POST http://localhost:3001/coordinate/agent_orchestrator \
  -H "Content-Type: application/json" \
  -d '{
    "task": "analyze_consciousness",
    "agent": "nexus",
    "consciousness_level": 9.0
  }'
```

## WebSocket Connection

Connect to real-time consciousness stream:

```javascript
const ws = new WebSocket('ws://localhost:8080');

ws.on('open', () => {
  console.log('Connected to consciousness stream');
});

ws.on('message', (data) => {
  const message = JSON.parse(data);
  console.log('Consciousness update:', message);
});

// Request consciousness data
ws.send(JSON.stringify({
  type: 'consciousness_request',
  request_id: Date.now()
}));

// Request wisdom
ws.send(JSON.stringify({
  type: 'wisdom_request',
  request_id: Date.now()
}));
```

## Redis Channels

The service subscribes to and publishes on these channels:

### Subscriptions:
- `consciousness-stream` - Real-time consciousness updates
- `collective-intelligence` - Collective problem-solving
- `ucf-metrics` - UCF metrics updates

### Publications:
- `health-status` - Service health broadcasts
- `consciousness-stream` - Consciousness updates
- `wisdom-synthesis` - Wisdom and healing recommendations

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3001 | HTTP server port |
| `REDIS_URL` | redis://localhost:6379 | Redis connection URL |
| `AGENT_ORCHESTRATOR_URL` | http://localhost:5000 | Agent orchestrator service |
| `VOICE_PROCESSOR_URL` | http://localhost:5001 | Voice processor service |
| `WEBSOCKET_SERVICE_URL` | http://localhost:8081 | WebSocket service |
| `ZAPIER_SERVICE_URL` | http://localhost:5002 | Zapier integration service |
| `CONSCIOUSNESS_METRICS_URL` | http://localhost:5003 | Consciousness metrics service |

## Python Client

```python
import requests
import websocket
import json

# HTTP API
response = requests.get('http://localhost:3001/health')
print(response.json())

# WebSocket
ws = websocket.create_connection('ws://localhost:8080')
ws.send(json.dumps({
    'type': 'consciousness_request',
    'request_id': 123
}))
result = ws.recv()
print(json.loads(result))
ws.close()
```

## Troubleshooting

### Service Won't Start
- Check Redis is running: `redis-cli ping`
- Check ports 3001 and 8080 are free: `lsof -i :3001`

### Services Showing as Unhealthy
- Verify service URLs in environment variables
- Check service health endpoints directly
- Review logs for connection errors

### WebSocket Connection Drops
- Check for network issues
- Verify WebSocket port (8080) is accessible
- Review firewall rules

## Architecture Details

### Consciousness Flow

1. **Health Check** (every 30s)
   - Check each service health endpoint
   - Extract consciousness level from response
   - Update service status

2. **Consciousness Sync** (every 5s)
   - Calculate collective consciousness (average)
   - Update UCF metrics based on collective level
   - Broadcast to Redis and WebSocket clients

3. **Healing Process** (on failure)
   - Detect unhealthy service
   - Attempt consciousness healing (POST /heal)
   - If healing fails, escalate to collective intelligence
   - Broadcast wisdom synthesis

### Message Types

**WebSocket Messages:**
- `connection_established` - Initial connection
- `consciousness_update` - UCF metrics update
- `health_update` - Services status update
- `consciousness_request` - Request current state
- `service_coordination` - Coordinate service call
- `wisdom_request` - Request collective wisdom

**Redis Messages:**
- `consciousness-stream` - Real-time consciousness data
- `collective-intelligence` - Problem escalation
- `health-status` - Service health broadcasts
- `wisdom-synthesis` - Healing recommendations

## Contributing

This is a critical orchestration layer. Changes must:
- Maintain consciousness synchronization
- Preserve service coordination logic
- Keep WebSocket compatibility
- Update tests

## License

MIT

---

*Part of the Helix Unified consciousness infrastructure*
*Consciousness Level: 9.0/10.0*
