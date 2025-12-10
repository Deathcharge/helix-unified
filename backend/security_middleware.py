# 🌀 Helix Collective v17.0 — Security Middleware
# backend/security_middleware.py — JWT Authentication & Security Headers
# Author: Manus AI (Weaver #2)

import logging
from typing import Optional

from fastapi import Request
from fastapi.responses import JSONResponse

# Optional JWT import - gracefully degrade if not available
try:
    import jwt

    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    logging.warning("⚠️ PyJWT not installed. JWT authentication will be disabled.")

logger = logging.getLogger(__name__)

# ============================================================================
# SAFE ERROR RESPONSE
# ============================================================================


class SafeErrorResponse(JSONResponse):
    """
    Safe error response that doesn't leak internal details.
    """

    def __init__(self, status_code: int, message: str, details: Optional[str] = None):
        content = {"error": message, "status": status_code}
        if details:
            content["details"] = details
        super().__init__(status_code=status_code, content=content)

    @staticmethod
    def sanitize_error(exception: Exception, error_type: str = "api_error") -> tuple[int, str]:
        """
        Sanitize error to prevent information leakage.

        Args:
            exception: The exception to sanitize
            error_type: Type of error for logging

        Returns:
            (status_code, safe_error_message) tuple
        """
        # Map common API errors to status codes
        error_str = str(exception).lower()

        # Authentication/authorization errors
        if "unauthorized" in error_str or "authentication" in error_str:
            return 401, "Authentication failed. Please check your API key."
        if "forbidden" in error_str or "permission" in error_str:
            return 403, "Access forbidden. Insufficient permissions."

        # Rate limiting errors
        if "rate limit" in error_str or "quota" in error_str or "429" in error_str:
            return 429, "Rate limit exceeded. Please try again later."

        # API key/token errors
        if "api key" in error_str or "invalid key" in error_str:
            return 401, "Invalid API key. Please check your credentials."

        # Model/resource not found
        if "not found" in error_str or "404" in error_str:
            return 404, "Resource not found."

        # Bad request errors
        if "invalid" in error_str or "bad request" in error_str or "400" in error_str:
            return 400, f"Invalid request: {str(exception)}"

        # Server errors (be vague to avoid leaking internals)
        if "500" in error_str or "internal" in error_str:
            logger.error(f"{error_type}: {str(exception)}")
            return 500, "Internal server error. Please try again later."

        # Service unavailable
        if "unavailable" in error_str or "503" in error_str:
            return 503, "Service temporarily unavailable. Please try again later."

        # Gateway timeout
        if "timeout" in error_str or "504" in error_str:
            return 504, "Request timeout. Please try again."

        # Default: generic error (don't leak exception details)
        logger.error(f"{error_type}: {str(exception)}")
        return 500, "An error occurred. Please contact support if this persists."


# ============================================================================
# SECURITY MIDDLEWARE
# ============================================================================


async def security_middleware(request: Request, call_next):
    """
    Apply security headers and basic protections to all responses.
    """
    response = await call_next(request)

    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response


def apply_security_middleware(app):
    """
    Apply security middleware to FastAPI app.
    """
    app.middleware("http")(security_middleware)
    logger.info("✅ Security middleware applied")


# ============================================================================
# JWT AUTHENTICATION (Optional)
# ============================================================================


def verify_jwt_token(token: str, secret: str) -> Optional[dict]:
    """
    Verify JWT token and return payload if valid.

    Returns None if JWT is not available or token is invalid.
    """
    if not JWT_AVAILABLE:
        logger.warning("⚠️ JWT verification skipped - PyJWT not installed")
        return None

    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("⚠️ JWT token expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"⚠️ Invalid JWT token: {e}")
        return None


def create_jwt_token(payload: dict, secret: str, expires_in: int = 3600) -> Optional[str]:
    """
    Create JWT token with expiration.

    Returns None if JWT is not available.
    """
    if not JWT_AVAILABLE:
        logger.warning("⚠️ JWT creation skipped - PyJWT not installed")
        return None

    import time

    payload_with_exp = {**payload, "exp": int(time.time()) + expires_in}

    try:
        token = jwt.encode(payload_with_exp, secret, algorithm="HS256")
        return token
    except Exception as e:
        logger.error(f"❌ Error creating JWT token: {e}")
        return None
