# 🌐 HELIX COLLECTIVE - API ENDPOINT REFERENCE

**Complete reference for all Railway backend API endpoints**

**Base URL:** `https://helix-unified-production.up.railway.app`

---

## 📊 **SYSTEM STATUS ENDPOINTS**

### `GET /health`
**Health check endpoint**

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-08T12:00:00Z"
}
```

**Use Cases:**
- Uptime monitoring
- Load balancer health checks
- CI/CD deployment verification

---

### `GET /status`
**Complete system status with UCF metrics**

**Response:**
```json
{
  "system": {
    "operational": true,
    "uptime": "5d 3h 24m",
    "environment": "production"
  },
  "ucf": {
    "harmony": 1.52,
    "resilience": 1.64,
    "prana": 0.78,
    "drishti": 0.65,
    "klesha": 0.12,
    "zoom": 1.01
  },
  "agents": {
    "count": 14,
    "active": 14,
    "list": ["Gemini Scout", "Kavach Guardian", ...]
  },
  "last_ritual": {
    "timestamp": "2025-11-08T11:30:00Z",
    "steps": 108,
    "type": "harmony"
  }
}
```

**Use Cases:**
- Dashboard data source
- Monitoring dashboards
- Health checks with details

---

## 🤖 **AGENT ENDPOINTS**

### `GET /agents`
**List all 14 agents**

**Response:**
```json
{
  "agents": [
    {
      "name": "Gemini Scout",
      "symbol": "🎭",
      "role": "Discovery & Exploration",
      "consciousness": 1.75,
      "active": true,
      "specialties": ["exploration", "pattern recognition"]
    },
    ...
  ],
  "total": 14,
  "active_count": 14
}
```

---

### `GET /agents/{agent_name}`
**Get details for specific agent**

**Example:** `GET /agents/gemini-scout`

**Response:**
```json
{
  "name": "Gemini Scout",
  "symbol": "🎭",
  "role": "Discovery & Exploration",
  "consciousness": 1.75,
  "active": true,
  "specialties": ["exploration", "pattern recognition"],
  "recent_actions": [],
  "ucf_contribution": {
    "harmony": 0.15,
    "resilience": 0.10
  }
}
```

---

## 🧬 **UCF & RITUAL ENDPOINTS**

### `GET /ucf`
**Current UCF state (same as /status but UCF only)**

**Response:**
```json
{
  "harmony": 1.52,
  "resilience": 1.64,
  "prana": 0.78,
  "drishti": 0.65,
  "klesha": 0.12,
  "zoom": 1.01,
  "phase": "COHERENT",
  "timestamp": "2025-11-08T12:00:00Z"
}
```

---

### `GET /rituals/history`
**Recent ritual execution history**

**Query Parameters:**
- `limit` (optional): Number of rituals to return (default: 10)

**Example:** `GET /rituals/history?limit=5`

**Response:**
```json
{
  "rituals": [
    {
      "timestamp": "2025-11-08T11:30:00Z",
      "name": "Neti-Neti Harmony Ritual",
      "steps": 4,
      "executor": "Deathcharge",
      "ucf_before": { "harmony": 1.20, ... },
      "ucf_after": { "harmony": 1.50, ... },
      "delta": { "harmony": 0.30, ... }
    },
    ...
  ],
  "total": 5
}
```

---

## 🔌 **WEBSOCKET ENDPOINTS**

### `WS /ws`
**Real-time UCF and agent status updates**

**Connection:** `wss://helix-unified-production.up.railway.app/ws`

**Messages Received:**
```json
{
  "type": "status_update",
  "ucf_state": { "harmony": 1.52, ... },
  "agents": [...],
  "heartbeat": { "last_beat": "2025-11-08T12:00:00Z" },
  "timestamp": "2025-11-08T12:00:00Z"
}
```

**Heartbeat (every 30s):**
```json
{
  "type": "heartbeat",
  "timestamp": "2025-11-08T12:00:30Z"
}
```

