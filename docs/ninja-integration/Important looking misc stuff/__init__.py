"""
Test suite for Helix Unified system
"""
import asyncio
import os
import sys
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def mock_discord_client():
    """Mock Discord client for testing"""
    client = Mock()
    client.user = Mock(id=12345, name="TestBot")
    client.guilds = [Mock(id=67890, name="TestGuild")]
    return client

@pytest.fixture
def mock_agent():
    """Mock agent for testing"""
    agent = Mock()
    agent.id = "agent_001"
    agent.name = "TestAgent"
    agent.personality = "friendly"
    agent.is_active = True
    return agent

@pytest.fixture
async def mock_voice_system():
    """Mock voice system for testing"""
    voice_system = Mock()
    voice_system.is_connected = True
    voice_system.current_channel = Mock(id=11111, name="test-voice")
    return voice_system

@pytest.fixture
def event_loop():
    """Create an event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()