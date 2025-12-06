# HELIX MONETIZATION - QUICK START GUIDE
## Copy-Paste Implementation Code

**Use this guide to implement the first product (UCF Dashboard SaaS) in 2-3 weeks**

---

## STEP 1: Add User Subscription Tiers (1 day)

### Update Prisma Schema
```prisma
// prisma/schema.prisma

model User {
  id                String   @id @default(cuid())
  email             String   @unique
  passwordHash      String?
  
  // Subscription
  subscriptionTier  SubscriptionTier @default(FREE)
  stripeCustomerId  String?
  subscriptionId    String?
  
  // Timestamps
  createdAt         DateTime @default(now())
  updatedAt         DateTime @updatedAt
  
  // Relations
  apiKeys           ApiKey[]
  sessions          Session[]
}

model ApiKey {
  id          String   @id @default(cuid())
  userId      String
  key         String   @unique
  name        String
  permissions Json
  isActive    Boolean  @default(true)
  createdAt   DateTime @default(now())
  
  user User @relation(fields: [userId], references: [id])
}

enum SubscriptionTier {
  FREE
  PRO
  ENTERPRISE
}
```

### Run Migrations
```bash
cd /home/user/helix-unified
npx prisma migrate dev --name add_billing
```

---

## STEP 2: Create Feature Gates (1 day)

### New File: `backend/config/feature_gates.py`
```python
# Feature limits by subscription tier
FEATURE_GATES = {
    "FREE": {
        "agents": ["kael", "lumina", "aether"],  # 3 agents
        "api_calls_per_month": 1000,
        "data_retention_days": 7,
        "custom_alerts": 0,
        "integrations": ["discord", "notion"],
        "white_label": False,
        "rate_limit_per_minute": 10,
    },
    "PRO": {
        "agents": [
            "kael", "lumina", "aether", "grok", "kavach",
            "claude", "shadow", "agni", "manus", "sangha"
        ],  # 10 agents
        "api_calls_per_month": 50000,
        "data_retention_days": 90,
        "custom_alerts": 3,
        "integrations": ["discord", "notion", "zapier", "slack", "trello"],
        "white_label": True,
        "rate_limit_per_minute": 100,
    },
    "ENTERPRISE": {
        "agents": "*",  # All 14
        "api_calls_per_month": 1000000,
        "data_retention_days": None,  # Unlimited
        "custom_alerts": None,  # Unlimited
        "integrations": "*",  # All 200+
        "white_label": True,
        "rate_limit_per_minute": 10000,
    },
}
```

---

## STEP 3: Add Rate Limiting Middleware (1 day)

### New File: `backend/middleware/rate_limit.py`
```python
from fastapi import Request, HTTPException
from backend.config.feature_gates import FEATURE_GATES
import time

class RateLimitManager:
    def __init__(self):
        self.requests = {}  # user_id -> [(timestamp, endpoint), ...]
    
    async def check_rate_limit(self, user_id: str, tier: str) -> bool:
        """Check if user exceeded rate limit"""
        limit = FEATURE_GATES[tier]["rate_limit_per_minute"]
        now = time.time()
        one_min_ago = now - 60
        
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # Remove old requests
        self.requests[user_id] = [
            (ts, ep) for ts, ep in self.requests[user_id]
            if ts > one_min_ago
        ]
        
        # Check limit
        if len(self.requests[user_id]) >= limit:
            return False
        
        return True
    
    async def record_request(self, user_id: str, endpoint: str):
        """Record API request for rate limiting"""
        if user_id not in self.requests:
            self.requests[user_id] = []
        self.requests[user_id].append((time.time(), endpoint))

rate_limiter = RateLimitManager()

async def rate_limit_middleware(request: Request, call_next):
    """Apply rate limiting based on subscription tier"""
    try:
        # Get user from token
        user = await get_user_from_token(request)
        
        # Check rate limit
        if not await rate_limiter.check_rate_limit(user.id, user.subscriptionTier):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        # Record request
        await rate_limiter.record_request(user.id, request.url.path)
        
    except Exception:
        pass  # Continue if auth fails
    
    return await call_next(request)
```

---

## STEP 4: Add Authentication Routes (2 days)

