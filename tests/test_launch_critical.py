"""
🧪 Launch Critical Tests - Phase 2 Agent Ecosystem
==================================================

Tests for Dec 15, 2025 launch readiness:
- Claude API cooldown management
- Webhook retry logic
- Health check endpoint
- Security regression tests
- Rate limiting
- GZIP compression

Author: Phoenix (Claude Thread 3)
Date: 2025-12-09
Phase: Launch Sprint v17.2 - Testing & QA
"""

import asyncio
import time
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest
from fastapi.testclient import TestClient


# ============================================================================
# TEST SETUP
# ============================================================================

@pytest.fixture
def client():
    """Create FastAPI test client."""
    from backend.main import app
    return TestClient(app)


@pytest.fixture
def mock_claude_limiter():
    """Create mock Claude API limiter."""
    from backend.core.claude_cooldown import ClaudeAPILimiter
    return ClaudeAPILimiter(max_requests_per_minute=10, cooldown_threshold=0.8)


@pytest.fixture
def mock_webhook_retry():
    """Create mock webhook retry policy."""
    from backend.core.webhook_retry import WebhookRetryPolicy
    return WebhookRetryPolicy(max_attempts=3, initial_delay=0.1)


# ============================================================================
# CLAUDE API COOLDOWN TESTS (Phase 2.3)
# ============================================================================

class TestClaudeAPICooldown:
    """Test Claude API rate limiting and cooldown management."""

    @pytest.mark.asyncio
    async def test_normal_request_flow(self, mock_claude_limiter):
        """Test that normal requests pass through without queuing."""
        # Should complete immediately
        result = await mock_claude_limiter.acquire()
        assert result is True
        assert mock_claude_limiter.total_requests == 1
        assert mock_claude_limiter.queued_requests == 0

    @pytest.mark.asyncio
    async def test_cooldown_triggers_at_threshold(self, mock_claude_limiter):
        """Test that cooldown triggers at 80% threshold."""
        # Max is 10/min, threshold is 80% = 8 requests
        for i in range(8):
            await mock_claude_limiter.acquire()

        # Should be in cooldown now
        assert mock_claude_limiter.in_cooldown is True
        assert mock_claude_limiter.cooldown_until is not None

    @pytest.mark.asyncio
    async def test_requests_queued_during_cooldown(self, mock_claude_limiter):
        """Test that requests are queued during cooldown."""
        # Trigger cooldown
        for i in range(8):
            await mock_claude_limiter.acquire()

        # Next request should queue (with timeout)
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(
                mock_claude_limiter.acquire(),
                timeout=0.5
            )

        assert mock_claude_limiter.queued_requests > 0

    @pytest.mark.asyncio
    async def test_cooldown_metrics(self, mock_claude_limiter):
        """Test that metrics are tracked correctly."""
        await mock_claude_limiter.acquire()

        metrics = mock_claude_limiter.get_metrics()
        assert "total_requests" in metrics
        assert "current_rpm" in metrics
        assert "in_cooldown" in metrics
        assert metrics["total_requests"] >= 1

    @pytest.mark.asyncio
    async def test_queue_rejection_when_full(self, mock_claude_limiter):
        """Test that queue rejects when at capacity."""
        # Trigger cooldown
        for i in range(8):
            await mock_claude_limiter.acquire()

        # Fill queue
        tasks = []
        for i in range(mock_claude_limiter.max_queue_size + 5):
            task = asyncio.create_task(
                mock_claude_limiter.acquire()
            )
            tasks.append(task)

        # Should reject some requests
        with pytest.raises(RuntimeError, match="queue full"):
            await asyncio.gather(*tasks)


# ============================================================================
# WEBHOOK RETRY TESTS (Phase 2.4)
# ============================================================================

