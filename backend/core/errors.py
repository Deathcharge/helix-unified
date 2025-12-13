"""
❌ Error Handling Module
Centralized exception hierarchy and error responses
"""

from typing import Any, Dict, Optional

from fastapi import HTTPException, status


class HelixException(HTTPException):
    """Base exception for all Helix errors"""

    def __init__(
        self,
        status_code: int,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        detail = {"message": message}
        if details:
            detail["details"] = details
        super().__init__(status_code=status_code, detail=detail, headers=headers)


# Authentication Errors
class AuthenticationError(HelixException):
    """Authentication failed"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message)


class InvalidCredentialsError(AuthenticationError):
    """Invalid email or password"""
    def __init__(self):
        super().__init__("Invalid email or password")


class TokenExpiredError(AuthenticationError):
    """JWT token has expired"""
    def __init__(self):
        super().__init__("Token has expired")


class InvalidTokenError(AuthenticationError):
    """JWT token is invalid"""
    def __init__(self):
        super().__init__("Invalid token")


# Authorization Errors
class AuthorizationError(HelixException):
    """User not authorized for this action"""
    def __init__(self, message: str = "Not authorized"):
        super().__init__(status.HTTP_403_FORBIDDEN, message)


class InsufficientPermissionsError(AuthorizationError):
    """User lacks required permissions"""
    def __init__(self, required_permission: str):
        super().__init__(f"Insufficient permissions. Required: {required_permission}")


class SubscriptionRequiredError(AuthorizationError):
    """Action requires active subscription"""
    def __init__(self, required_tier: str = "pro"):
        super().__init__(f"This feature requires {required_tier} subscription")


# Resource Errors
class NotFoundError(HelixException):
    """Resource not found"""
    def __init__(self, resource: str, resource_id: Optional[str] = None):
        message = f"{resource} not found"
        if resource_id:
            message += f": {resource_id}"
        super().__init__(status.HTTP_404_NOT_FOUND, message)


class AlreadyExistsError(HelixException):
    """Resource already exists"""
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            status.HTTP_409_CONFLICT,
            f"{resource} already exists: {identifier}"
        )


# Validation Errors
class ValidationError(HelixException):
    """Input validation failed"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, message, details)


class InvalidInputError(ValidationError):
    """Invalid input provided"""
    def __init__(self, field: str, reason: str):
        super().__init__(
            f"Invalid {field}",
            details={"field": field, "reason": reason}
        )


# Rate Limiting Errors
class RateLimitError(HelixException):
    """Rate limit exceeded"""
    def __init__(self, retry_after: Optional[int] = None):
        message = "Rate limit exceeded"
        headers = {}
        if retry_after:
            message += f". Retry after {retry_after} seconds"
            headers["Retry-After"] = str(retry_after)
        super().__init__(status.HTTP_429_TOO_MANY_REQUESTS, message, headers=headers)


# Payment Errors
class PaymentError(HelixException):
    """Payment processing failed"""
    def __init__(self, message: str = "Payment processing failed"):
        super().__init__(status.HTTP_402_PAYMENT_REQUIRED, message)


class InsufficientCreditsError(PaymentError):
    """User has insufficient credits"""
    def __init__(self, required: int, available: int):
        super().__init__(
            f"Insufficient credits. Required: {required}, Available: {available}"
        )


# External Service Errors
class ExternalServiceError(HelixException):
    """External service error"""
    def __init__(self, service: str, message: str = "Service unavailable"):
        super().__init__(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            f"{service}: {message}"
        )


class LLMError(ExternalServiceError):
    """LLM API error"""
    def __init__(self, provider: str, message: str):
        super().__init__(f"LLM ({provider})", message)


class DatabaseError(ExternalServiceError):
    """Database error"""
    def __init__(self, message: str = "Database operation failed"):
        super().__init__("Database", message)


# Server Errors
class InternalServerError(HelixException):
    """Internal server error"""
    def __init__(self, message: str = "Internal server error"):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, message)


class ConfigurationError(InternalServerError):
    """Server configuration error"""
    def __init__(self, message: str):
        super().__init__(f"Configuration error: {message}")


__all__ = [
    "HelixException",
    "AuthenticationError",
    "InvalidCredentialsError",
    "TokenExpiredError",
    "InvalidTokenError",
    "AuthorizationError",
    "InsufficientPermissionsError",
    "SubscriptionRequiredError",
    "NotFoundError",
    "AlreadyExistsError",
    "ValidationError",
    "InvalidInputError",
    "RateLimitError",
    "PaymentError",
    "InsufficientCreditsError",
    "ExternalServiceError",
    "LLMError",
    "DatabaseError",
    "InternalServerError",
    "ConfigurationError",
]
