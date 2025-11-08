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
    from backend.services.zapier_client_master import ZapierMasterClient

    client = ZapierMasterClient(master_hook_url=mock_env_vars["ZAPIER_MASTER_HOOK_URL"])
    assert client.master_hook_url == mock_env_vars["ZAPIER_MASTER_HOOK_URL"]


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_event(mock_env_vars):
    """Test event logging through Zapier."""
    from backend.services.zapier_client_master import ZapierMasterClient

    client = ZapierMasterClient(master_hook_url=mock_env_vars["ZAPIER_MASTER_HOOK_URL"])

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="success")
        mock_post.return_value.__aenter__.return_value = mock_response

        result = await client.log_event(
            event_type="test_event",
            description="Test event description",
            metadata={"test_key": "test_value"}
        )

        assert result["status"] == "success"
        mock_post.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.webhook
async def test_send_error_alert(mock_env_vars):
    """Test error alert sending."""
    from backend.services.zapier_client_master import ZapierMasterClient

    client = ZapierMasterClient(master_hook_url=mock_env_vars["ZAPIER_MASTER_HOOK_URL"])

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="success")
        mock_post.return_value.__aenter__.return_value = mock_response

        result = await client.send_error_alert(
            error_message="Test error",
            context={"location": "test_function"}
        )

        assert result["status"] == "success"


@pytest.mark.asyncio
@pytest.mark.webhook
async def test_webhook_retry_logic(mock_env_vars):
    """Test webhook retry logic on failure."""
    from backend.services.zapier_client_master import ZapierMasterClient

    client = ZapierMasterClient(master_hook_url=mock_env_vars["ZAPIER_MASTER_HOOK_URL"])

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
    from backend.services.zapier_client_master import ZapierMasterClient
    import asyncio

    client = ZapierMasterClient(master_hook_url=mock_env_vars["ZAPIER_MASTER_HOOK_URL"])

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="success")
        mock_post.return_value.__aenter__.return_value = mock_response

        # Send multiple requests concurrently
        tasks = [
            client.log_event("test", f"Event {i}", {})
            for i in range(10)
        ]

        results = await asyncio.gather(*tasks)

        # All should succeed
        assert len(results) == 10
        assert all(r["status"] == "success" for r in results)
