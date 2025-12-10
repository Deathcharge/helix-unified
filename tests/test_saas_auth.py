"""
Comprehensive test suite for SaaS Authentication System
========================================================

Tests:
- User registration (success, validation, duplicates)
- User login (success, failures)
- JWT token generation and validation
- API key creation, validation, and revocation
- Rate limiting
- Tier enforcement
- Password hashing and validation
"""

import asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import jwt
import pytest
from fastapi import HTTPException

from backend.saas_auth import (
    API_KEY_PREFIX,
    JWT_ALGORITHM,
    JWT_SECRET,
    TIER_LIMITS,
    APIKeyCreate,
    APIKeyResponse,
    TokenResponse,
    UserLogin,
    UserRegistration,
    check_rate_limit,
    create_api_key,
    generate_api_key,
    get_current_user_api_key,
    get_current_user_jwt,
    list_api_keys,
    login_user,
    register_user,
    revoke_api_key,
    track_usage,
    verify_api_key,
    verify_jwt_token,
)


class TestUserRegistration:
    """Test user registration functionality"""

    @pytest.mark.asyncio
    async def test_register_user_success(self):
        """Test successful user registration"""
        registration = UserRegistration(
            email="test@example.com",
            password="SecurePass123",
            full_name="Test User",
            company="Test Corp"
        )

        # Mock database operations
        with patch('backend.saas_auth.Database') as mock_db:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool
            mock_pool.fetchrow.return_value = None  # No existing user

            # Mock user creation
            mock_pool.fetchrow.side_effect = [
                None,  # Check for existing user
                {
                    "id": "user_123",
                    "email": "test@example.com",
                    "full_name": "Test User",
                    "company": "Test Corp",
                    "tier": "free",
                    "created_at": datetime.utcnow()
                }  # Created user
            ]

            result = await register_user(registration)

            assert isinstance(result, TokenResponse)
            assert result.token_type == "bearer"
            assert result.expires_in > 0
            assert result.user["email"] == "test@example.com"
            assert result.user["tier"] == "free"

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self):
        """Test registration with duplicate email"""
        registration = UserRegistration(
            email="existing@example.com",
            password="SecurePass123"
        )

        with patch('backend.saas_auth.Database') as mock_db:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool
            # Mock existing user found
            mock_pool.fetchrow.return_value = {"id": "existing_user"}

            with pytest.raises(HTTPException) as exc_info:
                await register_user(registration)

            assert exc_info.value.status_code == 400
            assert "already registered" in str(exc_info.value.detail).lower()

    def test_password_validation_weak(self):
        """Test password strength validation"""
        # Too short
        with pytest.raises(ValueError, match="at least 8 characters"):
            UserRegistration(email="test@example.com", password="Short1")

        # No uppercase
        with pytest.raises(ValueError, match="uppercase"):
            UserRegistration(email="test@example.com", password="lowercase123")

        # No lowercase
        with pytest.raises(ValueError, match="lowercase"):
            UserRegistration(email="test@example.com", password="UPPERCASE123")

        # No digit
        with pytest.raises(ValueError, match="digit"):
            UserRegistration(email="test@example.com", password="NoDigitsHere")

    def test_password_validation_strong(self):
        """Test that strong passwords pass validation"""
        registration = UserRegistration(
            email="test@example.com",
            password="SecurePass123"
        )
        assert registration.password == "SecurePass123"


class TestUserLogin:
    """Test user login functionality"""

    @pytest.mark.asyncio
    async def test_login_success(self):
        """Test successful login"""
        login = UserLogin(email="test@example.com", password="SecurePass123")

        with patch('backend.saas_auth.Database') as mock_db, \
             patch('backend.saas_auth.bcrypt') as mock_bcrypt:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            # Mock user found
            mock_pool.fetchrow.return_value = {
                "id": "user_123",
                "email": "test@example.com",
                "password_hash": b"hashed_password",
                "full_name": "Test User",
                "tier": "pro",
                "created_at": datetime.utcnow()
            }

            # Mock password verification
            mock_bcrypt.checkpw.return_value = True

            result = await login_user(login)

            assert isinstance(result, TokenResponse)
            assert result.user["email"] == "test@example.com"
            assert result.user["tier"] == "pro"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self):
        """Test login with wrong password"""
        login = UserLogin(email="test@example.com", password="WrongPass123")

        with patch('backend.saas_auth.Database') as mock_db, \
             patch('backend.saas_auth.bcrypt') as mock_bcrypt:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            mock_pool.fetchrow.return_value = {
                "id": "user_123",
                "password_hash": b"hashed_password"
            }

            # Mock password verification failure
            mock_bcrypt.checkpw.return_value = False

            with pytest.raises(HTTPException) as exc_info:
                await login_user(login)

            assert exc_info.value.status_code == 401
            assert "invalid" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self):
        """Test login with non-existent email"""
        login = UserLogin(email="nonexistent@example.com", password="Pass123")

        with patch('backend.saas_auth.Database') as mock_db:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool
            mock_pool.fetchrow.return_value = None  # User not found

            with pytest.raises(HTTPException) as exc_info:
                await login_user(login)

            assert exc_info.value.status_code == 401


