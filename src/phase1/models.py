# Task: T006, T007
# Spec: specs/001-phase1-console-app/spec.md#data-model
# Purpose: Task dataclass with validation

"""Data models for Phase 1 Todo Console App.

This module defines the Task dataclass with all required fields and validation logic.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

# Type alias for priority levels
Priority = Literal["High", "Medium", "Low"]


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique task identifier (sequential, auto-generated)
        title: Task title (required, 1-200 characters)
        description: Optional task description (max 1000 characters)
        completed: Completion status (False=pending, True=done)
        priority: Priority level (High/Medium/Low, default Medium)
        tags: List of category tags (max 5, each max 20 chars)
        created_at: Timestamp when task was created (immutable)
        updated_at: Timestamp of last modification (auto-updated)

    Example:
        >>> task = Task(id=1, title="Buy groceries")
        >>> task.completed
        False
        >>> task.priority
        'Medium'

    Raises:
        ValueError: If validation fails for any field
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: Priority = "Medium"
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate fields after initialization.

        Raises:
            ValueError: If any validation constraint is violated
        """
        # Title validation
        if not self.title or self.title.isspace():
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 200:
            raise ValueError(f"Task title too long: {len(self.title)} chars (max 200)")

        # Description validation
        if len(self.description) > 1000:
            raise ValueError(
                f"Description too long: {len(self.description)} chars (max 1000)"
            )

        # Priority validation
        if self.priority not in ("High", "Medium", "Low"):
            raise ValueError(f"Invalid priority: {self.priority}")

        # Tags validation
        if len(self.tags) > 5:
            raise ValueError(f"Too many tags: {len(self.tags)} (max 5)")
        for tag in self.tags:
            if len(tag) > 20:
                raise ValueError(f"Tag too long: '{tag}' ({len(tag)} chars, max 20)")
