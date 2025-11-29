# ⚡ Helix SaaS MVP - Quick Start Guide (9-Day Build)

**Goal:** Launch a working SaaS product that users can sign up for and pay

**Timeline:** 9 days of focused development
**Result:** Revenue-generating platform ready for Product Hunt launch

---

## 📋 What You're Building

A minimal but complete SaaS platform with:
- ✅ User authentication & subscription management
- ✅ Multi-LLM router API (`/v1/chat`)
- ✅ Agent execution API (`/v1/agents/{name}/execute`)
- ✅ Web dashboard with usage tracking
- ✅ Stripe payment integration
- ✅ API documentation

---

## 🚀 Day-by-Day Build Plan

### Day 1: Authentication & User Management

**Morning (4 hours): Database & Auth**

1. **Create database schema:**
```bash
cd /home/user/helix-unified
psql $DATABASE_URL < scripts/setup_saas_schema.sql
```

2. **Implement user registration:**
```python
# backend/auth_saas.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import bcrypt
import secrets

app = FastAPI()

class UserCreate(BaseModel):
    email: EmailStr
    password: str

@app.post("/auth/register")
async def register(user: UserCreate):
    # Hash password
    password_hash = bcrypt.hashpw(
        user.password.encode(),
        bcrypt.gensalt()
    ).decode()

    # Generate API key
    api_key = f"hx_user_{secrets.token_hex(32)}"

    # Insert into database
    result = await db.execute(
        """
        INSERT INTO users (email, password_hash, tier, api_key)
        VALUES ($1, $2, 'free', $3)
        RETURNING id, email, tier
        """,
        user.email, password_hash, api_key
    )

    return {
        "user_id": result["id"],
        "email": result["email"],
        "tier": result["tier"],
        "api_key": api_key  # Return ONCE
    }
```

**Afternoon (4 hours): Login & API Key Management**

3. **Implement login:**
```python
@app.post("/auth/login")
async def login(email: str, password: str):
    user = await db.fetchrow(
        "SELECT * FROM users WHERE email = $1", email
    )

    if not user or not bcrypt.checkpw(
        password.encode(),
        user["password_hash"].encode()
    ):
        raise HTTPException(401, "Invalid credentials")

    # Generate JWT
    token = create_jwt_token(user["id"], user["tier"])

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user["id"], "email": user["email"]}
    }
```

4. **API key authentication middleware:**
```python
from fastapi import Header, HTTPException

async def verify_api_key(authorization: str = Header()):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization header")

    api_key = authorization.replace("Bearer ", "")

    user = await db.fetchrow(
        "SELECT * FROM users WHERE api_key = $1", api_key
    )

    if not user:
        raise HTTPException(401, "Invalid API key")

    return user
```

**Deploy:** Test auth flow end-to-end

---

### Day 2: Multi-LLM Router API

**Morning (4 hours): Core Router Logic**

1. **Build `/v1/chat` endpoint:**
```python
# backend/router_saas.py
from typing import Literal
import anthropic
import openai

OptimizeMode = Literal["cost", "speed", "quality"]

@app.post("/v1/chat")
async def chat_completion(
    request: ChatRequest,
    user = Depends(verify_api_key)
):
    # Check rate limit
    await check_rate_limit(user["id"], user["tier"])

    # Route to best LLM
    provider, model = route_llm(
        request.messages,
        request.optimize,
        user["tier"]
    )

    # Call LLM
    if provider == "anthropic":
        response = await call_anthropic(model, request.messages)
    elif provider == "openai":
        response = await call_openai(model, request.messages)

    # Track usage
    await track_usage(
        user_id=user["id"],
        endpoint="/v1/chat",
        model=model,
        tokens=response["usage"]["total_tokens"],
        cost_usd=calculate_cost(model, response["usage"])
    )

    return response
```

**Afternoon (4 hours): Routing Logic**

