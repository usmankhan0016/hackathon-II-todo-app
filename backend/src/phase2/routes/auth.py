"""
Authentication routes for signup, signin, and token management.
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..handlers.errors import EmailExistsError, InvalidCredentialsError
from ..schemas.auth import SigninRequest, SigninResponse, SignupRequest, SignupResponse, UserResponse
from ..services.auth import AuthService


router = APIRouter(tags=["Authentication"])  # No prefix here, will be added in main.py with API_PREFIX + /auth

# Full path will be: /api/auth + router paths
# Example: /api/auth/signup


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    """Dependency to get AuthService instance."""
    return AuthService(db)



@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=201,
    summary="Create a new user account",
)
async def signup(
    request: SignupRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, Any]:
    """
    Create a new user account with email and password.

    Validates:
    - Email format
    - Email uniqueness
    - Password strength (min 8 characters, max 72 bytes)

    Returns:
        SignupResponse with user details and tokens

    Raises:
        EmailExistsError: If email is already registered
        HTTPException(422): If password validation fails
    """
    try:
        # Create user using AuthService
        user = await auth_service.signup(request)

        # Generate JWT tokens
        tokens = auth_service.generate_tokens(user.id)

        # Return response
        return {
            "user": UserResponse(
                id=str(user.id),
                email=user.email,
                name=user.name,
                created_at=user.created_at,
                updated_at=user.updated_at,
                is_active=user.is_active,
            ),
            "tokens": tokens,
        }

    except IntegrityError:
        # This should be caught in the service, but keeping it as a fallback
        raise EmailExistsError()


@router.post(
    "/signin",
    response_model=SigninResponse,
    status_code=200,
    summary="Sign in with email and password",
)
async def signin(
    request: SigninRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, Any]:
    """
    Sign in user with email and password.

    Validates:
    - Email exists
    - Password matches
    - Account is active

    Returns:
        SigninResponse with user details and tokens

    Raises:
        InvalidCredentialsError: If email/password is incorrect or account is inactive
    """
    # Authenticate user using AuthService
    user = await auth_service.signin(request)

    # Generate JWT tokens
    tokens = auth_service.generate_tokens(user.id)

    # Return response
    return {
        "user": UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
        ),
        "tokens": tokens,
    }


