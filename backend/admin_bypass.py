"""
🔑 Admin Bypass System
=====================

Allows site administrators to use all platform features without Stripe payments.
Configure admin users via environment variables.

Usage:
- Set ADMIN_EMAILS="your@email.com,other@admin.com" in .env
- Admin users automatically get 'enterprise' tier privileges
- Bypass subscription checks, usage limits, and payment requirements

Author: Claude (Helix Collective)
Date: 2025-12-07
"""

import os
from datetime import datetime
from typing import List, Optional, Set
from functools import wraps

from fastapi import Request, HTTPException
from pydantic import BaseModel

# ============================================================================
# CONFIGURATION
# ============================================================================

# Admin emails from environment (comma-separated)
ADMIN_EMAILS_STR = os.getenv("ADMIN_EMAILS", "")
ADMIN_EMAILS: Set[str] = {
    email.strip().lower()
    for email in ADMIN_EMAILS_STR.split(",")
    if email.strip()
}

# Admin user IDs (for direct ID-based checks)
ADMIN_USER_IDS_STR = os.getenv("ADMIN_USER_IDS", "")
ADMIN_USER_IDS: Set[str] = {
    uid.strip()
    for uid in ADMIN_USER_IDS_STR.split(",")
    if uid.strip()
}

# Master admin key for emergency access
MASTER_ADMIN_KEY = os.getenv("MASTER_ADMIN_KEY", "")

print(f"[ADMIN_BYPASS] Loaded {len(ADMIN_EMAILS)} admin emails")
print(f"[ADMIN_BYPASS] Loaded {len(ADMIN_USER_IDS)} admin user IDs")
print(f"[ADMIN_BYPASS] Master key configured: {bool(MASTER_ADMIN_KEY)}")

# ============================================================================
# MODELS
# ============================================================================

class AdminUser(BaseModel):
    """Enhanced user model with admin privileges"""
    id: str
    email: str
    name: str
    is_admin: bool = False
    subscription_tier: str = "free"

    @property
    def effective_tier(self) -> str:
        """Get effective subscription tier (admins always get enterprise)"""
        if self.is_admin:
            return "enterprise"
        return self.subscription_tier

    @property
    def has_unlimited_access(self) -> bool:
        """Check if user has unlimited access"""
        return self.is_admin

# ============================================================================
# ADMIN DETECTION
# ============================================================================

def is_admin_email(email: str) -> bool:
    """Check if email belongs to an admin"""
    if not email:
        return False
    return email.lower() in ADMIN_EMAILS

def is_admin_user_id(user_id: str) -> bool:
    """Check if user ID belongs to an admin"""
    if not user_id:
        return False
    return user_id in ADMIN_USER_IDS

def is_admin_user(user: dict) -> bool:
    """Check if user object represents an admin"""
    # Check by email
    if "email" in user and is_admin_email(user["email"]):
        return True

    # Check by user ID
    if "id" in user and is_admin_user_id(user["id"]):
        return True

    # Check explicit admin flag
    if user.get("is_admin", False):
        return True

    return False

def check_master_key(key: Optional[str]) -> bool:
    """Verify master admin key"""
    if not MASTER_ADMIN_KEY or not key:
        return False
    return key == MASTER_ADMIN_KEY

# ============================================================================
# TIER ENFORCEMENT BYPASS
# ============================================================================

def get_effective_tier(user: dict) -> str:
    """
    Get user's effective subscription tier.
    Admins always return 'enterprise'.
    """
    if is_admin_user(user):
        return "enterprise"
    return user.get("subscription_tier", "free")

def can_access_feature(user: dict, required_tier: str) -> bool:
    """
    Check if user can access a feature requiring a specific tier.

    Tier hierarchy: free < hobby < starter < pro < enterprise
    Admins can access everything.
    """
    if is_admin_user(user):
        return True  # Admins bypass all tier checks

    tier_hierarchy = ["free", "hobby", "starter", "pro", "enterprise"]
    user_tier = user.get("subscription_tier", "free")

    try:
        user_tier_level = tier_hierarchy.index(user_tier)
        required_tier_level = tier_hierarchy.index(required_tier)
        return user_tier_level >= required_tier_level
    except ValueError:
        return False

def bypass_rate_limit(user: dict) -> bool:
    """Check if user should bypass rate limits"""
    return is_admin_user(user)

def bypass_payment(user: dict) -> bool:
    """Check if user should bypass payment requirements"""
    return is_admin_user(user)