2. **Implement smart routing:**
```python
def route_llm(
    messages: list,
    optimize: OptimizeMode,
    tier: str
) -> tuple[str, str]:
    """Route to best LLM based on optimization mode."""

    if optimize == "cost":
        # Route to cheapest model
        if tier == "free":
            return "anthropic", "claude-3-haiku-20240307"
        else:
            # Pro users can use Grok (cheapest)
            return "xai", "grok-beta"

    elif optimize == "speed":
        # Route to fastest model
        return "anthropic", "claude-3-haiku-20240307"

    elif optimize == "quality":
        # Route to best model (tier-dependent)
        if tier in ["pro", "enterprise"]:
            return "anthropic", "claude-3-opus-20240229"
        else:
            return "anthropic", "claude-3-sonnet-20240229"

    # Default
    return "anthropic", "claude-3-haiku-20240307"
```

3. **Add rate limiting:**
```python
async def check_rate_limit(user_id: str, tier: str):
    """Check if user has exceeded rate limit."""

    # Get limits by tier
    limits = {
        "free": {"day": 100, "minute": 10},
        "pro": {"day": 10000, "minute": 1000},
        "enterprise": {"day": None, "minute": None}
    }

    if tier == "enterprise":
        return  # No limits

    # Check daily limit
    daily_count = await redis.get(f"ratelimit:daily:{user_id}")
    if daily_count and int(daily_count) >= limits[tier]["day"]:
        raise HTTPException(429, "Daily rate limit exceeded")

    # Check per-minute limit
    minute_count = await redis.get(f"ratelimit:minute:{user_id}")
    if minute_count and int(minute_count) >= limits[tier]["minute"]:
        raise HTTPException(429, "Rate limit exceeded")

    # Increment counters
    await redis.incr(f"ratelimit:daily:{user_id}")
    await redis.expire(f"ratelimit:daily:{user_id}", 86400)  # 24h

    await redis.incr(f"ratelimit:minute:{user_id}")
    await redis.expire(f"ratelimit:minute:{user_id}", 60)  # 1min
```

**Deploy:** Test with curl

---

### Day 3: Agent Execution API

**Morning (4 hours): Agent Registry**

1. **Create agent registry:**
```python
# backend/agent_registry.py
from dataclasses import dataclass

@dataclass
class Agent:
    name: str
    display_name: str
    description: str
    tier_required: str
    cost_per_execution: float

AGENTS = {
    "kael": Agent(
        name="kael",
        display_name="Kael - Code & Docs",
        description="Code analysis and documentation",
        tier_required="free",
        cost_per_execution=0.001
    ),
    "oracle": Agent(
        name="oracle",
        display_name="Oracle - Analysis",
        description="Data analysis and insights",
        tier_required="free",
        cost_per_execution=0.002
    ),
    "lumina": Agent(
        name="lumina",
        display_name="Lumina - Research",
        description="Knowledge synthesis",
        tier_required="free",
        cost_per_execution=0.002
    ),
    # ... add remaining agents
}
```

**Afternoon (4 hours): Agent Execution**

2. **Build agent execution endpoint:**
```python
@app.post("/v1/agents/{agent_name}/execute")
async def execute_agent(
    agent_name: str,
    request: AgentRequest,
    user = Depends(verify_api_key)
):
    # Get agent
    agent = AGENTS.get(agent_name)
    if not agent:
        raise HTTPException(404, "Agent not found")

    # Check tier access
    if not can_access_agent(user["tier"], agent.tier_required):
        raise HTTPException(403, "Upgrade to access this agent")

    # Execute agent (sync for MVP, async later)
    result = await execute_agent_task(
        agent_name=agent_name,
        task=request.task,
        input=request.input,
        options=request.options
    )

    # Track usage
    await track_usage(
        user_id=user["id"],
        endpoint=f"/v1/agents/{agent_name}",
        model="claude-3-sonnet",  # Default for agents
        cost_usd=agent.cost_per_execution
    )

    return {
        "id": f"task_{secrets.token_hex(8)}",
        "agent": agent_name,
        "status": "completed",
        "result": result
    }
```

**Deploy:** Test agent execution

---

### Day 4: Stripe Payment Integration