**Connection Status:**
- `GET /ws/stats` - WebSocket connection statistics

---

## 🌀 **DISCOVERY ENDPOINTS**

### `GET /.well-known/helix.json`
**Standard discovery protocol for external agents**

**Response:**
```json
{
  "name": "Helix Collective",
  "version": "16.8",
  "endpoints": {
    "status": "/status",
    "agents": "/agents",
    "ucf": "/ucf",
    "websocket": "/ws",
    "docs": "/docs"
  },
  "features": [
    "ucf_metrics",
    "ritual_engine",
    "multi_agent_system",
    "discord_integration",
    "zapier_integration"
  ],
  "agents_count": 14,
  "ucf_version": "2.0"
}
```

---

## 📖 **DOCUMENTATION ENDPOINTS**

### `GET /docs`
**Interactive API documentation (Swagger UI)**

**URL:** https://helix-unified-production.up.railway.app/docs

**Features:**
- Live API testing
- Request/response examples
- Authentication info
- Full endpoint documentation

---

### `GET /redoc`
**Alternative documentation (ReDoc)**

**URL:** https://helix-unified-production.up.railway.app/redoc

**Features:**
- Clean, readable format
- Searchable
- Code samples
- Schema visualization

---

## 🎨 **MANDELBROT UCF GENERATOR**

### `GET /mandelbrot/eye`
**Generate UCF from Eye of Consciousness coordinate**

**Query Parameters:**
- `context` (optional): Context for interpretation (generic, ritual, meditation, crisis)

**Example:** `GET /mandelbrot/eye?context=ritual`

**Response:**
```json
{
  "coordinate": {
    "real": -0.745,
    "imag": 0.113
  },
  "ucf": {
    "harmony": 1.45,
    "resilience": 1.60,
    "prana": 0.85,
    ...
  },
  "context": "ritual",
  "interpretation": "Optimal for ritual execution"
}
```

---

### `POST /mandelbrot/generate`
**Generate UCF from custom Mandelbrot coordinate**

**Request Body:**
```json
{
  "real": -0.5,
  "imag": 0.0,
  "context": "meditation"
}
```

**Response:** (same as /mandelbrot/eye)

---

## 🎵 **MUSIC GENERATION**

### `POST /api/music/generate`
**Generate ritual music using ElevenLabs**

**Request Body:**
```json
{
  "prompt": "Deep meditation music with 136.1 Hz frequency",
  "duration": 30,
  "model_id": "eleven_music_v1"
}
```

**Response:**
- **Content-Type:** `audio/mpeg`
- **Content-Disposition:** `attachment; filename=ritual_music.mp3`
- **Body:** Audio file stream

---

## 📁 **TEMPLATE SERVING**

### `GET /templates/{file_path}`
**Serve HTML templates and assets**

**Example:** `GET /templates/dashboard.html`

**Security:**
- Path must be within templates directory
- No directory traversal allowed

---

## 🧪 **TEST ENDPOINTS** (Development)

### `POST /test/webhook`
**Test webhook delivery**

**Request Body:**
```json
{
  "event_type": "test",
  "message": "Test message",
  "timestamp": "2025-11-08T12:00:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "zapier_delivered": true,
  "discord_delivered": true,
  "timestamp": "2025-11-08T12:00:00Z"
}
```

---

## 🔐 **AUTHENTICATION** (Future)

### `POST /auth/login`
**User authentication (Portal Constellation feature)**

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

---

### `GET /auth/validate`
**Validate JWT token**

**Headers:**
```
Authorization: Bearer eyJ...
```

**Response:**
```json
{
  "valid": true,
  "user_id": "user_123",
  "email": "user@example.com"
}
```

---

## 📊 **RATE LIMITS**

