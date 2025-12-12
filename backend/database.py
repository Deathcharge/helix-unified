"""
🗄️ Database Models
SQLAlchemy models for users, subscriptions, usage

VILLAIN DATABASE: STORING ALL THE SECRETS 😈
"""

import os
from datetime import datetime

from sqlalchemy import (JSON, Boolean, Column, DateTime, Float, Integer,
                        String, create_engine)
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL (Railway provides this automatically)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./helix.db"  # Fallback to SQLite for local dev
)

# PostgreSQL URL fix (Railway uses postgres://, SQLAlchemy needs postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine with connection pooling
# pool_size: Number of connections to keep open
# max_overflow: Additional connections that can be created when pool is full
# pool_pre_ping: Test connections before using them (handles stale connections)
# pool_recycle: Recycle connections after 1 hour to prevent stale connections
engine = create_engine(
    DATABASE_URL,
    pool_size=20,  # Keep 20 connections in pool
    max_overflow=40,  # Allow up to 40 additional connections
    pool_pre_ping=True,  # Verify connection health before use
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=False,  # Set to True for SQL query logging (debug only)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============================================================================
# MODELS
# ============================================================================

class User(Base):
    """User model - VILLAIN PROFILES"""
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    picture = Column(String)
    password_hash = Column(String)  # For email/password auth
    auth_provider = Column(String, default="email")  # email, google, github
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)

    # Subscription
    subscription_tier = Column(String, default="free")  # free, pro, enterprise
    stripe_customer_id = Column(String)
    stripe_subscription_id = Column(String)
    subscription_status = Column(String, default="inactive")  # active, inactive, canceled
    subscription_end_date = Column(DateTime)

    # Usage & Limits
    api_calls_count = Column(Integer, default=0)
    api_calls_limit = Column(Integer, default=1000)  # Free tier limit
    storage_used_mb = Column(Float, default=0)
    storage_limit_mb = Column(Float, default=100)  # Free tier limit

    # Feature flags
    has_web_os_access = Column(Boolean, default=True)
    has_agent_rental_access = Column(Boolean, default=False)
    has_dashboard_pro_access = Column(Boolean, default=False)

    # User preferences
    language = Column(String, default="en")  # Language preference (en, es, fr, de, hi, sa)

class APIKey(Base):
    """API Keys for programmatic access"""
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    key_hash = Column(String, nullable=False, unique=True)
    name = Column(String)
    prefix = Column(String)  # First 8 chars for display (e.g., "hx_1234...")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)
    is_active = Column(Boolean, default=True)
    rate_limit_per_minute = Column(Integer, default=60)

class UsageLog(Base):
    """Usage tracking for billing"""
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    endpoint = Column(String)
    method = Column(String)
    status_code = Column(Integer)
    response_time_ms = Column(Float)
    request_metadata = Column(JSON)  # Renamed from metadata (reserved keyword)

class AgentRental(Base):
    """Agent rental sessions"""
    __tablename__ = "agent_rentals"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    agent_id = Column(String, nullable=False)  # rishi, kael, oracle, etc.
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    messages_count = Column(Integer, default=0)
    tokens_used = Column(Integer, default=0)
    cost_credits = Column(Integer, default=0)
    status = Column(String, default="active")  # active, completed, error

class WebOSSession(Base):
    """Web OS usage sessions"""
    __tablename__ = "web_os_sessions"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    commands_executed = Column(Integer, default=0)
    files_accessed = Column(Integer, default=0)
    session_duration_seconds = Column(Integer, default=0)

class Team(Base):
    """Team/Workspace model - VILLAIN ORGANIZATIONS"""
    __tablename__ = "teams"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    owner_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Subscription (team-level billing)
    subscription_tier = Column(String, default="free")  # free, pro, workflow, enterprise
    stripe_customer_id = Column(String)
    stripe_subscription_id = Column(String)
    subscription_status = Column(String, default="inactive")
    subscription_end_date = Column(DateTime)

    # Team settings
    settings = Column(JSON, default={})

class TeamMember(Base):
    """Team membership with RBAC - VILLAIN MINIONS"""
    __tablename__ = "team_members"

    id = Column(String, primary_key=True)
    team_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)  # owner, admin, member, viewer
    joined_at = Column(DateTime, default=datetime.utcnow)
    invited_by = Column(String)  # User ID who invited

    # Permissions
    permissions = Column(JSON, default={})  # Custom permissions override

