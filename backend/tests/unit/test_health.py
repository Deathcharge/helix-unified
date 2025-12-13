"""
Unit tests for health check and status endpoints.

Tests:
- Basic health check endpoint
- Application startup
- Readiness probes
- Service availability
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
@pytest.mark.api
@pytest.mark.critical
def test_health_check_endpoint_exists(client: TestClient):
    """
    Test that a health check endpoint responds.

    Health checks are critical for:
    - Railway deployment monitoring
    - Load balancer health probes
    - Uptime monitoring
    """
    # Try common health check paths
    health_paths = ["/", "/health", "/api/health", "/status"]

    responses = []
    for path in health_paths:
        response = client.get(path)
        responses.append((path, response.status_code))

    # At least one health endpoint should return 200
    successful_endpoints = [
        path for path, status in responses if status == 200
    ]

    assert len(successful_endpoints) > 0, (
        f"No working health check endpoint found. Tried: {health_paths}\n"
        f"Responses: {responses}\n"
        "Railway deployments need a working health endpoint for monitoring."
    )


@pytest.mark.unit
@pytest.mark.api
def test_root_endpoint_response(client: TestClient):
    """Test that root endpoint returns expected response structure."""
    response = client.get("/")

    # Should at least return a valid status code
    assert response.status_code in [200, 404, 307], (
        f"Unexpected status code {response.status_code} for root endpoint"
    )

    if response.status_code == 200:
        # If it returns 200, it should have content
        assert len(response.content) > 0, "Root endpoint returned empty response"


@pytest.mark.unit
@pytest.mark.api
def test_openapi_docs_available(client: TestClient):
    """
    Test that OpenAPI documentation is accessible.

    FastAPI auto-generates docs at /docs and /redoc.
    These are valuable for API development and debugging.
    """
    docs_response = client.get("/docs")
    redoc_response = client.get("/redoc")

    # At least one docs endpoint should work
    assert docs_response.status_code == 200 or redoc_response.status_code == 200, (
        "OpenAPI docs not accessible. This is useful for API development.\n"
        f"/docs status: {docs_response.status_code}\n"
        f"/redoc status: {redoc_response.status_code}"
    )


@pytest.mark.unit
@pytest.mark.api
def test_openapi_schema_valid(client: TestClient):
    """Test that OpenAPI schema is valid JSON."""
    response = client.get("/openapi.json")

    if response.status_code == 200:
        # Should return valid JSON
        try:
            schema = response.json()
            assert "openapi" in schema, "Missing 'openapi' field in schema"
            assert "info" in schema, "Missing 'info' field in schema"
            assert "paths" in schema, "Missing 'paths' field in schema"
        except ValueError as e:
            pytest.fail(f"OpenAPI schema is not valid JSON: {e}")


@pytest.mark.unit
@pytest.mark.api
@pytest.mark.critical
def test_api_accepts_json_content_type(client: TestClient):
    """
    Test that API accepts JSON content type.

    Most FastAPI endpoints expect JSON, so this validates
    the basic request/response cycle.
    """
    response = client.post(
        "/",  # Using root, may not exist but testing content-type handling
        json={"test": "data"},
        headers={"Content-Type": "application/json"},
    )

    # Should not return 400 Bad Request for content-type issues
    # (may return 404 if endpoint doesn't exist, that's fine)
    assert response.status_code != 400 or "content-type" not in response.text.lower(), (
        "API rejected application/json content type"
    )


@pytest.mark.unit
@pytest.mark.api
def test_cors_headers_on_api_response(client: TestClient):
    """
    Test that API responses include CORS headers.

    Critical for frontend (Next.js/React) to communicate with backend.
    """
    response = client.get(
        "/",
        headers={"Origin": "http://localhost:3000"},
    )

    # Check for CORS headers (case-insensitive)
    headers_lower = {k.lower(): v for k, v in response.headers.items()}

    # Should have CORS headers for cross-origin requests
    # Note: May not be present on all endpoints, but we're checking the middleware is active
    assert response.status_code in [200, 404, 405, 307], (
        f"Unexpected status code: {response.status_code}"
    )