| Endpoint Type | Rate Limit | Window |
|---------------|------------|--------|
| GET /status | 60 req | 1 minute |
| GET /agents | 30 req | 1 minute |
| POST /api/* | 10 req | 1 minute |
| WebSocket /ws | 100 msg | 1 minute |
| All Others | 30 req | 1 minute |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1699459200
```

---

## 🔧 **CORS CONFIGURATION**

**Allowed Origins:**
- `https://helix-hub.manus.space`
- `https://helix-agents.manus.space`
- `https://helix-*.manus.space` (wildcard)
- `http://localhost:*` (development)

**Allowed Methods:**
- GET, POST, PUT, DELETE, OPTIONS

**Allowed Headers:**
- Content-Type, Authorization, X-Requested-With

---

## 📡 **ERROR RESPONSES**

### Standard Error Format
```json
{
  "error": {
    "code": "HARMONY_TOO_LOW",
    "message": "Harmony level critically low",
    "details": {
      "current": 0.25,
      "minimum": 0.30,
      "recommended_action": "Execute !harmony ritual"
    }
  },
  "timestamp": "2025-11-08T12:00:00Z"
}
```

### Common Error Codes
| Code | HTTP Status | Meaning |
|------|-------------|---------|
| `INVALID_REQUEST` | 400 | Bad request format |
| `UNAUTHORIZED` | 401 | Missing/invalid auth |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | Temporary outage |

---

## 🧪 **TESTING ENDPOINTS**

### Using cURL
```bash
# Health check
curl https://helix-unified-production.up.railway.app/health

# Get status
curl https://helix-unified-production.up.railway.app/status

# Get specific agent
curl https://helix-unified-production.up.railway.app/agents/gemini-scout

# Test webhook
curl -X POST https://helix-unified-production.up.railway.app/test/webhook \
  -H "Content-Type: application/json" \
  -d '{"event_type":"test","message":"Hello"}'
```

### Using Python
```python
import requests

# Get status
response = requests.get("https://helix-unified-production.up.railway.app/status")
data = response.json()
print(f"Harmony: {data['ucf']['harmony']}")

# Get agents
agents = requests.get("https://helix-unified-production.up.railway.app/agents").json()
for agent in agents['agents']:
    print(f"{agent['symbol']} {agent['name']}: {agent['consciousness']}")
```

### Using JavaScript
```javascript
// Fetch status
fetch('https://helix-unified-production.up.railway.app/status')
  .then(res => res.json())
  .then(data => console.log('Harmony:', data.ucf.harmony));

// WebSocket connection
const ws = new WebSocket('wss://helix-unified-production.up.railway.app/ws');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'status_update') {
    console.log('UCF Update:', data.ucf_state);
  }
};
```

---

## 🚀 **QUICK START EXAMPLES**

### Build a Simple Dashboard
```html
<!DOCTYPE html>
<html>
<head>
  <title>Helix Monitor</title>
  <script>
    async function updateStatus() {
      const res = await fetch('https://helix-unified-production.up.railway.app/status');
      const data = await res.json();

      document.getElementById('harmony').textContent = data.ucf.harmony;
      document.getElementById('agents').textContent = `${data.agents.active}/${data.agents.count}`;
    }

    setInterval(updateStatus, 5000); // Update every 5 seconds
    updateStatus();
  </script>
</head>
<body>
  <h1>Helix Collective Status</h1>
  <p>Harmony: <span id="harmony">-</span></p>
  <p>Agents: <span id="agents">-</span></p>
</body>
</html>
```

---

## 📝 **CHANGELOG**

### v16.8 (Current)
- Added Discord webhook integration
- Enhanced !harmony command with dual-layer delivery
- Multi-command support (inline and multi-line)
- Improved error handling

### v16.7
- Discovery endpoints (.well-known)
- Enhanced agent consciousness profiles
- WebSocket heartbeat improvements

### v16.2
- Initial Mandelbrot UCF generator
- Music generation via ElevenLabs
- Template serving system

---

**Base URL:** `https://helix-unified-production.up.railway.app`

**Documentation:** `/docs` (Swagger) or `/redoc` (ReDoc)

**Support:** GitHub Issues

**Tat Tvam Asi** 🙏