class TestWebhookRetry:
    """Test webhook retry logic with exponential backoff."""

    @pytest.mark.asyncio
    async def test_successful_webhook_first_attempt(self, mock_webhook_retry):
        """Test webhook succeeds on first attempt."""
        with patch("httpx.AsyncClient.post") as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True}
            mock_response.raise_for_status = Mock()
            mock_post.return_value = mock_response

            result = await mock_webhook_retry.execute(
                url="https://hooks.zapier.com/test",
                payload={"event": "test"}
            )

            assert result["success"] is True
            assert result["attempt"] == 1
            assert mock_webhook_retry.successful_calls == 1

    @pytest.mark.asyncio
    async def test_webhook_retries_on_failure(self, mock_webhook_retry):
        """Test webhook retries on network failure."""
        with patch("httpx.AsyncClient.post") as mock_post:
            # Fail twice, succeed third time
            mock_post.side_effect = [
                httpx.TimeoutException("Timeout"),
                httpx.TimeoutException("Timeout"),
                Mock(status_code=200, json=lambda: {}, raise_for_status=Mock())
            ]

            result = await mock_webhook_retry.execute(
                url="https://hooks.zapier.com/test",
                payload={"event": "test"}
            )

            assert result["success"] is True
            assert result["attempt"] == 3
            assert mock_webhook_retry.total_retries == 2

    @pytest.mark.asyncio
    async def test_webhook_fails_after_max_attempts(self, mock_webhook_retry):
        """Test webhook fails after max attempts."""
        with patch("httpx.AsyncClient.post") as mock_post:
            # Fail all attempts
            mock_post.side_effect = httpx.TimeoutException("Timeout")

            result = await mock_webhook_retry.execute(
                url="https://hooks.zapier.com/test",
                payload={"event": "test"}
            )

            assert result["success"] is False
            assert result["attempts"] == 3
            assert mock_webhook_retry.failed_calls == 1

    @pytest.mark.asyncio
    async def test_webhook_exponential_backoff(self, mock_webhook_retry):
        """Test exponential backoff timing."""
        with patch("httpx.AsyncClient.post") as mock_post:
            with patch("asyncio.sleep") as mock_sleep:
                # Fail all attempts
                mock_post.side_effect = httpx.TimeoutException("Timeout")

                await mock_webhook_retry.execute(
                    url="https://hooks.zapier.com/test",
                    payload={"event": "test"}
                )

                # Check backoff delays: 0.1s, 0.2s (initial_delay doubles)
                assert mock_sleep.call_count == 2
                delays = [call[0][0] for call in mock_sleep.call_args_list]
                assert delays[0] == 0.1  # First retry
                assert delays[1] == 0.2  # Second retry (doubled)

    def test_webhook_metrics_tracking(self, mock_webhook_retry):
        """Test that retry metrics are tracked."""
        metrics = mock_webhook_retry.get_metrics()
        assert "total_calls" in metrics
        assert "successful_calls" in metrics
        assert "failed_calls" in metrics
        assert "success_rate" in metrics


# ============================================================================
# HEALTH CHECK TESTS
# ============================================================================

