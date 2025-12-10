"""
🔐 Authentication Router
Google OAuth + JWT tokens + Email/Password

VILLAIN LOGIN SYSTEM: ENABLED 😈
"""

import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy.orm import Session

from backend.core.errors import (AlreadyExistsError, InvalidCredentialsError,
                                 InvalidTokenError)
from backend.core.rate_limit import get_rate_limit, limiter
# Import security utilities
from backend.core.security import (create_access_token, decode_access_token,
                                   generate_secure_token, hash_password,
                                   verify_password)
# Import database
from backend.database import User as DBUser
from backend.database import get_db

router = APIRouter()

# Config
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

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

    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

    @validator('name')
    def name_length(cls, v):
        """Validate name length"""
        if len(v) < 2:
            raise ValueError('Name must be at least 2 characters long')
        if len(v) > 100:
            raise ValueError('Name must be less than 100 characters')
        return v.strip()

class GoogleTokenRequest(BaseModel):
    id_token: str

# ============================================================================
# JWT HELPERS
# ============================================================================

def create_user_token(user: User) -> str:
    """Create JWT token for user"""
    payload = {
        "sub": user.id,
        "email": user.email,
        "name": user.name,
        "tier": user.subscription_tier,
    }
    return create_access_token(payload)

async def get_current_user(request: Request) -> User:
    """Get current user from token (dependency)"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise InvalidTokenError()

    token = auth_header.replace("Bearer ", "")
    payload = decode_access_token(token)

    if not payload:
        raise InvalidTokenError()

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

    token = create_user_token(user)

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

    access_token = create_user_token(user)

    return Token(access_token=access_token, user=user)

# ============================================================================
# EMAIL/PASSWORD ROUTES
# ============================================================================

@router.post("/signup")
@limiter.limit(get_rate_limit("auth_signup"))
async def signup(request: Request, req: SignupRequest, db: Session = Depends(get_db)) -> Token:
    """Sign up with email/password - JOIN THE DARK SIDE"""
    # Check if user exists
    existing_user = db.query(DBUser).filter(DBUser.email == req.email).first()
    if existing_user:
        raise AlreadyExistsError("User", req.email)

    # Create user in database
    user_id = f"user_{generate_secure_token(8)}"
    db_user = DBUser(
        id=user_id,
        email=req.email,
        name=req.name,
        password_hash=hash_password(req.password),
        auth_provider="email",
        subscription_tier="free",
        created_at=datetime.utcnow(),
        last_login=datetime.utcnow()
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create response user model
    user = User(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        subscription_tier=db_user.subscription_tier,
        created_at=db_user.created_at.isoformat()
    )

    # Create token
    access_token = create_user_token(user)

    return Token(access_token=access_token, user=user)

@router.post("/login")
@limiter.limit(get_rate_limit("auth_login"))
async def login(request: Request, req: LoginRequest, db: Session = Depends(get_db)) -> Token:
    """Login with email/password - ENTER THE LAIR"""
    # Check if user exists
    db_user = db.query(DBUser).filter(DBUser.email == req.email).first()
    if not db_user:
        raise InvalidCredentialsError()

    # Verify password using bcrypt
    if not verify_password(req.password, db_user.password_hash):
        raise InvalidCredentialsError()

    # Update last login
    db_user.last_login = datetime.utcnow()
    db.commit()

    # Create response user model
    user = User(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        picture=db_user.picture,
        subscription_tier=db_user.subscription_tier,
        created_at=db_user.created_at.isoformat() if db_user.created_at else None
    )

    # Create token
    access_token = create_user_token(user)

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
@limiter.limit("10/hour")  # Limit demo account creation
async def demo_login(request: Request) -> Token:
    """Create demo account for testing - INSTANT VILLAIN ACCESS"""
    user = User(
        id=f"demo_{generate_secure_token(8)}",
        email="demo@helixspiral.work",
        name="Demo Villain",
        picture="https://api.dicebear.com/7.x/avataaars/svg?seed=villain",
        subscription_tier="pro",  # Give demo users pro tier!
        created_at=datetime.utcnow().isoformat()
    )

    access_token = create_user_token(user)

    return Token(access_token=access_token, user=user)

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = ["router", "get_current_user", "User", "Token"]