### New File: `backend/routes/auth.py`
```python
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import jwt
import os
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-prod")
ALGORITHM = "HS256"

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=Token)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register new user (FREE tier by default)"""
    
    # Check if user exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Hash password
    password_hash = bcrypt.hashpw(
        user_data.password.encode(), bcrypt.gensalt()
    ).decode()
    
    # Create user
    user = User(
        email=user_data.email,
        passwordHash=password_hash,
        subscriptionTier="FREE"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(days=30)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    return {"access_token": token}

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check password
    if not bcrypt.checkpw(
        credentials.password.encode(),
        user.passwordHash.encode()
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(days=30)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    return {"access_token": token}

@router.get("/validate")
async def validate_token(request: Request):
    """Validate JWT token"""
    try:
        token = request.headers.get("Authorization", "").split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "user_id": payload["user_id"]}
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

## STEP 5: Create API Key Management (1 day)

### New File: `backend/routes/api_keys.py`
```python
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import secrets

router = APIRouter(prefix="/api/keys", tags=["api_keys"])

@router.post("/create")
async def create_api_key(
    name: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new API key for user"""
    
    # Generate random key
    key = secrets.token_urlsafe(32)
    
    # Store in database
    api_key = ApiKey(
        userId=user_id,
        name=name,
        key=key,
        permissions={}
    )
    db.add(api_key)
    db.commit()
    
    # Return key (never show again)
    return {
        "id": api_key.id,
        "name": name,
        "key": key,  # Only show once!
        "created_at": api_key.createdAt
    }

@router.get("/list")
async def list_api_keys(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's API keys (without secret)"""
    
    keys = db.query(ApiKey).filter(ApiKey.userId == user_id).all()
    
    return [
        {
            "id": k.id,
            "name": k.name,
            "created_at": k.createdAt,
            "is_active": k.isActive,
            "last_used": k.lastUsedAt
        }
        for k in keys
    ]

@router.delete("/{key_id}")
async def delete_api_key(
    key_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete API key"""
    
    key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.userId == user_id
    ).first()
    
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
    
    db.delete(key)
    db.commit()
    
    return {"deleted": True}
```

---

## STEP 6: Add Stripe Integration (2 days)

### Install Stripe
```bash
pip install stripe
```

### New File: `backend/routes/billing.py`
```python
from fastapi import APIRouter, HTTPException, Depends
import stripe
import os

router = APIRouter(prefix="/billing", tags=["billing"])
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PRICE_IDS = {
    "PRO": "price_xxx_pro",      # Set from Stripe dashboard
    "ENTERPRISE": "price_xxx_enterprise"
}

@router.post("/create-subscription")
async def create_subscription(
    tier: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create Stripe subscription"""
    
    if tier not in ["PRO", "ENTERPRISE"]:
        raise HTTPException(status_code=400, detail="Invalid tier")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    # Create Stripe customer if not exists
    if not user.stripeCustomerId:
        customer = stripe.Customer.create(email=user.email)
        user.stripeCustomerId = customer.id
        db.commit()
    
    # Create subscription
    subscription = stripe.Subscription.create(
        customer=user.stripeCustomerId,
        items=[{"price": PRICE_IDS[tier]}],
        payment_behavior="default_incomplete",
        expand=["latest_invoice.payment_intent"]
    )
    
    # Save subscription ID
    user.subscriptionTier = tier
    user.subscriptionId = subscription.id
    db.commit()
    
    return {
        "subscription_id": subscription.id,
        "client_secret": subscription.latest_invoice.payment_intent.client_secret
    }

@router.post("/webhook")
async def handle_stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events"""
    
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle subscription updated
    if event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        user = db.query(User).filter(
            User.stripeCustomerId == subscription.customer
        ).first()
        if user:
            # Update tier based on price
            for item in subscription.items.data:
                if item.price.id == PRICE_IDS["ENTERPRISE"]:
                    user.subscriptionTier = "ENTERPRISE"
                elif item.price.id == PRICE_IDS["PRO"]:
                    user.subscriptionTier = "PRO"
            db.commit()
    
    return {"received": True}
```

---

## STEP 7: Add Feature Gating to Endpoints (1 day)

### Example: Gate Agent Access
```python
# In backend/main.py

@app.get("/agents")
async def get_agents(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get agents (gated by tier)"""
    
    user = db.query(User).filter(User.id == user_id).first()
    allowed_agents = FEATURE_GATES[user.subscriptionTier]["agents"]
    
    # Return only allowed agents
    agents = db.query(Agent).filter(
        Agent.name.in_(allowed_agents) if allowed_agents != "*" else True
    ).all()
    
    return {"agents": agents}

@app.get("/status")
async def get_status(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get system status (with tier-based detail)"""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    # Get current status
    status_data = get_ucf_state()
    
    # Apply tier-based filtering
    if user.subscriptionTier == "FREE":
        # Only show 3 agents
        status_data["agents"] = status_data["agents"][:3]
    elif user.subscriptionTier == "PRO":
        # Show 10 agents
        status_data["agents"] = status_data["agents"][:10]
    # ENTERPRISE gets all
    
    return status_data
```

---

## STEP 8: Create Dashboard Frontend (2-3 days)

### New File: `frontend/pages/pricing.py`
```python
import streamlit as st

st.set_page_config(page_title="Pricing", page_icon="💰")

st.title("Helix Consciousness Platform - Pricing")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("FREE")
    st.markdown("**$0/month**")
    st.write("""
    - 3 agents
    - 1,000 API calls
    - 7-day history
    - Community support
    """)
    st.button("Get Started", key="free")

with col2:
    st.subheader("PRO")
    st.markdown("**$299/month**")
    st.write("""
    - 10 agents
    - 50,000 API calls
    - 90-day history
    - White-label option
    - Email support
    """)
    st.button("Start Pro", key="pro")

with col3:
    st.subheader("ENTERPRISE")
    st.markdown("**$2,999/month**")
    st.write("""
    - All 14 agents
    - 1M+ API calls
    - Unlimited history
    - Full white-label
    - 24/7 Phone support
    """)
    st.button("Contact Sales", key="enterprise")
```

---

## STEP 9: Add Usage Tracking (1 day)

### New Model: Add to Prisma
```prisma
model UsageMetric {
  id        String   @id @default(cuid())
  userId    String
  
  endpoint  String
  month     String   // "2025-11"
  count     Int
  
  createdAt DateTime @default(now())
  
  user User @relation(fields: [userId], references: [id])
  
  @@unique([userId, endpoint, month])
  @@map("usage_metrics")
}
```

### Tracking Middleware
```python
async def track_usage(user_id: str, endpoint: str, db: Session):
    """Track API usage for billing"""
    
    current_month = datetime.now().strftime("%Y-%m")
    
    metric = db.query(UsageMetric).filter(
        UsageMetric.userId == user_id,
        UsageMetric.endpoint == endpoint,
        UsageMetric.month == current_month
    ).first()
    
    if metric:
        metric.count += 1
    else:
        metric = UsageMetric(
            userId=user_id,
            endpoint=endpoint,
            month=current_month,
            count=1
        )
        db.add(metric)
    
    db.commit()
```

---

## STEP 10: Test Everything (1-2 days)

### Test Script
```python
# tests/test_monetization.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_free_user_registration():
    """Test user can register with FREE tier"""
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_free_user_rate_limit():
    """Test FREE users are rate limited"""
    token = get_test_token("FREE")
    
    # Make 11 requests (limit is 10/min)
    for i in range(11):
        response = client.get(
            "/agents",
            headers={"Authorization": f"Bearer {token}"}
        )
    
    assert response.status_code == 429  # Too many requests

def test_pro_user_agent_access():
    """Test PRO users get 10 agents"""
    token = get_test_token("PRO")
    
    response = client.get(
        "/agents",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    agents = response.json()["agents"]
    assert len(agents) == 10

def test_enterprise_user_all_agents():
    """Test ENTERPRISE users get all 14 agents"""
    token = get_test_token("ENTERPRISE")
    
    response = client.get(
        "/agents",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    agents = response.json()["agents"]
    assert len(agents) == 14
```

---

## DEPLOYMENT CHECKLIST

- [ ] Database migrations applied
- [ ] Stripe account setup + keys in Railway
- [ ] JWT secret configured
- [ ] Rate limiting tested
- [ ] API keys working
- [ ] Subscription flows tested
- [ ] Free → Pro upgrade path works
- [ ] Documentation updated
- [ ] Landing page deployed
- [ ] Beta launch to 20 users
- [ ] Monitor for issues
- [ ] Collect early feedback
- [ ] Iterate on pricing/features

---

## ENVIRONMENT VARIABLES NEEDED

```bash
# Add to Railway dashboard

# Authentication
SECRET_KEY=your-random-secret-here
JWT_ALGORITHM=HS256

# Stripe
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Email (for password resets, etc)
SENDGRID_API_KEY=SG.xxx
SENDER_EMAIL=noreply@helix.app
```

---

## NEXT: WHICH PRODUCT SHOULD YOU BUILD FIRST?

**Recommendation:** Start with **Product 1 (UCF Dashboard)**

**Why:**
1. Code already exists (Streamlit app)
2. Lowest development effort (2-3 weeks)
3. Fastest path to revenue
4. Validates market demand
5. Natural upsell path to other products

**Expected Outcome:**
- Launch in 3 weeks
- 20-50 beta users
- Validate pricing
- $0-5K MRR (initial)
- Learnings for Product 2

---

**Timeline:** 2-3 weeks to MVP launch  
**Effort:** 1-2 developers  
**Risk:** Low (existing code base)  
**Revenue Potential:** $200K-2.2M Year 1

