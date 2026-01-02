# Task: T008
# Spec: specs/001-phase1-console-app/spec.md#business-logic
# Purpose: In-memory CRUD operations for task management

"""Task management module for Phase 1 Todo Console App.

This module provides all business logic for CRUD operations on tasks.
All tasks are stored in-memory using a Python list (no persistence).
"""

from datetime import datetime
from src.phase1.models import Task, Priority

# Global in-memory task list (session-scoped, data lost on exit)
tasks: list[Task] = []

# Global sort state (session-scoped, persists across view operations)
current_sort: dict[str, str | bool] = {"by": "id", "descending": False}


def generate_next_id() -> int:
    """Generate next sequential task ID.

    Uses max(existing IDs) + 1 strategy to handle deletions correctly.
    IDs are never reused within a session.

    Returns:
        int: Next available ID (1 if list empty, max_id + 1 otherwise)

    Example:
        >>> tasks = []
        >>> generate_next_id()
        1
        >>> tasks = [Task(id=1, title="Test"), Task(id=3, title="Test")]
        >>> generate_next_id()
        4
    """
    return max([t.id for t in tasks], default=0) + 1


def add_task(
    title: str,
    description: str = "",
    priority: Priority = "Medium",
    tags: list[str] | None = None,
) -> Task:
    """Create and add a new task to the list.

    Args:
        title: Task title (1-200 characters, required)
        description: Optional task description (max 1000 characters)
        priority: Priority level (High/Medium/Low, default Medium)
        tags: List of category tags (max 5, each max 20 chars)

    Returns:
        Task: The newly created task with auto-generated ID and timestamps

    Raises:
        ValueError: If task validation fails

    Example:
        >>> task = add_task("Buy groceries", priority="High", tags=["home", "urgent"])
        >>> task.id
        1
        >>> task.completed
        False
    """
    if tags is None:
        tags = []

    task_id = generate_next_id()
    now = datetime.now()
    task = Task(
        id=task_id,
        title=title,
        description=description,
        priority=priority,
        tags=tags,
        created_at=now,
        updated_at=now,
    )
    tasks.append(task)
    return task


def get_all_tasks() -> list[Task]:
    """Return all tasks in insertion order.

    Returns a copy to prevent external modification of the global list.

    Returns:
        list[Task]: Copy of all tasks

    Example:
        >>> all_tasks = get_all_tasks()
        >>> len(all_tasks)
        3
    """
    return tasks.copy()


def get_task_by_id(task_id: int) -> Task | None:
    """Find task by ID.

    Args:
        task_id: Unique task identifier

    Returns:
        Task | None: Task if found, None if not found

    Example:
        >>> task = get_task_by_id(1)
        >>> task.title if task else "Not found"
        'Buy groceries'
    """
    return next((t for t in tasks if t.id == task_id), None)


def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
) -> bool:
    """Update task title and/or description.

    Preserves created_at timestamp, updates updated_at to current time.

    Args:
        task_id: Unique task identifier
        title: New title (if provided)
        description: New description (if provided)

    Returns:
        bool: True if task updated, False if task not found

    Example:
        >>> update_task(1, title="Buy groceries and household items")
        True
        >>> update_task(999)
        False
    """
    task = get_task_by_id(task_id)
    if not task:
        return False

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description

    task.updated_at = datetime.now()
    return True


def delete_task(task_id: int) -> bool:
    """Remove task from list.

    Args:
        task_id: Unique task identifier

    Returns:
        bool: True if task deleted, False if task not found

    Example:
        >>> delete_task(1)
        True
        >>> delete_task(999)
        False
    """
    task = get_task_by_id(task_id)
    if not task:
        return False

    tasks.remove(task)
    return True


def toggle_complete(task_id: int) -> bool:
    """Toggle task completion status.

    Flips completed status (True ↔ False) and updates timestamp.

    Args:
        task_id: Unique task identifier

    Returns:
        bool: True if toggled, False if task not found

    Example:
        >>> toggle_complete(1)  # Pending → Completed
        True
        >>> toggle_complete(1)  # Completed → Pending
        True
    """
    task = get_task_by_id(task_id)
    if not task:
        return False

    task.completed = not task.completed
    task.updated_at = datetime.now()
    return True


def search_tasks(keyword: str) -> list[Task]:
    """Search tasks by keyword in title or description (case-insensitive).

    Args:
        keyword: Search term

    Returns:
        list[Task]: List of matching tasks

    Example:
        >>> results = search_tasks("meeting")
        >>> len(results)
        3
    """
    keyword_lower = keyword.lower()
    return [
        t
        for t in tasks
        if keyword_lower in t.title.lower() or keyword_lower in t.description.lower()
    ]


def filter_tasks(
    status: Literal["all", "pending", "completed"] | None = None,
    priority: Priority | None = None,
    tag: str | None = None,
) -> list[Task]:
    """Filter tasks by status, priority, and/or tag.

    Args:
        status: Filter by completion status (all/pending/completed)
        priority: Filter by priority level (High/Medium/Low)
        tag: Filter by tag (must be in task's tags list)

    Returns:
        list[Task]: List of tasks matching all provided filters

    Example:
        >>> high_priority_tasks = filter_tasks(priority="High")
        >>> pending_work_tasks = filter_tasks(status="pending", tag="work")
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


def sort_tasks(
    tasks_to_sort: list[Task],
    by: Literal["id", "title", "priority", "created", "status"] = "id",
    descending: bool = False,
) -> list[Task]:
    """Sort tasks by specified field.

    Args:
        tasks_to_sort: List of tasks to sort
        by: Sort field (id/title/priority/created/status)
        descending: Sort descending if True, ascending if False

    Returns:
        list[Task]: New sorted list (original unchanged)

    Raises:
        ValueError: If sort field is invalid

    Example:
        >>> sorted_tasks = sort_tasks(get_all_tasks(), by="priority", descending=True)
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


def get_task_stats() -> dict[str, int]:
    """Get task count statistics.

    Returns:
        dict[str, int]: Dictionary with total, completed, and pending counts

    Example:
        >>> stats = get_task_stats()
        >>> stats
        {'total': 10, 'completed': 3, 'pending': 7}
    """
    total = len(tasks)
    completed = sum(1 for t in tasks if t.completed)
    pending = total - completed
    return {"total": total, "completed": completed, "pending": pending}
