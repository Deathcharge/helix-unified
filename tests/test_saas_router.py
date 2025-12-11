"""
Comprehensive test suite for SaaS Multi-LLM Router
===================================================

Tests:
- LLM routing based on optimization strategy (cost/speed/quality)
- Model pricing calculations
- Tier-based model access restrictions
- Cost estimation
- Multiple LLM provider integration (Anthropic, OpenAI, xAI, Perplexity)
- Error handling and fallbacks
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from backend.saas_router import (
    MODEL_PRICING,
    MODEL_PROFILES,
    ChatRequest,
    ChatResponse,
    Message,
    chat_completion,
    estimate_cost,
    get_available_models,
    route_to_best_model,
)


class TestModelRouting:
    """Test intelligent model routing"""

    def test_route_cost_optimization_free_tier(self):
        """Test cost-optimized routing for free tier"""
        result = route_to_best_model(
            tier="free",
            optimize="cost",
            model=None
        )

        # Should route to cheapest free tier model (claude-3-haiku)
        assert result in ["claude-3-haiku-20240307", "gpt-3.5-turbo-0125"]

    def test_route_speed_optimization(self):
        """Test speed-optimized routing"""
        result = route_to_best_model(
            tier="pro",
            optimize="speed",
            model=None
        )

        # Should route to fastest model
        assert "haiku" in result.lower() or "3.5" in result

    def test_route_quality_optimization(self):
        """Test quality-optimized routing"""
        result = route_to_best_model(
            tier="pro",
            optimize="quality",
            model=None
        )

        # Should route to highest quality model (claude-opus or gpt-4)
        assert "opus" in result.lower() or "gpt-4" in result

    def test_route_specific_model_allowed(self):
        """Test routing to specific model when allowed"""
        result = route_to_best_model(
            tier="pro",
            optimize="cost",
            model="gpt-4-turbo-2024-04-09"
        )

        assert result == "gpt-4-turbo-2024-04-09"

    def test_route_specific_model_restricted(self):
        """Test routing blocked when model not allowed for tier"""
        with pytest.raises(HTTPException) as exc_info:
            route_to_best_model(
                tier="free",
                optimize="cost",
                model="claude-3-opus-20240229"  # Pro+ only
            )

        assert exc_info.value.status_code == 403
        assert "not available" in str(exc_info.value.detail).lower()


class TestModelPricing:
    """Test model pricing calculations"""

    def test_pricing_data_complete(self):
        """Test that all models have pricing data"""
        for model, pricing in MODEL_PRICING.items():
            assert "input" in pricing
            assert "output" in pricing
            assert pricing["input"] > 0
            assert pricing["output"] > 0

    def test_estimate_cost_haiku(self):
        """Test cost estimation for Claude Haiku"""
        cost = estimate_cost(
            model="claude-3-haiku-20240307",
            input_tokens=1000,
            output_tokens=500
        )

        # Haiku: $0.25 per 1M input, $1.25 per 1M output
        # (1000 / 1M) * 0.25 + (500 / 1M) * 1.25 = 0.000875
        expected = (1000 / 1_000_000) * 0.25 + (500 / 1_000_000) * 1.25
        assert abs(cost - expected) < 0.000001

    def test_estimate_cost_opus(self):
        """Test cost estimation for Claude Opus"""
        cost = estimate_cost(
            model="claude-3-opus-20240229",
            input_tokens=2000,
            output_tokens=1000
        )

        # Opus: $15 per 1M input, $75 per 1M output
        expected = (2000 / 1_000_000) * 15 + (1000 / 1_000_000) * 75
        assert abs(cost - expected) < 0.000001

    def test_estimate_cost_gpt35(self):
        """Test cost estimation for GPT-3.5"""
        cost = estimate_cost(
            model="gpt-3.5-turbo-0125",
            input_tokens=1500,
            output_tokens=750
        )

        # GPT-3.5: $0.50 per 1M input, $1.50 per 1M output
        expected = (1500 / 1_000_000) * 0.50 + (750 / 1_000_000) * 1.50
        assert abs(cost - expected) < 0.000001

    def test_estimate_cost_unknown_model(self):
        """Test cost estimation for unknown model"""
        with pytest.raises(HTTPException) as exc_info:
            estimate_cost(
                model="unknown-model-v1",
                input_tokens=1000,
                output_tokens=500
            )

        assert exc_info.value.status_code == 400


class TestTierModelAccess:
    """Test tier-based model access restrictions"""

    @pytest.mark.asyncio
    async def test_get_available_models_free_tier(self):
        """Test free tier has limited model access"""
        models = await get_available_models(tier="free")

        model_names = [m["model"] for m in models]

        # Free tier should only have basic models
        assert "claude-3-haiku-20240307" in model_names
        assert "gpt-3.5-turbo-0125" in model_names

        # Should NOT have premium models
        assert "claude-3-opus-20240229" not in model_names
        assert "gpt-4-turbo-2024-04-09" not in model_names

    @pytest.mark.asyncio
    async def test_get_available_models_pro_tier(self):
        """Test pro tier has access to all models"""
        models = await get_available_models(tier="pro")

        model_names = [m["model"] for m in models]

        # Pro tier should have all models
        assert "claude-3-haiku-20240307" in model_names
        assert "claude-3-opus-20240229" in model_names
        assert "gpt-3.5-turbo-0125" in model_names
        assert "gpt-4-turbo-2024-04-09" in model_names

    @pytest.mark.asyncio
    async def test_get_available_models_include_pricing(self):
        """Test that available models include pricing info"""
        models = await get_available_models(tier="pro")

        for model in models:
            assert "model" in model
            assert "provider" in model
            assert "pricing" in model
            assert "input" in model["pricing"]
            assert "output" in model["pricing"]


class TestChatCompletion:
    """Test chat completion functionality"""

    @pytest.mark.asyncio
    async def test_chat_completion_anthropic_success(self):
        """Test successful chat completion with Anthropic"""
        request = ChatRequest(
            messages=[
                Message(role="user", content="Hello, how are you?")
            ],
            optimize="cost",
            temperature=0.7,
            max_tokens=100
        )

        user = {
            "id": "user_123",
            "tier": "pro",
            "email": "test@example.com"
        }

        with patch('backend.saas_router.anthropic_client') as mock_client, \
             patch('backend.saas_router.track_usage') as mock_track:

            # Mock Anthropic API response
            mock_response = MagicMock()
            mock_response.id = "msg_123"
            mock_response.model = "claude-3-haiku-20240307"
            mock_response.content = [MagicMock(text="Hello! I'm doing well, thank you.")]
            mock_response.usage = MagicMock(
                input_tokens=10,
                output_tokens=15
            )

            mock_client.messages.create = AsyncMock(return_value=mock_response)

            result = await chat_completion(request, user)

            assert isinstance(result, ChatResponse)
            assert result.model == "claude-3-haiku-20240307"
            assert result.provider == "anthropic"
            assert result.usage["input_tokens"] == 10
            assert result.usage["output_tokens"] == 15
            assert result.cost_usd > 0
            assert mock_track.called

    @pytest.mark.asyncio
    async def test_chat_completion_openai_success(self):
        """Test successful chat completion with OpenAI"""
        request = ChatRequest(
            messages=[
                Message(role="user", content="What is 2+2?")
            ],
            optimize="speed",
            model="gpt-3.5-turbo-0125"
        )

        user = {
            "id": "user_123",
            "tier": "pro",
            "email": "test@example.com"
        }

        with patch('backend.saas_router.openai_client') as mock_client, \
             patch('backend.saas_router.track_usage') as mock_track:

            # Mock OpenAI API response
            mock_response = MagicMock()
            mock_response.id = "chatcmpl_123"
            mock_response.model = "gpt-3.5-turbo-0125"
            mock_response.choices = [
                MagicMock(
                    message=MagicMock(
                        role="assistant",
                        content="2+2 equals 4."
                    )
                )
            ]
            mock_response.usage = MagicMock(
                prompt_tokens=8,
                completion_tokens=6
            )

            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

            result = await chat_completion(request, user)

            assert isinstance(result, ChatResponse)
            assert result.model == "gpt-3.5-turbo-0125"
            assert result.provider == "openai"
            assert result.usage["input_tokens"] == 8
            assert result.usage["output_tokens"] == 6

    @pytest.mark.asyncio
    async def test_chat_completion_rate_limit_check(self):
        """Test that rate limiting is checked before completion"""
        request = ChatRequest(
            messages=[Message(role="user", content="Test")]
        )

        user = {
            "id": "user_123",
            "tier": "free",
            "email": "test@example.com"
        }

        with patch('backend.saas_router.check_rate_limit') as mock_limit:
            mock_limit.side_effect = HTTPException(status_code=429, detail="Rate limit exceeded")

            with pytest.raises(HTTPException) as exc_info:
                await chat_completion(request, user)

            assert exc_info.value.status_code == 429

    @pytest.mark.asyncio
    async def test_chat_completion_invalid_model_for_tier(self):
        """Test chat completion with model not available for tier"""
        request = ChatRequest(
            messages=[Message(role="user", content="Test")],
            model="claude-3-opus-20240229"  # Not available for free tier
        )

        user = {
            "id": "user_123",
            "tier": "free",
            "email": "test@example.com"
        }

        with pytest.raises(HTTPException) as exc_info:
            await chat_completion(request, user)

        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_chat_completion_api_error_handling(self):
        """Test error handling when LLM API fails"""
        request = ChatRequest(
            messages=[Message(role="user", content="Test")]
        )

        user = {
            "id": "user_123",
            "tier": "pro",
            "email": "test@example.com"
        }

        with patch('backend.saas_router.anthropic_client') as mock_client, \
             patch('backend.saas_router.check_rate_limit'):

            # Mock API error
            mock_client.messages.create = AsyncMock(
                side_effect=Exception("API connection failed")
            )

            with pytest.raises(HTTPException) as exc_info:
                await chat_completion(request, user)

            assert exc_info.value.status_code == 500


class TestModelProfiles:
    """Test model performance profiles"""

    def test_model_profiles_exist(self):
        """Test that model profiles are defined"""
        assert "claude-3-opus-20240229" in MODEL_PROFILES
        assert "claude-3-haiku-20240307" in MODEL_PROFILES
        assert "gpt-4-turbo-2024-04-09" in MODEL_PROFILES
        assert "gpt-3.5-turbo-0125" in MODEL_PROFILES

    def test_model_profiles_structure(self):
        """Test model profiles have required fields"""
        for model, profile in MODEL_PROFILES.items():
            assert "provider" in profile
            assert "tier_requirement" in profile
            assert "quality_score" in profile
            assert "speed_score" in profile
            assert profile["provider"] in ["anthropic", "openai", "xai", "perplexity"]
            assert profile["tier_requirement"] in ["free", "pro", "workflow", "enterprise"]
            assert 0 <= profile["quality_score"] <= 10
            assert 0 <= profile["speed_score"] <= 10


class TestRequestValidation:
    """Test request validation"""

    def test_chat_request_valid_messages(self):
        """Test valid chat request"""
        request = ChatRequest(
            messages=[
                Message(role="system", content="You are a helpful assistant"),
                Message(role="user", content="Hello")
            ]
        )

        assert len(request.messages) == 2
        assert request.messages[0].role == "system"
        assert request.messages[1].role == "user"

    def test_chat_request_temperature_bounds(self):
        """Test temperature validation"""
        # Valid temperatures
        ChatRequest(messages=[Message(role="user", content="Test")], temperature=0.0)
        ChatRequest(messages=[Message(role="user", content="Test")], temperature=1.0)
        ChatRequest(messages=[Message(role="user", content="Test")], temperature=2.0)

        # Invalid temperatures should be caught by pydantic
        with pytest.raises(Exception):
            ChatRequest(messages=[Message(role="user", content="Test")], temperature=-0.1)

        with pytest.raises(Exception):
            ChatRequest(messages=[Message(role="user", content="Test")], temperature=2.1)

    def test_chat_request_max_tokens_bounds(self):
        """Test max_tokens validation"""
        # Valid max_tokens
        ChatRequest(messages=[Message(role="user", content="Test")], max_tokens=1)
        ChatRequest(messages=[Message(role="user", content="Test")], max_tokens=4096)

        # Invalid max_tokens
        with pytest.raises(Exception):
            ChatRequest(messages=[Message(role="user", content="Test")], max_tokens=0)

        with pytest.raises(Exception):
            ChatRequest(messages=[Message(role="user", content="Test")], max_tokens=5000)

    def test_message_role_validation(self):
        """Test message role validation"""
        # Valid roles
        Message(role="system", content="Test")
        Message(role="user", content="Test")
        Message(role="assistant", content="Test")

        # Invalid role should be caught by pydantic
        with pytest.raises(Exception):
            Message(role="invalid", content="Test")


class TestPerformance:
    """Test performance-related functionality"""

    @pytest.mark.asyncio
    async def test_chat_completion_response_time_tracking(self):
        """Test that response time is tracked"""
        request = ChatRequest(
            messages=[Message(role="user", content="Test")]
        )

        user = {
            "id": "user_123",
            "tier": "pro",
            "email": "test@example.com"
        }

        with patch('backend.saas_router.anthropic_client') as mock_client, \
             patch('backend.saas_router.track_usage'), \
             patch('backend.saas_router.check_rate_limit'):

            mock_response = MagicMock()
            mock_response.id = "msg_123"
            mock_response.model = "claude-3-haiku-20240307"
            mock_response.content = [MagicMock(text="Response")]
            mock_response.usage = MagicMock(input_tokens=10, output_tokens=10)

            mock_client.messages.create = AsyncMock(return_value=mock_response)

            result = await chat_completion(request, user)

            # Response time should be tracked
            assert result.response_time_ms > 0
            assert isinstance(result.response_time_ms, int)
