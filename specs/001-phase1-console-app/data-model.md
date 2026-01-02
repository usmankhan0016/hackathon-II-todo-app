# Data Model: Phase 1 - Todo Console App

**Date**: 2026-01-02
**Feature**: 001-phase1-console-app

## Entity: Task

### Definition
A `Task` represents a single todo item with metadata for tracking status, priority, categorization, and timestamps.

### Fields

| Field | Type | Required | Default | Constraints | Immutable |
|-------|------|----------|---------|-------------|-----------|
| id | int | Yes | Auto | Positive integer, unique within session | Yes |
| title | str | Yes | - | 1-200 characters, not empty/whitespace | No |
| description | str | No | "" | Max 1000 characters | No |
| completed | bool | No | False | True (done) or False (pending) | No |
| priority | str | No | "Medium" | One of: "High", "Medium", "Low" | No |
| tags | list[str] | No | [] | Max 5 tags, each max 20 chars | No |
| created_at | datetime | Yes | Auto | ISO 8601 timestamp | Yes |
| updated_at | datetime | Yes | Auto | ISO 8601 timestamp, refreshed on update | No |

### State Machine

```
┌─────────┐
│   New   │
└────┬────┘
     │ create()
     ▼
┌──────────┐  toggle_complete()  ┌───────────┐
│ Pending  │◄───────────────────►│ Completed │
└──────────┘                     └───────────┘
     │                                 │
     │ update() [preserves status]     │
     ├─────────────────────────────────┤
     │                                 │
     ▼                                 ▼
┌──────────────────────────────────────────┐
│           delete() → Removed             │
└──────────────────────────────────────────┘
```

**States**:
- **New**: Task object created but not yet added to list
- **Pending**: Task exists in list, `completed=False`
- **Completed**: Task exists in list, `completed=True`
- **Removed**: Task deleted from list (no longer exists)

**Transitions**:
- `create()`: New → Pending
- `toggle_complete()`: Pending ↔ Completed
- `update()`: Pending → Pending OR Completed → Completed (status preserved)
- `delete()`: Pending/Completed → Removed

### Validation Rules

**Title**:
```python
# Valid
title = "Buy groceries"
title = "A"  # Minimum 1 character

# Invalid
title = ""           # Empty string → Error
title = "   "        # Whitespace only → Error
title = "x" * 201    # >200 characters → Error
```

**Description**:
```python
# Valid
description = ""                 # Empty allowed
description = "Any text here"
description = "x" * 1000        # Max 1000 characters

# Invalid
description = "x" * 1001        # >1000 characters → Error
```

**Priority**:
```python
# Valid (normalized to title case)
priority = "High" | "Medium" | "Low"
priority = "high" → "High"  # Case-insensitive input accepted

# Invalid
priority = "Critical"  # Not in allowed set → Error, defaults to "Medium"
priority = ""          # Empty → Error, defaults to "Medium"
```

**Tags**:
```python
# Valid
tags = []                              # Empty allowed
tags = ["work"]                        # Single tag
tags = ["work", "urgent", "home"]      # Multiple tags (max 5)

# Invalid
tags = ["a"] * 6                       # >5 tags → Error
tags = ["x" * 21]                      # Tag >20 chars → Error
```

**ID**:
```python
# Valid
id = 1                    # Positive integer
id = max_existing_id + 1  # Sequential

# Invalid (handled by task_manager)
id = 0      # Non-positive → Never generated
id = -1     # Negative → Never generated
id = 1.5    # Float → Type error (int required)
```

### Relationships

```
TaskList (Global in-memory state)
  │
  ├─► Task (id=1, title="Buy groceries")
  ├─► Task (id=2, title="Call mom")
  └─► Task (id=3, title="Finish report")
```

**Cardinality**:
- TaskList : Task = 1 : N (one list, zero or more tasks)
- Task : TaskList = N : 1 (many tasks belong to one list)

**Constraints**:
- Task IDs must be unique within the list
- IDs are never reused (even after deletion)
- List order is maintained (insertion order preserved)

### Example Instances

**Minimal Task** (required fields only):
```python
Task(
    id=1,
    title="Buy milk"
)
# Auto-generated: description="", completed=False, priority="Medium",
#                 tags=[], created_at=now(), updated_at=now()
```

**Complete Task** (all fields populated):
```python
Task(
    id=2,
    title="Finish project report",
    description="Include Q4 metrics and budget analysis",
    completed=False,
    priority="High",
    tags=["work", "deadline", "urgent"],
    created_at=datetime(2026, 1, 2, 10, 30, 0),
    updated_at=datetime(2026, 1, 2, 14, 15, 0)
)
```