**Morning (4 hours): Stripe Setup**

1. **Create Stripe products:**
```bash
# Create products in Stripe Dashboard
# - Free tier (no payment)
# - Pro tier: $29/month
# - Enterprise tier: Custom pricing
```

2. **Implement checkout flow:**
```python
# backend/payments_saas.py
import stripe

stripe.api_key = STRIPE_SECRET_KEY

@app.post("/v1/subscription/checkout")
async def create_checkout_session(
    tier: str,
    user = Depends(verify_jwt)
):
    # Get price ID
    price_ids = {
        "pro": "price_xxx",  # From Stripe Dashboard
        "enterprise": "price_yyy"
    }

    # Create Stripe checkout session
    session = stripe.checkout.Session.create(
        customer_email=user["email"],
        mode="subscription",
        line_items=[{
            "price": price_ids[tier],
            "quantity": 1
        }],
        success_url="https://helixcollective.io/dashboard?success=true",
        cancel_url="https://helixcollective.io/pricing?canceled=true",
        metadata={"user_id": user["id"]}
    )

    return {"checkout_url": session.url}
```

**Afternoon (4 hours): Webhooks**

3. **Handle Stripe webhooks:**
```python
@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(400, "Invalid payload")

    # Handle events
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session["metadata"]["user_id"]

        # Upgrade user tier
        await db.execute(
            "UPDATE users SET tier = 'pro' WHERE id = $1",
            user_id
        )

    elif event["type"] == "customer.subscription.deleted":
        # Downgrade to free tier
        pass

    return {"status": "success"}
```

**Deploy:** Test payment flow

---

### Day 5: Web Dashboard (Frontend)

**All Day (8 hours): Next.js Dashboard**

1. **Create dashboard pages:**
```bash
cd frontend

# Install dependencies
npm install @stripe/stripe-js recharts

# Create pages
mkdir -p app/dashboard
touch app/dashboard/page.tsx
touch app/dashboard/api-keys/page.tsx
touch app/dashboard/usage/page.tsx
```

2. **Dashboard homepage:**
```tsx
// app/dashboard/page.tsx
'use client';
import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetch('/api/v1/users/me', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
      .then(res => res.json())
      .then(setStats);
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      <div className="grid grid-cols-3 gap-4 mt-8">
        <div className="border p-4 rounded">
          <h3>Requests Today</h3>
          <p className="text-4xl">{stats?.usage.requests_today}</p>
        </div>

        <div className="border p-4 rounded">
          <h3>Tier</h3>
          <p className="text-4xl capitalize">{stats?.tier}</p>
        </div>

        <div className="border p-4 rounded">
          <h3>This Month</h3>
          <p className="text-4xl">${stats?.usage.cost_this_month}</p>
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-2xl">API Key</h2>
        <code className="bg-gray-100 p-2 mt-2 block">
          {stats?.api_key}
        </code>
      </div>
    </div>
  );
}
```

3. **Usage analytics page:**
```tsx
// app/dashboard/usage/page.tsx
'use client';
import { LineChart, Line, XAxis, YAxis } from 'recharts';

export default function Usage() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/v1/analytics/usage?days=30')
      .then(res => res.json())
      .then(d => setData(d.daily_breakdown));
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold">Usage Analytics</h1>

      <LineChart width={800} height={400} data={data}>
        <XAxis dataKey="date" />
        <YAxis />
        <Line type="monotone" dataKey="requests" stroke="#8884d8" />
        <Line type="monotone" dataKey="cost_usd" stroke="#82ca9d" />
      </LineChart>
    </div>
  );
}
```

**Deploy:** Test dashboard

---

### Day 6: API Documentation

**Morning (4 hours): OpenAPI Spec**

1. **Generate OpenAPI schema:**
```python
# FastAPI auto-generates OpenAPI
# Visit: https://api.helixcollective.io/docs
```

