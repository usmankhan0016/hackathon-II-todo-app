"""
Task SQLModel for todo application.
Includes relationship to User with cascade delete.
Composite indexes for efficient user-scoped queries.
"""
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ARRAY, Column, DateTime, Index, String
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


# Enums for type safety - defined BEFORE Task class uses them
class TaskStatus(str, Enum):
    """Task completion status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(SQLModel, table=True):
    """
    Task model with user isolation and full audit trail.

    Indexes:
        - user_id (single)
        - status (single)
        - user_id + status (composite)
        - user_id + due_date (composite)
    """

    __tablename__ = "tasks"

    __table_args__ = (
        Index('idx_tasks_user_status', 'user_id', 'status'),
        Index('idx_tasks_user_due', 'user_id', 'due_date'),
    )

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        index=True,
        nullable=False,
    )

    user_id: UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,
    )

    title: str = Field(
        sa_column=Column(String(255), nullable=False),
        max_length=255,
    )

    description: Optional[str] = Field(
        default=None,
        sa_column=Column(String(5000)),
        max_length=5000,
    )

    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        sa_column=Column(SAEnum(TaskStatus), nullable=False, index=True),
    )

    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        sa_column=Column(SAEnum(TaskPriority), nullable=False),
    )

    due_date: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime, index=True, nullable=True),
    )

    tags: List[str] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String)),
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False, onupdate=datetime.utcnow),
    )

    # Relationships - use string annotation to avoid circular import
    user: Optional["User"] = Relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task {self.title[:30]}... (id={self.id})>"
