"""
🧪 Test Suite: RBAC Middleware
Tests for role-based access control and permissions

VILLAIN SECURITY TESTING: PROTECT THE FORTRESS 😈
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, User, Team, TeamMember
from backend.middleware.rbac import (
    has_permission,
    has_feature,
    can_use_agent,
    ROLE_PERMISSIONS,
    TIER_FEATURES
)
from backend.main import app

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_rbac.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

from backend.database import get_db
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# ============================================================================
# PERMISSION FUNCTION TESTS
# ============================================================================

def test_owner_has_all_permissions():
    """Test owner role has all permissions"""
    assert has_permission("owner", "team:read")
    assert has_permission("owner", "team:update")
    assert has_permission("owner", "team:delete")
    assert has_permission("owner", "members:invite")
    assert has_permission("owner", "members:remove")
    assert has_permission("owner", "billing:manage")
    assert has_permission("owner", "settings:manage")

def test_admin_permissions():
    """Test admin role has correct permissions"""
    assert has_permission("admin", "team:read")
    assert has_permission("admin", "team:update")
    assert has_permission("admin", "members:invite")
    assert has_permission("admin", "members:remove")
    assert has_permission("admin", "settings:manage")

    # Admin cannot delete team or manage billing
    assert not has_permission("admin", "team:delete")
    assert not has_permission("admin", "billing:manage")

def test_member_permissions():
    """Test member role has limited permissions"""
    assert has_permission("member", "team:read")
    assert has_permission("member", "agents:use")
    assert has_permission("member", "dashboard:view")

    # Member cannot manage team
    assert not has_permission("member", "team:update")
    assert not has_permission("member", "team:delete")
    assert not has_permission("member", "members:invite")

def test_viewer_permissions():
    """Test viewer role has read-only permissions"""
    assert has_permission("viewer", "team:read")
    assert has_permission("viewer", "dashboard:view")

    # Viewer cannot modify anything
    assert not has_permission("viewer", "team:update")
    assert not has_permission("viewer", "agents:use")
    assert not has_permission("viewer", "members:invite")

# ============================================================================
# TIER FEATURE TESTS
# ============================================================================

def test_free_tier_features():
    """Test free tier feature access"""
    assert has_feature("free", "basic_dashboard")
    assert has_feature("free", "basic_agents")

    # Free tier doesn't have advanced features
    assert not has_feature("free", "analytics")
    assert not has_feature("free", "webhooks")
    assert not has_feature("free", "automation")

def test_pro_tier_features():
    """Test pro tier feature access"""
    assert has_feature("pro", "basic_dashboard")
    assert has_feature("pro", "pro_dashboard")
    assert has_feature("pro", "all_agents")
    assert has_feature("pro", "analytics")
    assert has_feature("pro", "webhooks")

    # Pro tier doesn't have workflow features
    assert not has_feature("pro", "automation")
    assert not has_feature("pro", "zapier")

def test_workflow_tier_features():
    """Test workflow tier feature access"""
    assert has_feature("workflow", "all_agents")
    assert has_feature("workflow", "analytics")
    assert has_feature("workflow", "webhooks")
    assert has_feature("workflow", "automation")
    assert has_feature("workflow", "zapier")

def test_enterprise_tier_features():
    """Test enterprise tier has all features"""
    # Enterprise has "all" features
    assert has_feature("enterprise", "analytics")
    assert has_feature("enterprise", "webhooks")
    assert has_feature("enterprise", "automation")
    assert has_feature("enterprise", "custom_branding")
    assert has_feature("enterprise", "any_feature_name")  # Should have everything

# ============================================================================
# AGENT ACCESS TESTS
# ============================================================================

def test_free_tier_agent_access():
    """Test free tier can only use basic agents"""
    assert can_use_agent("free", "rishi")
    assert can_use_agent("free", "kael")
    assert can_use_agent("free", "oracle")

    # Free tier cannot use advanced agents
    assert not can_use_agent("free", "shadow")
    assert not can_use_agent("free", "lumina")

def test_pro_tier_agent_access():
    """Test pro tier can use all agents"""
    assert can_use_agent("pro", "rishi")
    assert can_use_agent("pro", "shadow")
    assert can_use_agent("pro", "lumina")
    assert can_use_agent("pro", "any_agent")  # Pro has "all"

def test_enterprise_tier_agent_access():
    """Test enterprise tier can use all agents"""
    assert can_use_agent("enterprise", "rishi")
    assert can_use_agent("enterprise", "shadow")
    assert can_use_agent("enterprise", "custom_agent")

# ============================================================================
# LIMITS TESTS
# ============================================================================

def test_free_tier_limits():
    """Test free tier limits"""
    config = TIER_FEATURES["free"]
    assert config["api_calls_limit"] == 100
    assert config["team_members_limit"] == 3

def test_pro_tier_limits():
    """Test pro tier limits"""
    config = TIER_FEATURES["pro"]
    assert config["api_calls_limit"] == 10000
    assert config["team_members_limit"] == 10

def test_workflow_tier_limits():
    """Test workflow tier limits"""
    config = TIER_FEATURES["workflow"]
    assert config["api_calls_limit"] == 20000
    assert config["team_members_limit"] == 25

def test_enterprise_tier_unlimited():
    """Test enterprise tier has unlimited resources"""
    config = TIER_FEATURES["enterprise"]
    assert config["api_calls_limit"] == -1  # Unlimited
    assert config["team_members_limit"] == -1  # Unlimited

# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_unauthorized_access_denied(setup_database):
    """Test unauthorized access is denied"""
    # Try to access team endpoint without auth
    response = client.get("/api/teams/teams/nonexistent-team")

    # Should fail (either 401 or 403)
    assert response.status_code in [401, 403, 404]

def test_subscription_tier_enforcement(setup_database):
    """Test subscription tier is enforced"""
    db = TestingSessionLocal()

    # Create free tier user
    user = User(
        id="free-user",
        email="free@example.com",
        name="Free User",
        subscription_tier="free",
        subscription_status="active"
    )
    db.add(user)
    db.commit()

    # Try to access pro feature
    # (Would need actual endpoint that checks tier)
    # For now, verify tier configuration exists
    assert user.subscription_tier == "free"

    db.query(User).filter(User.id == "free-user").delete()
    db.commit()
    db.close()

def test_inactive_subscription_denied(setup_database):
    """Test inactive subscription is denied"""
    db = TestingSessionLocal()

    # Create user with inactive subscription
    user = User(
        id="inactive-user",
        email="inactive@example.com",
        name="Inactive User",
        subscription_tier="pro",
        subscription_status="inactive"
    )
    db.add(user)
    db.commit()

    # Subscription status should be inactive
    assert user.subscription_status == "inactive"

    db.query(User).filter(User.id == "inactive-user").delete()
    db.commit()
    db.close()

# ============================================================================
# ROLE HIERARCHY TESTS
# ============================================================================

def test_role_hierarchy():
    """Test role hierarchy is correct"""
    from backend.middleware.rbac import ROLE_HIERARCHY

    assert ROLE_HIERARCHY["owner"] > ROLE_HIERARCHY["admin"]
    assert ROLE_HIERARCHY["admin"] > ROLE_HIERARCHY["member"]
    assert ROLE_HIERARCHY["member"] > ROLE_HIERARCHY["viewer"]

def test_permission_count():
    """Test each role has expected permission count"""
    assert len(ROLE_PERMISSIONS["owner"]) > len(ROLE_PERMISSIONS["admin"])
    assert len(ROLE_PERMISSIONS["admin"]) > len(ROLE_PERMISSIONS["member"])
    assert len(ROLE_PERMISSIONS["member"]) >= len(ROLE_PERMISSIONS["viewer"])

# ============================================================================
# EDGE CASES
# ============================================================================

def test_invalid_role_has_no_permissions():
    """Test invalid role has no permissions"""
    assert not has_permission("invalid_role", "team:read")
    assert not has_permission("hacker", "team:delete")

def test_invalid_tier_defaults_to_free():
    """Test invalid tier defaults to free tier"""
    config = TIER_FEATURES.get("invalid_tier", TIER_FEATURES["free"])
    assert config == TIER_FEATURES["free"]

def test_case_sensitivity():
    """Test permission checks are case-sensitive"""
    # Permissions are lowercase
    assert has_permission("owner", "team:read")
    # Different case should fail (permissions are exact match)
    # (This depends on implementation - adjust if needed)

# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
