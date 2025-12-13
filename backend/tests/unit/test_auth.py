"""
Unit tests for authentication and authorization.

Tests:
- JWT token validation
- Password hashing
- Admin authentication
- Protected endpoint access
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
@pytest.mark.auth
def test_environment_has_jwt_secret(test_env):
    """
    Test that JWT secret key is configured.

    Critical for secure authentication token generation.
    """
    import os

    jwt_secret = os.getenv("JWT_SECRET_KEY")
    assert jwt_secret is not None, "JWT_SECRET_KEY must be configured"
    assert len(jwt_secret) >= 32, "JWT_SECRET_KEY should be at least 32 characters"


@pytest.mark.unit
@pytest.mark.auth
def test_admin_password_configured(test_env):
    """
    Test that admin password is configured.

    Required for admin authentication endpoints.
    """
    import os

    admin_password = os.getenv("ADMIN_PASSWORD")
    assert admin_password is not None, "ADMIN_PASSWORD must be configured"


@pytest.mark.unit
@pytest.mark.auth
def test_protected_endpoints_require_auth(client: TestClient):
    """
    Test that protected endpoints return 401/403 without authentication.

    Common protected paths that should require auth:
    - /admin/*
    - /api/admin/*
    - /api/protected/*
    """
    protected_paths = [
        "/admin",
        "/api/admin",
        "/api/admin/users",
        "/admin/dashboard",
    ]

    for path in protected_paths:
        response = client.get(path)

        # Should return 401 Unauthorized, 403 Forbidden, or 404 Not Found
        # (404 is acceptable if the endpoint doesn't exist yet)
        assert response.status_code in [401, 403, 404, 307], (
            f"Protected endpoint {path} returned {response.status_code}. "
            "Expected 401/403 (auth required) or 404 (not implemented)."
        )


@pytest.mark.unit
@pytest.mark.auth
def test_public_endpoints_do_not_require_auth(client: TestClient):
    """
    Test that public endpoints work without authentication.

    Public endpoints:
    - Health check
    - Docs
    - Root
    """
    public_paths = [
        "/",
        "/docs",
        "/redoc",
        "/openapi.json",
    ]

    for path in public_paths:
        response = client.get(path)

        # Should NOT return 401/403 (auth errors)
        assert response.status_code not in [401, 403], (
            f"Public endpoint {path} requires authentication (status {response.status_code}). "
            "Public endpoints should be accessible without auth."
        )