**Completed Task**:
```python
Task(
    id=3,
    title="Call mom",
    description="Wish happy birthday",
    completed=True,  # Marked done
    priority="High",
    tags=["personal"],
    created_at=datetime(2026, 1, 1, 9, 0, 0),
    updated_at=datetime(2026, 1, 1, 17, 30, 0)  # When marked complete
)
```

## Implementation

### Dataclass Definition

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

# Type alias for priority
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
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: Priority = "Medium"
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate fields after initialization."""
        # Title validation
        if not self.title or self.title.isspace():
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 200:
            raise ValueError(f"Task title too long: {len(self.title)} chars (max 200)")

        # Description validation
        if len(self.description) > 1000:
            raise ValueError(f"Description too long: {len(self.description)} chars (max 1000)")

        # Priority validation
        if self.priority not in ("High", "Medium", "Low"):
            raise ValueError(f"Invalid priority: {self.priority}")

        # Tags validation
        if len(self.tags) > 5:
            raise ValueError(f"Too many tags: {len(self.tags)} (max 5)")
        for tag in self.tags:
            if len(tag) > 20:
                raise ValueError(f"Tag too long: '{tag}' ({len(tag)} chars, max 20)")
```

### Storage Structure

**Global State** (in `task_manager.py`):
```python
# In-memory task list (session-scoped)
tasks: list[Task] = []

# ID generation
def generate_next_id() -> int:
    """Generate next sequential task ID.

    Returns:
        1 if list is empty, otherwise max(existing IDs) + 1
    """
    return max([t.id for t in tasks], default=0) + 1
```

**Memory Footprint** (estimated):
- Per task: ~400 bytes (fields + overhead)
- 100 tasks: ~40 KB
- 1000 tasks: ~400 KB

**Conclusion**: In-memory storage acceptable for Phase 1 scope (<100 tasks typical)

## Query Patterns

### Get All Tasks
```python
def get_all_tasks() -> list[Task]:
    """Return all tasks in insertion order."""
    return tasks.copy()  # Return copy to prevent external modification
```

### Get Task By ID
```python
def get_task_by_id(task_id: int) -> Task | None:
    """Find task by ID.

    Returns:
        Task if found, None if not found
    """
    return next((t for t in tasks if t.id == task_id), None)
```

### Search Tasks
```python
def search_tasks(keyword: str) -> list[Task]:
    """Search tasks by keyword in title or description (case-insensitive).

    Args:
        keyword: Search term

    Returns:
        List of matching tasks
    """
    keyword_lower = keyword.lower()
    return [
        t for t in tasks
        if keyword_lower in t.title.lower() or keyword_lower in t.description.lower()
    ]
```

### Filter Tasks
```python
def filter_tasks(
    status: Literal["all", "pending", "completed"] | None = None,
    priority: Priority | None = None,
    tag: str | None = None
) -> list[Task]:
    """Filter tasks by status, priority, and/or tag.

    Returns:
        List of tasks matching all provided filters
    """
    filtered = tasks

    if status == "completed":
        filtered = [t for t in filtered if t.completed]
    elif status == "pending":
        filtered = [t for t in filtered if not t.completed]

    if priority:
        filtered = [t for t in filtered if t.priority == priority]

    if tag:
        filtered = [t for t in filtered if tag in t.tags]

    return filtered
```

### Sort Tasks
```python
def sort_tasks(
    tasks_to_sort: list[Task],
    by: Literal["id", "title", "priority", "created", "status"] = "id",
    descending: bool = False
) -> list[Task]:
    """Sort tasks by specified field.

    Returns:
        New sorted list (original unchanged)
    """
    priority_order = {"High": 3, "Medium": 2, "Low": 1}

    if by == "id":
        key_func = lambda t: t.id
    elif by == "title":
        key_func = lambda t: t.title.lower()
    elif by == "priority":
        key_func = lambda t: priority_order[t.priority]
    elif by == "created":
        key_func = lambda t: t.created_at
    elif by == "status":
        key_func = lambda t: t.completed
    else:
        raise ValueError(f"Invalid sort field: {by}")

    return sorted(tasks_to_sort, key=key_func, reverse=descending)
```

## Future Enhancements (Out of Scope for Phase 1)

- Due dates (`due_date: datetime | None`)
- Subtasks (`subtasks: list[Task]`)
- Attachments (`attachments: list[str]`)
- Recurring tasks (`recurrence: str | None`)
- Task history (`history: list[Change]`)
- Assignees (`assigned_to: str | None`)

These will be considered in Phase 2+ when persistence and multi-user support are added.
