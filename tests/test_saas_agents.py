"""
Comprehensive test suite for SaaS AI Agents
============================================

Tests:
- Agent registry and definitions
- Agent execution with tier restrictions
- Agent task validation
- System prompt generation
- Model preference handling
- Usage tracking for agent executions
- Error handling
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from backend.saas_agents import (
    AGENT_REGISTRY,
    AgentExecutionRequest,
    AgentExecutionResponse,
    execute_agent,
    get_agent_info,
    list_agents,
)


class TestAgentRegistry:
    """Test agent registry and definitions"""

    def test_agent_registry_exists(self):
        """Test that agent registry is defined"""
        assert AGENT_REGISTRY is not None
        assert len(AGENT_REGISTRY) >= 14  # Should have at least 14 agents

    def test_all_agents_have_required_fields(self):
        """Test that all agents have required fields"""
        required_fields = [
            "name",
            "specialization",
            "description",
            "system_prompt",
            "model_preference",
            "tier_restriction",
            "tasks"
        ]

        for agent_id, agent in AGENT_REGISTRY.items():
            for field in required_fields:
                assert field in agent, f"Agent {agent_id} missing {field}"

    def test_agent_system_prompts_not_empty(self):
        """Test that all agents have non-empty system prompts"""
        for agent_id, agent in AGENT_REGISTRY.items():
            assert len(agent["system_prompt"]) > 50, f"Agent {agent_id} has too short system prompt"
            assert agent["name"] in agent["system_prompt"], f"Agent {agent_id} name not in prompt"

    def test_agent_specializations_unique(self):
        """Test that agent specializations are unique"""
        specializations = [agent["specialization"] for agent in AGENT_REGISTRY.values()]
        assert len(specializations) == len(set(specializations))

    def test_specific_agents_exist(self):
        """Test that key agents are defined"""
        expected_agents = [
            "kael", "oracle", "lumina", "shadow", "agni",
            "vega", "echo", "phoenix", "manus", "gemini",
            "aether", "samsara", "kavach", "sanghacore"
        ]

        for agent_id in expected_agents:
            assert agent_id in AGENT_REGISTRY, f"Agent {agent_id} not found"


class TestListAgents:
    """Test agent listing functionality"""

    @pytest.mark.asyncio
    async def test_list_agents_free_tier(self):
        """Test listing agents for free tier"""
        agents = await list_agents(tier="free")

        # Free tier should have limited access
        assert len(agents) >= 3  # At least 3 agents for free

        # Check that all returned agents allow free tier
        for agent in agents:
            agent_data = AGENT_REGISTRY[agent["id"]]
            assert agent_data["tier_restriction"] is None or agent_data["tier_restriction"] == "free"

    @pytest.mark.asyncio
    async def test_list_agents_pro_tier(self):
        """Test listing agents for pro tier"""
        agents = await list_agents(tier="pro")

        # Pro tier should have more agents
        assert len(agents) >= 10  # Most agents available for pro

        # Should include agents with pro restriction
        agent_ids = [agent["id"] for agent in agents]
        assert "oracle" in agent_ids
        assert "lumina" in agent_ids

    @pytest.mark.asyncio
    async def test_list_agents_enterprise_tier(self):
        """Test listing agents for enterprise tier"""
        agents = await list_agents(tier="enterprise")

        # Enterprise should have all agents
        assert len(agents) == len(AGENT_REGISTRY)

        # Should include enterprise-only agents
        agent_ids = [agent["id"] for agent in agents]
        assert "manus" in agent_ids
        assert "kavach" in agent_ids
        assert "sanghacore" in agent_ids

    @pytest.mark.asyncio
    async def test_list_agents_includes_metadata(self):
        """Test that agent list includes required metadata"""
        agents = await list_agents(tier="pro")

        for agent in agents:
            assert "id" in agent
            assert "name" in agent
            assert "specialization" in agent
            assert "description" in agent
            assert "tasks" in agent
            assert "tier_restriction" in agent


class TestGetAgentInfo:
    """Test getting individual agent information"""

    @pytest.mark.asyncio
    async def test_get_agent_info_success(self):
        """Test getting agent info for accessible agent"""
        agent_info = await get_agent_info("kael", tier="free")

        assert agent_info["id"] == "kael"
        assert agent_info["name"] == "Kael"
        assert agent_info["specialization"] == "Code & Documentation"
        assert len(agent_info["system_prompt"]) > 0
        assert "tasks" in agent_info

    @pytest.mark.asyncio
    async def test_get_agent_info_restricted_agent(self):
        """Test getting info for agent restricted by tier"""
        with pytest.raises(HTTPException) as exc_info:
            await get_agent_info("oracle", tier="free")  # Oracle requires pro

        assert exc_info.value.status_code == 403
        assert "not available" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_get_agent_info_nonexistent_agent(self):
        """Test getting info for nonexistent agent"""
        with pytest.raises(HTTPException) as exc_info:
            await get_agent_info("nonexistent_agent", tier="enterprise")

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_get_agent_info_pro_access(self):
        """Test that pro tier can access pro agents"""
        agent_info = await get_agent_info("oracle", tier="pro")
        assert agent_info["id"] == "oracle"

    @pytest.mark.asyncio
    async def test_get_agent_info_enterprise_access(self):
        """Test that enterprise tier can access enterprise agents"""
        agent_info = await get_agent_info("manus", tier="enterprise")
        assert agent_info["id"] == "manus"


class TestAgentExecution:
    """Test agent execution functionality"""

    @pytest.mark.asyncio
    async def test_execute_agent_success(self):
        """Test successful agent execution"""
        request = AgentExecutionRequest(
            task="document",
            input="Write documentation for a REST API endpoint",
            parameters={"format": "markdown"},
            optimize="cost"
        )

        user = {
            "id": "user_123",
            "tier": "pro",
            "email": "test@example.com"
        }

        with patch('backend.saas_agents.call_anthropic') as mock_call, \
             patch('backend.saas_agents.track_usage') as mock_track, \
             patch('backend.saas_agents.check_rate_limit'):

            # Mock LLM response
            mock_call.return_value = {
                "content": "# API Documentation\n\nThis endpoint...",
                "usage": {"input_tokens": 100, "output_tokens": 200},
                "model": "claude-3-sonnet-20240229"
            }

            result = await execute_agent("kael", request, user)

            assert isinstance(result, AgentExecutionResponse)
            assert result.agent_id == "kael"
            assert result.task == "document"
            assert len(result.result) > 0
            assert result.metadata["model"] == "claude-3-sonnet-20240229"
            assert result.metadata["tokens"] > 0
            assert result.metadata["cost_usd"] > 0

            # Verify usage was tracked
            assert mock_track.called

    @pytest.mark.asyncio
    async def test_execute_agent_tier_restriction(self):
        """Test agent execution blocked by tier restriction"""
        request = AgentExecutionRequest(
            task="analyze",
            input="Analyze this data",
            optimize="quality"
        )

        user = {
            "id": "user_123",
            "tier": "free",  # Free tier
            "email": "test@example.com"
        }

        # Try to execute Oracle (pro only)
        with pytest.raises(HTTPException) as exc_info:
            await execute_agent("oracle", request, user)

        assert exc_info.value.status_code == 403
        assert "not available" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_execute_agent_invalid_task(self):
        """Test agent execution with invalid task type"""
        request = AgentExecutionRequest(
            task="invalid_task",
            input="Test input",
            optimize="cost"
        )

        user = {
            "id": "user_123",
            "tier": "pro",
            "email": "test@example.com"
        }

        with pytest.raises(HTTPException) as exc_info:
            await execute_agent("kael", request, user)

        assert exc_info.value.status_code == 400
        assert "not supported" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_execute_agent_nonexistent_agent(self):
        """Test executing nonexistent agent"""
        request = AgentExecutionRequest(
            task="test",
            input="Test",
            optimize="cost"
        )

        user = {"id": "user_123", "tier": "enterprise", "email": "test@example.com"}

        with pytest.raises(HTTPException) as exc_info:
            await execute_agent("nonexistent", request, user)

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_execute_agent_rate_limit(self):
        """Test agent execution blocked by rate limit"""
        request = AgentExecutionRequest(
            task="document",
            input="Test",
            optimize="cost"
        )

        user = {"id": "user_123", "tier": "free", "email": "test@example.com"}

        with patch('backend.saas_agents.check_rate_limit') as mock_limit:
            mock_limit.side_effect = HTTPException(status_code=429, detail="Rate limit exceeded")

            with pytest.raises(HTTPException) as exc_info:
                await execute_agent("kael", request, user)

            assert exc_info.value.status_code == 429

    @pytest.mark.asyncio
    async def test_execute_agent_with_custom_parameters(self):
        """Test agent execution with custom parameters"""
        request = AgentExecutionRequest(
            task="analyze",
            input="Analyze this dataset",
            parameters={
                "depth": "detailed",
                "focus": "trends",
                "output_format": "json"
            },
            optimize="quality"
        )

        user = {"id": "user_123", "tier": "pro", "email": "test@example.com"}

        with patch('backend.saas_agents.call_anthropic') as mock_call, \
             patch('backend.saas_agents.track_usage'), \
             patch('backend.saas_agents.check_rate_limit'):

            mock_call.return_value = {
                "content": '{"trends": ["growth", "decline"]}',
                "usage": {"input_tokens": 150, "output_tokens": 100},
                "model": "gpt-4-turbo-2024-04-09"
            }

            result = await execute_agent("oracle", request, user)

            assert result.agent_id == "oracle"
            # Verify parameters were passed to the agent
            call_args = mock_call.call_args
            assert "parameters" in str(call_args) or "depth" in str(call_args)


class TestAgentModels:
    """Test Pydantic models"""

    def test_agent_execution_request_valid(self):
        """Test valid agent execution request"""
        request = AgentExecutionRequest(
            task="document",
            input="Test input",
            parameters={"key": "value"},
            optimize="cost"
        )

        assert request.task == "document"
        assert request.input == "Test input"
        assert request.optimize == "cost"

    def test_agent_execution_request_defaults(self):
        """Test agent execution request defaults"""
        request = AgentExecutionRequest(
            task="test",
            input="Input"
        )

        assert request.parameters == {}
        assert request.optimize == "cost"

    def test_agent_execution_request_optimization_values(self):
        """Test valid optimization values"""
        for optimize_val in ["cost", "speed", "quality"]:
            request = AgentExecutionRequest(
                task="test",
                input="Input",
                optimize=optimize_val
            )
            assert request.optimize == optimize_val

        # Invalid optimization value
        with pytest.raises(Exception):
            AgentExecutionRequest(
                task="test",
                input="Input",
                optimize="invalid"
            )


class TestAgentTierRestrictions:
    """Test tier restriction logic"""

    def test_kael_available_all_tiers(self):
        """Test Kael is available for all tiers"""
        kael = AGENT_REGISTRY["kael"]
        assert kael["tier_restriction"] is None

    def test_oracle_requires_pro(self):
        """Test Oracle requires pro tier"""
        oracle = AGENT_REGISTRY["oracle"]
        assert oracle["tier_restriction"] == "pro"

    def test_manus_requires_enterprise(self):
        """Test Manus requires enterprise tier"""
        manus = AGENT_REGISTRY["manus"]
        assert manus["tier_restriction"] == "enterprise"

    def test_kavach_requires_enterprise(self):
        """Test Kavach requires enterprise tier"""
        kavach = AGENT_REGISTRY["kavach"]
        assert kavach["tier_restriction"] == "enterprise"


class TestAgentSystemPrompts:
    """Test agent system prompts"""

    def test_kael_system_prompt_mentions_documentation(self):
        """Test Kael's system prompt is about documentation"""
        kael_prompt = AGENT_REGISTRY["kael"]["system_prompt"].lower()
        assert "documentation" in kael_prompt or "document" in kael_prompt
        assert "code" in kael_prompt

    def test_oracle_system_prompt_mentions_analysis(self):
        """Test Oracle's system prompt is about analysis"""
        oracle_prompt = AGENT_REGISTRY["oracle"]["system_prompt"].lower()
        assert "pattern" in oracle_prompt or "analysis" in oracle_prompt

    def test_shadow_system_prompt_mentions_deep_analysis(self):
        """Test Shadow's system prompt is about deep analysis"""
        shadow_prompt = AGENT_REGISTRY["shadow"]["system_prompt"].lower()
        assert "deep" in shadow_prompt or "hidden" in shadow_prompt
        assert "analysis" in shadow_prompt

    def test_kavach_system_prompt_mentions_security(self):
        """Test Kavach's system prompt is about security"""
        kavach_prompt = AGENT_REGISTRY["kavach"]["system_prompt"].lower()
        assert "security" in kavach_prompt or "protection" in kavach_prompt


