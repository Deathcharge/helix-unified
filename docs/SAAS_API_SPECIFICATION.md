# 🔌 Helix Collective SaaS - Complete API Specification

**Version:** 1.0.0
**Base URL:** `https://api.helixcollective.io/v1`
**Authentication:** Bearer token (API Key)

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Multi-LLM Router API](#multi-llm-router-api)
3. [Agent Execution API](#agent-execution-api)
4. [Prompt Library API](#prompt-library-api)
5. [Conversation Memory API](#conversation-memory-api)
6. [User Management API](#user-management-api)
7. [Analytics API](#analytics-api)
8. [Error Handling](#error-handling)
9. [Rate Limits](#rate-limits)
10. [Webhooks](#webhooks)

---

## 🔐 Authentication

All API requests require an API key passed via the `Authorization` header:

```bash
Authorization: Bearer hx_user_1234567890abcdef
```

### Get API Key

**Endpoint:** `POST /auth/api-keys`

**Description:** Generate a new API key for your account

**Request:**
```json
{
  "name": "Production Key",
  "expires_at": "2025-12-31T23:59:59Z"  // Optional
}
```

**Response:**
```json
{
  "api_key": "hx_user_1234567890abcdef",
  "name": "Production Key",
  "created_at": "2024-11-29T10:00:00Z",
  "expires_at": "2025-12-31T23:59:59Z",
  "tier": "pro"
}
```

### List API Keys

**Endpoint:** `GET /auth/api-keys`

**Response:**
```json
{
  "keys": [
    {
      "id": "key_abc123",
      "name": "Production Key",
      "prefix": "hx_user_1234",
      "created_at": "2024-11-29T10:00:00Z",
      "last_used": "2024-11-29T15:30:00Z",
      "expires_at": null
    }
  ]
}
```

### Revoke API Key

**Endpoint:** `DELETE /auth/api-keys/{key_id}`

**Response:**
```json
{
  "message": "API key revoked successfully",
  "revoked_at": "2024-11-29T16:00:00Z"
}
```

---

## 🧠 Multi-LLM Router API

### Chat Completion

**Endpoint:** `POST /v1/chat`

**Description:** Send a chat completion request that auto-routes to the best LLM based on your optimization preference.

**Request:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Explain quantum computing in simple terms."
    }
  ],
  "optimize": "cost",  // Options: "cost", "speed", "quality"
  "model": null,  // Optional: Override with specific model
  "max_tokens": 1000,
  "temperature": 0.7,
  "stream": false
}
```

**Response:**
```json
{
  "id": "chat_abc123",
  "object": "chat.completion",
  "created": 1701234567,
  "model": "claude-3-haiku-20240307",
  "routed_to": "anthropic",
  "routing_reason": "Cost optimized: 70% cheaper than GPT-4",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Quantum computing is like having a super-powered calculator..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 150,
    "total_tokens": 175
  },
  "cost": {
    "usd": 0.000525,
    "savings_vs_gpt4": 0.00368,
    "savings_percent": 87.5
  }
}
```

### Streaming Response

**Request:**
```json
{
  "messages": [...],
  "stream": true
}
```

**Response:** Server-Sent Events (SSE)
```
data: {"id":"chat_abc","object":"chat.completion.chunk","choices":[{"delta":{"content":"Quantum"}}]}

data: {"id":"chat_abc","object":"chat.completion.chunk","choices":[{"delta":{"content":" computing"}}]}

data: [DONE]
```

### Supported Models

**Endpoint:** `GET /v1/models`

**Response:**
```json
{
  "models": [
    {
      "id": "claude-3-opus-20240229",
      "provider": "anthropic",
      "context_window": 200000,
      "cost_per_1k_input": 0.015,
      "cost_per_1k_output": 0.075,
      "capabilities": ["chat", "vision", "function_calling"]
    },
    {
      "id": "gpt-4-turbo-preview",
      "provider": "openai",
      "context_window": 128000,
      "cost_per_1k_input": 0.01,
      "cost_per_1k_output": 0.03,
      "capabilities": ["chat", "vision", "function_calling"]
    },
    {
      "id": "grok-beta",
      "provider": "xai",
      "context_window": 131072,
      "cost_per_1k_input": 0.005,
      "cost_per_1k_output": 0.015,
      "capabilities": ["chat"]
    }
  ]
}
```

---

## 🤖 Agent Execution API

### Execute Agent Task

**Endpoint:** `POST /v1/agents/{agent_name}/execute`

**Description:** Execute a task using a specialized AI agent

**Available Agents:**
- `kael` - Code & Documentation
- `oracle` - Analysis & Insights
- `lumina` - Research & Knowledge
- `shadow` - Deep Analysis
- `agni` - Data Transformation
- `vega` - Strategy & Planning
- `nexus` - Integration & Coordination
- `sentinel` - Security & Validation
- `weaver` - Content Creation
- `catalyst` - Innovation & Ideation
- `architect` - System Design
- `ninja` - Code Optimization
- `sage` - Wisdom & Advice
- `forge` - Tool Building

**Request (Kael - Code Documentation):**
```json
{
  "task": "document",
  "input": {
    "code": "function isPrime(n) {\n  if (n <= 1) return false;\n  for (let i = 2; i * i <= n; i++) {\n    if (n % i === 0) return false;\n  }\n  return true;\n}",
    "language": "javascript"
  },
  "options": {
    "include_examples": true,
    "format": "markdown"
  }
}
```

**Response:**
```json
{
  "id": "task_xyz789",
  "agent": "kael",
  "status": "completed",
  "created_at": "2024-11-29T10:00:00Z",
  "completed_at": "2024-11-29T10:00:15Z",
  "execution_time_ms": 15230,
  "result": {
    "documentation": "## isPrime(n)\n\nChecks if a number is prime...",
    "examples": [
      "isPrime(7)  // true",
      "isPrime(10) // false"
    ]
  },
  "usage": {
    "tokens": 450,
    "cost_usd": 0.00135
  }
}
```

### Agent Task Status

**Endpoint:** `GET /v1/agents/tasks/{task_id}`

**Description:** Get the status of a long-running agent task

**Response:**
```json
{
  "id": "task_xyz789",
  "agent": "lumina",
  "status": "processing",  // queued, processing, completed, failed
  "progress": 45,  // Percentage (0-100)
  "created_at": "2024-11-29T10:00:00Z",
  "estimated_completion": "2024-11-29T10:02:30Z"
}
```

### List Available Agents

**Endpoint:** `GET /v1/agents`

**Response:**
```json
{
  "agents": [
    {
      "name": "kael",
      "display_name": "Kael - Code & Documentation",
      "description": "Specializes in code analysis, documentation generation, and technical writing",
      "capabilities": ["document", "analyze", "review"],
      "tier_required": "free",
      "cost_per_execution": 0.001
    },
    {
      "name": "oracle",
      "display_name": "Oracle - Analysis & Insights",
      "description": "Expert in pattern recognition, data analysis, and strategic insights",
      "capabilities": ["analyze", "predict", "recommend"],
      "tier_required": "free",
      "cost_per_execution": 0.002
    }
  ]
}
```

---

## 📚 Prompt Library API

### Create Prompt

**Endpoint:** `POST /v1/prompts`

**Request:**
```json
{
  "name": "Product Description Generator",
  "template": "Create a compelling product description for {product_name}. It should highlight the following features: {features}. Target audience: {audience}.",
  "tags": ["marketing", "ecommerce", "copywriting"],
  "is_public": false,
  "model_preference": "claude-3-sonnet-20240229",
  "default_parameters": {
    "temperature": 0.8,
    "max_tokens": 500
  }
}
```

**Response:**
```json
{
  "id": "prompt_abc123",
  "name": "Product Description Generator",
  "template": "Create a compelling product description...",
  "tags": ["marketing", "ecommerce", "copywriting"],
  "version": 1,
  "is_public": false,
  "created_at": "2024-11-29T10:00:00Z",
  "updated_at": "2024-11-29T10:00:00Z"
}
```

### Execute Prompt

**Endpoint:** `POST /v1/prompts/{prompt_id}/execute`

**Request:**
```json
{
  "variables": {
    "product_name": "Wireless Headphones Pro",
    "features": "noise cancellation, 40-hour battery, premium sound quality",
    "audience": "tech-savvy professionals"
  },
  "override_parameters": {
    "temperature": 0.9
  }
}
```

**Response:**
```json
{
  "id": "execution_xyz456",
  "prompt_id": "prompt_abc123",
  "result": "Introducing the Wireless Headphones Pro – your ultimate audio companion...",
  "usage": {
    "tokens": 320,
    "cost_usd": 0.00096
  },
  "created_at": "2024-11-29T10:05:00Z"
}
```

### List Prompts

**Endpoint:** `GET /v1/prompts`

**Query Parameters:**
- `page` - Page number (default: 1)
- `limit` - Results per page (default: 20, max: 100)
- `tags` - Filter by tags (comma-separated)
- `public` - Filter public prompts (true/false)

**Response:**
```json
{
  "prompts": [
    {
      "id": "prompt_abc123",
      "name": "Product Description Generator",
      "tags": ["marketing", "ecommerce"],
      "version": 3,
      "is_public": false,
      "executions": 45,
      "created_at": "2024-11-29T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 87,
    "total_pages": 5
  }
}
```

### Update Prompt (Creates New Version)

**Endpoint:** `PUT /v1/prompts/{prompt_id}`

**Request:**
```json
{
  "template": "Updated template with new instructions...",
  "tags": ["marketing", "ecommerce", "ai"]
}
```

**Response:**
```json
{
  "id": "prompt_abc123",
  "version": 4,  // Incremented
  "updated_at": "2024-11-29T11:00:00Z",
  "changelog": "Updated template with clearer instructions"
}
```

### Get Prompt Version History

**Endpoint:** `GET /v1/prompts/{prompt_id}/versions`

**Response:**
```json
{
  "prompt_id": "prompt_abc123",
  "versions": [
    {
      "version": 4,
      "template": "Updated template...",
      "updated_at": "2024-11-29T11:00:00Z",
      "updated_by": "user_123"
    },
    {
      "version": 3,
      "template": "Previous template...",
      "updated_at": "2024-11-28T15:00:00Z",
      "updated_by": "user_123"
    }
  ]
}
```

---

## 🧠 Conversation Memory API

### Create Conversation

**Endpoint:** `POST /v1/conversations`

**Request:**
```json
{
  "title": "Product Strategy Discussion",
  "metadata": {
    "project": "Q1 Launch",
    "team": "product"
  }
}
```

**Response:**
```json
{
  "id": "conv_abc123",
  "title": "Product Strategy Discussion",
  "created_at": "2024-11-29T10:00:00Z",
  "message_count": 0
}
```

### Add Message to Conversation

**Endpoint:** `POST /v1/conversations/{conversation_id}/messages`

**Request:**
```json
{
  "role": "user",
  "content": "What are the key features we should prioritize for Q1?"
}
```

**Response:**
```json
{
  "id": "msg_xyz789",
  "conversation_id": "conv_abc123",
  "role": "user",
  "content": "What are the key features we should prioritize for Q1?",
  "created_at": "2024-11-29T10:01:00Z"
}
```

### Continue Conversation (with AI)

**Endpoint:** `POST /v1/conversations/{conversation_id}/chat`

**Description:** Send a message and get an AI response with full conversation context

**Request:**
```json
{
  "message": "What are the key features we should prioritize for Q1?",
  "optimize": "quality",
  "retrieve_context": true  // Automatically pull relevant past messages
}
```

**Response:**
```json
{
  "message_id": "msg_xyz789",
  "response": {
    "id": "msg_xyz790",
    "role": "assistant",
    "content": "Based on our previous discussions about the target market...",
    "context_retrieved": [
      "msg_abc111",
      "msg_abc112"
    ]
  },
  "usage": {
    "tokens": 450,
    "cost_usd": 0.00135
  }
}
```

### Get Conversation

**Endpoint:** `GET /v1/conversations/{conversation_id}`

**Response:**
```json
{
  "id": "conv_abc123",
  "title": "Product Strategy Discussion",
  "messages": [
    {
      "id": "msg_xyz789",
      "role": "user",
      "content": "What are the key features...",
      "created_at": "2024-11-29T10:01:00Z"
    },
    {
      "id": "msg_xyz790",
      "role": "assistant",
      "content": "Based on our previous discussions...",
      "created_at": "2024-11-29T10:01:15Z"
    }
  ],
  "metadata": {
    "project": "Q1 Launch",
    "team": "product"
  },
  "created_at": "2024-11-29T10:00:00Z",
  "last_updated": "2024-11-29T10:01:15Z"
}
```

### List Conversations

**Endpoint:** `GET /v1/conversations`

**Query Parameters:**
- `page` - Page number
- `limit` - Results per page
- `search` - Search in titles and messages

**Response:**
```json
{
  "conversations": [
    {
      "id": "conv_abc123",
      "title": "Product Strategy Discussion",
      "message_count": 24,
      "last_message_at": "2024-11-29T10:01:15Z",
      "created_at": "2024-11-29T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 35
  }
}
```

### Export Conversation

**Endpoint:** `GET /v1/conversations/{conversation_id}/export`

**Query Parameters:**
- `format` - `json`, `markdown`, `pdf`

**Response (JSON):**
```json
{
  "conversation": {
    "id": "conv_abc123",
    "title": "Product Strategy Discussion",
    "messages": [...],
    "exported_at": "2024-11-29T12:00:00Z"
  }
}
```

---

## 👤 User Management API

### Get Current User

**Endpoint:** `GET /v1/users/me`

**Response:**
```json
{
  "id": "user_123",
  "email": "developer@example.com",
  "tier": "pro",
  "created_at": "2024-11-01T10:00:00Z",
  "subscription": {
    "status": "active",
    "current_period_end": "2024-12-01T10:00:00Z",
    "cancel_at_period_end": false
  },
  "usage": {
    "requests_today": 245,
    "requests_limit": 10000,
    "agents_available": 14,
    "prompts_count": 23
  }
}
```

### Update User Profile

**Endpoint:** `PATCH /v1/users/me`

**Request:**
```json
{
  "name": "John Doe",
  "company": "Acme Corp",
  "notification_preferences": {
    "usage_alerts": true,
    "product_updates": true
  }
}
```

### Upgrade Subscription

**Endpoint:** `POST /v1/users/me/subscription/upgrade`

**Request:**
```json
{
  "tier": "pro",  // or "enterprise"
  "billing_cycle": "monthly"  // or "yearly"
}
```

**Response:**
```json
{
  "checkout_url": "https://stripe.com/checkout/session_xyz",
  "tier": "pro",
  "price": 29.00
}
```

---

## 📊 Analytics API

### Get Usage Stats

**Endpoint:** `GET /v1/analytics/usage`

**Query Parameters:**
- `start_date` - ISO 8601 date
- `end_date` - ISO 8601 date
- `granularity` - `day`, `week`, `month`

**Response:**
```json
{
  "period": {
    "start": "2024-11-01T00:00:00Z",
    "end": "2024-11-30T23:59:59Z"
  },
  "summary": {
    "total_requests": 4523,
    "total_tokens": 1234567,
    "total_cost_usd": 37.04,
    "average_cost_per_request": 0.00819
  },
  "by_model": [
    {
      "model": "claude-3-haiku-20240307",
      "requests": 2341,
      "tokens": 456789,
      "cost_usd": 13.70,
      "percentage": 37.0
    },
    {
      "model": "gpt-4-turbo-preview",
      "requests": 1234,
      "tokens": 567890,
      "cost_usd": 17.04,
      "percentage": 46.0
    }
  ],
  "daily_breakdown": [
    {
      "date": "2024-11-01",
      "requests": 156,
      "cost_usd": 1.28
    }
  ]
}
```

### Get Cost Optimization Report

**Endpoint:** `GET /v1/analytics/cost-optimization`

**Response:**
```json
{
  "current_monthly_cost": 37.04,
  "projected_monthly_cost": 111.12,
  "potential_savings": {
    "by_switching_models": {
      "amount_usd": 23.45,
      "percentage": 21.1,
      "recommendation": "Switch 45% of GPT-4 requests to Claude Haiku for simple tasks"
    },
    "by_caching": {
      "amount_usd": 8.90,
      "percentage": 8.0,
      "recommendation": "Enable prompt caching for repeated system messages"
    }
  },
  "model_comparison": [
    {
      "task_type": "code_generation",
      "current_model": "gpt-4-turbo",
      "current_cost": 0.023,
      "alternative_model": "claude-3-sonnet",
      "alternative_cost": 0.012,
      "quality_impact": "minimal",
      "savings_per_request": 0.011
    }
  ]
}
```

### Get Agent Performance

**Endpoint:** `GET /v1/analytics/agents`

**Response:**
```json
{
  "agents": [
    {
      "name": "kael",
      "executions": 234,
      "average_execution_time_ms": 12340,
      "success_rate": 98.7,
      "total_cost_usd": 7.02,
      "average_cost_per_execution": 0.03
    },
    {
      "name": "oracle",
      "executions": 145,
      "average_execution_time_ms": 18900,
      "success_rate": 99.3,
      "total_cost_usd": 11.60,
      "average_cost_per_execution": 0.08
    }
  ]
}
```

---

## ⚠️ Error Handling

### Error Response Format

All errors follow this structure:

```json
{
  "error": {
    "type": "rate_limit_exceeded",
    "message": "You have exceeded your daily request limit of 100 requests",
    "details": {
      "limit": 100,
      "used": 101,
      "reset_at": "2024-11-30T00:00:00Z"
    },
    "doc_url": "https://docs.helixcollective.io/errors/rate-limit"
  }
}
```

### Common Error Codes

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | `invalid_request` | Malformed request body or parameters |
| 401 | `authentication_failed` | Invalid or expired API key |
| 403 | `permission_denied` | Feature not available in your tier |
| 404 | `resource_not_found` | Requested resource doesn't exist |
| 429 | `rate_limit_exceeded` | Too many requests |
| 500 | `internal_error` | Server-side error |
| 503 | `service_unavailable` | Temporary service outage |

### Rate Limit Headers

Every API response includes rate limit information:

```
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9876
X-RateLimit-Reset: 1701302400
X-RateLimit-Tier: pro
```

---

## 🚦 Rate Limits

### By Subscription Tier

| Tier | Requests/Day | Requests/Minute | Agents | Prompts | Conversations |
|------|--------------|-----------------|--------|---------|---------------|
| Free | 100 | 10 | 3 | 10 | 10 (7-day) |
| Pro | 10,000 | 1,000 | 14 | Unlimited | Unlimited (90-day) |
| Enterprise | Unlimited | Custom | Custom | Unlimited | Unlimited (Forever) |

### Rate Limit Exceeded Response

```json
{
  "error": {
    "type": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Upgrade to Pro for higher limits.",
    "details": {
      "limit": 100,
      "used": 100,
      "reset_at": "2024-11-30T00:00:00Z",
      "upgrade_url": "https://helixcollective.io/upgrade"
    }
  }
}
```

---

## 🔔 Webhooks

### Configure Webhook

**Endpoint:** `POST /v1/webhooks`

**Request:**
```json
{
  "url": "https://your-app.com/webhooks/helix",
  "events": [
    "conversation.message.created",
    "agent.task.completed",
    "usage.limit.reached"
  ],
  "secret": "your_webhook_secret"
}
```

### Available Events

**Conversation Events:**
- `conversation.created`
- `conversation.message.created`
- `conversation.updated`

**Agent Events:**
- `agent.task.queued`
- `agent.task.processing`
- `agent.task.completed`
- `agent.task.failed`

**Usage Events:**
- `usage.limit.warning` (80% of limit)
- `usage.limit.reached`
- `subscription.updated`
- `subscription.cancelled`

### Webhook Payload Example

```json
{
  "id": "evt_abc123",
  "type": "agent.task.completed",
  "created_at": "2024-11-29T10:05:00Z",
  "data": {
    "task_id": "task_xyz789",
    "agent": "kael",
    "status": "completed",
    "result": {...}
  }
}
```

### Webhook Signature Verification

All webhooks include an `X-Helix-Signature` header:

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

---

## 🔧 SDKs & Code Examples

### Python

```python
from helix import Helix

client = Helix(api_key="hx_user_123...")

# Chat completion
response = client.chat.create(
    messages=[{"role": "user", "content": "Hello!"}],
    optimize="cost"
)
print(response.choices[0].message.content)

# Execute agent
result = client.agents.execute(
    agent="kael",
    task="document",
    input={"code": "function hello() { ... }"}
)
print(result.documentation)

# Create prompt
prompt = client.prompts.create(
    name="Email Generator",
    template="Write an email about {topic} to {recipient}"
)

# Execute prompt
email = prompt.execute(
    variables={"topic": "Q1 Results", "recipient": "investors"}
)
```

### JavaScript/TypeScript

```javascript
import { Helix } from '@helix/sdk';

const helix = new Helix({ apiKey: 'hx_user_123...' });

// Chat completion
const response = await helix.chat.create({
  messages: [{ role: 'user', content: 'Hello!' }],
  optimize: 'cost'
});

// Execute agent
const result = await helix.agents.execute('kael', {
  task: 'document',
  input: { code: 'function hello() { ... }' }
});

// Streaming
const stream = await helix.chat.stream({
  messages: [{ role: 'user', content: 'Tell me a story' }]
});

for await (const chunk of stream) {
  process.stdout.write(chunk.content);
}
```

### cURL Examples

```bash
# Chat completion
curl https://api.helixcollective.io/v1/chat \
  -H "Authorization: Bearer hx_user_123..." \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "optimize": "cost"
  }'

# Execute agent
curl https://api.helixcollective.io/v1/agents/kael/execute \
  -H "Authorization: Bearer hx_user_123..." \
  -H "Content-Type: application/json" \
  -d '{
    "task": "document",
    "input": {"code": "function hello() { console.log(\"Hi\"); }"}
  }'

# Create prompt
curl https://api.helixcollective.io/v1/prompts \
  -H "Authorization: Bearer hx_user_123..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Email Generator",
    "template": "Write an email about {topic}"
  }'
```

---

## 📚 Additional Resources

- **OpenAPI Spec:** https://api.helixcollective.io/openapi.json
- **Postman Collection:** https://docs.helixcollective.io/postman
- **SDK Documentation:**
  - Python: https://pypi.org/project/helix-sdk
  - JavaScript: https://npmjs.com/package/@helix/sdk
- **Support:** support@helixcollective.io
- **Status Page:** https://status.helixcollective.io

---

**Ready to build? Get your API key at https://helixcollective.io/signup** 🚀
