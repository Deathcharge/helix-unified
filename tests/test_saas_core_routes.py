"""
Comprehensive test suite for SaaS Core API Routes
==================================================

Tests all API endpoints in routes/saas_core.py:
- Authentication endpoints (register, login, API keys)
- Chat completion endpoints
- AI agent endpoints
- Subscription/billing endpoints
- Usage/analytics endpoints
- Health/status endpoints
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from urllib.parse import urlparse

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

# Note: These tests assume FastAPI app setup
# They can be integrated into main test suite or run independently


class TestAuthenticationEndpoints:
    """Test authentication API endpoints"""

    @pytest.mark.asyncio
    async def test_register_endpoint_success(self):
        """Test POST /auth/register"""
        with patch('backend.routes.saas_core.register_user') as mock_register:
            mock_register.return_value = {
                "access_token": "jwt_token_here",
                "token_type": "bearer",
                "expires_in": 604800,
                "user": {
                    "id": "user_123",
                    "email": "test@example.com",
                    "tier": "free"
                }
            }

            # In actual integration test, would use TestClient
            # For unit test, just verify function call
            from backend.routes.saas_core import auth_register
            from backend.saas_auth import UserRegistration

            registration = UserRegistration(
                email="test@example.com",
                password="SecurePass123"
            )

            result = await auth_register(registration)

            assert result["access_token"] == "jwt_token_here"
            assert result["user"]["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_login_endpoint_success(self):
        """Test POST /auth/login"""
        with patch('backend.routes.saas_core.login_user') as mock_login:
            mock_login.return_value = {
                "access_token": "jwt_token_here",
                "token_type": "bearer",
                "expires_in": 604800,
                "user": {
                    "id": "user_123",
                    "email": "test@example.com",
                    "tier": "pro"
                }
            }

            from backend.routes.saas_core import auth_login
            from backend.saas_auth import UserLogin

            login = UserLogin(
                email="test@example.com",
                password="SecurePass123"
            )

            result = await auth_login(login)

            assert result["user"]["tier"] == "pro"

    @pytest.mark.asyncio
    async def test_create_api_key_endpoint(self):
        """Test POST /auth/api-keys"""
        with patch('backend.routes.saas_core.create_api_key') as mock_create:
            mock_create.return_value = {
                "api_key": "hx_user_test123456789",
                "key_id": "key_123",
                "name": "Test API Key",
                "scopes": ["chat", "agents"],
                "created_at": datetime.utcnow(),
                "expires_at": None
            }

            from backend.routes.saas_core import create_new_api_key
            from backend.saas_auth import APIKeyCreate

            key_data = APIKeyCreate(
                name="Test API Key",
                scopes=["chat", "agents"]
            )

            user = {"id": "user_123", "tier": "pro"}

            result = await create_new_api_key(key_data, user)

            assert result["name"] == "Test API Key"
            assert "hx_user_" in result["api_key"]

    @pytest.mark.asyncio
    async def test_list_api_keys_endpoint(self):
        """Test GET /auth/api-keys"""
        with patch('backend.routes.saas_core.list_api_keys') as mock_list:
            mock_list.return_value = [
                {
                    "id": "key_1",
                    "name": "Key 1",
                    "key_preview": "hx_user_abc...xyz",
                    "scopes": ["chat"],
                    "created_at": datetime.utcnow()
                }
            ]

            from backend.routes.saas_core import get_api_keys

            user = {"id": "user_123"}

            result = await get_api_keys(user)

            assert len(result) == 1
            assert result[0]["name"] == "Key 1"

    @pytest.mark.asyncio
    async def test_delete_api_key_endpoint(self):
        """Test DELETE /auth/api-keys/{key_id}"""
        with patch('backend.routes.saas_core.revoke_api_key') as mock_revoke:
            mock_revoke.return_value = None

            from backend.routes.saas_core import delete_api_key

            user = {"id": "user_123"}
            key_id = "key_1"

            result = await delete_api_key(key_id, user)

            assert result["success"] is True
            assert "revoked" in result["message"]

    @pytest.mark.asyncio
    async def test_get_current_user_endpoint(self):
        """Test GET /auth/me"""
        with patch('backend.routes.saas_core.get_user_stats') as mock_stats:
            mock_stats.return_value = {
                "total_requests": 50,
                "total_tokens": 10000,
                "total_cost_usd": 0.50
            }

            from backend.routes.saas_core import get_current_user

            user = {
                "id": "user_123",
                "email": "test@example.com",
                "tier": "pro"
            }

            result = await get_current_user(user)

            assert result["user"]["email"] == "test@example.com"
            assert result["stats"]["total_requests"] == 50


class TestChatEndpoints:
    """Test chat completion API endpoints"""

    @pytest.mark.asyncio
    async def test_chat_endpoint_success(self):
        """Test POST /v1/chat"""
        with patch('backend.routes.saas_core.chat_completion') as mock_chat:
            mock_chat.return_value = {
                "id": "chat_123",
                "model": "claude-3-haiku-20240307",
                "provider": "anthropic",
                "choices": [{"message": {"role": "assistant", "content": "Hello!"}}],
                "usage": {"input_tokens": 10, "output_tokens": 5},
                "cost_usd": 0.0001,
                "response_time_ms": 250,
                "optimize_mode": "cost"
            }

            from backend.routes.saas_core import chat
            from backend.saas_router import ChatRequest, Message

            request = ChatRequest(
                messages=[Message(role="user", content="Hello")]
            )

            user = {"id": "user_123", "tier": "pro"}

            result = await chat(request, user)

            assert result["model"] == "claude-3-haiku-20240307"
            assert result["cost_usd"] > 0

    @pytest.mark.asyncio
    async def test_get_models_endpoint(self):
        """Test GET /v1/models"""
        with patch('backend.routes.saas_core.get_available_models') as mock_models:
            mock_models.return_value = [
                {
                    "model": "claude-3-haiku-20240307",
                    "provider": "anthropic",
                    "pricing": {"input": 0.25, "output": 1.25}
                },
                {
                    "model": "gpt-3.5-turbo-0125",
                    "provider": "openai",
                    "pricing": {"input": 0.50, "output": 1.50}
                }
            ]

            from backend.routes.saas_core import get_models

            user = {"id": "user_123", "tier": "free"}

            result = await get_models(user)

            assert len(result["models"]) >= 2
            assert "claude" in result["models"][0]["model"]

    @pytest.mark.asyncio
    async def test_estimate_cost_endpoint(self):
        """Test POST /v1/estimate"""
        with patch('backend.routes.saas_core.estimate_cost') as mock_estimate:
            mock_estimate.return_value = 0.0015

            from backend.routes.saas_core import estimate_completion_cost

            user = {"id": "user_123", "tier": "pro"}

            result = await estimate_completion_cost(
                model="claude-3-sonnet-20240229",
                input_tokens=1000,
                output_tokens=500,
                user=user
            )

            assert result["estimated_cost_usd"] == 0.0015
            assert result["model"] == "claude-3-sonnet-20240229"


class TestAgentEndpoints:
    """Test AI agent API endpoints"""

    @pytest.mark.asyncio
    async def test_list_agents_endpoint(self):
        """Test GET /v1/agents"""
        with patch('backend.routes.saas_core.list_agents') as mock_list:
            mock_list.return_value = [
                {
                    "id": "kael",
                    "name": "Kael",
                    "specialization": "Code & Documentation"
                },
                {
                    "id": "oracle",
                    "name": "Oracle",
                    "specialization": "Analysis & Patterns"
                }
            ]

            from backend.routes.saas_core import get_agents

            user = {"id": "user_123", "tier": "pro"}

            result = await get_agents(user)

            assert len(result["agents"]) >= 2
            assert result["agents"][0]["id"] == "kael"

    @pytest.mark.asyncio
    async def test_get_agent_endpoint(self):
        """Test GET /v1/agents/{agent_id}"""
        with patch('backend.routes.saas_core.get_agent_info') as mock_info:
            mock_info.return_value = {
                "id": "kael",
                "name": "Kael",
                "specialization": "Code & Documentation",
                "description": "Technical documentation expert"
            }

            from backend.routes.saas_core import get_agent

            user = {"id": "user_123", "tier": "pro"}

            result = await get_agent("kael", user)

            assert result["id"] == "kael"
            assert result["specialization"] == "Code & Documentation"

    @pytest.mark.asyncio
    async def test_execute_agent_endpoint(self):
        """Test POST /v1/agents/{agent_id}/execute"""
        with patch('backend.routes.saas_core.execute_agent') as mock_execute:
            mock_execute.return_value = {
                "agent_id": "kael",
                "task": "document",
                "result": "# API Documentation\n\nThis is...",
                "metadata": {
                    "model": "claude-3-sonnet-20240229",
                    "tokens": 300,
                    "cost_usd": 0.002,
                    "response_time_ms": 500
                }
            }

            from backend.routes.saas_core import execute_agent_task
            from backend.saas_agents import AgentExecutionRequest

            request = AgentExecutionRequest(
                task="document",
                input="Document this API",
                optimize="cost"
            )

            user = {"id": "user_123", "tier": "pro"}

            result = await execute_agent_task("kael", request, user)

            assert result["agent_id"] == "kael"
            assert result["task"] == "document"
            assert len(result["result"]) > 0


class TestBillingEndpoints:
    """Test subscription/billing API endpoints"""

    @pytest.mark.asyncio
    async def test_subscribe_endpoint(self):
        """Test POST /billing/subscribe"""
        with patch('backend.routes.saas_core.create_subscription') as mock_create:
            mock_create.return_value = {
                "subscription_id": "sub_123",
                "customer_id": "cus_123",
                "status": "active",
                "tier": "pro",
                "current_period_end": datetime.utcnow() + timedelta(days=30),
                "cancel_at_period_end": False
            }

            from backend.routes.saas_core import subscribe
            from backend.saas_stripe import SubscriptionRequest

            subscription = SubscriptionRequest(
                tier="pro",
                billing_cycle="monthly"
            )

            user = {
                "id": "user_123",
                "email": "test@example.com"
            }

            result = await subscribe(subscription, user)

            assert result["tier"] == "pro"
            assert result["status"] == "active"

    @pytest.mark.asyncio
    async def test_cancel_subscription_endpoint(self):
        """Test POST /billing/cancel"""
        with patch('backend.routes.saas_core.cancel_subscription') as mock_cancel:
            mock_cancel.return_value = {
                "status": "scheduled_cancellation",
                "cancel_at_period_end": True
            }

            from backend.routes.saas_core import cancel_plan

            user = {"id": "user_123"}

            result = await cancel_plan(immediate=False, user=user)

            assert result["status"] == "scheduled_cancellation"

    @pytest.mark.asyncio
    async def test_update_subscription_endpoint(self):
        """Test PUT /billing/update"""
        with patch('backend.routes.saas_core.update_subscription') as mock_update:
            mock_update.return_value = {
                "status": "updated",
                "new_tier": "enterprise",
                "new_billing_cycle": "yearly"
            }

            from backend.routes.saas_core import update_plan

            user = {"id": "user_123"}

            result = await update_plan(
                new_tier="enterprise",
                new_billing_cycle="yearly",
                user=user
            )

            assert result["new_tier"] == "enterprise"

    @pytest.mark.asyncio
    async def test_create_checkout_session_endpoint(self):
        """Test POST /billing/checkout"""
        with patch('backend.routes.saas_core.create_checkout_session') as mock_checkout:
            mock_checkout.return_value = {
                "id": "cs_123",
                "url": "https://checkout.stripe.com/pay/cs_123"
            }

            from backend.routes.saas_core import create_checkout
            from backend.saas_stripe import CheckoutSessionRequest

            checkout = CheckoutSessionRequest(
                tier="pro",
                billing_cycle="monthly",
                success_url="https://example.com/success",
                cancel_url="https://example.com/cancel"
            )

            user = {
                "id": "user_123",
                "email": "test@example.com"
            }

            result = await create_checkout(checkout, user)

            assert "checkout_url" in result
            assert urlparse(result["checkout_url"]).hostname == "checkout.stripe.com"

    @pytest.mark.asyncio
    async def test_payment_history_endpoint(self):
        """Test GET /billing/history"""
        with patch('backend.routes.saas_core.get_payment_history') as mock_history:
            mock_history.return_value = [
                {
                    "id": "in_123",
                    "amount": 29.00,
                    "currency": "usd",
                    "status": "paid",
                    "created": datetime.utcnow()
                }
            ]

            from backend.routes.saas_core import payment_history

            user = {"id": "user_123"}

            result = await payment_history(limit=10, user=user)

            assert len(result["payments"]) == 1
            assert result["payments"][0]["amount"] == 29.00


class TestUsageEndpoints:
    """Test usage/analytics API endpoints"""

    @pytest.mark.asyncio
    async def test_get_usage_stats_endpoint(self):
        """Test GET /usage/stats"""
        with patch('backend.routes.saas_core.get_user_stats') as mock_stats:
            mock_stats.return_value = {
                "total_requests": 500,
                "total_tokens": 100000,
                "total_cost_usd": 5.00,
                "today_requests": 50
            }

            from backend.routes.saas_core import get_usage_stats

            user = {
                "id": "user_123",
                "tier": "pro",
                "agents_allowed": 14,
                "prompts_allowed": 1000
            }

            result = await get_usage_stats(user)

            assert result["tier"] == "pro"
            assert result["usage"]["total_requests"] == 500
            assert "limits" in result


class TestHealthEndpoints:
    """Test health/status API endpoints"""

    @pytest.mark.asyncio
    async def test_health_check_endpoint(self):
        """Test GET /health"""
        with patch('backend.routes.saas_core.Database') as mock_db, \
             patch('backend.routes.saas_core.Cache') as mock_cache:

            # Mock healthy components
            mock_db.connect = AsyncMock()
            mock_cache.connect = AsyncMock()

            from backend.routes.saas_core import health_check

            result = await health_check()

            assert result["status"] == "healthy"
            assert "components" in result
            assert "database" in result["components"]
            assert "redis" in result["components"]
            assert "providers" in result["components"]
            assert "stripe" in result["components"]

    @pytest.mark.asyncio
    async def test_health_check_degraded(self):
        """Test health check when components are unhealthy"""
        with patch('backend.routes.saas_core.Database') as mock_db, \
             patch('backend.routes.saas_core.Cache') as mock_cache:

            # Mock failed database connection
            mock_db.connect = AsyncMock(side_effect=Exception("Connection failed"))
            mock_cache.connect = AsyncMock()

            from backend.routes.saas_core import health_check

            result = await health_check()

            assert result["status"] == "degraded"
            assert "unhealthy" in result["components"]["database"]

    @pytest.mark.asyncio
    async def test_root_endpoint(self):
        """Test GET / (root endpoint)"""
        from backend.routes.saas_core import root

        result = await root()

        assert result["name"] == "Helix Collective SaaS API"
        assert result["version"] == "1.0.0"
        assert "endpoints" in result
        assert "documentation" in result


class TestErrorHandling:
    """Test error handling in endpoints"""

    @pytest.mark.asyncio
    async def test_register_duplicate_email_error(self):
        """Test registration error handling"""
        with patch('backend.routes.saas_core.register_user') as mock_register:
            mock_register.side_effect = HTTPException(
                status_code=400,
                detail="Email already registered"
            )

            from backend.routes.saas_core import auth_register
            from backend.saas_auth import UserRegistration

            registration = UserRegistration(
                email="existing@example.com",
                password="SecurePass123"
            )

            with pytest.raises(HTTPException) as exc_info:
                await auth_register(registration)

            assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_chat_rate_limit_error(self):
        """Test chat endpoint rate limit error"""
        with patch('backend.routes.saas_core.chat_completion') as mock_chat:
            mock_chat.side_effect = HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )

            from backend.routes.saas_core import chat
            from backend.saas_router import ChatRequest, Message

            request = ChatRequest(
                messages=[Message(role="user", content="Hello")]
            )

            user = {"id": "user_123", "tier": "free"}

            with pytest.raises(HTTPException) as exc_info:
                await chat(request, user)

            assert exc_info.value.status_code == 429

    @pytest.mark.asyncio
    async def test_agent_tier_restriction_error(self):
        """Test agent endpoint tier restriction error"""
        with patch('backend.routes.saas_core.execute_agent') as mock_execute:
            mock_execute.side_effect = HTTPException(
                status_code=403,
                detail="Agent not available for your tier"
            )

            from backend.routes.saas_core import execute_agent_task
            from backend.saas_agents import AgentExecutionRequest

            request = AgentExecutionRequest(
                task="analyze",
                input="Test",
                optimize="quality"
            )

            user = {"id": "user_123", "tier": "free"}

            with pytest.raises(HTTPException) as exc_info:
                await execute_agent_task("oracle", request, user)

            assert exc_info.value.status_code == 403


class TestWebhookEndpoints:
    """Test webhook endpoints"""

    @pytest.mark.asyncio
    async def test_stripe_webhook_endpoint(self):
        """Test POST /billing/webhook"""
        with patch('backend.routes.saas_core.stripe.Webhook.construct_event') as mock_construct, \
             patch('backend.routes.saas_core.handle_webhook_event') as mock_handle:

            # Mock valid webhook event
            mock_event = {
                "type": "checkout.session.completed",
                "data": {"object": {}}
            }
            mock_construct.return_value = mock_event

            from fastapi import Request

            from backend.routes.saas_core import stripe_webhook

            # Mock request
            mock_request = MagicMock(spec=Request)
            mock_request.body = AsyncMock(return_value=b'{"type": "test"}')
            mock_request.headers.get.return_value = "test_signature"

            with patch('backend.routes.saas_core.os.getenv', return_value="test_secret"):
                result = await stripe_webhook(mock_request)

                assert result["status"] == "success"
                assert mock_handle.called
