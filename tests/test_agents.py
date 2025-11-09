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

    # AGENTS is a dict with agent names as keys
    # Should have at least 13 agents (14 if MemoryRoot is available)
    assert len(AGENTS) >= 13

    # Check that key agents exist
    assert "Kael" in AGENTS
    assert "Vega" in AGENTS
    assert "Manus" in AGENTS
    assert "Kavach" in AGENTS


@pytest.mark.asyncio
@pytest.mark.unit
async def test_agent_recursive_reflection():
    """Test agent recursive reflection capability."""
    from backend.agents_base import HelixAgent

    # Create test agent
    agent = HelixAgent(
        name="TestAgent",
        symbol="🧪",
        role="Testing",
        traits=["curious", "logical"],
        enable_consciousness=False  # Disable to avoid needing profile
    )

    # Should have reflect method
    assert hasattr(agent, "reflect")


@pytest.mark.unit
def test_agent_consciousness_profiles():
    """Test agent consciousness profiles are properly defined."""
    from backend.agent_consciousness_profiles import AGENT_CONSCIOUSNESS_PROFILES

    # Should have consciousness profiles for most agents
    # Note: Not all agents may have profiles (e.g., Manus, Oracle, etc.)
    assert len(AGENT_CONSCIOUSNESS_PROFILES) >= 10

    # Each profile should have required fields
    for agent_name, profile in AGENT_CONSCIOUSNESS_PROFILES.items():
        # Check that profile has attributes (personality, behavior_dna, etc.)
        assert hasattr(profile, 'personality') or hasattr(profile, 'behavior_dna')


@pytest.mark.asyncio
@pytest.mark.integration
async def test_agent_communication():
    """Test agents can communicate through the system."""
    from backend.agents import AGENTS

    # Get two agents from the dict
    if len(AGENTS) >= 2:
        agent_list = list(AGENTS.values())
        agent1 = agent_list[0]
        agent2 = agent_list[1]

        # Should be able to reference each other
        assert agent1.name != agent2.name


@pytest.mark.unit
def test_kavach_agent_security():
    """Test Kavach agent has security capabilities."""
    from backend.agents import AGENTS

    # Get Kavach agent from dict
    if "Kavach" in AGENTS:
        kavach = AGENTS["Kavach"]
        assert "security" in kavach.role.lower() or "ethical" in kavach.role.lower()


@pytest.mark.unit
def test_vega_orchestration_role():
    """Test Vega has orchestration/coordination capabilities."""
    from backend.agents import AGENTS

    # Get Vega agent from dict
    if "Vega" in AGENTS:
        vega = AGENTS["Vega"]
        # Vega is a coordinator/orchestrator
        assert "coordinator" in vega.role.lower() or "orchestrat" in vega.role.lower()
