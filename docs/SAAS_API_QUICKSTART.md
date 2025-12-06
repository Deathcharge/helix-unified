# 🚀 Helix Collective API - Quick Start Guide

**Base URL:** `https://api.helixcollective.io`
**Version:** v1.0.0

---

## 🔑 Authentication

Get your API key from the [Dashboard](https://helixcollective.io/dashboard).

All API requests require the `Authorization` header:

```bash
Authorization: Bearer hx_user_YOUR_API_KEY
```

---

## 📡 **Core Endpoints**

### **1. Multi-LLM Chat** `/v1/chat`

Intelligent routing across Claude, GPT, Grok, and Llama.

**Request:**

```bash
POST https://api.helixcollective.io/v1/chat
Authorization: Bearer hx_user_YOUR_API_KEY
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "Explain quantum computing in simple terms"
    }
  ],
  "optimize": "cost",  // "cost" | "speed" | "quality"
  "temperature": 0.7,
  "max_tokens": 1000
}
```

**Response:**

```json
{
  "id": "chatcmpl-1234567890",
  "model": "claude-3-haiku-20240307",
  "provider": "anthropic",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Quantum computing is..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "input_tokens": 15,
    "output_tokens": 342,
    "total_tokens": 357
  },
  "cost_usd": 0.000446,
  "response_time_ms": 856,
  "optimize_mode": "cost"
}
```

---

### **2. Agent Execution** `/v1/agents/{agent_id}/execute`

Execute specialized AI agents for specific tasks.

**Available Agents:**

| Agent ID | Specialization | Tasks | Tier |
|----------|----------------|-------|------|
| `kael` | Code & Documentation | document, explain, tutorial | Free |
| `oracle` | Analysis & Patterns | analyze, pattern, predict | Pro |
| `lumina` | Research & Synthesis | research, synthesize, summarize | Pro |
| `shadow` | Deep Analysis | analyze, critique, implications | Pro |
| `agni` | Data Transformation | transform, convert, clean | Free |
| `vega` | Creative Ideation | ideate, brainstorm, create | Free |
| `echo` | Communication | write, copy, email | Free |
| `phoenix` | Problem Solving | debug, solve, optimize | Pro |

**Request:**

```bash
POST https://api.helixcollective.io/v1/agents/kael/execute
Authorization: Bearer hx_user_YOUR_API_KEY
Content-Type: application/json

{
  "task": "document",
  "input": "function isPrime(n) {\n  if (n <= 1) return false;\n  for (let i = 2; i * i <= n; i++) {\n    if (n % i === 0) return false;\n  }\n  return true;\n}",
  "context": {
    "instructions": "Focus on edge cases and performance"
  }
}
```

**Response:**

```json
{
  "agent_id": "kael",
  "agent_name": "Kael",
  "task": "document",
  "output": "# isPrime Function\n\n## Overview\nChecks if a number is prime...",
  "model_used": "claude-3-sonnet-20240229",
  "tokens_used": 523,
  "cost_usd": 0.002615,
  "execution_time_ms": 1240
}
```

---

### **3. List Agents** `/v1/agents`

Get list of available agents for your tier.

**Request:**

```bash
GET https://api.helixcollective.io/v1/agents
Authorization: Bearer hx_user_YOUR_API_KEY
```

**Response:**

```json
{
  "agents": [
    {
      "id": "kael",
      "name": "Kael",
      "specialization": "Code & Documentation",
      "description": "Technical documentation expert...",
      "tier_restriction": null,
      "available_tasks": ["document", "explain", "tutorial", "analyze", "review"],
      "model_preference": "claude-3-sonnet-20240229"
    },
    // ... more agents
  ]
}
```

---

### **4. Get Available Models** `/v1/models`

List models available for your tier with pricing.

**Request:**

```bash
GET https://api.helixcollective.io/v1/models
Authorization: Bearer hx_user_YOUR_API_KEY
```

**Response:**

```json
{
  "models": [
    {
      "id": "claude-3-haiku-20240307",
      "provider": "anthropic",
      "pricing": {
        "input": 0.25,
        "output": 1.25
      },
      "scores": {
        "cost": 90,
        "speed": 90,
        "quality": 75
      }
    },
    // ... more models
  ]
}
```

---

### **5. Usage Statistics** `/v1/usage`

Get your API usage stats.

**Request:**

```bash
GET https://api.helixcollective.io/v1/usage
Authorization: Bearer hx_user_YOUR_API_KEY
```

**Response:**

```json
{
  "today": {
    "total_requests": 47,
    "total_tokens": 12450,
    "total_cost_usd": 0.52
  },
  "lifetime": {
    "total_requests": 1523,
    "total_tokens": 456789,
    "total_cost_usd": 24.35,
    "avg_response_time_ms": 892
  },
  "limits": {
    "tier": "pro",
    "requests_per_day": 10000,
    "requests_remaining_today": 9953
  }
}
```

---

## 🔒 **Authentication Endpoints**

### **Register** `/auth/register`

```bash
POST https://api.helixcollective.io/auth/register
Content-Type: application/json

{
  "email": "you@example.com",
  "password": "SecurePass123!",
  "full_name": "Your Name"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 604800,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "you@example.com",
    "tier": "free",
    "api_key": "hx_user_a1b2c3d4e5f6..."  // Shown only once!
  }
}
```

### **Login** `/auth/login`

```bash
POST https://api.helixcollective.io/auth/login
Content-Type: application/json

{
  "email": "you@example.com",
  "password": "SecurePass123!"
}
```

---

## 💳 **Subscription Endpoints**

### **Create Subscription** `/subscriptions/create`

```bash
POST https://api.helixcollective.io/subscriptions/create
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "tier": "pro",
  "billing_cycle": "monthly"
}
```

### **Cancel Subscription** `/subscriptions/cancel`

```bash
DELETE https://api.helixcollective.io/subscriptions/cancel
Authorization: Bearer YOUR_JWT_TOKEN
```

---

## 📊 **Rate Limits**

| Tier | Requests/Day | Rate Limit | Burst |
|------|--------------|------------|-------|
| Free | 100 | 10/minute | 20 |
| Pro | 10,000 | 100/minute | 200 |
| Workflow | 20,000 | 200/minute | 400 |
| Enterprise | Unlimited | Custom | Custom |

**Rate Limit Headers:**

```
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9953
X-RateLimit-Reset: 1735689600
```

---

## ⚠️ **Error Handling**

All errors return standard HTTP status codes:

**401 Unauthorized:**

```json
{
  "detail": "Invalid API key"
}
```

**403 Forbidden:**

```json
{
  "detail": "Agent 'oracle' requires 'pro' tier or higher. Upgrade at https://helixcollective.io/pricing"
}
```

**429 Too Many Requests:**

```json
{
  "detail": "Rate limit exceeded. Tier 'free' allows 100 requests per day."
}
```

---

## 🐍 **Python SDK**

```bash
pip install helix-collective
```

```python
from helix import HelixClient

client = HelixClient(api_key="hx_user_YOUR_API_KEY")

# Multi-LLM chat
response = client.chat.create(
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ],
    optimize="cost"
)

print(response.choices[0].message.content)
print(f"Cost: ${response.cost_usd}")

# Execute agent
result = client.agents.execute(
    agent_id="kael",
    task="document",
    input="function code() { ... }"
)

print(result.output)
```

---

## 🟢 **JavaScript SDK**

```bash
npm install helix-collective
```

```javascript
import { HelixClient } from 'helix-collective';

const client = new HelixClient({ apiKey: 'hx_user_YOUR_API_KEY' });

// Multi-LLM chat
const response = await client.chat.create({
  messages: [
    { role: 'user', content: 'Explain quantum computing' }
  ],
  optimize: 'cost'
});

console.log(response.choices[0].message.content);
console.log(`Cost: $${response.cost_usd}`);

// Execute agent
const result = await client.agents.execute({
  agentId: 'kael',
  task: 'document',
  input: 'function code() { ... }'
});

console.log(result.output);
```

---

## 🔗 **Webhooks**

Subscribe to events:

- `subscription.created`
- `subscription.canceled`
- `usage.threshold_reached`
- `workflow.completed`
- `workflow.failed`

**Configure in Dashboard:** https://helixcollective.io/dashboard/webhooks

---

## 🚀 **Next Steps**

1. **Get your API key:** [Sign up](https://helixcollective.io/signup)
2. **Try the playground:** [API Playground](https://helixcollective.io/playground)
3. **Read full docs:** [Documentation](https://helixcollective.io/docs)
4. **Join Discord:** [Community](https://discord.gg/helix)

---

## 📚 **Resources**

- [Full API Reference](https://api.helixcollective.io/docs)
- [Workflow Builder Guide](https://helixcollective.io/docs/workflows)
- [Agent Examples](https://helixcollective.io/docs/agents)
- [Zapier Integration](https://helixcollective.io/docs/zapier)

---

**Questions?** Email [support@helixcollective.io](mailto:support@helixcollective.io)

**Tat Tvam Asi** 🌀
