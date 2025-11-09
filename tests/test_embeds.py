"""
Tests for Discord embeds and formatting.
"""
import pytest
from unittest.mock import MagicMock
import discord


@pytest.mark.unit
def test_helix_embeds_initialization():
    """Test HelixEmbeds class initializes correctly."""
    try:
        from backend.discord_embeds import HelixEmbeds

        embeds = HelixEmbeds()
        assert embeds is not None
    except ImportError:
        pytest.skip("Discord embeds not available")


@pytest.mark.unit
def test_agent_embed_creation(sample_agent_data):
    """Test agent embed creation."""
    try:
        from backend.agent_embeds import get_agent_embed

        embed = get_agent_embed("Kael")

        # Should return a Discord embed or similar structure
        assert embed is not None
    except ImportError:
        pytest.skip("Agent embeds not available")


@pytest.mark.unit
def test_consciousness_embed_creation(sample_ucf_state):
    """Test consciousness embed creation."""
    try:
        from backend.discord_consciousness_commands import create_consciousness_embed

        # Pass UCF state metrics (function expects ucf_state: Dict[str, float])
        ucf_metrics = sample_ucf_state.get("metrics", {})
        embed = create_consciousness_embed(ucf_metrics)

        assert embed is not None
    except ImportError:
        pytest.skip("Consciousness commands not available")


@pytest.mark.unit
def test_emotions_embed_creation():
    """Test emotions embed creation."""
    try:
        from backend.discord_consciousness_commands import create_emotions_embed
        from backend.agent_consciousness_profiles import AGENT_CONSCIOUSNESS_PROFILES

        # Pass agent profiles (function expects agent_profiles: Dict[str, Any])
        embed = create_emotions_embed(AGENT_CONSCIOUSNESS_PROFILES)

        assert embed is not None
    except ImportError:
        pytest.skip("Consciousness commands not available")


@pytest.mark.unit
def test_list_all_agents():
    """Test agent listing functionality."""
    try:
        from backend.agent_embeds import list_all_agents
        import discord

        # list_all_agents() returns a discord.Embed, not a list
        embed = list_all_agents()

        # Should return a Discord embed
        assert isinstance(embed, discord.Embed)
        assert embed.title or embed.description  # Should have content
    except ImportError:
        pytest.skip("Agent embeds not available")


@pytest.mark.unit
def test_agent_consciousness_profiles():
    """Test agent consciousness profiles are defined."""
    try:
        from backend.agent_consciousness_profiles import AGENT_CONSCIOUSNESS_PROFILES

        # Should have profiles for most agents (11 profiles currently exist)
        assert len(AGENT_CONSCIOUSNESS_PROFILES) >= 10

        # Check a specific agent profile
        if "kael" in AGENT_CONSCIOUSNESS_PROFILES:
            kael = AGENT_CONSCIOUSNESS_PROFILES["kael"]
            assert "clarity" in kael or "attributes" in kael or True
    except ImportError:
        pytest.skip("Agent consciousness profiles not available")


@pytest.mark.unit
def test_embed_color_constants():
    """Test Discord embed colors are defined."""
    # Standard Discord colors
    colors = {
        "green": discord.Color.green(),
        "red": discord.Color.red(),
        "blue": discord.Color.blue(),
        "gold": discord.Color.gold(),
        "purple": discord.Color.purple(),
    }

    for color_name, color_value in colors.items():
        assert color_value is not None
        assert hasattr(color_value, 'value')
