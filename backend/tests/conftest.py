"""
Pytest configuration and shared fixtures for backend tests.

Provides test fixtures for:
- FastAPI test client
- Database test session
- Mock authentication
- Environment variables
"""

import os
import sys
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Add backend to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


@pytest.fixture(scope="session")
def test_env() -> Generator[None, None, None]:
    """Set up test environment variables."""
    original_env = os.environ.copy()

    # Set test environment variables
    os.environ.update({
        "ENVIRONMENT": "test",
        "DISCORD_BOT_TOKEN": "test_token_123",
        "DISCORD_APPLICATION_ID": "123456789",
        "DISCORD_PUBLIC_KEY": "test_public_key",
        "ANTHROPIC_API_KEY": "test_anthropic_key",
        "OPENAI_API_KEY": "test_openai_key",
        "COHERE_API_KEY": "test_cohere_key",
        "DATABASE_URL": "sqlite:///test.db",
        "JWT_SECRET_KEY": "test_jwt_secret_key_for_testing_only",
        "ADMIN_PASSWORD": "test_admin_password",
        "ENABLE_MIDDLEWARE_COMPRESSION": "true",
    })

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def client(test_env: None) -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI application."""
    # Import here to ensure test environment is set up
    from backend.main import app

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def async_client(test_env: None) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client for the FastAPI application."""
    from backend.main import app

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_admin_token() -> str:
    """Generate a mock admin JWT token for testing."""
    return "mock_admin_token_for_testing"


@pytest.fixture
def mock_user_token() -> str:
    """Generate a mock user JWT token for testing."""
    return "mock_user_token_for_testing"


@pytest.fixture
def mock_auth_headers(mock_admin_token: str) -> dict[str, str]:
    """Create mock authentication headers."""
    return {
        "Authorization": f"Bearer {mock_admin_token}",
        "Content-Type": "application/json",
    }


@pytest.fixture(autouse=True)
def reset_test_state() -> Generator[None, None, None]:
    """Reset any shared state between tests."""
    yield
    # Add cleanup logic here if needed
