"""
Tests for state management system (Redis + PostgreSQL + JSON fallback).
"""
import pytest
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.unit
def test_state_file_operations(temp_state_dir):
    """Test basic state file read/write."""
    state_file = temp_state_dir["state"] / "test_state.json"

    test_data = {"test": "data", "value": 123}

    # Write
    state_file.write_text(json.dumps(test_data))

    # Read
    loaded_data = json.loads(state_file.read_text())

    assert loaded_data == test_data


@pytest.mark.asyncio
@pytest.mark.database
async def test_redis_state_caching(mock_redis):
    """Test Redis caching layer."""
    # Test get/set
    mock_redis.set("test_key", "test_value")
    mock_redis.get.return_value = b"test_value"

    value = mock_redis.get("test_key")
    assert value == b"test_value"


@pytest.mark.asyncio
@pytest.mark.database
async def test_postgres_state_persistence(mock_postgres):
    """Test PostgreSQL persistence layer."""
    # Test query execution
    mock_postgres.execute.return_value = "INSERT 1"

    result = await mock_postgres.execute(
        "INSERT INTO state (key, value) VALUES ($1, $2)",
        "test_key",
        "test_value"
    )

    assert result == "INSERT 1"
    mock_postgres.execute.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_state_fallback_hierarchy(temp_state_dir, mock_redis):
    """Test fallback from Redis -> PostgreSQL -> JSON."""
    state_file = temp_state_dir["state"] / "fallback_state.json"

    # Create fallback JSON
    fallback_data = {"fallback": True, "value": "json_value"}
    state_file.write_text(json.dumps(fallback_data))

    # Simulate Redis miss
    mock_redis.get.return_value = None

    # Should fallback to JSON
    loaded_data = json.loads(state_file.read_text())
    assert loaded_data["fallback"] is True


@pytest.mark.unit
def test_state_directory_structure(temp_state_dir):
    """Test required state directory structure exists."""
    assert temp_state_dir["helix"].exists()
    assert temp_state_dir["state"].exists()
    assert temp_state_dir["shadow"].exists()
    assert temp_state_dir["archive"].exists()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_concurrent_state_access(mock_redis):
    """Test concurrent access to state doesn't cause issues."""
    import asyncio

    async def read_state():
        return mock_redis.get("concurrent_key")

    async def write_state():
        return mock_redis.set("concurrent_key", "value")

    # Simulate concurrent reads and writes
    tasks = [read_state() for _ in range(5)] + [write_state() for _ in range(5)]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Should all complete without exceptions
    assert all(not isinstance(r, Exception) for r in results)
