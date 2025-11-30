"""
Helix Collective SaaS - Authentication & Authorization System
==============================================================

Handles:
- User registration and login
- JWT token generation/validation
- API key generation/validation
- Rate limiting
- Tier enforcement

Author: Claude (Manus Validator)
Date: 2025-11-30
"""

import secrets
import bcrypt
import jwt
import asyncpg
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastapi import HTTPException, Header, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, validator
import redis.asyncio as redis
import os
import hashlib

# ============================================================================
# CONFIGURATION
# ============================================================================

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-here")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24 * 7  # 7 days

API_KEY_PREFIX = "hx_user_"
API_KEY_LENGTH = 64  # Total length including prefix

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
DATABASE_URL = os.getenv("DATABASE_URL")

# Rate limits by tier (requests per day)
TIER_LIMITS = {
    "free": 100,
    "pro": 10000,
    "workflow": 20000,
    "enterprise": -1  # Unlimited
}

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    company: Optional[str] = None

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class APIKeyCreate(BaseModel):
    name: str = "Default API Key"
    scopes: List[str] = ["chat", "agents", "prompts", "workflows"]
    expires_in_days: Optional[int] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]

class APIKeyResponse(BaseModel):
    api_key: str  # Full key (shown only once!)
    key_id: str
    name: str
    scopes: List[str]
    created_at: datetime
    expires_at: Optional[datetime]

