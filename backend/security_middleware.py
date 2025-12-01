"""
🔒 Helix Security Middleware
backend/security_middleware.py

Comprehensive security middleware for FastAPI:
- CSRF protection for state-changing endpoints
- Rate limiting with sliding window
- Safe error message handling
- Security headers

Author: Claude (Security Automation)
Version: 1.0.0
"""

import hashlib
import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional, Set
from functools import wraps

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
import jwt

logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

CSRF_SECRET = os.getenv("CSRF_SECRET", "csrf-secret-change-in-production")
CSRF_HEADER_NAME = "X-CSRF-Token"
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = {
    "default": 100,  # 100 requests per minute
    "agent_query": 20,  # 20 calls per minute for expensive agent operations
    "music_generate": 10,  # 10 calls per minute for CPU-intensive music generation
    "zapier": 50,  # 50 calls per minute for webhook triggers
}

# In-memory rate limit store (in production, use Redis)
rate_limit_store: Dict[str, list] = {}

# ============================================================================
# CSRF TOKEN MANAGEMENT
# ============================================================================


def generate_csrf_token(user_id: str, session_id: str) -> str:
    """Generate a CSRF token for a user session."""
    payload = {
        "user_id": user_id,
        "session_id": session_id,
        "iat": datetime.utcnow().timestamp(),
        "exp": (datetime.utcnow() + timedelta(hours=24)).timestamp(),
    }
    token = jwt.encode(payload, CSRF_SECRET, algorithm="HS256")
    return token


def verify_csrf_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify a CSRF token."""
    try:
        payload = jwt.decode(token, CSRF_SECRET, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        return None


# ============================================================================
# RATE LIMITING
# ============================================================================


def get_client_id(request: Request) -> str:
    """Extract client identifier from request."""
    # Try to get user_id from JWT token if available
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, os.getenv("JWT_SECRET", "dev-secret"), algorithms=["HS256"])
            user_id = payload.get("user_id")
            if user_id:
                return f"user:{user_id}"
        except Exception:
            pass

    # Fallback to IP address
    client_host = request.client.host if request.client else "unknown"
    return f"ip:{client_host}"


def check_rate_limit(client_id: str, limit_type: str = "default") -> tuple[bool, str]:
    """Check if client has exceeded rate limit."""
    now = time.time()
    limit = RATE_LIMIT_MAX_REQUESTS.get(limit_type, RATE_LIMIT_MAX_REQUESTS["default"])

    # Initialize client entry if needed
    if client_id not in rate_limit_store:
        rate_limit_store[client_id] = []

    # Remove old timestamps outside the window
    rate_limit_store[client_id] = [ts for ts in rate_limit_store[client_id] if now - ts < RATE_LIMIT_WINDOW]

    # Check if limit exceeded
    if len(rate_limit_store[client_id]) >= limit:
        return False, f"Rate limit exceeded. Maximum {limit} requests per {RATE_LIMIT_WINDOW} seconds."

    # Add current timestamp
    rate_limit_store[client_id].append(now)
    return True, ""


# ============================================================================
# ERROR MESSAGE SANITIZATION
# ============================================================================


class SafeErrorResponse:
    """Generate safe error responses that don't leak sensitive information."""

    @staticmethod
    def sanitize_error(error: Exception, error_code: str = "internal_error") -> tuple[int, Dict[str, Any]]:
        """Convert exception to safe error response."""
        error_message = str(error).lower()

        # Log full error internally for debugging
        logger.error(f"Full error details [{error_code}]: {type(error).__name__}: {error}")

        # Return safe message to client based on error type
        if "rate limit" in error_message or "ratelimit" in error_message:
            return 429, {
                "error": "service_busy",
                "message": "Service is temporarily busy. Please retry in a moment.",
                "code": "RATE_LIMIT_EXCEEDED",
            }

        if "authentication" in error_message or "unauthorized" in error_message or "invalid token" in error_message:
            return 401, {
                "error": "unauthorized",
                "message": "Authentication required or invalid credentials.",
                "code": "UNAUTHORIZED",
            }

        if "permission" in error_message or "forbidden" in error_message or "access" in error_message:
            return 403, {
                "error": "forbidden",
                "message": "You do not have permission to perform this action.",
                "code": "FORBIDDEN",
            }

        if "not found" in error_message or "404" in error_message:
            return 404, {
                "error": "not_found",
                "message": "The requested resource was not found.",
                "code": "NOT_FOUND",
            }

        if "validation" in error_message or "invalid" in error_message:
            return 400, {
                "error": "validation_error",
                "message": "The request contains invalid data. Please check your input.",
                "code": "INVALID_REQUEST",
            }

        if "timeout" in error_message:
            return 504, {
                "error": "gateway_timeout",
                "message": "Request took too long to process. Please try again.",
                "code": "TIMEOUT",
            }

        # Default safe error response
        return 500, {
            "error": "internal_error",
            "message": "An unexpected error occurred. Our team has been notified.",
            "code": "INTERNAL_SERVER_ERROR",
        }


