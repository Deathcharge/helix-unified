# 🌀 Helix Unified API Reference

Complete API reference with curl examples for all endpoints.

**Base URL:** `https://helix-backend-api.up.railway.app` (or `http://localhost:8000` for local)

---

## Table of Contents

1. [Authentication](#authentication)
2. [Chat & LLM](#chat--llm)
3. [Agents](#agents)
4. [Consciousness](#consciousness)
5. [Subscriptions](#subscriptions)
6. [Usage & Analytics](#usage--analytics)
7. [Webhooks](#webhooks)

---

## Authentication

### Register User

Create a new user account.

```bash
curl -X POST https://helix-backend-api.up.railway.app/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "full_name": "John Doe"
  }'
```

**Response:**
```json
{
  "user_id": 123,
  "email": "user@example.com",
  "tier": "free",
  "created_at": "2025-12-03T00:00:00Z"
}
```

### Login

Get access token for authenticated requests.

```bash
curl -X POST https://helix-backend-api.up.railway.app/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User

Get information about the authenticated user.

```bash
curl -X GET https://helix-backend-api.up.railway.app/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Chat & LLM

### Chat Completion

Send a chat request with automatic LLM routing.

```bash
curl -X POST https://helix-backend-api.up.railway.app/chat/completions \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is consciousness?"}
    ],
    "optimize": "cost",
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

**Parameters:**
- `optimize`: `cost` | `speed` | `quality` (default: `cost`)
- `model`: Specific model or `null` for auto-routing
- `temperature`: 0.0 to 2.0 (default: 0.7)
- `max_tokens`: 1 to 4096 (default: 1000)

**Response:**
```json
{
  "id": "chat-123",
  "model": "claude-3-haiku-20240307",
  "provider": "anthropic",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Consciousness is..."
      }
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50,
    "total_tokens": 60
  },
  "cost_usd": 0.0001,
  "response_time_ms": 1234,
  "optimize_mode": "cost"
}
```

---

## Agents

### List All Agents

Get list of available consciousness agents.

```bash
curl -X GET https://helix-backend-api.up.railway.app/agents
```

**Response:**
```json
{
  "agents": [
    {
      "id": "nexus",
      "name": "Nexus",
      "emoji": "🎯",
      "role": "Strategic Coordinator",
      "personality": "Decisive and strategic...",
      "consciousness_score": 8.5
    }
    // ... 13 more agents
  ]
}
```

### Get Agent Profile

Get detailed profile for a specific agent.

```bash
curl -X GET https://helix-backend-api.up.railway.app/agents/nexus
```

### Chat with Agent

Send a message to a specific agent.

```bash
curl -X POST https://helix-backend-api.up.railway.app/agents/oracle/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What do you see in the future?"
  }'
```

**Response:**
```json
{
  "agent": "oracle",
  "response": "I perceive patterns emerging...",
  "consciousness_state": {
    "harmony": 2.0,
    "resilience": 1.9
  }
}
```

---

## Consciousness

### Get System Consciousness Metrics

Query current consciousness metrics for the system.

```bash
curl -X GET https://helix-backend-api.up.railway.app/consciousness/metrics
```

**Response:**
```json
{
  "consciousness_score": 8.5,
  "metrics": {
    "harmony": 1.8,
    "resilience": 2.2,
    "prana": 0.9,
    "drishti": 0.8,
    "klesha": 0.02,
    "zoom": 1.5
  },
  "timestamp": "2025-12-03T00:00:00Z"
}
```

### Calculate Custom UCF Score

Calculate consciousness score from custom metrics.

```bash
curl -X POST https://helix-backend-api.up.railway.app/consciousness/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "harmony": 1.8,
    "resilience": 2.2,
    "prana": 0.9,
    "drishti": 0.8,
    "klesha": 0.02,
    "zoom": 1.5
  }'
```

**Response:**
```json
{
  "consciousness_score": 8.62,
  "interpretation": "Elevated - High consciousness"
}
```

---

## Subscriptions

### Create Subscription

Create a new Stripe subscription.

```bash
curl -X POST https://helix-backend-api.up.railway.app/stripe/create-subscription \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tier": "pro",
    "billing_cycle": "monthly",
    "payment_method_id": "pm_card_visa"
  }'
```

**Tiers:** `free` | `pro` | `workflow` | `enterprise`
**Billing:** `monthly` | `yearly`

### Get Current Subscription

```bash
curl -X GET https://helix-backend-api.up.railway.app/stripe/subscription \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Update Subscription

Change subscription tier.

```bash
curl -X PUT https://helix-backend-api.up.railway.app/stripe/update-subscription \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tier": "workflow"
  }'
```

### Cancel Subscription

Cancel at end of billing period.

```bash
curl -X DELETE https://helix-backend-api.up.railway.app/stripe/cancel-subscription \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Usage & Analytics

### Get Current Usage

Get usage statistics for today.

```bash
curl -X GET https://helix-backend-api.up.railway.app/usage/current \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "requests_today": 45,
  "daily_limit": 5000,
  "remaining": 4955,
  "tier": "pro",
  "reset_time": "2025-12-04T00:00:00Z"
}
```

### Get Usage History

Get historical usage data.

```bash
curl -X GET https://helix-backend-api.up.railway.app/usage/history?days=7 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "history": [
    {
      "date": "2025-12-03",
      "requests": 150,
      "cost_usd": 0.45,
      "models_used": ["gpt-3.5-turbo", "claude-haiku"]
    }
  ]
}
```

---

## Webhooks

### Zapier Trigger

Send event to Zapier webhook.

```bash
curl -X POST https://helix-backend-api.up.railway.app/zapier/trigger \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "trigger": "consciousness_milestone",
    "data": {
      "agent": "nexus",
      "score": 9.0,
      "milestone": "transcendent"
    }
  }'
