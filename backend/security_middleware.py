# 🌀 Helix Collective v17.0 — Security Middleware
# backend/security_middleware.py — JWT Authentication & Security Headers
# Author: Manus AI (Weaver #2)

import logging
from typing import Optional
from fastapi import Request, Response
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
        content = {
            "error": message,
            "status": status_code
        }
        if details:
            content["details"] = details
        super().__init__(status_code=status_code, content=content)


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
    payload_with_exp = {
        **payload,
        "exp": int(time.time()) + expires_in
    }
    
    try:
        token = jwt.encode(payload_with_exp, secret, algorithm="HS256")
        return token
    except Exception as e:
        logger.error(f"❌ Error creating JWT token: {e}")
        return None