class TestJWTTokens:
    """Test JWT token generation and validation"""

    def test_jwt_token_generation(self):
        """Test JWT token contains correct data"""
        user_data = {
            "id": "user_123",
            "email": "test@example.com",
            "tier": "pro"
        }

        token = jwt.encode(user_data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        assert decoded["id"] == "user_123"
        assert decoded["email"] == "test@example.com"
        assert decoded["tier"] == "pro"

    def test_jwt_token_expiry(self):
        """Test JWT token expiry validation"""
        expired_time = datetime.utcnow() - timedelta(days=1)
        user_data = {
            "id": "user_123",
            "exp": expired_time.timestamp()
        }

        token = jwt.encode(user_data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

    def test_jwt_invalid_signature(self):
        """Test JWT with invalid signature"""
        token = jwt.encode({"id": "user_123"}, "wrong_secret", algorithm=JWT_ALGORITHM)

        with pytest.raises(jwt.InvalidSignatureError):
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

    @pytest.mark.asyncio
    async def test_verify_jwt_token_success(self):
        """Test JWT token verification"""
        token = jwt.encode(
            {"id": "user_123", "email": "test@example.com", "tier": "pro"},
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

        result = await verify_jwt_token(token)
        assert result["id"] == "user_123"
        assert result["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_verify_jwt_token_invalid(self):
        """Test invalid JWT token verification"""
        with pytest.raises(HTTPException) as exc_info:
            await verify_jwt_token("invalid_token")

        assert exc_info.value.status_code == 401


class TestAPIKeys:
    """Test API key functionality"""

    def test_generate_api_key_format(self):
        """Test API key generation format"""
        api_key = generate_api_key()

        assert api_key.startswith(API_KEY_PREFIX)
        assert len(api_key) == 64
        # Check it's alphanumeric
        assert api_key.replace(API_KEY_PREFIX, "").replace("_", "").isalnum()

    def test_generate_api_key_uniqueness(self):
        """Test that generated API keys are unique"""
        keys = [generate_api_key() for _ in range(100)]
        assert len(keys) == len(set(keys))  # All unique

    @pytest.mark.asyncio
    async def test_create_api_key_success(self):
        """Test API key creation"""
        user_id = "user_123"
        key_data = APIKeyCreate(
            name="Test API Key",
            scopes=["chat", "agents"],
            expires_in_days=30
        )

        with patch('backend.saas_auth.Database') as mock_db:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            result = await create_api_key(user_id, key_data)

            assert isinstance(result, APIKeyResponse)
            assert result.api_key.startswith(API_KEY_PREFIX)
            assert result.name == "Test API Key"
            assert result.scopes == ["chat", "agents"]

    @pytest.mark.asyncio
    async def test_verify_api_key_success(self):
        """Test API key verification"""
        api_key = "hx_user_test123456789"

        with patch('backend.saas_auth.Cache') as mock_cache:
            mock_redis = AsyncMock()
            mock_cache.get_client.return_value = mock_redis

            # Mock cache hit
            mock_redis.get.return_value = '{"id": "user_123", "tier": "pro", "scopes": ["chat"]}'

            result = await verify_api_key(api_key)

            assert result["id"] == "user_123"
            assert result["tier"] == "pro"

    @pytest.mark.asyncio
    async def test_verify_api_key_expired(self):
        """Test expired API key verification"""
        api_key = "hx_user_expired_key"

        with patch('backend.saas_auth.Cache') as mock_cache, \
             patch('backend.saas_auth.Database') as mock_db:
            mock_redis = AsyncMock()
            mock_cache.get_client.return_value = mock_redis
            mock_redis.get.return_value = None  # Cache miss

            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            # Mock expired key
            expired_date = datetime.utcnow() - timedelta(days=1)
            mock_pool.fetchrow.return_value = {
                "expires_at": expired_date,
                "is_active": True
            }

            with pytest.raises(HTTPException) as exc_info:
                await verify_api_key(api_key)

            assert exc_info.value.status_code == 401
            assert "expired" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_list_api_keys(self):
        """Test listing user's API keys"""
        user_id = "user_123"

        with patch('backend.saas_auth.Database') as mock_db:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            mock_pool.fetch.return_value = [
                {
                    "id": "key_1",
                    "name": "Key 1",
                    "key_preview": "hx_user_abc...xyz",
                    "scopes": ["chat"],
                    "created_at": datetime.utcnow(),
                    "expires_at": None,
                    "last_used_at": datetime.utcnow()
                }
            ]

            result = await list_api_keys(user_id)

            assert len(result) == 1
            assert result[0]["name"] == "Key 1"

    @pytest.mark.asyncio
    async def test_revoke_api_key(self):
        """Test API key revocation"""
        user_id = "user_123"
        key_id = "key_1"

        with patch('backend.saas_auth.Database') as mock_db, \
             patch('backend.saas_auth.Cache') as mock_cache:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            mock_redis = AsyncMock()
            mock_cache.get_client.return_value = mock_redis

            await revoke_api_key(user_id, key_id)

            # Verify database update was called
            assert mock_pool.execute.called


class TestRateLimiting:
    """Test rate limiting functionality"""

    @pytest.mark.asyncio
    async def test_rate_limit_free_tier(self):
        """Test rate limiting for free tier"""
        user_id = "user_123"
        tier = "free"

        with patch('backend.saas_auth.Cache') as mock_cache:
            mock_redis = AsyncMock()
            mock_cache.get_client.return_value = mock_redis

            # Mock current usage at 50
            mock_redis.get.return_value = "50"

            # Should pass (under limit of 100)
            result = await check_rate_limit(user_id, tier)
            assert result is True

    @pytest.mark.asyncio
    async def test_rate_limit_exceeded(self):
        """Test rate limit exceeded"""
        user_id = "user_123"
        tier = "free"

        with patch('backend.saas_auth.Cache') as mock_cache:
            mock_redis = AsyncMock()
            mock_cache.get_client.return_value = mock_redis

            # Mock current usage at limit
            mock_redis.get.return_value = str(TIER_LIMITS["free"])

            with pytest.raises(HTTPException) as exc_info:
                await check_rate_limit(user_id, tier)

            assert exc_info.value.status_code == 429
            assert "rate limit" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_rate_limit_enterprise_unlimited(self):
        """Test that enterprise tier has no limits"""
        user_id = "user_123"
        tier = "enterprise"

        with patch('backend.saas_auth.Cache') as mock_cache:
            mock_redis = AsyncMock()
            mock_cache.get_client.return_value = mock_redis

            # Even with high usage, should pass
            mock_redis.get.return_value = "999999"

            result = await check_rate_limit(user_id, tier)
            assert result is True

    @pytest.mark.asyncio
    async def test_track_usage(self):
        """Test usage tracking"""
        user_id = "user_123"
        usage_data = {
            "tokens": 1000,
            "cost_usd": 0.05,
            "model": "claude-3-haiku"
        }

        with patch('backend.saas_auth.Database') as mock_db, \
             patch('backend.saas_auth.Cache') as mock_cache:
            mock_pool = AsyncMock()
            mock_db.get_pool.return_value = mock_pool

            mock_redis = AsyncMock()
            mock_cache.get_client.return_value = mock_redis

            await track_usage(user_id, usage_data)

            # Verify database insert was called
            assert mock_pool.execute.called
            # Verify cache increment was called
            assert mock_redis.incr.called


class TestTierEnforcement:
    """Test tier restriction enforcement"""

    def test_tier_limits_defined(self):
        """Test that all tiers have limits defined"""
        assert "free" in TIER_LIMITS
        assert "pro" in TIER_LIMITS
        assert "workflow" in TIER_LIMITS
        assert "enterprise" in TIER_LIMITS

    def test_tier_limits_values(self):
        """Test tier limit values are reasonable"""
        assert TIER_LIMITS["free"] == 100
        assert TIER_LIMITS["pro"] == 10000
        assert TIER_LIMITS["workflow"] == 20000
        assert TIER_LIMITS["enterprise"] == -1  # Unlimited


class TestDependencies:
    """Test FastAPI dependencies"""

    @pytest.mark.asyncio
    async def test_get_current_user_jwt_success(self):
        """Test JWT dependency extraction"""
        token = jwt.encode(
            {"id": "user_123", "email": "test@example.com", "tier": "pro"},
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

        # Mock HTTPBearer credentials
        credentials = MagicMock()
        credentials.credentials = token

        result = await get_current_user_jwt(credentials)

        assert result["id"] == "user_123"
        assert result["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_current_user_api_key_success(self):
        """Test API key dependency extraction"""
        api_key = "hx_user_test123"

        with patch('backend.saas_auth.verify_api_key') as mock_verify:
            mock_verify.return_value = {
                "id": "user_123",
                "tier": "pro",
                "scopes": ["chat"]
            }

            result = await get_current_user_api_key(x_api_key=api_key)

            assert result["id"] == "user_123"
            assert result["tier"] == "pro"

    @pytest.mark.asyncio
    async def test_get_current_user_api_key_missing(self):
        """Test API key dependency with missing key"""
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user_api_key(x_api_key=None)

        assert exc_info.value.status_code == 401
