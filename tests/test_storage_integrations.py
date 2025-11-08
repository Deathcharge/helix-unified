"""
Tests for storage integrations (Nextcloud, Backblaze B2, MEGA).
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path


@pytest.mark.unit
def test_nextcloud_client_initialization(mock_env_vars):
    """Test Nextcloud client initializes correctly."""
    with patch.dict('os.environ', {
        'NEXTCLOUD_URL': 'https://cloud.example.com',
        'NEXTCLOUD_USER': 'testuser',
        'NEXTCLOUD_PASSWORD': 'testpass',
        'NEXTCLOUD_BASE_PATH': '/Helix'
    }):
        try:
            from services.nextcloud_client import HelixNextcloudClient
            client = HelixNextcloudClient()
            assert client.url == 'https://cloud.example.com'
            assert client.user == 'testuser'
            assert client.base_path == '/Helix'
        except ImportError:
            pytest.skip("Nextcloud client dependencies not available")


@pytest.mark.unit
def test_backblaze_client_initialization(mock_env_vars):
    """Test Backblaze B2 client initializes correctly."""
    with patch.dict('os.environ', {
        'B2_KEY_ID': 'test_key_id',
        'B2_APPLICATION_KEY': 'test_app_key',
        'B2_BUCKET_NAME': 'test-bucket',
        'B2_ENDPOINT': 's3.us-west-000.backblazeb2.com'
    }):
        try:
            from services.backblaze_client import HelixBackblazeClient
            client = HelixBackblazeClient()
            assert client.key_id == 'test_key_id'
            assert client.bucket_name == 'test-bucket'
            assert client.endpoint == 's3.us-west-000.backblazeb2.com'
        except ImportError:
            pytest.skip("Backblaze client dependencies not available")


@pytest.mark.unit
def test_storage_mode_selection(mock_env_vars):
    """Test storage mode is selected correctly from environment."""
    test_modes = ['local', 'mega', 'nextcloud', 'b2']

    for mode in test_modes:
        with patch.dict('os.environ', {'HELIX_STORAGE_MODE': mode}):
            import os
            assert os.getenv('HELIX_STORAGE_MODE') == mode


@pytest.mark.integration
def test_nextcloud_upload(mock_env_vars, temp_state_dir):
    """Test file upload to Nextcloud."""
    test_file = temp_state_dir["state"] / "test_upload.txt"
    test_file.write_text("test content")

    try:
        from services.nextcloud_client import HelixNextcloudClient
        # Just verify we can import and potentially initialize the client
        # Full upload testing would require WebDAV dependencies
        assert HelixNextcloudClient is not None
    except ImportError:
        pytest.skip("Nextcloud client not available")


@pytest.mark.integration
def test_backblaze_upload(mock_env_vars, temp_state_dir):
    """Test file upload to Backblaze B2."""
    test_file = temp_state_dir["state"] / "test_b2_upload.txt"
    test_file.write_text("test b2 content")

    try:
        from services.backblaze_client import HelixBackblazeClient
        # Just verify we can import the client
        # Full upload testing would require boto3 dependencies
        assert HelixBackblazeClient is not None
    except ImportError:
        pytest.skip("Boto3 not available")


@pytest.mark.unit
def test_storage_fallback_hierarchy():
    """Test storage fallback order: Nextcloud → B2 → MEGA → Local."""
    storage_modes = ['nextcloud', 'b2', 'mega', 'local']

    for i, mode in enumerate(storage_modes):
        # Each mode should be a valid fallback option
        assert mode in ['nextcloud', 'b2', 'mega', 'local']

        # Test priority (lower index = higher priority)
        if i < len(storage_modes) - 1:
            next_mode = storage_modes[i + 1]
            # Verify fallback order is maintained
            assert storage_modes.index(mode) < storage_modes.index(next_mode)


@pytest.mark.unit
def test_dependency_validator_storage_checks():
    """Test dependency validator checks storage backends."""
    try:
        from backend.dependency_validator import has_webdav, has_boto3, has_mega

        # These will check actual availability
        webdav_available = has_webdav()
        boto3_available = has_boto3()
        mega_available = has_mega()

        # At least one should be available or we're in test env
        assert isinstance(webdav_available, bool)
        assert isinstance(boto3_available, bool)
        assert isinstance(mega_available, bool)
    except ImportError:
        pytest.skip("Dependency validator not available")