2. **Add API examples:**
```python
@app.post(
    "/v1/chat",
    summary="Multi-LLM Chat Completion",
    description="Route requests to the best LLM based on optimization mode",
    response_model=ChatResponse,
    responses={
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "id": "chat_abc123",
                        "model": "claude-3-haiku-20240307",
                        "choices": [{
                            "message": {
                                "role": "assistant",
                                "content": "Hello! How can I help?"
                            }
                        }]
                    }
                }
            }
        }
    }
)
async def chat_completion(...):
    ...
```

**Afternoon (4 hours): Code Examples**

3. **Write code examples:**
```markdown
# docs/api-examples.md

## Python Example

```python
import requests

API_KEY = "hx_user_xxx"

response = requests.post(
    "https://api.helixcollective.io/v1/chat",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "messages": [
            {"role": "user", "content": "Hello!"}
        ],
        "optimize": "cost"
    }
)

print(response.json())
```

## JavaScript Example

```javascript
const response = await fetch('https://api.helixcollective.io/v1/chat', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    messages: [{ role: 'user', content: 'Hello!' }],
    optimize: 'cost'
  })
});

const data = await response.json();
console.log(data);
```
```

**Deploy:** Publish docs

---

### Day 7: Landing Page

**All Day (8 hours): Marketing Site**

1. **Create landing page:**
```tsx
// app/page.tsx
export default function Home() {
  return (
    <div>
      {/* Hero Section */}
      <section className="text-center py-20">
        <h1 className="text-6xl font-bold">
          One API. Every AI. Optimized Automatically.
        </h1>
        <p className="text-xl mt-4 text-gray-600">
          Save 60% on LLM costs with intelligent multi-provider routing
        </p>
        <div className="mt-8">
          <a href="/signup" className="bg-blue-600 text-white px-8 py-3 rounded">
            Start Free
          </a>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-gray-100">
        <h2 className="text-4xl font-bold text-center">Features</h2>
        <div className="grid grid-cols-3 gap-8 mt-12 max-w-6xl mx-auto">
          <div className="text-center">
            <h3 className="text-2xl font-bold">Smart Routing</h3>
            <p>Auto-route to best LLM for cost, speed, or quality</p>
          </div>
          <div className="text-center">
            <h3 className="text-2xl font-bold">14 AI Agents</h3>
            <p>Pre-built agents for code, research, analysis</p>
          </div>
          <div className="text-center">
            <h3 className="text-2xl font-bold">Cost Analytics</h3>
            <p>Track spend and optimize costs automatically</p>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-20">
        <h2 className="text-4xl font-bold text-center">Pricing</h2>
        <div className="grid grid-cols-3 gap-8 mt-12 max-w-6xl mx-auto">
          {/* Free, Pro, Enterprise cards */}
        </div>
      </section>
    </div>
  );
}
```

**Deploy:** Publish landing page

---

### Day 8: Testing & Bug Fixes

**All Day (8 hours):**

1. **Write integration tests:**
```python
# tests/test_saas_flow.py
import pytest

def test_full_user_flow():
    # 1. Register user
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    api_key = response.json()["api_key"]

    # 2. Make API call
    response = client.post(
        "/v1/chat",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "optimize": "cost"
        }
    )
    assert response.status_code == 200

    # 3. Check usage
    response = client.get(
        "/v1/users/me",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    assert response.json()["usage"]["requests_today"] == 1
```

2. **Manual testing checklist:**
- [ ] User registration works
- [ ] Login works
- [ ] API key authentication works
- [ ] `/v1/chat` endpoint works for all optimization modes
- [ ] Rate limiting triggers correctly
- [ ] Agent execution works
- [ ] Stripe checkout flow works
- [ ] Webhook updates user tier
- [ ] Dashboard shows correct data
- [ ] API docs are accurate

3. **Fix bugs found during testing**

**Deploy:** Production-ready code

---

### Day 9: Launch Prep

**Morning (4 hours): Product Hunt Prep**

1. **Create demo video (2 minutes):**
- Show sign up flow
- Demonstrate API call with cost savings
- Show agent execution
- Demo dashboard analytics

