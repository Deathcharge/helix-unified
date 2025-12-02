# 🌀 Helix Collective - Unified Dashboard API
# FastAPI backend for authentication, subscriptions, and monitoring
# Author: Claude Code + Andrew John Ward

import hashlib
import os
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import jwt
import stripe
from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Helix Collective Unified Dashboard API",
    version="1.0.0",
    description="Authentication, subscriptions, and monitoring for the Helix ecosystem"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "helix_secret_key_change_in_production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24 * 7  # 7 days

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_your_key_here")
STRIPE_PRICE_IDS = {
    "pro_monthly": os.getenv("STRIPE_PRO_MONTHLY_PRICE_ID", "price_pro_monthly"),
    "pro_yearly": os.getenv("STRIPE_PRO_YEARLY_PRICE_ID", "price_pro_yearly"),
}

# In-memory database (TODO: Replace with PostgreSQL/MongoDB in production)
users_db = {}
subscriptions_db = {}
api_keys_db = {}


# ============================================================================
# DATA MODELS
# ============================================================================

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember: bool = False


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    subscription: str
    api_key: str
    created_at: str


class SubscriptionCheckout(BaseModel):
    plan: str  # 'pro'
    billing: str  # 'monthly' or 'yearly'


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed


def generate_api_key(prefix: str = "hx") -> str:
    """Generate a secure API key"""
    return f"{prefix}_{secrets.token_urlsafe(32)}"