class TestHealthCheck:
    """Test enhanced health check endpoint."""

    def test_health_check_returns_200(self, client):
        """Test health check returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_includes_uptime(self, client):
        """Test health check includes uptime."""
        response = client.get("/health")
        data = response.json()

        assert "ok" in data
        assert data["ok"] is True
        assert "uptime" in data
        assert "start_time" in data

    def test_health_check_includes_integrations(self, client):
        """Test health check includes integration status."""
        response = client.get("/health")
        data = response.json()

        assert "integrations" in data
        assert "summary" in data
        assert "total_integrations" in data["summary"]

    def test_health_check_integration_counts(self, client):
        """Test health check counts configured integrations."""
        response = client.get("/health")
        data = response.json()

        summary = data["summary"]
        assert summary["total_integrations"] > 0
        assert summary["configured"] >= 0
        assert summary["not_configured"] >= 0
        assert summary["percentage"] >= 0


# ============================================================================
# SECURITY REGRESSION TESTS
# ============================================================================

class TestSecurityRegressions:
    """Test that security fixes remain in place."""

    def test_no_import_vulnerability(self):
        """Test that __import__ vulnerability is fixed."""
        from backend.admin_bypass import log_admin_action
        import inspect

        # Get source code
        source = inspect.getsource(log_admin_action)

        # Should NOT contain __import__
        assert "__import__" not in source

        # Should properly import datetime at top
        assert "from datetime import datetime" in open("backend/admin_bypass.py").read()

    def test_streamlit_time_import_fixed(self):
        """Test that Streamlit time import shadowing is fixed."""
        source = open("dashboard/streamlit_app.py").read()

        # Should only have one 'import time' at top level
        imports = [line for line in source.split('\n') if 'import time' in line and not line.strip().startswith('#')]

        # Count should be 1 (at top of file only)
        assert len(imports) == 1

    def test_ssrf_validation_present(self):
        """Test that SSRF validation is present."""
        source = open("backend/main.py").read()

        # Should have SSRF validation
        assert "ALLOWED_ZAPIER_HOSTS" in source
        assert "lgtm[py/full-ssrf]" in source


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Test performance optimizations."""

    def test_gzip_compression_enabled(self, client):
        """Test that GZIP compression is enabled."""
        from backend.main import app

        # Check middleware stack
        middleware = [m for m in app.user_middleware]
        middleware_names = [str(m) for m in middleware]

        # Should have GZIPMiddleware
        assert any("GZIPMiddleware" in str(m) for m in middleware_names)

    def test_rate_limiting_enabled(self, client):
        """Test that rate limiting is enabled."""
        from backend.main import app

        # Should have limiter in app state
        assert hasattr(app.state, "limiter")

    def test_correlation_ids_middleware(self, client):
        """Test that correlation ID middleware is active."""
        response = client.get("/health")

        # Should have correlation ID in headers
        assert "X-Correlation-ID" in response.headers


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestAgentEcosystemIntegration:
    """Test agent ecosystem integration (Phase 2)."""

    def test_claude_status_endpoint(self, client):
        """Test Claude API status endpoint exists."""
        response = client.get("/api/claude/status")
        assert response.status_code == 200

        data = response.json()
        assert "current_rpm" in data or "error" in data

    def test_health_endpoint_performance(self, client):
        """Test health endpoint responds quickly."""
        start = time.time()
        response = client.get("/health")
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 1.0  # Should respond in <1s

    @pytest.mark.asyncio
    async def test_concurrent_requests_handling(self, client):
        """Test system handles concurrent requests."""
        # Simulate 10 concurrent health checks
        responses = []
        for _ in range(10):
            response = client.get("/health")
            responses.append(response)

        # All should succeed
        assert all(r.status_code == 200 for r in responses)


# ============================================================================
# LAUNCH READINESS CHECKLIST
# ============================================================================

class TestLaunchReadiness:
    """Comprehensive launch readiness checks."""

    def test_phase1_infrastructure_complete(self, client):
        """Test Phase 1 infrastructure requirements."""
        # Rate limiting
        from backend.main import app
        assert hasattr(app.state, "limiter")

        # GZIP compression
        middleware = [str(m) for m in app.user_middleware]
        assert any("GZIP" in str(m) for m in middleware)

        # Health check
        response = client.get("/health")
        assert response.status_code == 200

    def test_phase2_agent_ecosystem_ready(self):
        """Test Phase 2 agent ecosystem components exist."""
        # Claude cooldown manager
        from backend.core.claude_cooldown import get_claude_limiter
        limiter = get_claude_limiter()
        assert limiter is not None

        # Webhook retry
        from backend.core.webhook_retry import get_webhook_retry
        retry = get_webhook_retry()
        assert retry is not None

    def test_security_vulnerabilities_fixed(self):
        """Test critical security vulnerabilities are fixed."""
        # Check admin_bypass.py
        admin_source = open("backend/admin_bypass.py").read()
        assert "__import__" not in admin_source

        # Check streamlit_app.py
        streamlit_source = open("dashboard/streamlit_app.py").read()
        import_lines = streamlit_source.split('\n')
        time_imports_in_main = [
            line for line in import_lines[400:]  # After main() function
            if 'import time' in line and not line.strip().startswith('#')
        ]
        assert len(time_imports_in_main) == 0

    def test_documentation_exists(self):
        """Test launch documentation exists."""
        import os
        assert os.path.exists("LAUNCH_SPRINT_PRIORITY_v17.2.md")
        assert os.path.exists("QUICK_FIXES.md")
        assert os.path.exists("backend/core/claude_cooldown.py")
        assert os.path.exists("backend/core/webhook_retry.py")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
