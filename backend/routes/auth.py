"""
🔐 Authentication Router
Google OAuth + JWT tokens + Email/Password

VILLAIN LOGIN SYSTEM: ENABLED 😈
"""

import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr

router = APIRouter()

# Config
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
JWT_SECRET = os.getenv("JWT_SECRET", "helix-secret-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24 * 7  # 7 days

# ============================================================================
# MODELS
# ============================================================================

class User(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None
    subscription_tier: str = "free"
    created_at: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

class GoogleTokenRequest(BaseModel):
    id_token: str

# ============================================================================
# JWT HELPERS
# ============================================================================

def create_access_token(user: User) -> str:
    """Create JWT token"""
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    payload = {
        "sub": user.id,
        "email": user.email,
        "name": user.name,
        "tier": user.subscription_tier,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

async def get_current_user(request: Request) -> User:
    """Get current user from token (dependency)"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = auth_header.replace("Bearer ", "")
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return User(
        id=payload["sub"],
        email=payload["email"],
        name=payload["name"],
        subscription_tier=payload.get("tier", "free")
    )

# ============================================================================
# GOOGLE OAUTH ROUTES
# ============================================================================

@router.get("/google")
async def google_login():
    """Redirect to Google OAuth - VILLAIN AUTHENTICATION PORTAL"""
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth not configured. Set GOOGLE_CLIENT_ID in environment."
        )

    redirect_uri = "http://localhost:8000/auth/google/callback"
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"access_type=offline"
    )
    return RedirectResponse(google_auth_url)

@router.get("/google/callback")
async def google_callback(code: str):
    """Handle Google OAuth callback"""
    # TODO: Exchange code for tokens with Google
    # TODO: Verify ID token
    # TODO: Create/update user in database
    # TODO: Generate JWT

    # For now, create a demo user
    user = User(
        id=f"google_{secrets.token_hex(8)}",
        email="demo@helixspiral.work",
        name="Demo User",
        picture="https://api.dicebear.com/7.x/avataaars/svg?seed=demo",
        subscription_tier="free",
        created_at=datetime.utcnow().isoformat()
    )

    token = create_access_token(user)

    # Redirect to frontend with token
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    return RedirectResponse(f"{frontend_url}/dashboard?token={token}")

@router.post("/verify-google-token")
async def verify_google_token(req: GoogleTokenRequest) -> Token:
    """Verify Google ID token and create session"""
    # TODO: Implement actual Google token verification
    # For now, create demo user

    user = User(
        id=f"google_{secrets.token_hex(8)}",
        email="demo@helixspiral.work",
        name="Demo User",
        picture="https://api.dicebear.com/7.x/avataaars/svg?seed=demo",
        subscription_tier="free",
        created_at=datetime.utcnow().isoformat()
    )

    access_token = create_access_token(user)

    return Token(access_token=access_token, user=user)

# ============================================================================
# EMAIL/PASSWORD ROUTES (Simple implementation)
# ============================================================================

# In-memory user store (replace with database in production)
_users_store = {}

@router.post("/signup")
async def signup(req: SignupRequest) -> Token:
    """Sign up with email/password - JOIN THE DARK SIDE"""
    # Check if user exists
    if req.email in _users_store:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create user
    user = User(
        id=f"user_{secrets.token_hex(8)}",
        email=req.email,
        name=req.name,
        subscription_tier="free",
        created_at=datetime.utcnow().isoformat()
    )

    # Store user (in production, hash password and store in database)
    _users_store[req.email] = {
        "user": user,
        "password": req.password,  # TODO: Hash this!
    }

    # Create token
    access_token = create_access_token(user)

    return Token(access_token=access_token, user=user)

@router.post("/login")
async def login(req: LoginRequest) -> Token:
    """Login with email/password - ENTER THE LAIR"""
    # Check if user exists
    if req.email not in _users_store:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    stored = _users_store[req.email]

    # Verify password (in production, use proper password hashing)
    if stored["password"] != req.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create token
    user = stored["user"]
    access_token = create_access_token(user)

    return Token(access_token=access_token, user=user)

# ============================================================================
# USER INFO ROUTES
# ============================================================================

@router.get("/me")
async def get_current_user_info(user: User = Depends(get_current_user)) -> User:
    """Get current user info - REVEAL YOUR IDENTITY"""
    return user

@router.post("/logout")
async def logout():
    """Logout (client should delete token) - ESCAPE THE LAIR"""
    return {"message": "Logged out successfully. Delete your token, villain!"}

# ============================================================================
# DEMO / TESTING ROUTES
# ============================================================================

@router.post("/demo-login")
async def demo_login() -> Token:
    """Create demo account for testing - INSTANT VILLAIN ACCESS"""
    user = User(
        id=f"demo_{secrets.token_hex(8)}",
        email="demo@helixspiral.work",
        name="Demo Villain",
        picture="https://api.dicebear.com/7.x/avataaars/svg?seed=villain",
        subscription_tier="pro",  # Give demo users pro tier!
        created_at=datetime.utcnow().isoformat()
    )

    access_token = create_access_token(user)

    return Token(access_token=access_token, user=user)

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = ["router", "get_current_user", "User", "Token"]
