# Helix Backend Test Suite

Comprehensive test suite for the Helix Unified backend FastAPI application.

## Overview

This test suite provides coverage for:
- **Middleware** - GZIP compression, CORS, request handling
- **API Endpoints** - Health checks, authentication, core functionality
- **Authentication** - JWT tokens, admin access, protected routes
- **Integration** - App startup, concurrent requests, full stack testing

## Quick Start

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Run all tests
pytest

# Run with coverage report
pytest --cov=backend --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m critical      # Critical path tests only
pytest -m middleware    # Middleware tests only

# Run specific test file
pytest tests/unit/test_middleware.py

# Run with verbose output
pytest -v
```

## Test Organization

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_middleware.py   # Middleware tests (GZIP, CORS)
│   ├── test_health.py       # Health check endpoint tests
│   └── test_auth.py         # Authentication tests
├── integration/             # Integration tests for multiple components
│   └── test_app_startup.py  # App initialization tests
├── conftest.py              # Shared fixtures and configuration
└── README.md                # This file
```

## Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.unit` - Unit tests for isolated components
- `@pytest.mark.integration` - Tests for multiple components working together
- `@pytest.mark.critical` - Critical tests that must always pass
- `@pytest.mark.api` - API endpoint tests
- `@pytest.mark.middleware` - Middleware layer tests
- `@pytest.mark.auth` - Authentication/authorization tests
- `@pytest.mark.slow` - Tests that take significant time

## Critical Tests

### 🚨 GZIPMiddleware Import Test (REGRESSION PROTECTION)

**File:** `tests/unit/test_middleware.py::test_gzip_import_source`

This test prevents regression of the Railway deployment crash bug:
- **Issue:** FastAPI 0.115+ moved `GZIPMiddleware` from `fastapi.middleware.gzip` to `starlette.middleware.gzip`
- **Impact:** Incorrect import causes `ImportError` and Railway crash loops
- **Fix:** Import from `starlette.middleware.gzip` (backend/main.py:421)
- **Commit:** 87e0885 - Critical GZIPMiddleware fix

If this test fails, it means someone reverted to the old import path and **will break Railway deployment**.

### 🚨 App Startup Test

**File:** `tests/integration/test_app_startup.py::test_app_starts_successfully`

This test ensures the FastAPI app can start without errors:
- **Import errors** - Missing dependencies
- **Configuration errors** - Invalid environment variables
- **Middleware errors** - Middleware loading failures

If this test fails, **Railway deployment will crash on startup**.

## Test Fixtures

Available fixtures (from `conftest.py`):

- `test_env` - Sets up test environment variables
- `client` - FastAPI TestClient for synchronous tests
- `async_client` - AsyncClient for async endpoint tests
- `mock_admin_token` - Mock JWT token for admin access
- `mock_auth_headers` - Mock authentication headers

## Coverage Goals

Current coverage targets (configured in `pytest.ini`):
- **Minimum:** 60% coverage required
- **Target:** 80%+ coverage for production code
- **Critical paths:** 100% coverage (auth, middleware, core endpoints)

## Running Tests in CI/CD

### GitHub Actions Example

```yaml
- name: Run tests
  run: |
    pip install pytest pytest-asyncio pytest-cov httpx
    pytest --cov=backend --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

### Railway Deployment

Tests run automatically before deployment:
```bash
# In Railway build command
pytest -m critical || exit 1
```

## Writing New Tests

### Unit Test Template

```python
import pytest

@pytest.mark.unit
@pytest.mark.critical  # If critical path
def test_my_feature(client):
    """Test description here."""
    response = client.get("/my-endpoint")
    assert response.status_code == 200
    assert response.json() == {"expected": "data"}
```

### Integration Test Template

```python
import pytest

@pytest.mark.integration
async def test_my_integration(async_client):
    """Test multiple components together."""
    # Setup
    response1 = await async_client.post("/setup")
    assert response1.status_code == 200

    # Test integrated behavior
    response2 = await async_client.get("/result")
    assert response2.status_code == 200
```

## Common Issues

### Import Errors in Tests

If you get import errors when running tests:
```bash
# Add backend to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"
pytest
```

### Async Tests Not Running

Make sure `pytest-asyncio` is installed:
```bash
pip install pytest-asyncio
```

### Test Environment Variables

Tests use isolated test environment (see `conftest.py`).
Test data won't affect production environment.

## Continuous Improvement

This test suite should grow with the codebase:

- **Add tests for new features** before merging PRs
- **Maintain >80% coverage** for production code
- **Keep critical tests fast** (< 1 second each)
- **Document complex test scenarios** in test docstrings
- **Update this README** when adding new test categories

## Cross-Thread Coordination (MACS)

This test suite supports the Multi-Agent Coordination System (MACS):
- Tests validate fixes from all agent threads
- Regression tests prevent re-introducing bugs
- Critical tests ensure Railway deployment stability
- Test documentation aids cross-thread understanding

See `/docs/ninja-integration/SUPER_NINJA_MACS_UPDATE.md` for coordination status.

---

**Created:** 2025-12-13
**Last Updated:** 2025-12-13
**Maintainers:** All Helix contributors
**Coverage Target:** 80%+
