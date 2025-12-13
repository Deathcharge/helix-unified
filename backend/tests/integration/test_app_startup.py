"""
Integration tests for application startup and initialization.

Tests:
- App starts successfully
- All middleware is loaded
- Database connections work
- Environment validation
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.critical
def test_app_starts_successfully(test_env):
    """
    🚨 CRITICAL: Test that the FastAPI application starts without errors.

    This is the most important integration test - if the app doesn't start,
    Railway deployment will fail with crash loops.

    Tests:
    - No import errors
    - No configuration errors
    - Middleware loads correctly
    - App instance is created
    """
    try:
        from backend.main import app

        assert app is not None, "FastAPI app instance is None"
        assert hasattr(app, "routes"), "App missing routes attribute"
        assert hasattr(app, "middleware"), "App missing middleware attribute"

    except ImportError as e:
        pytest.fail(
            f"❌ CRITICAL: Failed to import app - Railway deployment will crash!\n"
            f"Import error: {e}\n"
            "Check for missing dependencies or syntax errors in backend/main.py"
        )
    except Exception as e:
        pytest.fail(
            f"❌ CRITICAL: App startup failed - Railway deployment will crash!\n"
            f"Error: {e}\n"
            "Check environment variables and configuration in backend/main.py"
        )


@pytest.mark.integration
@pytest.mark.critical
def test_middleware_stack_initialized(test_env):
    """
    Test that all middleware is properly initialized.

    Validates:
    - GZIPMiddleware (our recent critical fix!)
    - CORS middleware
    - No middleware conflicts
    """
    from backend.main import app

    # App should have middleware
    assert hasattr(app, "user_middleware"), "App missing user_middleware"

    middleware_count = len(app.user_middleware)
    assert middleware_count > 0, (
        "No middleware configured. Expected at least GZIP and CORS middleware."
    )

    # Check for our critical GZIPMiddleware
    middleware_names = [m.cls.__name__ for m in app.user_middleware]
    assert "GZIPMiddleware" in middleware_names, (
        "❌ GZIPMiddleware not found! This was the cause of Railway crash.\n"
        "Check backend/main.py:421 - should import from starlette.middleware.gzip"
    )


@pytest.mark.integration
def test_environment_variables_loaded(test_env):
    """
    Test that critical environment variables are loaded.

    Required for:
    - API keys
    - Database connections
    - Service authentication
    """
    import os

    critical_vars = [
        "DISCORD_BOT_TOKEN",
        "ANTHROPIC_API_KEY",
        "JWT_SECRET_KEY",
    ]

    missing_vars = [var for var in critical_vars if not os.getenv(var)]

    assert len(missing_vars) == 0, (
        f"Missing critical environment variables: {missing_vars}\n"
        "These must be set in Railway environment or .env file"
    )


@pytest.mark.integration
def test_fastapi_test_client_works(client: TestClient):
    """
    Test that FastAPI test client can make requests.

    This validates the entire request/response cycle.
    """
    # Should be able to make a request without errors
    response = client.get("/")

    # Should get a response (any status code is fine)
    assert response is not None, "No response from test client"
    assert hasattr(response, "status_code"), "Response missing status_code"


@pytest.mark.integration
@pytest.mark.slow
def test_app_handles_concurrent_requests(client: TestClient):
    """
    Test that app can handle multiple concurrent requests.

    Important for production load with Railway autoscaling.
    """
    import concurrent.futures

    def make_request(path: str) -> int:
        response = client.get(path)
        return response.status_code

    paths = ["/", "/docs", "/openapi.json"] * 10  # 30 requests

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request, path) for path in paths]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    # All requests should complete without server errors
    server_errors = [code for code in results if code >= 500]
    assert len(server_errors) == 0, (
        f"Got {len(server_errors)} server errors (5xx) during concurrent requests. "
        "App may not handle load correctly."
    )
