"""
🛡️ RBAC (Role-Based Access Control) Middleware
Enforces permissions at the API level

VILLAIN SECURITY: WHO GETS TO PRESS THE RED BUTTON? 😈
"""

from datetime import datetime
from functools import wraps
from typing import Callable, List, Optional

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from ..database import Team, TeamMember, User, get_db

# ============================================================================
# ROLE HIERARCHY
# ============================================================================

ROLE_HIERARCHY = {
    "owner": 4,
    "admin": 3,
    "member": 2,
    "viewer": 1
}

ROLE_PERMISSIONS = {
    "owner": [
        "team:read",
        "team:update",
        "team:delete",
        "members:invite",
        "members:remove",
        "members:update_role",
        "billing:manage",
        "billing:view",
        "settings:manage",
        "agents:use",
        "agents:manage",
        "dashboard:view",
        "dashboard:manage",
        "analytics:view",
        "analytics:export",
        "webhooks:manage",
        "api_keys:manage"
    ],
    "admin": [
        "team:read",
        "team:update",
        "members:invite",
        "members:remove",
        "settings:manage",
        "agents:use",
        "agents:manage",
        "dashboard:view",
        "dashboard:manage",
        "analytics:view",
        "analytics:export",
        "api_keys:create"
    ],
    "member": [
        "team:read",
        "agents:use",
        "dashboard:view",
        "analytics:view",
        "api_keys:create"
    ],
    "viewer": [
        "team:read",
        "dashboard:view",
        "analytics:view"
    ]
}

# ============================================================================
# SUBSCRIPTION TIER PERMISSIONS
# ============================================================================

