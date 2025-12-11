"""
🧪 Test Suite: Analytics Export API
Tests for usage statistics and data export

VILLAIN ANALYTICS TESTING: MEASURE YOUR EVIL SUCCESS 😈
"""

import pytest
import csv
import json
import io
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, User, UsageLog, AgentRental, Team, TeamMember
from backend.main import app

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_analytics.db"
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

@pytest.fixture
def test_user():
    """Create test user with usage data"""
    db = TestingSessionLocal()

    user = User(
        id="analytics-user-1",
        email="analytics@example.com",
        name="Analytics User",
        subscription_tier="pro",
        subscription_status="active"
    )
    db.add(user)
    db.commit()

    # Add usage logs
    for i in range(10):
        log = UsageLog(
            user_id=user.id,
            timestamp=datetime.utcnow() - timedelta(days=i),
            endpoint=f"/api/endpoint-{i % 3}",
            method="GET",
            status_code=200,
            response_time_ms=50.0 + i
        )
        db.add(log)

    # Add agent sessions
    for i in range(5):
        session = AgentRental(
            id=f"session-{i}",
            user_id=user.id,
            agent_id=["rishi", "kael", "oracle"][i % 3],
            started_at=datetime.utcnow() - timedelta(days=i),
            messages_count=10 + i,
            tokens_used=1000 + (i * 100),
            cost_credits=50 + i,
            status="completed"
        )
        db.add(session)

    db.commit()
    yield user

    # Cleanup
    db.query(UsageLog).filter(UsageLog.user_id == user.id).delete()
    db.query(AgentRental).filter(AgentRental.user_id == user.id).delete()
    db.query(User).filter(User.id == user.id).delete()
    db.commit()
    db.close()

# ============================================================================
# USAGE STATS TESTS
# ============================================================================

def test_get_usage_stats(setup_database, test_user):
    """Test getting usage statistics"""
    response = client.get(
        "/api/analytics/usage",
        headers={"X-User-ID": test_user.id}
    )

    assert response.status_code == 200
    data = response.json()

    assert "total_api_calls" in data
    assert "total_agent_sessions" in data
    assert "total_tokens_used" in data
    assert "breakdown_by_endpoint" in data
    assert "breakdown_by_agent" in data

    # Verify counts
    assert data["total_api_calls"] >= 10
    assert data["total_agent_sessions"] >= 5
    assert data["total_tokens_used"] > 0

def test_get_usage_stats_with_date_range(setup_database, test_user):
    """Test usage stats with custom date range"""
    start = (datetime.utcnow() - timedelta(days=7)).isoformat()
    end = datetime.utcnow().isoformat()

    response = client.get(
        f"/api/analytics/usage?start_date={start}&end_date={end}",
        headers={"X-User-ID": test_user.id}
    )

    assert response.status_code == 200
    data = response.json()
    assert "date_range" in data
    assert "start" in data["date_range"]
    assert "end" in data["date_range"]

def test_endpoint_breakdown(setup_database, test_user):
    """Test endpoint usage breakdown"""
    response = client.get(
        "/api/analytics/usage",
        headers={"X-User-ID": test_user.id}
    )

    data = response.json()
    breakdown = data["breakdown_by_endpoint"]

    # Should have multiple endpoints
    assert len(breakdown) > 0
    # Each endpoint should have a count
    for endpoint, count in breakdown.items():
        assert isinstance(count, int)
        assert count > 0

def test_agent_breakdown(setup_database, test_user):
    """Test agent usage breakdown"""
    response = client.get(
        "/api/analytics/usage",
        headers={"X-User-ID": test_user.id}
    )

    data = response.json()
    breakdown = data["breakdown_by_agent"]

    # Should have multiple agents
    assert len(breakdown) > 0
    # Should include our test agents
    assert any(agent in ["rishi", "kael", "oracle"] for agent in breakdown.keys())

# ============================================================================
# EXPORT TESTS
# ============================================================================