# ============================================================================
# FASTAPI DEPENDENCIES
# ============================================================================

async def get_admin_user(request: Request) -> Optional[AdminUser]:
    """
    Extract user from request and enhance with admin privileges.
    Use this instead of get_current_user for admin-aware endpoints.
    """
    # Check for master admin key in header
    master_key = request.headers.get("X-Admin-Key")
    if check_master_key(master_key):
        return AdminUser(
            id="master_admin",
            email="admin@helixspiral.work",
            name="Master Admin",
            is_admin=True,
            subscription_tier="enterprise"
        )

    # Get user from JWT token (assuming it's in request.state)
    user_data = getattr(request.state, "user", None)
    if not user_data:
        return None

    # Convert to AdminUser with admin detection
    is_admin = is_admin_user(user_data)

    return AdminUser(
        id=user_data.get("id", ""),
        email=user_data.get("email", ""),
        name=user_data.get("name", "Unknown"),
        is_admin=is_admin,
        subscription_tier=user_data.get("subscription_tier", "free")
    )

def require_admin(func):
    """
    Decorator to require admin privileges for an endpoint.

    Usage:
        @router.get("/admin/stats")
        @require_admin
        async def get_stats(user: AdminUser = Depends(get_admin_user)):
            return {"stats": "admin only"}
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract user from kwargs
        user = kwargs.get("user")
        if not user or not user.is_admin:
            raise HTTPException(
                status_code=403,
                detail="Admin privileges required"
            )
        return await func(*args, **kwargs)
    return wrapper

# ============================================================================
# USAGE TRACKING BYPASS
# ============================================================================

class UsageTracker:
    """Mock usage tracker that bypasses limits for admins"""

    @staticmethod
    async def check_rate_limit(user: dict) -> bool:
        """Check if user has exceeded rate limit"""
        if bypass_rate_limit(user):
            return True  # Admins never hit rate limits

        # Implement actual rate limit check here
        # This is a placeholder
        return True

    @staticmethod
    async def track_usage(user: dict, endpoint: str, cost: float = 0):
        """Track API usage (skip for admins to avoid polluting metrics)"""
        if is_admin_user(user):
            # Don't track admin usage, or track separately
            return

        # Implement actual usage tracking here
        pass

# ============================================================================
# MIDDLEWARE INTEGRATION
# ============================================================================

async def admin_bypass_middleware(request: Request, call_next):
    """
    Middleware to inject admin privileges into request context.

    Add to FastAPI app:
        app.middleware("http")(admin_bypass_middleware)
    """
    # Check for master admin key
    master_key = request.headers.get("X-Admin-Key")
    if check_master_key(master_key):
        request.state.is_admin = True
        request.state.effective_tier = "enterprise"

    # Process request
    response = await call_next(request)

    # Add admin indicator header if user is admin
    if hasattr(request.state, "is_admin") and request.state.is_admin:
        response.headers["X-User-Is-Admin"] = "true"

    return response

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def upgrade_user_to_admin(user: dict) -> dict:
    """
    Upgrade a regular user object to have admin privileges.
    Returns a new dict with admin flags set.
    """
    enhanced_user = user.copy()

    if is_admin_user(user):
        enhanced_user["is_admin"] = True
        enhanced_user["subscription_tier"] = "enterprise"
        enhanced_user["effective_tier"] = "enterprise"

    return enhanced_user

def get_admin_dashboard_url() -> str:
    """Get URL for admin dashboard"""
    base_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    return f"{base_url}/admin/dashboard"

def log_admin_action(user: dict, action: str, details: dict = None):
    """
    Log admin actions for audit trail.
    In production, send to logging service or database.
    """
    if not is_admin_user(user):
        return

    import json
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "admin_email": user.get("email"),
        "admin_id": user.get("id"),
        "action": action,
        "details": details or {}
    }

    print(f"[ADMIN_ACTION] {json.dumps(log_entry)}")

    # TODO: Send to logging service (CloudWatch, Datadog, etc.)

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "is_admin_email",
    "is_admin_user_id",
    "is_admin_user",
    "check_master_key",
    "get_effective_tier",
    "can_access_feature",
    "bypass_rate_limit",
    "bypass_payment",
    "get_admin_user",
    "require_admin",
    "UsageTracker",
    "admin_bypass_middleware",
    "upgrade_user_to_admin",
    "get_admin_dashboard_url",
    "log_admin_action",
    "AdminUser",
    "ADMIN_EMAILS",
    "ADMIN_USER_IDS",
]
