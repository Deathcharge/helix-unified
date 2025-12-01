"""
🌀 Helix Collective v17.1 - SaaS Authentication & User Management
backend/saas/auth_service.py

Multi-tenant authentication with email + OAuth:
- Email/password authentication
- OAuth providers (Google, GitHub)
- Session management
- User profile management
- Subscription tracking

Author: Claude (Automation)
Version: 17.1.0
"""

import hashlib
import json
import logging
import os
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import jwt

logger = logging.getLogger(__name__)

# Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
JWT_EXPIRY_HOURS = 24
OAUTH_PROVIDERS = {
    "google": {
        "client_id": os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    },
    "github": {
        "client_id": os.getenv("GITHUB_OAUTH_CLIENT_ID"),
        "client_secret": os.getenv("GITHUB_OAUTH_CLIENT_SECRET"),
    },
}

# ============================================================================
# USER MANAGEMENT
# ============================================================================


class UserManager:
    """Manages user accounts and subscriptions."""

    def __init__(self):
        self.users_file = Path("Helix/state/saas_users.json")
        self.users_file.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file()

    def _ensure_file(self) -> None:
        """Ensure users file exists."""
        if not self.users_file.exists():
            with open(self.users_file, "w") as f:
                json.dump({}, f)

    def _load_users(self) -> Dict[str, Dict[str, Any]]:
        """Load all users."""
        with open(self.users_file, "r") as f:
            return json.load(f)

    def _save_users(self, users: Dict[str, Dict[str, Any]]) -> None:
        """Save all users."""
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=2)

    async def create_user(
        self,
        email: str,
        password: Optional[str] = None,
        name: str = "",
        oauth_provider: Optional[str] = None,
        oauth_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create new user account."""
        users = self._load_users()

        # Check if already exists
        if email in users:
            return {"status": "error", "error": "User already exists"}

        user_id = secrets.token_urlsafe(16)

        user = {
            "user_id": user_id,
            "email": email,
            "name": name or email.split("@")[0],
            "created_at": datetime.utcnow().isoformat() + "Z",
            "subscription_tier": "free",
            "subscription_id": None,
            "stripe_customer_id": None,
            "api_key": secrets.token_urlsafe(32),
            "verified": False,
        }

        # Store password hash if provided
        if password:
            user["password_hash"] = self._hash_password(password)

        # Store OAuth info if provided
        if oauth_provider:
            user[f"oauth_{oauth_provider}_id"] = oauth_id

        users[email] = user
        self._save_users(users)

        logger.info(f"✅ Created user: {email}")
        return {"status": "success", "user_id": user_id, "email": email}

    async def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        users = self._load_users()
        return users.get(email)

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        users = self._load_users()
        for user in users.values():
            if user.get("user_id") == user_id:
                return user
        return None

    async def verify_password(self, email: str, password: str) -> bool:
        """Verify user password."""
        user = await self.get_user(email)
        if not user:
            return False

        password_hash = user.get("password_hash")
        if not password_hash:
            return False

        return self._verify_password(password, password_hash)

    async def update_subscription(
        self, email: str, tier: str, subscription_id: str, stripe_customer_id: str
    ) -> Dict[str, Any]:
        """Update user subscription."""
        users = self._load_users()
        user = users.get(email)

        if not user:
            return {"status": "error", "error": "User not found"}

        user["subscription_tier"] = tier
        user["subscription_id"] = subscription_id
        user["stripe_customer_id"] = stripe_customer_id

        self._save_users(users)
        logger.info(f"✅ Updated subscription: {email} → {tier}")

        return {"status": "success", "tier": tier}

    def _hash_password(self, password: str) -> str:
        """Hash password with salt."""
        salt = secrets.token_hex(32)
        pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
        return f"{salt}${pwd_hash.hex()}"

    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against hash."""
        try:
            salt, pwd_hash = stored_hash.split("$")
            new_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
            return new_hash.hex() == pwd_hash
        except Exception:
            return False


# ============================================================================
# JWT TOKEN MANAGEMENT
# ============================================================================


class TokenManager:
    """Manages JWT tokens."""

    @staticmethod
    def create_token(user_id: str, email: str, tier: str) -> str:
        """Create JWT token."""
        payload = {
            "user_id": user_id,
            "email": email,
            "tier": tier,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS),
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        logger.info(f"✅ Token created: {email}")
        return token

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token."""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None

    @staticmethod
    def refresh_token(token: str) -> Optional[str]:
        """Refresh token if valid."""
        payload = TokenManager.verify_token(token)
        if not payload:
            return None

        # Create new token
        return TokenManager.create_token(
            payload["user_id"], payload["email"], payload["tier"]
        )


# ============================================================================
# OAUTH HANDLERS
# ============================================================================


class OAuthHandler:
    """Handles OAuth authentication."""

    @staticmethod
    async def get_google_user_info(access_token: str) -> Optional[Dict[str, Any]]:
        """Get Google user info from access token."""
        import aiohttp

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"},
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return None
        except Exception as e:
            logger.error(f"Google OAuth error: {e}")
            return None

    @staticmethod
    async def get_github_user_info(access_token: str) -> Optional[Dict[str, Any]]:
        """Get GitHub user info from access token."""
        import aiohttp

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.github.com/user",
                    headers={"Authorization": f"token {access_token}"},
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return None
        except Exception as e:
            logger.error(f"GitHub OAuth error: {e}")
            return None


# ============================================================================
# SESSION MANAGER
# ============================================================================


class SessionManager:
    """Manages user sessions."""

    def __init__(self):
        self.sessions_file = Path("Helix/state/saas_sessions.json")
        self.sessions_file.parent.mkdir(parents=True, exist_ok=True)

    def create_session(self, user_id: str, token: str, ip_address: str) -> str:
        """Create user session."""
        sessions = self._load_sessions()
        session_id = secrets.token_urlsafe(16)

        sessions[session_id] = {
            "user_id": user_id,
            "token": token,
            "ip_address": ip_address,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z",
            "last_activity": datetime.utcnow().isoformat() + "Z",
        }

        self._save_sessions(sessions)
        logger.info(f"✅ Session created: {session_id}")
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session."""
        sessions = self._load_sessions()
        return sessions.get(session_id)

    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate session (logout)."""
        sessions = self._load_sessions()
        if session_id in sessions:
            del sessions[session_id]
            self._save_sessions(sessions)
            logger.info(f"✅ Session invalidated: {session_id}")
            return True
        return False

    def _load_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Load sessions."""
        if not self.sessions_file.exists():
            return {}
        with open(self.sessions_file, "r") as f:
            return json.load(f)

    def _save_sessions(self, sessions: Dict[str, Dict[str, Any]]) -> None:
        """Save sessions."""
        with open(self.sessions_file, "w") as f:
            json.dump(sessions, f)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = ["UserManager", "TokenManager", "OAuthHandler", "SessionManager"]

import asyncio