def test_export_usage_csv(setup_database, test_user):
    """Test exporting usage data as CSV"""
    response = client.get(
        "/api/analytics/export/usage?format=csv",
        headers={"X-User-ID": test_user.id}
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "attachment" in response.headers["content-disposition"]

    # Parse CSV
    csv_content = response.text
    reader = csv.reader(io.StringIO(csv_content))
    rows = list(reader)

    # Should have header + data rows
    assert len(rows) > 1
    header = rows[0]
    assert "timestamp" in header
    assert "endpoint" in header
    assert "status_code" in header

def test_export_usage_json(setup_database, test_user):
    """Test exporting usage data as JSON"""
    response = client.get(
        "/api/analytics/export/usage?format=json",
        headers={"X-User-ID": test_user.id}
    )

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert "attachment" in response.headers["content-disposition"]

    # Parse JSON
    data = json.loads(response.text)
    assert isinstance(data, list)
    assert len(data) > 0

    # Verify structure
    first_record = data[0]
    assert "timestamp" in first_record
    assert "endpoint" in first_record
    assert "status_code" in first_record

def test_export_agent_sessions_csv(setup_database, test_user):
    """Test exporting agent sessions as CSV"""
    response = client.get(
        "/api/analytics/export/agent-sessions?format=csv",
        headers={"X-User-ID": test_user.id}
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"

    # Parse CSV
    csv_content = response.text
    reader = csv.reader(io.StringIO(csv_content))
    rows = list(reader)

    # Should have header + data rows
    assert len(rows) > 1
    header = rows[0]
    assert "agent_id" in header
    assert "tokens_used" in header
    assert "cost_credits" in header

def test_export_agent_sessions_json(setup_database, test_user):
    """Test exporting agent sessions as JSON"""
    response = client.get(
        "/api/analytics/export/agent-sessions?format=json",
        headers={"X-User-ID": test_user.id}
    )

    assert response.status_code == 200
    data = json.loads(response.text)
    assert isinstance(data, list)
    assert len(data) > 0

    first_session = data[0]
    assert "agent_id" in first_session
    assert "tokens_used" in first_session
    assert "messages_count" in first_session

def test_export_invalid_format(setup_database, test_user):
    """Test export with invalid format fails"""
    response = client.get(
        "/api/analytics/export/usage?format=xml",
        headers={"X-User-ID": test_user.id}
    )

    assert response.status_code == 400
    assert "invalid format" in response.json()["detail"].lower()

# ============================================================================
# BILLING SUMMARY TESTS
# ============================================================================

def test_get_billing_summary(setup_database, test_user):
    """Test getting billing summary"""
    response = client.get(
        "/api/analytics/billing-summary",
        headers={"X-User-ID": test_user.id}
    )

    assert response.status_code == 200
    data = response.json()

    # Verify structure
    assert "subscription_tier" in data
    assert "subscription_status" in data
    assert "billing_period" in data
    assert "costs" in data
    assert "usage" in data

    # Verify costs
    costs = data["costs"]
    assert "base_subscription" in costs
    assert "agent_usage" in costs
    assert "total" in costs

    # Pro tier should have $29 base cost
    assert costs["base_subscription"] == 29

    # Verify usage
    usage = data["usage"]
    assert "api_calls" in usage
    assert "agent_credits_used" in usage

def test_billing_summary_with_date_range(setup_database, test_user):
    """Test billing summary with custom date range"""
    start = (datetime.utcnow() - timedelta(days=30)).isoformat()
    end = datetime.utcnow().isoformat()

    response = client.get(
        f"/api/analytics/billing-summary?start_date={start}&end_date={end}",
        headers={"X-User-ID": test_user.id}
    )

    assert response.status_code == 200
    data = response.json()

    # Verify date range is reflected
    assert "billing_period" in data
    assert "start" in data["billing_period"]
    assert "end" in data["billing_period"]

# ============================================================================
# TEAM ANALYTICS TESTS
# ============================================================================

def test_team_usage_stats(setup_database, test_user):
    """Test getting usage stats for a team"""
    db = TestingSessionLocal()

    # Create team
    team = Team(
        id="analytics-team-1",
        name="Analytics Team",
        slug="analytics-team",
        owner_id=test_user.id,
        subscription_tier="pro",
        subscription_status="active"
    )
    db.add(team)

    # Add member
    member = TeamMember(
        id="analytics-member-1",
        team_id=team.id,
        user_id=test_user.id,
        role="owner"
    )
    db.add(member)
    db.commit()

    # Get team analytics
    response = client.get(
        f"/api/analytics/usage?team_id={team.id}",
        headers={"X-User-ID": test_user.id}
    )

    assert response.status_code == 200
    data = response.json()
    assert "total_api_calls" in data

    # Cleanup
    db.query(TeamMember).filter(TeamMember.team_id == team.id).delete()
    db.query(Team).filter(Team.id == team.id).delete()
    db.commit()
    db.close()

# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
