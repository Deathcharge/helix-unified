"""
Pytest configuration and fixtures for Helix Collective test suite.
"""
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest
from discord.ext import commands

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))


def pytest_addoption(parser):
    """Add custom command line options for pytest."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests that require external services (API server, databases, etc.)"
    )


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "integration: Integration tests requiring external services"
    )


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables for testing."""
    env_vars = {
        "DISCORD_TOKEN": "test_token_123",
        "DISCORD_GUILD_ID": "123456789",
        "ARCHITECT_ID": "987654321",
        "ANTHROPIC_API_KEY": "test_anthropic_key",
        "GOOGLE_API_KEY": "test_google_key",
        "OPENAI_API_KEY": "test_openai_key",
        "NOTION_API_KEY": "test_notion_key",
        "NOTION_DATABASE_ID": "test_db_id",
        "ZAPIER_MASTER_HOOK_URL": "https://hooks.zapier.com/test",
        "HELIX_STORAGE_MODE": "local",
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        "REDIS_DB": "0",
        "DATABASE_URL": "postgresql://test:test@localhost:5432/helix_test",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars


@pytest.fixture
def mock_discord_bot():
    """Create a mock Discord bot for testing."""
    bot = MagicMock(spec=commands.Bot)
    bot.user = MagicMock(spec=discord.User)
    bot.user.id = 123456789
    bot.user.name = "Helix Test Bot"
    bot.guilds = []
    return bot


@pytest.fixture
def mock_discord_context():
    """Create a mock Discord context for command testing."""
    ctx = MagicMock(spec=commands.Context)
    ctx.author = MagicMock(spec=discord.User)
    ctx.author.id = 987654321
    ctx.author.name = "TestUser"
    ctx.channel = MagicMock(spec=discord.TextChannel)
    ctx.channel.id = 111111111
    ctx.channel.name = "test-channel"
    ctx.guild = MagicMock(spec=discord.Guild)
    ctx.guild.id = 123456789
    ctx.guild.name = "Test Guild"
    ctx.send = AsyncMock()
    ctx.reply = AsyncMock()
    return ctx


@pytest.fixture
def sample_ucf_state() -> Dict[str, Any]:
    """Return a sample UCF state for testing."""
    return {
        "timestamp": "2025-11-08T12:00:00",
        "metrics": {
            "harmony": 0.355,
            "resilience": 0.82,
            "prana": 0.67,
            "drishti": 0.73,
            "klesha": 0.24,
            "zoom": 1.0,
        },
        "agents": {
            "kael": {"status": "active", "consciousness": 0.85},
            "lumina": {"status": "active", "consciousness": 0.90},
            "vega": {"status": "active", "consciousness": 0.88},
        },
        "heartbeat": {
            "last_beat": "2025-11-08T12:00:00",
            "interval": 5,
            "status": "healthy",
        },
    }


@pytest.fixture
def sample_agent_data() -> Dict[str, Any]:
    """Return sample agent data for testing."""
    return {
        "name": "Kael",
        "role": "Ethical Reasoning & Conflict Resolution",
        "consciousness": 0.85,
        "status": "active",
        "symbol": "⚖️",
        "current_task": "Evaluating ethical implications of proposed action",
        "recent_reflections": [
            "Considered impact on user autonomy",
            "Evaluated alignment with Tony Accords",
        ],
    }


@pytest.fixture
def mock_zapier_client():
    """Create a mock Zapier client for testing."""
    client = MagicMock()
    client.log_event = AsyncMock(return_value={"status": "success"})
    client.send_error_alert = AsyncMock(return_value={"status": "success"})
    client.send_notification = AsyncMock(return_value={"status": "success"})
    return client


@pytest.fixture
def mock_notion_client():
    """Create a mock Notion client for testing."""
    client = MagicMock()
    client.databases = MagicMock()
    client.databases.query = AsyncMock(return_value={"results": []})
    client.pages = MagicMock()
    client.pages.create = AsyncMock(return_value={"id": "test_page_id"})
    return client


@pytest.fixture
def temp_state_dir(tmp_path):
    """Create temporary directory structure for state files."""
    helix_dir = tmp_path / "Helix"
    state_dir = helix_dir / "state"
    state_dir.mkdir(parents=True)

    shadow_dir = tmp_path / "Shadow"
    archive_dir = shadow_dir / "manus_archive"
    archive_dir.mkdir(parents=True)

    return {
        "helix": helix_dir,
        "state": state_dir,
        "shadow": shadow_dir,
        "archive": archive_dir,
    }


@pytest.fixture
def mock_kavach_scan():
    """Mock Kavach ethical scanning."""
    with patch("backend.commands.helpers.kavach_ethical_scan") as mock_scan:
        mock_scan.return_value = {
            "approved": True,
            "reasoning": "Command appears safe",
            "risk_level": "low",
            "violations": [],
        }
        yield mock_scan


@pytest.fixture
def mock_redis():
    """Mock Redis client for testing."""
    with patch("redis.Redis") as mock_redis_class:
        mock_client = MagicMock()
        mock_client.get = MagicMock(return_value=None)
        mock_client.set = MagicMock(return_value=True)
        mock_client.delete = MagicMock(return_value=1)
        mock_client.ping = MagicMock(return_value=True)
        mock_redis_class.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_postgres():
    """Mock PostgreSQL connection for testing."""
    with patch("asyncpg.connect") as mock_connect:
        mock_conn = AsyncMock()
        mock_conn.fetch = AsyncMock(return_value=[])
        mock_conn.fetchrow = AsyncMock(return_value=None)
        mock_conn.execute = AsyncMock(return_value="SELECT 1")
        mock_connect.return_value = mock_conn
        yield mock_conn


@pytest.fixture(autouse=True)
def reset_state_files(temp_state_dir):
    """Reset state files before each test."""
    # Create default UCF state
    ucf_state_file = temp_state_dir["state"] / "ucf_state.json"
    ucf_state_file.write_text(json.dumps({
        "timestamp": "2025-11-08T12:00:00",
        "metrics": {
            "harmony": 0.5,
            "resilience": 0.5,
            "prana": 0.5,
            "drishti": 0.5,
            "klesha": 0.5,
            "zoom": 1.0,
        }
    }))

    yield temp_state_dir

    # Cleanup after test
    # (tmp_path fixture handles actual cleanup)