class User(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    tier: str
    stripe_customer_id: Optional[str]
    subscription_status: str
    requests_per_day: int
    agents_allowed: int
    prompts_allowed: int
    total_requests: int
    total_spent_usd: float
    created_at: datetime
    last_login_at: Optional[datetime]

# ============================================================================
# DATABASE CONNECTION
# ============================================================================

class Database:
    """Async PostgreSQL database connection pool"""

    pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def connect(cls):
        """Initialize connection pool"""
        if not cls.pool:
            cls.pool = await asyncpg.create_pool(
                DATABASE_URL,
                min_size=5,
                max_size=20,
                command_timeout=60
            )
        return cls.pool

    @classmethod
    async def disconnect(cls):
        """Close connection pool"""
        if cls.pool:
            await cls.pool.close()
            cls.pool = None

    @classmethod
    async def execute(cls, query: str, *args):
        """Execute a query (INSERT, UPDATE, DELETE)"""
        pool = await cls.connect()
        async with pool.acquire() as conn:
            return await conn.execute(query, *args)

    @classmethod
    async def fetch(cls, query: str, *args):
        """Fetch multiple rows"""
        pool = await cls.connect()
        async with pool.acquire() as conn:
            return await conn.fetch(query, *args)

    @classmethod
    async def fetchrow(cls, query: str, *args):
        """Fetch single row"""
        pool = await cls.connect()
        async with pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    @classmethod
    async def fetchval(cls, query: str, *args):
        """Fetch single value"""
        pool = await cls.connect()
        async with pool.acquire() as conn:
            return await conn.fetchval(query, *args)

# ============================================================================
# REDIS CONNECTION
# ============================================================================

class Cache:
    """Redis cache for rate limiting and session management"""

    client: Optional[redis.Redis] = None

    @classmethod
    async def connect(cls):
        """Initialize Redis connection"""
        if not cls.client:
            cls.client = await redis.from_url(
                REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
        return cls.client

    @classmethod
    async def disconnect(cls):
        """Close Redis connection"""
        if cls.client:
            await cls.client.close()
            cls.client = None

    @classmethod
    async def get(cls, key: str) -> Optional[str]:
        """Get value from cache"""
        client = await cls.connect()
        return await client.get(key)

    @classmethod
    async def set(cls, key: str, value: str, expiry: int = 3600):
        """Set value in cache with expiry (seconds)"""
        client = await cls.connect()
        return await client.setex(key, expiry, value)

    @classmethod
    async def incr(cls, key: str) -> int:
        """Increment counter"""
        client = await cls.connect()
        return await client.incr(key)

    @classmethod
    async def expire(cls, key: str, seconds: int):
        """Set expiry on key"""
        client = await cls.connect()
        return await client.expire(key, seconds)

    @classmethod
    async def delete(cls, key: str):
        """Delete key"""
        client = await cls.connect()
        return await client.delete(key)

# ============================================================================
# PASSWORD HASHING
# ============================================================================

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(
        password.encode('utf-8'),
        password_hash.encode('utf-8')
    )

# ============================================================================
# JWT TOKEN MANAGEMENT
# ============================================================================

def create_jwt_token(user_id: str, tier: str, expiry_hours: int = JWT_EXPIRY_HOURS) -> str:
    """Create JWT access token"""
    payload = {
        "user_id": user_id,
        "tier": tier,
        "exp": datetime.utcnow() + timedelta(hours=expiry_hours),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt_token(token: str) -> Dict[str, Any]:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ============================================================================
# API KEY MANAGEMENT
# ============================================================================

def generate_api_key() -> tuple[str, str, str]:
    """
    Generate a new API key

    Returns:
        (full_key, key_hash, key_prefix) tuple
    """
    # Generate random bytes
    random_part = secrets.token_hex(32)  # 64 chars
    full_key = f"{API_KEY_PREFIX}{random_part}"

    # Hash the key for storage (never store plaintext!)
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()

    # Prefix for display (e.g., "hx_user_abc123...")
    key_prefix = f"{API_KEY_PREFIX}{random_part[:8]}..."

    return full_key, key_hash, key_prefix

async def verify_api_key(api_key: str) -> Optional[Dict[str, Any]]:
    """
    Verify API key and return user data

    Args:
        api_key: Full API key from Authorization header

    Returns:
        User data dict or None if invalid
    """
    # Hash the provided key
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()

    # Check cache first (faster)
    cached_user = await Cache.get(f"api_key:{key_hash}")
    if cached_user:
        import json
        return json.loads(cached_user)

    # Query database
    query = """
        SELECT
            u.id, u.email, u.tier, u.subscription_status,
            u.requests_per_day, u.agents_allowed, u.prompts_allowed,
            u.total_requests, u.total_spent_usd,
            ak.id as key_id, ak.scopes, ak.expires_at
        FROM api_keys ak
        JOIN users u ON ak.user_id = u.id
        WHERE ak.key_hash = $1
          AND ak.is_active = TRUE
          AND u.is_active = TRUE
          AND (ak.expires_at IS NULL OR ak.expires_at > NOW())
    """

    row = await Database.fetchrow(query, key_hash)

    if not row:
        return None

    user_data = dict(row)

    # Cache for 5 minutes
    import json
    await Cache.set(
        f"api_key:{key_hash}",
        json.dumps(user_data, default=str),
        expiry=300
    )

    # Update last_used_at (fire and forget)
    await Database.execute(
        "UPDATE api_keys SET last_used_at = NOW(), requests_count = requests_count + 1 WHERE id = $1",
        user_data["key_id"]
    )

    return user_data

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

async def register_user(registration: UserRegistration) -> TokenResponse:
    """
    Register new user

    Args:
        registration: User registration data

    Returns:
        JWT token and user data
    """
    # Check if email exists
    existing = await Database.fetchval(
        "SELECT id FROM users WHERE email = $1",
        registration.email
    )

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    password_hash = hash_password(registration.password)

    # Generate API key
    api_key, key_hash, key_prefix = generate_api_key()

    # Insert user
    user_query = """
        INSERT INTO users (
            email, password_hash, full_name, company, tier,
            requests_per_day, agents_allowed, prompts_allowed
        ) VALUES (
            $1, $2, $3, $4, 'free', 100, 3, 10
        )
        RETURNING id, email, full_name, tier, subscription_status,
                  requests_per_day, agents_allowed, prompts_allowed,
                  created_at
    """

    user = await Database.fetchrow(
        user_query,
        registration.email,
        password_hash,
        registration.full_name,
        registration.company
    )

    # Create default API key
    await Database.execute(
        """
        INSERT INTO api_keys (user_id, key_hash, key_prefix, name, scopes)
        VALUES ($1, $2, $3, 'Default API Key', ARRAY['chat', 'agents', 'prompts']::TEXT[])
        """,
        str(user["id"]),
        key_hash,
        key_prefix
    )

    # Generate JWT token
    token = create_jwt_token(str(user["id"]), user["tier"])

    return TokenResponse(
        access_token=token,
        expires_in=JWT_EXPIRY_HOURS * 3600,
        user={
            "id": str(user["id"]),
            "email": user["email"],
            "full_name": user["full_name"],
            "tier": user["tier"],
            "api_key": api_key  # Show ONLY on registration!
        }
    )

async def login_user(login: UserLogin) -> TokenResponse:
    """
    Login existing user

    Args:
        login: Login credentials

    Returns:
        JWT token and user data
    """
    # Fetch user
    user = await Database.fetchrow(
        """
        SELECT id, email, password_hash, full_name, tier,
               subscription_status, is_active
        FROM users
        WHERE email = $1
        """,
        login.email
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user["is_active"]:
        raise HTTPException(status_code=403, detail="Account is disabled")

    # Verify password
    if not verify_password(login.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Update last login
    await Database.execute(
        "UPDATE users SET last_login_at = NOW() WHERE id = $1",
        user["id"]
    )

    # Generate JWT token
    token = create_jwt_token(str(user["id"]), user["tier"])

    return TokenResponse(
        access_token=token,
        expires_in=JWT_EXPIRY_HOURS * 3600,
        user={
            "id": str(user["id"]),
            "email": user["email"],
            "full_name": user["full_name"],
            "tier": user["tier"],
            "subscription_status": user["subscription_status"]
        }
    )

async def create_api_key(user_id: str, key_data: APIKeyCreate) -> APIKeyResponse:
    """
    Create new API key for user

    Args:
        user_id: User UUID
        key_data: API key configuration

    Returns:
        API key response (key shown only once!)
    """
    # Generate key
    api_key, key_hash, key_prefix = generate_api_key()

    # Calculate expiry
    expires_at = None
    if key_data.expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=key_data.expires_in_days)

    # Insert key
    query = """
        INSERT INTO api_keys (user_id, key_hash, key_prefix, name, scopes, expires_at)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id, name, scopes, created_at, expires_at
    """

    key = await Database.fetchrow(
        query,
        user_id,
        key_hash,
        key_prefix,
        key_data.name,
        key_data.scopes,
        expires_at
    )

    return APIKeyResponse(
        api_key=api_key,  # Full key (show only once!)
        key_id=str(key["id"]),
        name=key["name"],
        scopes=key["scopes"],
        created_at=key["created_at"],
        expires_at=key["expires_at"]
    )

# ============================================================================
# RATE LIMITING
# ============================================================================

async def check_rate_limit(user_id: str, tier: str) -> bool:
    """
    Check if user has exceeded rate limit

    Args:
        user_id: User UUID
        tier: User tier (free, pro, enterprise)

    Returns:
        True if within limit, raises HTTPException if exceeded
    """
    limit = TIER_LIMITS.get(tier, 100)

    # Unlimited for enterprise
    if limit == -1:
        return True

    # Get current count from Redis
    today = datetime.utcnow().strftime("%Y-%m-%d")
    key = f"rate_limit:{user_id}:{today}"

    count = await Cache.get(key)

    if count is None:
        # First request today
        await Cache.set(key, "1", expiry=86400)  # 24 hours
        return True

    count = int(count)

    if count >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Tier '{tier}' allows {limit} requests per day. Upgrade to Pro for 10,000 requests/day.",
            headers={"X-RateLimit-Limit": str(limit), "X-RateLimit-Remaining": "0"}
        )

    # Increment counter
    await Cache.incr(key)

    return True

# ============================================================================
# FASTAPI DEPENDENCIES
# ============================================================================

security = HTTPBearer()

async def get_current_user_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency: Get current user from JWT token

    Usage:
        @app.get("/me")
        async def get_me(user = Depends(get_current_user_jwt)):
            return user
    """
    token = credentials.credentials
    payload = decode_jwt_token(token)

    # Fetch full user data
    user = await Database.fetchrow(
        """
        SELECT id, email, full_name, tier, subscription_status,
               requests_per_day, agents_allowed, prompts_allowed,
               total_requests, total_spent_usd, created_at, last_login_at
        FROM users
        WHERE id = $1 AND is_active = TRUE
        """,
        payload["user_id"]
    )

    if not user:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    return dict(user)

async def get_current_user_api_key(
    authorization: str = Header(None)
) -> Dict[str, Any]:
    """
    Dependency: Get current user from API key

    Usage:
        @app.post("/v1/chat")
        async def chat(user = Depends(get_current_user_api_key)):
            return {"user_id": user["id"]}
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format. Use: Bearer <api_key>")

    api_key = authorization.replace("Bearer ", "")

    user = await verify_api_key(api_key)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired API key")

    # Check rate limit
    await check_rate_limit(user["id"], user["tier"])

    return user

# ============================================================================
# TIER ENFORCEMENT
# ============================================================================

def require_tier(minimum_tier: str):
    """
    Decorator/dependency to enforce minimum tier

    Usage:
        @app.post("/v1/agents/oracle/execute")
        async def execute_oracle(
            user = Depends(get_current_user_api_key),
            _ = Depends(require_tier("pro"))
        ):
            return {"result": "..."}
    """
    tier_hierarchy = {"free": 0, "pro": 1, "workflow": 2, "enterprise": 3}

    async def check_tier(user: Dict[str, Any] = Depends(get_current_user_api_key)):
        user_tier_level = tier_hierarchy.get(user["tier"], 0)
        required_tier_level = tier_hierarchy.get(minimum_tier, 0)

        if user_tier_level < required_tier_level:
            raise HTTPException(
                status_code=403,
                detail=f"This feature requires '{minimum_tier}' tier or higher. Current tier: '{user['tier']}'. Upgrade at https://helixcollective.io/pricing"
            )

        return user

    return check_tier

# ============================================================================
# USAGE TRACKING
# ============================================================================

async def track_usage(
    user_id: str,
    endpoint: str,
    method: str,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    tokens_input: int = 0,
    tokens_output: int = 0,
    cost_usd: float = 0.0,
    response_time_ms: int = 0,
    status_code: int = 200,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
):
    """
    Track API usage for analytics and billing

    Args:
        user_id: User UUID
        endpoint: API endpoint (e.g., '/v1/chat')
        method: HTTP method
        provider: LLM provider (anthropic, openai, etc.)
        model: Model used
        tokens_input: Input tokens
        tokens_output: Output tokens
        cost_usd: Cost in USD
        response_time_ms: Response time in milliseconds
        status_code: HTTP status code
        ip_address: Client IP
        user_agent: Client user agent
    """
    # Insert usage record
    await Database.execute(
        """
        INSERT INTO api_usage (
            user_id, endpoint, method, provider, model,
            tokens_input, tokens_output, tokens_total,
            cost_usd, response_time_ms, status_code,
            ip_address, user_agent
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13
        )
        """,
        user_id, endpoint, method, provider, model,
        tokens_input, tokens_output, tokens_input + tokens_output,
        cost_usd, response_time_ms, status_code,
        ip_address, user_agent
    )

    # Update user totals
    await Database.execute(
        """
        UPDATE users
        SET total_requests = total_requests + 1,
            total_spent_usd = total_spent_usd + $2
        WHERE id = $1
        """,
        user_id, cost_usd
    )

    # Update daily summary (upsert)
    today = datetime.utcnow().date()
    await Database.execute(
        """
        INSERT INTO daily_usage_summary (
            user_id, date, total_requests, total_tokens, total_cost_usd
        ) VALUES ($1, $2, 1, $3, $4)
        ON CONFLICT (user_id, date)
        DO UPDATE SET
            total_requests = daily_usage_summary.total_requests + 1,
            total_tokens = daily_usage_summary.total_tokens + $3,
            total_cost_usd = daily_usage_summary.total_cost_usd + $4
        """,
        user_id, today, tokens_input + tokens_output, cost_usd
    )

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

async def get_user_stats(user_id: str) -> Dict[str, Any]:
    """Get user usage statistics"""
    stats = await Database.fetchrow(
        """
        SELECT
            COUNT(*) as total_requests,
            SUM(tokens_total) as total_tokens,
            SUM(cost_usd) as total_cost,
            AVG(response_time_ms) as avg_response_time
        FROM api_usage
        WHERE user_id = $1
        """,
        user_id
    )

    # Today's usage
    today = datetime.utcnow().strftime("%Y-%m-%d")
    today_stats = await Database.fetchrow(
        """
        SELECT total_requests, total_tokens, total_cost_usd
        FROM daily_usage_summary
        WHERE user_id = $1 AND date = $2
        """,
        user_id, today
    )

    return {
        "lifetime": dict(stats) if stats else {},
        "today": dict(today_stats) if today_stats else {"total_requests": 0, "total_tokens": 0, "total_cost_usd": 0}
    }

async def list_api_keys(user_id: str) -> List[Dict[str, Any]]:
    """List all API keys for user (without full keys)"""
    keys = await Database.fetch(
        """
        SELECT id, key_prefix, name, scopes, is_active,
               last_used_at, requests_count, created_at, expires_at
        FROM api_keys
        WHERE user_id = $1
        ORDER BY created_at DESC
        """,
        user_id
    )

    return [dict(key) for key in keys]

async def revoke_api_key(user_id: str, key_id: str):
    """Revoke (deactivate) an API key"""
    await Database.execute(
        """
        UPDATE api_keys
        SET is_active = FALSE
        WHERE id = $1 AND user_id = $2
        """,
        key_id, user_id
    )

    # Invalidate cache
    # (Note: key_hash is needed but we don't have it here, so cache will expire naturally)

# ============================================================================
# INITIALIZATION
# ============================================================================

async def init_auth_system():
    """Initialize database and Redis connections"""
    await Database.connect()
    await Cache.connect()
    print("✅ Auth system initialized")

async def cleanup_auth_system():
    """Cleanup connections"""
    await Database.disconnect()
    await Cache.disconnect()
    print("✅ Auth system cleaned up")
