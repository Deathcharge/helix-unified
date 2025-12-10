"""
🔐 Security Module
Password hashing, JWT token management, security utilities
"""

import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError(
        "JWT_SECRET environment variable is required. "
        "Generate one with: openssl rand -hex 32"
    )

if len(JWT_SECRET) < 32:
    raise ValueError(
        f"JWT_SECRET must be at least 32 characters long. "
        f"Current length: {len(JWT_SECRET)}"
    )

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "168"))  # 7 days default


class TokenPayload(BaseModel):
    """JWT token payload structure"""
    sub: str  # user ID
    email: str
    name: str
    tier: str
    exp: datetime
    iat: datetime


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password string

    Example:
        >>> hashed = hash_password("my_secure_password")
        >>> verify_password("my_secure_password", hashed)
        True
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("my_password")
        >>> verify_password("my_password", hashed)
        True
        >>> verify_password("wrong_password", hashed)
        False
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary containing token payload (user_id, email, etc.)
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string

    Example:
        >>> token = create_access_token({"sub": "user123", "email": "user@example.com"})
        >>> payload = decode_access_token(token)
        >>> payload["sub"]
        'user123'
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT access token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload dict, or None if invalid/expired

    Example:
        >>> token = create_access_token({"sub": "user123"})
        >>> payload = decode_access_token(token)
        >>> payload["sub"]
        'user123'
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def generate_secure_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token.

    Args:
        length: Length of token in bytes (default: 32)

    Returns:
        Hex-encoded random token

    Example:
        >>> token = generate_secure_token()
        >>> len(token)
        64  # 32 bytes = 64 hex characters
    """
    import secrets
    return secrets.token_hex(length)


__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_access_token",
    "generate_secure_token",
    "TokenPayload",
    "JWT_SECRET",
    "JWT_ALGORITHM",
    "JWT_EXPIRATION_HOURS",
]
