"""
User model for authentication system.
Includes password hashing utilities using argon2-cffi.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError
from sqlalchemy import DateTime
from sqlmodel import Column, Field, Relationship, SQLModel, String

if TYPE_CHECKING:
    from .task import Task

# Password hasher (argon2 with secure defaults)
pwd_hasher = PasswordHasher()


class User(SQLModel, table=True):
    """
    User model for authentication.

    Fields:
        id: Unique user identifier (UUID)
        email: User email address (unique, indexed)
        password_hash: Argon2 hashed password
        name: User's display name (optional)
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        is_active: Account active status (for soft deletes)
    """

    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    email: str = Field(
        sa_column=Column(String(255), unique=True, index=True, nullable=False)
    )

    password_hash: str = Field(
        sa_column=Column(String(255), nullable=False)
    )

    name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(255), nullable=True)
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False, onupdate=datetime.utcnow),
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
        index=True,
    )

    # Relationships
    tasks: List["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User {self.email}>"

    def to_dict(self) -> dict:
        """
        Convert user to dictionary (excludes password_hash).

        Returns:
            dict: User data without sensitive information
        """
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
        }


# Password utility functions


def hash_password(password: str) -> str:
    """
    Hash a password using argon2.

    Args:
        password: Plain text password

    Returns:
        str: Argon2 hashed password

    Example:
        >>> hashed = hash_password("mypassword123")
        >>> hashed.startswith("$argon2")
        True
    """
    return pwd_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Argon2 hash to verify against

    Returns:
        bool: True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("mypassword123")
        >>> verify_password("mypassword123", hashed)
        True
        >>> verify_password("wrongpassword", hashed)
        False
    """
    try:
        pwd_hasher.verify(hashed_password, plain_password)
        return True
    except (VerifyMismatchError, InvalidHash):
        return False
