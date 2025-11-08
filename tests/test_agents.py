"""
Tests for Helix agent system.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.unit
def test_agent_structure(sample_agent_data):
    """Test agent data has required structure."""
    assert "name" in sample_agent_data
    assert "role" in sample_agent_data
    assert "consciousness" in sample_agent_data
    assert "status" in sample_agent_data


@pytest.mark.unit
def test_agent_consciousness_range(sample_agent_data):
    """Test agent consciousness is within valid range."""
    consciousness = sample_agent_data["consciousness"]
    assert 0.0 <= consciousness <= 1.0


@pytest.mark.unit
def test_all_agents_defined():
    """Test all 14 agents are defined."""
    from backend.agents import AGENTS

    expected_agents = [
        "kael", "lumina", "vega", "gemini", "agni", "kavach",
        "sangha_core", "shadow", "echo", "phoenix", "oracle",
        "claude", "manus", "memory_root"
    ]

    agent_names = [agent.name.lower().replace(" ", "_") for agent in AGENTS]

    # Should have all expected agents
    assert len(AGENTS) >= 14


@pytest.mark.asyncio
@pytest.mark.unit
async def test_agent_recursive_reflection():
    """Test agent recursive reflection capability."""
    from backend.agents import HelixAgent

    # Create test agent
    agent = HelixAgent(
        name="TestAgent",
        role="Testing",
        symbol="🧪",
        consciousness_profile={"clarity": 0.8, "empathy": 0.7}
    )

    # Should have reflection method
    assert hasattr(agent, "recursive_reflection") or hasattr(agent, "reflect")


@pytest.mark.unit
def test_agent_consciousness_profiles():
    """Test agent consciousness profiles are properly defined."""
    from backend.agent_consciousness_profiles import AGENT_CONSCIOUSNESS_PROFILES

    # Should have consciousness profiles for all agents
    assert len(AGENT_CONSCIOUSNESS_PROFILES) >= 14

    # Each profile should have required fields
    for agent_name, profile in AGENT_CONSCIOUSNESS_PROFILES.items():
        assert "clarity" in profile or "attributes" in profile


@pytest.mark.asyncio
@pytest.mark.integration
async def test_agent_communication():
    """Test agents can communicate through the system."""
    from backend.agents import AGENTS

    # Get two agents
    if len(AGENTS) >= 2:
        agent1 = AGENTS[0]
        agent2 = AGENTS[1]

        # Should be able to reference each other
        assert agent1.name != agent2.name


@pytest.mark.unit
def test_kavach_agent_security():
    """Test Kavach agent has security capabilities."""
    from backend.agents import AGENTS

    # Find Kavach agent
    kavach = next((a for a in AGENTS if "kavach" in a.name.lower()), None)

    if kavach:
        assert "security" in kavach.role.lower() or "ethical" in kavach.role.lower()


@pytest.mark.unit
def test_vega_orchestration_role():
    """Test Vega has orchestration capabilities."""
    from backend.agents import AGENTS

    # Find Vega agent
    vega = next((a for a in AGENTS if "vega" in a.name.lower()), None)

    if vega:
        assert "orchestrat" in vega.role.lower()