TIER_FEATURES = {
    "free": {
        "agents": ["rishi", "kael", "oracle"],
        "api_calls_limit": 100,
        "team_members_limit": 3,
        "features": ["basic_dashboard", "basic_agents"]
    },
    "pro": {
        "agents": "all",
        "api_calls_limit": 10000,
        "team_members_limit": 10,
        "features": ["pro_dashboard", "all_agents", "analytics", "webhooks"]
    },
    "workflow": {
        "agents": "all",
        "api_calls_limit": 20000,
        "team_members_limit": 25,
        "features": ["pro_dashboard", "all_agents", "analytics", "webhooks", "automation", "zapier"]
    },
    "enterprise": {
        "agents": "all",
        "api_calls_limit": -1,  # Unlimited
        "team_members_limit": -1,  # Unlimited
        "features": ["all"]
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def has_permission(role: str, permission: str) -> bool:
    """Check if a role has a specific permission"""
    return permission in ROLE_PERMISSIONS.get(role, [])

def has_feature(tier: str, feature: str) -> bool:
    """Check if a subscription tier has a specific feature"""
    tier_config = TIER_FEATURES.get(tier, TIER_FEATURES["free"])
    features = tier_config.get("features", [])
    return "all" in features or feature in features

def can_use_agent(tier: str, agent_id: str) -> bool:
    """Check if a subscription tier can use a specific agent"""
    tier_config = TIER_FEATURES.get(tier, TIER_FEATURES["free"])
    agents = tier_config.get("agents", [])
    return agents == "all" or agent_id in agents

# ============================================================================
# DEPENDENCY FUNCTIONS
# ============================================================================

async def get_current_user_from_request(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """
    Extract current user from request

    Priority:
    1. JWT token in Authorization header
    2. API key in X-API-Key header
    3. Session cookie
    """
    # TODO: Implement JWT validation
    # For now, use a test user ID from header
    user_id = request.headers.get("X-User-ID", "test-user-id")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    return user

async def get_team_membership(
    team_id: str,
    user: User = Depends(get_current_user_from_request),
    db: Session = Depends(get_db)
) -> TeamMember:
    """Get user's team membership"""
    member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user.id
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this team"
        )

    return member

# ============================================================================
# PERMISSION DECORATORS
# ============================================================================

def require_permission(permission: str):
    """
    Decorator to require a specific permission

    Usage:
        @require_permission("agents:use")
        async def use_agent(...):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, team_id: str, db: Session = Depends(get_db), **kwargs):
            # Get user from request
            request = kwargs.get("request")
            if not request:
                raise HTTPException(
                    status_code=500,
                    detail="Request object not found"
                )

            user = await get_current_user_from_request(request, db)

            # Get team membership
            member = db.query(TeamMember).filter(
                TeamMember.team_id == team_id,
                TeamMember.user_id == user.id
            ).first()

            if not member:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not a member of this team"
                )

            # Check permission
            if not has_permission(member.role, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: {permission} required"
                )

            return await func(*args, team_id=team_id, db=db, **kwargs)

        return wrapper
    return decorator

def require_subscription_tier(required_tier: str):
    """
    Decorator to require a minimum subscription tier

    Usage:
        @require_subscription_tier("pro")
        async def use_pro_feature(...):
            ...
    """
    tier_levels = {
        "free": 0,
        "pro": 1,
        "workflow": 2,
        "enterprise": 3
    }

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, team_id: str = None, db: Session = Depends(get_db), **kwargs):
            # If no team_id, check user's personal subscription
            request = kwargs.get("request")
            if not request:
                raise HTTPException(
                    status_code=500,
                    detail="Request object not found"
                )

            user = await get_current_user_from_request(request, db)

            if team_id:
                # Check team subscription
                team = db.query(Team).filter(Team.id == team_id).first()
                if not team:
                    raise HTTPException(
                        status_code=404,
                        detail="Team not found"
                    )

                current_tier = team.subscription_tier
                subscription_status = team.subscription_status
            else:
                # Check user's personal subscription
                current_tier = user.subscription_tier
                subscription_status = user.subscription_status

            # Check if subscription is active
            if subscription_status != "active":
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail="Subscription inactive. Please upgrade to access this feature."
                )

            # Check tier level
            current_level = tier_levels.get(current_tier, 0)
            required_level = tier_levels.get(required_tier, 0)

            if current_level < required_level:
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail=f"This feature requires {required_tier} tier or higher"
                )

            return await func(*args, team_id=team_id, db=db, **kwargs)

        return wrapper
    return decorator

def require_feature(feature: str):
    """
    Decorator to require a specific feature to be enabled

    Usage:
        @require_feature("webhooks")
        async def create_webhook(...):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, team_id: str = None, db: Session = Depends(get_db), **kwargs):
            request = kwargs.get("request")
            if not request:
                raise HTTPException(
                    status_code=500,
                    detail="Request object not found"
                )

            user = await get_current_user_from_request(request, db)

            if team_id:
                # Check team subscription
                team = db.query(Team).filter(Team.id == team_id).first()
                if not team:
                    raise HTTPException(
                        status_code=404,
                        detail="Team not found"
                    )

                tier = team.subscription_tier
            else:
                # Check user's personal subscription
                tier = user.subscription_tier

            if not has_feature(tier, feature):
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail=f"This feature requires a higher subscription tier"
                )

            return await func(*args, team_id=team_id, db=db, **kwargs)

        return wrapper
    return decorator

# ============================================================================
# USAGE LIMIT ENFORCEMENT
# ============================================================================

async def check_api_usage_limit(
    user: User,
    team_id: Optional[str] = None,
    db: Session = Depends(get_db)
) -> bool:
    """Check if user/team has exceeded API usage limits"""
    if team_id:
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            return False

        tier = team.subscription_tier
    else:
        tier = user.subscription_tier

    tier_config = TIER_FEATURES.get(tier, TIER_FEATURES["free"])
    limit = tier_config.get("api_calls_limit", 100)

    # -1 means unlimited
    if limit == -1:
        return True

    # Check current usage
    current_usage = user.api_calls_count if not team_id else 0  # TODO: Implement team usage tracking

    if current_usage >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"API usage limit exceeded. Upgrade to increase limit."
        )

    return True

async def check_team_member_limit(
    team_id: str,
    db: Session = Depends(get_db)
) -> bool:
    """Check if team has reached member limit"""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        return False

    tier_config = TIER_FEATURES.get(team.subscription_tier, TIER_FEATURES["free"])
    limit = tier_config.get("team_members_limit", 3)

    # -1 means unlimited
    if limit == -1:
        return True

    # Count current members
    member_count = db.query(TeamMember).filter(TeamMember.team_id == team_id).count()

    if member_count >= limit:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Team member limit reached. Upgrade to add more members."
        )

    return True
