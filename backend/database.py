"""
🗄️ Database Models
SQLAlchemy models for users, subscriptions, usage

VILLAIN DATABASE: STORING ALL THE SECRETS 😈
"""

import os
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (Railway provides this automatically)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./helix.db"  # Fallback to SQLite for local dev
)

# PostgreSQL URL fix (Railway uses postgres://, SQLAlchemy needs postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
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
    metadata = Column(JSON)

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
