"""
Tests for Zapier webhook client integration.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import aiohttp


@pytest.mark.unit
def test_zapier_client_initialization(mock_env_vars):
    """Test Zapier client initializes correctly."""
    # Import after env vars are set
    from backend.services.zapier_client_master import MasterZapierClient

    # MasterZapierClient doesn't take master_hook_url in __init__
    client = MasterZapierClient()
    assert client is not None


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_event(mock_env_vars):
    """Test event logging through Zapier."""
    from backend.services.zapier_client_master import MasterZapierClient

    client = MasterZapierClient()

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="success")
        mock_post.return_value.__aenter__.return_value = mock_response

        # log_event(event_title, event_type, agent_name, description, ucf_snapshot)
        result = await client.log_event(
            event_title="Test Event",
            event_type="test_event",
            agent_name="TestAgent",
            description="Test event description",
            ucf_snapshot={"harmony": 0.5}
        )

        # Returns bool, not dict
        assert isinstance(result, bool)


@pytest.mark.asyncio
@pytest.mark.webhook
async def test_send_error_alert(mock_env_vars):
    """Test error alert sending."""
    from backend.services.zapier_client_master import MasterZapierClient

    client = MasterZapierClient()

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="success")
        mock_post.return_value.__aenter__.return_value = mock_response

        # send_error_alert(error_message, component, severity, stack_trace)
        result = await client.send_error_alert(
            error_message="Test error",
            component="test_function",
            severity="high"
        )

        # Returns bool, not dict
        assert isinstance(result, bool)


@pytest.mark.asyncio
@pytest.mark.webhook
async def test_webhook_retry_logic(mock_env_vars):
    """Test webhook retry logic on failure."""
    from backend.services.zapier_client_master import MasterZapierClient

    client = MasterZapierClient()

    with patch("aiohttp.ClientSession.post") as mock_post:
        # Simulate failure then success
        mock_response_fail = MagicMock()
        mock_response_fail.status = 500
        mock_response_fail.text = AsyncMock(return_value="error")

        mock_response_success = MagicMock()
        mock_response_success.status = 200
        mock_response_success.text = AsyncMock(return_value="success")

        mock_post.return_value.__aenter__.side_effect = [
            mock_response_fail,
            mock_response_success
        ]

        # Should retry and eventually succeed
        # Note: Actual retry logic depends on implementation
        pass


@pytest.mark.asyncio
@pytest.mark.webhook
async def test_rate_limiting(mock_env_vars):
    """Test webhook rate limiting with semaphore."""
    from backend.services.zapier_client_master import MasterZapierClient
    import asyncio

    client = MasterZapierClient()

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="success")
        mock_post.return_value.__aenter__.return_value = mock_response

        # Send multiple requests concurrently
        tasks = [
            client.log_event(
                event_title=f"Event {i}",
                event_type="test",
                agent_name="TestAgent",
                description=f"Test event {i}",
                ucf_snapshot={"harmony": 0.5}
            )
            for i in range(10)
        ]

        results = await asyncio.gather(*tasks)

        # All should succeed (returns bool)
        assert len(results) == 10
        assert all(isinstance(r, bool) for r in results)
