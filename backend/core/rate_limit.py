"""
⏱️ Rate Limiting Module
Protect endpoints from brute force and abuse
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

# Create rate limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000/hour"],  # Default limit for all endpoints
    storage_uri="memory://",  # Use Redis in production: redis://localhost:6379
)

# Rate limit configurations for different endpoint types
RATE_LIMITS = {
    "auth_login": "5/minute",  # Strict limit for login attempts
    "auth_signup": "3/minute",  # Strict limit for signup
    "auth_password_reset": "3/hour",  # Very strict for password reset
    "api_general": "100/minute",  # General API endpoints
    "api_expensive": "10/minute",  # Expensive operations (AI, rendering)
    "webhook": "1000/hour",  # Webhooks from trusted sources
}


def get_rate_limit(endpoint_type: str) -> str:
    """
    Get rate limit string for endpoint type.
    
    Args:
        endpoint_type: Type of endpoint (auth_login, api_general, etc.)
        
    Returns:
        Rate limit string (e.g., "5/minute")
        
    Example:
        >>> get_rate_limit("auth_login")
        '5/minute'
    """
    return RATE_LIMITS.get(endpoint_type, "100/minute")


__all__ = ["limiter", "get_rate_limit", "RATE_LIMITS"]