class TestAgentTasks:
    """Test agent supported tasks"""

    def test_all_agents_have_tasks(self):
        """Test that all agents define supported tasks"""
        for agent_id, agent in AGENT_REGISTRY.items():
            assert len(agent["tasks"]) > 0, f"Agent {agent_id} has no tasks"

    def test_kael_supports_documentation_tasks(self):
        """Test Kael supports documentation tasks"""
        kael_tasks = AGENT_REGISTRY["kael"]["tasks"]
        assert "document" in kael_tasks
        assert "explain" in kael_tasks

    def test_oracle_supports_analysis_tasks(self):
        """Test Oracle supports analysis tasks"""
        oracle_tasks = AGENT_REGISTRY["oracle"]["tasks"]
        assert "analyze" in oracle_tasks
        assert "pattern" in oracle_tasks

    def test_agni_supports_transformation_tasks(self):
        """Test Agni supports data transformation tasks"""
        agni_tasks = AGENT_REGISTRY["agni"]["tasks"]
        assert "transform" in agni_tasks or "convert" in agni_tasks


class TestAgentUsageTracking:
    """Test usage tracking for agent executions"""

    @pytest.mark.asyncio
    async def test_usage_tracked_on_successful_execution(self):
        """Test that usage is tracked after successful execution"""
        request = AgentExecutionRequest(
            task="document",
            input="Test",
            optimize="cost"
        )

        user = {"id": "user_123", "tier": "pro", "email": "test@example.com"}

        with patch('backend.saas_agents.call_anthropic') as mock_call, \
             patch('backend.saas_agents.track_usage') as mock_track, \
             patch('backend.saas_agents.check_rate_limit'):

            mock_call.return_value = {
                "content": "Result",
                "usage": {"input_tokens": 50, "output_tokens": 100},
                "model": "claude-3-sonnet-20240229"
            }

            await execute_agent("kael", request, user)

            # Verify track_usage was called
            assert mock_track.called
            call_args = mock_track.call_args[0]
            assert call_args[0] == "user_123"  # user_id
            assert "tokens" in call_args[1]  # usage_data
            assert "cost_usd" in call_args[1]

    @pytest.mark.asyncio
    async def test_usage_not_tracked_on_failure(self):
        """Test that usage is not tracked when execution fails"""
        request = AgentExecutionRequest(
            task="document",
            input="Test",
            optimize="cost"
        )

        user = {"id": "user_123", "tier": "pro", "email": "test@example.com"}

        with patch('backend.saas_agents.call_anthropic') as mock_call, \
             patch('backend.saas_agents.track_usage') as mock_track, \
             patch('backend.saas_agents.check_rate_limit'):

            mock_call.side_effect = Exception("API Error")

            with pytest.raises(HTTPException):
                await execute_agent("kael", request, user)

            # Verify track_usage was NOT called
            assert not mock_track.called
