"""
JWT utilities for token generation and verification.
Uses HS256 algorithm with shared BETTER_AUTH_SECRET.
"""

from datetime import datetime, timedelta
from typing import Any, Optional
from uuid import UUID

from jose import JWTError, jwt

from ..config import get_settings

# Get settings
settings = get_settings()


def create_access_token(user_id: str | UUID, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token for user authentication.

    Args:
        user_id: User's unique identifier
        expires_delta: Optional custom expiration time (default: 7 days)

    Returns:
        str: Encoded JWT token

    Example:
        >>> token = create_access_token("550e8400-e29b-41d4-a716-446655440000")
        >>> len(token) > 100
        True
    """
    if expires_delta is None:
        expires_delta = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)

    # Ensure user_id is string
    user_id_str = str(user_id)

    # Token payload
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": user_id_str,  # Subject (user_id)
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at
        "type": "access",  # Token type
    }

    # Encode token
    encoded_jwt = jwt.encode(
        payload,
        settings.BETTER_AUTH_SECRET,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def create_refresh_token(user_id: str | UUID, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT refresh token for obtaining new access tokens.

    Args:
        user_id: User's unique identifier
        expires_delta: Optional custom expiration time (default: 30 days)

    Returns:
        str: Encoded JWT refresh token

    Example:
        >>> token = create_refresh_token("550e8400-e29b-41d4-a716-446655440000")
        >>> len(token) > 100
        True
    """
    if expires_delta is None:
        expires_delta = timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS)

    # Ensure user_id is string
    user_id_str = str(user_id)

    # Token payload
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": user_id_str,  # Subject (user_id)
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at
        "type": "refresh",  # Token type
    }

    # Encode token
    encoded_jwt = jwt.encode(
        payload,
        settings.BETTER_AUTH_SECRET,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def verify_token(token: str) -> dict[str, Any]:
    """
    Verify JWT token and return payload.

    Args:
        token: JWT token to verify

    Returns:
        dict: Decoded token payload

    Raises:
        JWTError: If token is invalid, expired, or malformed

    Example:
        >>> token = create_access_token("550e8400-e29b-41d4-a716-446655440000")
        >>> payload = verify_token(token)
        >>> "sub" in payload
        True
    """
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError as e:
        raise JWTError(f"Token verification failed: {str(e)}")


def extract_user_id(token: str) -> str:
    """
    Extract user_id from JWT token.

    Args:
        token: JWT token

    Returns:
        str: User ID from token's 'sub' claim

    Raises:
        JWTError: If token is invalid or missing 'sub' claim

    Example:
        >>> token = create_access_token("550e8400-e29b-41d4-a716-446655440000")
        >>> user_id = extract_user_id(token)
        >>> user_id
        '550e8400-e29b-41d4-a716-446655440000'
    """
    payload = verify_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise JWTError("Token missing 'sub' claim")

    return user_id


def decode_token_without_verification(token: str) -> dict[str, Any]:
    """
    Decode JWT token without verification (for checking expiry, etc.).

    WARNING: Do NOT use for authentication. This is for client-side
    checks only (e.g., checking if token is expiring soon).

    Args:
        token: JWT token to decode

    Returns:
        dict: Decoded token payload (unverified)

    Example:
        >>> token = create_access_token("550e8400-e29b-41d4-a716-446655440000")
        >>> payload = decode_token_without_verification(token)
        >>> "exp" in payload
        True
    """
    return jwt.get_unverified_claims(token)


def is_token_expired(token: str) -> bool:
    """
    Check if token is expired (without full verification).

    Args:
        token: JWT token to check

    Returns:
        bool: True if expired, False otherwise

    Example:
        >>> token = create_access_token("550e8400-e29b-41d4-a716-446655440000")
        >>> is_token_expired(token)
        False
    """
    try:
        payload = decode_token_without_verification(token)
        exp_timestamp = payload.get("exp")

        if not exp_timestamp:
            return True

        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        return datetime.utcnow() > exp_datetime
    except Exception:
        return True  # If any error, consider expired