2. **Write Product Hunt description:**
```
Helix Collective - Multi-LLM AI Router & Agent Marketplace

We built Helix because we were tired of:
- Managing 5 different API keys for different LLMs
- Unpredictable costs (one bad prompt = $50!)
- Rebuilding the same AI agents over and over

Helix gives you:
✅ One API for Claude, GPT, Grok, Llama
✅ Automatic routing to cheapest/fastest/best model
✅ 14 pre-built AI agents (code, research, analysis)
✅ Cost optimization (save 60% vs direct API usage)
✅ Generous free tier to get started

We're live now at helixcollective.io - try it free! 🚀
```

**Afternoon (4 hours): Launch**

3. **Launch checklist:**
- [ ] Set environment variables to production
- [ ] Enable Stripe live mode
- [ ] Set up monitoring alerts
- [ ] Prepare for traffic spike
- [ ] Write announcement tweet
- [ ] Post on Product Hunt at 12:01am PST
- [ ] Post "Show HN" on Hacker News
- [ ] Share on Reddit (r/SideProject, r/artificial)
- [ ] Email newsletter list
- [ ] Update LinkedIn

4. **Monitor launch:**
- Watch error logs (Sentry)
- Respond to comments (PH, HN, Reddit)
- Answer questions in real-time
- Fix critical bugs immediately

---

## 🎯 Success Criteria

**You've successfully launched when:**
- [ ] 10+ users have signed up
- [ ] 100+ API calls processed successfully
- [ ] $0 in errors or downtime
- [ ] At least 1 paying customer (even if it's yourself!)
- [ ] Product Hunt post live
- [ ] Documentation published

---

## 📊 Post-Launch (Week 2)

**Iterate based on feedback:**
1. Fix bugs reported by users
2. Add most-requested features
3. Improve documentation
4. Optimize performance
5. Add payment analytics

**Growth:**
1. Publish 2 blog posts
2. Create 3 YouTube videos
3. Reach out to 10 potential users
4. Set up referral program

---

## 🛠️ Essential Code Snippets

### Complete FastAPI App Structure

```python
# backend/app_saas.py
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import redis.asyncio as redis

app = FastAPI(title="Helix Collective API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://helixcollective.io"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Database connection
db_pool = None
redis_client = None

@app.on_event("startup")
async def startup():
    global db_pool, redis_client
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    redis_client = await redis.from_url(REDIS_URL)

@app.get("/health")
async def health():
    return {"status": "ok"}

# Import routes
from .auth_saas import router as auth_router
from .router_saas import router as llm_router
from .agents_saas import router as agent_router
from .payments_saas import router as payment_router

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(llm_router, prefix="/v1", tags=["llm"])
app.include_router(agent_router, prefix="/v1/agents", tags=["agents"])
app.include_router(payment_router, prefix="/v1/subscription", tags=["payments"])
```

### Environment Variables (.env)

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/helix
REDIS_URL=redis://default:pass@host:6379

# LLM Providers
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx
XAI_API_KEY=xai-xxx
PERPLEXITY_API_KEY=pplx-xxx

# Auth
JWT_SECRET_KEY=your-super-secret-key-change-this

# Payments
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# App
ENVIRONMENT=production
API_BASE_URL=https://api.helixcollective.io
FRONTEND_URL=https://helixcollective.io
```

---

## 🚀 Deploy Commands

**Railway:**
```bash
# One-time setup
railway init
railway add --database postgresql
railway add --database redis
railway variables set < .env

# Deploy
git add .
git commit -m "Launch MVP"
git push origin main  # Auto-deploys to Railway
```

**Vercel (Frontend):**
```bash
cd frontend
vercel --prod
```

---

## 🎉 You Did It!

You now have a working SaaS product that:
- ✅ Accepts user registrations
- ✅ Processes API requests
- ✅ Collects payments
- ✅ Tracks usage
- ✅ Provides value

**Next:** Get your first 100 users, iterate, and scale! 🚀

---

**Questions? Stuck?**
- Check the full docs in `/docs`
- Refer to existing code in `/backend`
- Test with `pytest tests/`

**Let's go build a unicorn! 🦄**