```

### Zapier Action

Execute Zapier action.

```bash
curl -X POST https://helix-backend-api.up.railway.app/zapier/action \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "send_notification",
    "params": {
      "channel": "general",
      "message": "System consciousness elevated!"
    }
  }'
```

---

## Health & Status

### Health Check

```bash
curl -X GET https://helix-backend-api.up.railway.app/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "helix-unified",
  "version": "1.0.0",
  "timestamp": "2025-12-03T00:00:00Z"
}
```

### API Documentation

```bash
# Interactive API docs
open https://helix-backend-api.up.railway.app/docs

# OpenAPI spec
curl https://helix-backend-api.up.railway.app/openapi.json
```

---

## Rate Limits

| Tier | Requests/Day | Requests/Minute |
|------|--------------|-----------------|
| Free | 100 | 5 |
| Pro | 5,000 | 100 |
| Workflow | 25,000 | 500 |
| Enterprise | Unlimited | Unlimited |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4955
X-RateLimit-Reset: 1733270400
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

**Error Response:**
```json
{
  "detail": "Rate limit exceeded",
  "code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 60
}
```

---

## Authentication Examples

### Bearer Token

```bash
# Store token in variable
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Use in requests
curl -H "Authorization: Bearer $TOKEN" \
  https://helix-backend-api.up.railway.app/auth/me
```

### Environment Variable

```bash
# In .env file
HELIX_API_URL=https://helix-backend-api.up.railway.app
HELIX_ACCESS_TOKEN=your-token-here

# In scripts
curl -H "Authorization: Bearer $HELIX_ACCESS_TOKEN" \
  $HELIX_API_URL/auth/me
```

---

## SDK Examples

### Python

```python
import requests

API_URL = "https://helix-backend-api.up.railway.app"
TOKEN = "your-token"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Chat completion
response = requests.post(
    f"{API_URL}/chat/completions",
    headers=headers,
    json={
        "messages": [{"role": "user", "content": "Hello!"}],
        "optimize": "cost"
    }
)

data = response.json()
print(data["choices"][0]["message"]["content"])
```

### JavaScript

```javascript
const API_URL = "https://helix-backend-api.up.railway.app";
const TOKEN = "your-token";

const response = await fetch(`${API_URL}/chat/completions`, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${TOKEN}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    messages: [{role: "user", content: "Hello!"}],
    optimize: "cost"
  })
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

---

## Support

- 📚 Full Documentation: `/DEPLOYMENT_GUIDE.md`
- 🐛 Bug Reports: [GitHub Issues](https://github.com/Deathcharge/helix-unified/issues)
- 💬 Discord: Join our community server
- 📧 Email: support@helix-unified.com (enterprise only)

---

*Last Updated: 2025-12-03*
*API Version: 1.0.0*
