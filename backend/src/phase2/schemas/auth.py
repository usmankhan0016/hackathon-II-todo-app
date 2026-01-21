"""
Pydantic schemas for authentication endpoints.
Includes request/response models and error codes.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# Error Codes (machine-readable for logging)
class ErrorCode:
    """Standard error codes for authentication system."""

    AUTH_INVALID_CREDENTIALS = "AUTH_INVALID_CREDENTIALS"
    AUTH_EMAIL_EXISTS = "AUTH_EMAIL_EXISTS"
    AUTH_INVALID_EMAIL = "AUTH_INVALID_EMAIL"
    AUTH_WEAK_PASSWORD = "AUTH_WEAK_PASSWORD"
    AUTH_TOKEN_EXPIRED = "AUTH_TOKEN_EXPIRED"
    AUTH_TOKEN_INVALID = "AUTH_TOKEN_INVALID"
    AUTH_TOKEN_MISSING = "AUTH_TOKEN_MISSING"
    AUTH_FORBIDDEN = "AUTH_FORBIDDEN"


# Request Schemas


class SignupRequest(BaseModel):
    """
    Signup request schema.

    Fields:
        email: Valid email address
        password: Password (minimum 8 characters)
        name: Optional display name
    """

    email: EmailStr = Field(
        ...,
        description="User email address",
        examples=["user@example.com"]
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Password (8-72 characters, bcrypt limit)",
        examples=["MyPass12"]
    )

    name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="User's display name",
        examples=["John Doe"]
    )

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
                "name": "John Doe"
            }
        }


class SigninRequest(BaseModel):
    """
    Signin request schema.

    Fields:
        email: User email address
        password: User password
    """

    email: EmailStr = Field(
        ...,
        description="User email address",
        examples=["user@example.com"]
    )

    password: str = Field(
        ...,
        description="User password",
        examples=["mypassword123"]
    )

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class RefreshRequest(BaseModel):
    """
    Token refresh request schema.

    Fields:
        refresh_token: Valid refresh token
    """

    refresh_token: str = Field(
        ...,
        description="Refresh token to exchange for new access token",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )


# Response Schemas


class TokenResponse(BaseModel):
    """
    Token response schema.

    Fields:
        access_token: JWT access token (7 days)
        refresh_token: JWT refresh token (30 days)
        token_type: Token type (always "bearer")
        expires_in: Access token expiry in seconds
    """

    access_token: str = Field(
        ...,
        description="JWT access token for API authentication"
    )

    refresh_token: str = Field(
        ...,
        description="JWT refresh token for obtaining new access tokens"
    )

    token_type: str = Field(
        default="bearer",
        description="Token type (always bearer)"
    )

    expires_in: int = Field(
        default=604800,  # 7 days in seconds
        description="Access token expiry time in seconds"
    )

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 604800
            }
        }


class UserResponse(BaseModel):
    """
    User response schema (excludes password_hash).

    Fields:
        id: User UUID
        email: User email
        name: User display name
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        is_active: Account active status
    """

    id: UUID = Field(..., description="User unique identifier")
    email: str = Field(..., description="User email address")
    name: Optional[str] = Field(None, description="User display name")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    is_active: bool = Field(True, description="Account active status")

    class Config:
        """Pydantic config."""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "name": "John Doe",
                "created_at": "2026-01-12T10:30:00Z",
                "updated_at": "2026-01-12T10:30:00Z",
                "is_active": True
            }
        }


class ErrorResponse(BaseModel):
    """
    Error response schema.

    Fields:
        error: Machine-readable error code (for logging)
        message: User-facing error message (generic, no info leakage)
        status_code: HTTP status code
    """

    error: str = Field(
        ...,
        description="Machine-readable error code",
        examples=["AUTH_INVALID_CREDENTIALS"]
    )

    message: str = Field(
        ...,
        description="User-facing error message",
        examples=["Invalid credentials"]
    )

    status_code: int = Field(
        ...,
        description="HTTP status code",
        examples=[401]
    )

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "error": "AUTH_INVALID_CREDENTIALS",
                "message": "Invalid credentials",
                "status_code": 401
            }
        }


class SignupResponse(BaseModel):
    """
    Signup response schema.

    Fields:
        user: User data
        tokens: Authentication tokens
    """

    user: UserResponse = Field(..., description="Created user data")
    tokens: TokenResponse = Field(..., description="Authentication tokens")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "user@example.com",
                    "name": "John Doe",
                    "created_at": "2026-01-12T10:30:00Z",
                    "updated_at": "2026-01-12T10:30:00Z",
                    "is_active": True
                },
                "tokens": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "expires_in": 604800
                }
            }
        }


class SigninResponse(BaseModel):
    """
    Signin response schema.

    Fields:
        user: User data
        tokens: Authentication tokens
    """

    user: UserResponse = Field(..., description="User data")
    tokens: TokenResponse = Field(..., description="Authentication tokens")

    class Config:
        """Pydantic config."""
        from_attributes = True