def create_jwt_token(user_id: str, remember: bool = False) -> str:
    """Create JWT token for authentication"""
    expiration = datetime.utcnow() + timedelta(
        hours=JWT_EXPIRATION_HOURS if remember else 24
    )

    payload = {
        "user_id": user_id,
        "exp": expiration,
        "iat": datetime.utcnow()
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_jwt_token(token: str) -> Optional[str]:
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


async def get_current_user(authorization: str = Header(None)) -> Dict[str, Any]:
    """Dependency to get current authenticated user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    user_id = verify_jwt_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/auth/signup")
async def signup(user_data: UserSignup):
    """Register a new user"""
    # Check if email already exists
    for user in users_db.values():
        if user["email"] == user_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    user_id = secrets.token_urlsafe(16)
    api_key = generate_api_key()

    new_user = {
        "id": user_id,
        "name": user_data.name,
        "email": user_data.email,
        "password_hash": hash_password(user_data.password),
        "subscription": "free",
        "api_key": api_key,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }

    users_db[user_id] = new_user
    api_keys_db[api_key] = user_id

    # Create JWT token
    token = create_jwt_token(user_id)

    return {
        "token": token,
        "user": {
            "id": user_id,
            "name": new_user["name"],
            "email": new_user["email"],
            "subscription": new_user["subscription"],
            "api_key": api_key,
        }
    }


@app.post("/auth/login")
async def login(credentials: UserLogin):
    """Login existing user"""
    # Find user by email
    user = None
    for u in users_db.values():
        if u["email"] == credentials.email:
            user = u
            break

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Verify password
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Create JWT token
    token = create_jwt_token(user["id"], credentials.remember)

    return {
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "subscription": user["subscription"],
            "api_key": user["api_key"],
        }
    }


@app.get("/auth/me")
async def get_me(user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "subscription": user["subscription"],
        "api_key": user["api_key"],
        "created_at": user["created_at"],
    }


@app.put("/auth/me")
async def update_profile(
    name: Optional[str] = None,
    email: Optional[EmailStr] = None,
    user: dict = Depends(get_current_user)
):
    """Update user profile"""
    if name:
        user["name"] = name
    if email:
        # Check if new email already exists
        for u in users_db.values():
            if u["email"] == email and u["id"] != user["id"]:
                raise HTTPException(status_code=400, detail="Email already in use")
        user["email"] = email

    user["updated_at"] = datetime.utcnow().isoformat()

    return {"message": "Profile updated successfully"}


# ============================================================================
# SUBSCRIPTION ENDPOINTS
# ============================================================================

@app.post("/subscriptions/create-checkout")
async def create_checkout_session(
    checkout: SubscriptionCheckout,
    user: dict = Depends(get_current_user)
):
    """Create Stripe checkout session for subscription"""
    try:
        # Determine price ID based on plan and billing
        if checkout.plan == "pro":
            price_id = (
                STRIPE_PRICE_IDS["pro_yearly"]
                if checkout.billing == "yearly"
                else STRIPE_PRICE_IDS["pro_monthly"]
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid plan")

        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            customer_email=user["email"],
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=os.getenv("FRONTEND_URL", "http://localhost:8000") + "/account.html?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=os.getenv("FRONTEND_URL", "http://localhost:8000") + "/pricing.html",
            metadata={
                "user_id": user["id"],
            }
        )

        return {"sessionId": session.id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/subscriptions/webhook")
async def stripe_webhook(background_tasks: BackgroundTasks):
    """Handle Stripe webhook events"""
    # TODO: Implement Stripe webhook signature verification
    # TODO: Handle events like checkout.session.completed, invoice.paid, etc.
    return {"status": "success"}


@app.get("/subscriptions/status")
async def get_subscription_status(user: dict = Depends(get_current_user)):
    """Get user's subscription status"""
    subscription = subscriptions_db.get(user["id"], {})

    return {
        "plan": user["subscription"],
        "status": subscription.get("status", "active"),
        "current_period_end": subscription.get("current_period_end"),
        "cancel_at_period_end": subscription.get("cancel_at_period_end", False),
    }


@app.post("/subscriptions/cancel")
async def cancel_subscription(user: dict = Depends(get_current_user)):
    """Cancel user's subscription"""
    subscription = subscriptions_db.get(user["id"])

    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription")

    try:
        # Cancel Stripe subscription
        stripe.Subscription.modify(
            subscription["stripe_subscription_id"],
            cancel_at_period_end=True
        )

        subscription["cancel_at_period_end"] = True

        return {"message": "Subscription will be canceled at period end"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# API KEY ENDPOINTS
# ============================================================================

@app.post("/api-keys/regenerate")
async def regenerate_api_key(user: dict = Depends(get_current_user)):
    """Regenerate user's API key"""
    old_key = user["api_key"]

    # Remove old key from database
    if old_key in api_keys_db:
        del api_keys_db[old_key]

    # Generate new key
    new_key = generate_api_key()
    user["api_key"] = new_key
    api_keys_db[new_key] = user["id"]

    return {"api_key": new_key}


@app.get("/api-keys/validate/{api_key}")
async def validate_api_key(api_key: str):
    """Validate an API key"""
    user_id = api_keys_db.get(api_key)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid API key")

    user = users_db.get(user_id)

    return {
        "valid": True,
        "user_id": user_id,
        "subscription": user["subscription"],
    }


# ============================================================================
# USAGE & MONITORING ENDPOINTS
# ============================================================================

@app.get("/usage/stats")
async def get_usage_stats(user: dict = Depends(get_current_user)):
    """Get user's usage statistics"""
    # TODO: Implement actual usage tracking
    return {
        "api_requests_today": 247,
        "api_requests_30d": 7842,
        "agents_accessed": 3,
        "days_active": 42,
        "avg_response_time": "142ms",
        "success_rate": 0.992,
    }


@app.get("/monitoring/services")
async def get_services_status():
    """Get status of all Railway services"""
    # TODO: Implement actual Railway API integration
    return {
        "services": [
            {
                "name": "Discord Bot",
                "url": "https://helix-discord-bot.up.railway.app",
                "status": "online",
                "uptime": "2d 12h 34m",
                "guilds": 2,
                "version": "v16.8"
            },
            {
                "name": "Claude API",
                "url": "https://helix-claude-api.up.railway.app",
                "status": "online",
                "uptime": "5d 8h 12m",
                "agents": 11,
                "requests_24h": 12483
            },
            {
                "name": "Backend API",
                "url": "https://helix-backend-api.up.railway.app",
                "status": "online",
                "uptime": "3d 14h 56m",
                "requests_24h": 8234
            },
            {
                "name": "Dashboard",
                "url": "https://helix-dashboard.up.railway.app",
                "status": "online",
                "uptime": "7d 2h 18m",
                "visitors_24h": 1247
            }
        ]
    }


# ============================================================================
# HEALTH & STATUS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "users_count": len(users_db),
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Helix Collective Unified Dashboard API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "auth": "/auth/signup, /auth/login, /auth/me",
            "subscriptions": "/subscriptions/*",
            "api_keys": "/api-keys/*",
            "usage": "/usage/stats",
            "monitoring": "/monitoring/services",
            "health": "/health"
        }
    }


# ============================================================================
# STARTUP EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize demo data on startup"""
    # Create demo user
    demo_user_id = "demo_user_001"
    demo_api_key = "hx_demo_key_for_testing_only"

    users_db[demo_user_id] = {
        "id": demo_user_id,
        "name": "Demo User",
        "email": "demo@helixcollective.io",
        "password_hash": hash_password("demo123"),
        "subscription": "pro",
        "api_key": demo_api_key,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }

    api_keys_db[demo_api_key] = demo_user_id

    print("=" * 80)
    print("🌀 Helix Collective Unified Dashboard API")
    print("=" * 80)
    print(f"Demo User: demo@helixcollective.io / demo123")  # noqa
    print(f"Demo API Key: {demo_api_key}")
    print("=" * 80)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # nosec B104