class TeamInvitation(Base):
    """Team invitations - RECRUITING VILLAINS"""
    __tablename__ = "team_invitations"

    id = Column(String, primary_key=True)
    team_id = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)  # admin, member, viewer
    invited_by = Column(String, nullable=False)  # User ID
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    status = Column(String, default="pending")  # pending, accepted, expired, revoked
    token = Column(String, unique=True, nullable=False)  # Secure invitation token

class UserActivation(Base):
    """Track user activation events - KEY METRICS"""
    __tablename__ = "user_activations"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    activation_type = Column(String, nullable=False)  # first_api_call, first_agent_session, profile_completed, etc.
    completed_at = Column(DateTime, default=datetime.utcnow, index=True)
    metadata = Column(JSON)  # Additional context

class RevenueEvent(Base):
    """Track revenue events for MRR/ARR calculation"""
    __tablename__ = "revenue_events"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    team_id = Column(String, index=True)
    event_type = Column(String, nullable=False)  # subscription_started, subscription_renewed, subscription_upgraded, subscription_canceled
    amount = Column(Float, nullable=False)  # Amount in USD
    currency = Column(String, default="USD")
    billing_period = Column(String)  # monthly, yearly
    occurred_at = Column(DateTime, default=datetime.utcnow, index=True)
    stripe_event_id = Column(String)  # Reference to Stripe event
    metadata = Column(JSON)

class NPSSurvey(Base):
    """Net Promoter Score surveys"""
    __tablename__ = "nps_surveys"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    score = Column(Integer, nullable=False)  # 0-10
    feedback = Column(String)  # Optional text feedback
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    survey_trigger = Column(String)  # dashboard, email, in_app, etc.

class SupportTicket(Base):
    """Support ticket tracking"""
    __tablename__ = "support_tickets"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    subject = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="open")  # open, in_progress, resolved, closed
    priority = Column(String, default="medium")  # low, medium, high, urgent
    category = Column(String)  # bug, feature_request, billing, general
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime)
    assigned_to = Column(String)  # Support agent ID

class ErrorLog(Base):
    """Application error tracking"""
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True)  # Optional - may be unauthenticated error
    error_type = Column(String, nullable=False)  # ValueError, HTTPException, etc.
    error_message = Column(String, nullable=False)
    stack_trace = Column(String)
    endpoint = Column(String, index=True)
    method = Column(String)
    request_data = Column(JSON)
    occurred_at = Column(DateTime, default=datetime.utcnow, index=True)
    severity = Column(String, default="error")  # warning, error, critical
    resolved = Column(Boolean, default=False)

class HealthCheck(Base):
    """API uptime and health monitoring"""
    __tablename__ = "health_checks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String, nullable=False, index=True)  # api, database, redis, etc.
    status = Column(String, nullable=False)  # healthy, degraded, down
    response_time_ms = Column(Float)
    checked_at = Column(DateTime, default=datetime.utcnow, index=True)
    metadata = Column(JSON)  # Additional health metrics

class DailyMetrics(Base):
    """Pre-calculated daily metrics for dashboard performance"""
    __tablename__ = "daily_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False, index=True, unique=True)

    # User metrics
    new_signups = Column(Integer, default=0)
    daily_active_users = Column(Integer, default=0)
    monthly_active_users = Column(Integer, default=0)
    activations_count = Column(Integer, default=0)

    # Revenue metrics
    mrr = Column(Float, default=0)  # Monthly Recurring Revenue
    arr = Column(Float, default=0)  # Annual Recurring Revenue
    new_revenue = Column(Float, default=0)
    churned_revenue = Column(Float, default=0)

    # Usage metrics
    api_calls_total = Column(Integer, default=0)
    agent_sessions_total = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    error_rate = Column(Float, default=0)  # Percentage

    # Support metrics
    new_tickets = Column(Integer, default=0)
    resolved_tickets = Column(Integer, default=0)
    avg_resolution_time_hours = Column(Float, default=0)

    # NPS
    nps_score = Column(Float)  # -100 to 100
    nps_responses = Column(Integer, default=0)

    calculated_at = Column(DateTime, default=datetime.utcnow)

# ============================================================================
# CREATE TABLES
# ============================================================================

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

# ============================================================================
# HELPERS
# ============================================================================

def get_db():
    """Dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# RUN IF MAIN
# ============================================================================

if __name__ == "__main__":
    print("🗄️ Initializing database...")
    init_db()
    print("😈 Villain database ready!")