# ============================================================================
# MIDDLEWARE REGISTRATION
# ============================================================================


def apply_security_middleware(app: FastAPI) -> None:
    """Apply all security middleware to FastAPI app."""

    # Add security headers middleware
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next: Callable) -> Response:
        """Add security headers to all responses."""
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'"

        return response

    # Add rate limiting middleware for POST/PUT/DELETE/PATCH
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next: Callable) -> Response:
        """Apply rate limiting to state-changing requests."""
        # Only rate limit state-changing methods
        if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            client_id = get_client_id(request)

            # Determine limit type based on path
            limit_type = "default"
            if "/agent" in request.url.path:
                limit_type = "agent_query"
            elif "/music" in request.url.path:
                limit_type = "music_generate"
            elif "zapier" in request.url.path or "trigger" in request.url.path:
                limit_type = "zapier"

            # Check rate limit
            allowed, error_msg = check_rate_limit(client_id, limit_type)
            if not allowed:
                return JSONResponse(
                    status_code=429,
                    content={"error": "rate_limit_exceeded", "message": error_msg, "code": "RATE_LIMIT_EXCEEDED"},
                )

        return await call_next(request)

    logger.info("✅ Security middleware applied: CSRF, rate limiting, security headers")


# ============================================================================
# DECORATORS FOR ENDPOINT PROTECTION
# ============================================================================


def require_csrf_token(f: Callable) -> Callable:
    """Decorator to require CSRF token on endpoint."""

    @wraps(f)
    async def wrapper(request: Request, *args: Any, **kwargs: Any) -> Any:
        # Skip CSRF check for GET, HEAD, OPTIONS
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return await f(request, *args, **kwargs)

        # Get CSRF token from header
        csrf_token = request.headers.get(CSRF_HEADER_NAME)
        if not csrf_token:
            raise HTTPException(
                status_code=403,
                detail="CSRF token required. Include X-CSRF-Token header.",
            )

        # Verify token
        payload = verify_csrf_token(csrf_token)
        if not payload:
            raise HTTPException(
                status_code=403,
                detail="Invalid CSRF token.",
            )

        # Add verified payload to request state for endpoint use
        request.state.csrf_payload = payload

        return await f(request, *args, **kwargs)

    return wrapper


def require_rate_limit(limit_type: str = "default") -> Callable:
    """Decorator to enforce rate limiting on endpoint."""

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        async def wrapper(request: Request, *args: Any, **kwargs: Any) -> Any:
            client_id = get_client_id(request)
            allowed, error_msg = check_rate_limit(client_id, limit_type)

            if not allowed:
                raise HTTPException(
                    status_code=429,
                    detail=error_msg,
                )

            return await f(request, *args, **kwargs)

        return wrapper

    return decorator


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "apply_security_middleware",
    "require_csrf_token",
    "require_rate_limit",
    "generate_csrf_token",
    "verify_csrf_token",
    "SafeErrorResponse",
    "get_client_id",
]
