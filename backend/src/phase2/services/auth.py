"""
AuthService - Business logic for authentication operations.

This service layer abstracts the authentication business logic from the API routes,
making it easier to test, maintain, and reuse.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.jwt import create_access_token, create_refresh_token
from ..handlers.errors import EmailExistsError, InvalidCredentialsError, WeakPasswordError
from ..models.user import User, hash_password, verify_password
from ..schemas.auth import SigninRequest, SignupRequest


class AuthService:
    """
    Service class for authentication operations.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize AuthService with database session.

        Args:
            db: Async database session
        """
        self.db = db

    async def signup(self, request: SignupRequest) -> User:
        """
        Create a new user account.

        Args:
            request: SignupRequest with email, password, and name

        Returns:
            User: Newly created user

        Raises:
            WeakPasswordError: If password is too short or too long
            EmailExistsError: If email is already registered
        """
        # Validate password strength (8-72 chars, bcrypt limit)
        if len(request.password) < 8:
            raise WeakPasswordError()
        if len(request.password) > 72:
            raise WeakPasswordError()  # Will be caught and converted to proper error

        # Hash password
        password_hash = hash_password(request.password)

        # Create new user
        user = User(
            email=str(request.email).lower().strip(),
            password_hash=password_hash,
            name=request.name.strip() if request.name else None,
        )

        try:
            # Add to database
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user

        except IntegrityError:
            await self.db.rollback()
            raise EmailExistsError()

    async def signin(self, request: SigninRequest) -> Optional[User]:
        """
        Authenticate a user with email and password.

        Args:
            request: SigninRequest with email and password

        Returns:
            User: Authenticated user if credentials are valid

        Raises:
            InvalidCredentialsError: If email/password is incorrect or account is inactive
        """
        # Find user by email
        result = await self.db.execute(
            select(User).where(User.email == str(request.email).lower().strip())
        )
        user = result.scalar_one_or_none()

        if not user:
            # Generic error to prevent email enumeration
            raise InvalidCredentialsError()

        if not user.is_active:
            # Account is deactivated
            raise InvalidCredentialsError()

        # Verify password
        if not verify_password(request.password, user.password_hash):
            raise InvalidCredentialsError()

        return user

    def generate_tokens(self, user_id: UUID | str) -> dict[str, str]:
        """
        Generate JWT access and refresh tokens for a user.

        Args:
            user_id: User ID (UUID or string)

        Returns:
            dict: Dictionary with access_token, refresh_token, token_type, and expires_in
        """
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 604800,  # 7 days
        }

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email address.

        Args:
            email: Email address to look up

        Returns:
            User: User if found, None otherwise
        """
        result = await self.db.execute(
            select(User).where(User.email == email.lower().strip())
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID | str) -> Optional[User]:
        """
        Get a user by ID.

        Args:
            user_id: User ID (UUID or string)

        Returns:
            User: User if found, None otherwise
        """
        result = await self.db.execute(select(User).where(User.id == str(user_id)))
        return result.scalar_one_or_none()
