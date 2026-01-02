# Add Sorting Logic

Generate standard sorting functions for task lists with multiple sort keys and ordering options.

## Instructions

When this skill is invoked, create a complete sorting function that allows users to sort tasks by various fields with ascending or descending order. The function should use Python's `sorted()` built-in with custom key functions.

### Input Required
- Sort keys needed (title, priority, status, date fields, custom fields)
- Task model structure (which fields are available)
- Feature context (what sorting scenario is needed)
- Task ID and Spec reference

### Core Sorting Pattern

```python
from typing import Literal, List
from models import Task

SortKey = Literal["title", "priority", "created_at", "status", "id"]

def sort_tasks(
    tasks: List[Task],
    key: SortKey = "created_at",
    reverse: bool = False
) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by specified key.

    Args:
        tasks (List[Task]): List of Task objects to sort
        key (SortKey): Field to sort by (default: "created_at")
        reverse (bool): True for descending order (default: False)

    Returns:
        List[Task]: Sorted list of tasks (new list, original unchanged)

    Example:
        >>> # Sort by title alphabetically
        >>> sorted_tasks = sort_tasks(all_tasks, key="title")
        >>> # Sort by priority (high to low)
        >>> sorted_tasks = sort_tasks(all_tasks, key="priority", reverse=True)
    """
    # Define sort key functions
    def get_sort_key(task: Task):
        if key == "title":
            return task.title.lower()  # Case-insensitive alphabetical
        elif key == "priority":
            # Map priority to numeric value (high=3, medium=2, low=1)
            priority_map = {"high": 3, "medium": 2, "low": 1}
            if hasattr(task, 'priority'):
                return priority_map.get(task.priority.lower(), 0)
            return 0
        elif key == "created_at":
            if hasattr(task, 'created_at'):
                return task.created_at
            return task.id  # Fallback to ID if no created_at
        elif key == "status":
            # Sort completed tasks to bottom by default
            return task.completed
        elif key == "id":
            return task.id
        else:
            return task.id  # Default fallback

    return sorted(tasks, key=get_sort_key, reverse=reverse)
```

---

## Standard Sort Templates

### Template 1: Basic Single-Key Sort

**Use Case:** Sort by one field only

```python
from typing import List
from models import Task

def sort_by_title(tasks: List[Task], reverse: bool = False) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks alphabetically by title (case-insensitive).

    Args:
        tasks (List[Task]): List of tasks to sort
        reverse (bool): True for Z-A, False for A-Z (default: False)

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> sorted_tasks = sort_by_title(all_tasks)
        >>> for task in sorted_tasks:
        ...     print(task.title)
    """
    return sorted(tasks, key=lambda t: t.title.lower(), reverse=reverse)


def sort_by_id(tasks: List[Task], reverse: bool = False) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by ID (chronological creation order).

    Args:
        tasks (List[Task]): List of tasks to sort
        reverse (bool): True for newest first, False for oldest first

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> sorted_tasks = sort_by_id(all_tasks, reverse=True)
    """
    return sorted(tasks, key=lambda t: t.id, reverse=reverse)


def sort_by_status(tasks: List[Task], reverse: bool = False) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by completion status.

    Args:
        tasks (List[Task]): List of tasks to sort
        reverse (bool): True for completed first, False for pending first

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> # Pending tasks first
        >>> sorted_tasks = sort_by_status(all_tasks)
    """
    return sorted(tasks, key=lambda t: t.completed, reverse=reverse)
```

---

### Template 2: Priority Sort

**Use Case:** Sort by priority levels (high > medium > low)

```python
from typing import List, Dict
from models import Task

def sort_by_priority(tasks: List[Task], reverse: bool = False) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by priority level (high > medium > low).

    Args:
        tasks (List[Task]): List of tasks to sort
        reverse (bool): True for low to high, False for high to low

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> # High priority first
        >>> sorted_tasks = sort_by_priority(all_tasks, reverse=True)
    """
    priority_map: Dict[str, int] = {
        "high": 3,
        "medium": 2,
        "low": 1
    }

    def get_priority_value(task: Task) -> int:
        if hasattr(task, 'priority') and task.priority:
            return priority_map.get(task.priority.lower(), 0)
        return 0  # No priority = lowest

    return sorted(tasks, key=get_priority_value, reverse=reverse)
```

---

### Template 3: Date Sort

**Use Case:** Sort by date fields (created, modified, due date)

```python
from typing import List, Optional
from datetime import datetime, date
from models import Task

def sort_by_created_date(tasks: List[Task], reverse: bool = False) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by creation date.

    Args:
        tasks (List[Task]): List of tasks to sort
        reverse (bool): True for newest first, False for oldest first

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> # Newest first
        >>> sorted_tasks = sort_by_created_date(all_tasks, reverse=True)
    """
    def get_created_date(task: Task) -> datetime:
        if hasattr(task, 'created_at') and task.created_at:
            return task.created_at
        # Fallback: use epoch for tasks without created_at
        return datetime.min

    return sorted(tasks, key=get_created_date, reverse=reverse)


def sort_by_due_date(tasks: List[Task], reverse: bool = False) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by due date (tasks without due date go to end).

    Args:
        tasks (List[Task]): List of tasks to sort
        reverse (bool): True for latest first, False for earliest first

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> # Earliest due date first
        >>> sorted_tasks = sort_by_due_date(all_tasks)
    """
    def get_due_date(task: Task) -> date:
        if hasattr(task, 'due_date') and task.due_date:
            return task.due_date
        # Tasks without due date go to end
        return date.max if not reverse else date.min

    return sorted(tasks, key=get_due_date, reverse=reverse)


def sort_by_modified_date(tasks: List[Task], reverse: bool = False) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by last modified date.

    Args:
        tasks (List[Task]): List of tasks to sort
        reverse (bool): True for most recently modified first

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> # Recently modified first
        >>> sorted_tasks = sort_by_modified_date(all_tasks, reverse=True)
    """
    def get_modified_date(task: Task) -> datetime:
        if hasattr(task, 'modified_at') and task.modified_at:
            return task.modified_at
        # Fallback to created_at or epoch
        if hasattr(task, 'created_at') and task.created_at:
            return task.created_at
        return datetime.min

    return sorted(tasks, key=get_modified_date, reverse=reverse)
```

---

### Template 4: Multi-Key Sort (Composite)

**Use Case:** Sort by multiple fields (e.g., priority then title)

```python
from typing import List, Tuple, Dict
from models import Task

def sort_by_priority_and_title(tasks: List[Task], reverse: bool = False) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by priority (high to low), then by title alphabetically.

    Args:
        tasks (List[Task]): List of tasks to sort
        reverse (bool): Reverses the entire sort order

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> # High priority first, then alphabetical within each priority
        >>> sorted_tasks = sort_by_priority_and_title(all_tasks)
    """
    priority_map: Dict[str, int] = {"high": 3, "medium": 2, "low": 1}

    def get_sort_key(task: Task) -> Tuple[int, str]:
        # Priority (descending) then title (ascending)
        priority_value = priority_map.get(
            task.priority.lower() if hasattr(task, 'priority') and task.priority else "",
            0
        )
        # Negate priority so higher priorities come first
        return (-priority_value, task.title.lower())

    return sorted(tasks, key=get_sort_key, reverse=reverse)


def sort_by_status_and_priority(tasks: List[Task], reverse: bool = False) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by status (pending first), then by priority.

    Args:
        tasks (List[Task]): List of tasks to sort
        reverse (bool): Reverses the entire sort order

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> # Pending high-priority tasks first
        >>> sorted_tasks = sort_by_status_and_priority(all_tasks)
    """
    priority_map: Dict[str, int] = {"high": 3, "medium": 2, "low": 1}

    def get_sort_key(task: Task) -> Tuple[bool, int]:
        priority_value = priority_map.get(
            task.priority.lower() if hasattr(task, 'priority') and task.priority else "",
            0
        )
        # Status (False=pending first), then priority (high first)
        return (task.completed, -priority_value)

    return sorted(tasks, key=get_sort_key, reverse=reverse)


def sort_by_due_date_and_priority(tasks: List[Task], reverse: bool = False) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by due date (earliest first), then by priority (high first).

    Args:
        tasks (List[Task]): List of tasks to sort
        reverse (bool): Reverses the entire sort order

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> # Due soon + high priority first
        >>> sorted_tasks = sort_by_due_date_and_priority(all_tasks)
    """
    from datetime import date

    priority_map: Dict[str, int] = {"high": 3, "medium": 2, "low": 1}

    def get_sort_key(task: Task) -> Tuple[date, int]:
        due_date = task.due_date if hasattr(task, 'due_date') and task.due_date else date.max
        priority_value = priority_map.get(
            task.priority.lower() if hasattr(task, 'priority') and task.priority else "",
            0
        )
        # Due date (ascending), then priority (descending)
        return (due_date, -priority_value)

    return sorted(tasks, key=get_sort_key, reverse=reverse)
```

---

### Template 5: Generic Sort (Type-Safe)

**Use Case:** Flexible sorting with type safety using Literal types

```python
from typing import List, Literal, Callable, Dict
from models import Task

SortKey = Literal["id", "title", "priority", "status", "created_at", "due_date"]
SortOrder = Literal["asc", "desc"]

def sort_tasks(
    tasks: List[Task],
    key: SortKey = "id",
    order: SortOrder = "asc"
) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by specified key with type-safe field names.

    Args:
        tasks (List[Task]): List of tasks to sort
        key (SortKey): Field to sort by
        order (SortOrder): "asc" for ascending, "desc" for descending

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> sorted_tasks = sort_tasks(all_tasks, key="title", order="asc")
        >>> sorted_tasks = sort_tasks(all_tasks, key="priority", order="desc")
    """
    from datetime import datetime, date

    priority_map: Dict[str, int] = {"high": 3, "medium": 2, "low": 1}

    # Define key extraction functions
    key_functions: Dict[SortKey, Callable[[Task], any]] = {
        "id": lambda t: t.id,
        "title": lambda t: t.title.lower(),
        "priority": lambda t: priority_map.get(
            t.priority.lower() if hasattr(t, 'priority') and t.priority else "",
            0
        ),
        "status": lambda t: t.completed,
        "created_at": lambda t: t.created_at if hasattr(t, 'created_at') and t.created_at else datetime.min,
        "due_date": lambda t: t.due_date if hasattr(t, 'due_date') and t.due_date else date.max,
    }

    sort_key_fn = key_functions.get(key, lambda t: t.id)
    reverse = (order == "desc")

    return sorted(tasks, key=sort_key_fn, reverse=reverse)


def sort_tasks_multi(
    tasks: List[Task],
    keys: List[Tuple[SortKey, SortOrder]]
) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by multiple keys in priority order.

    Args:
        tasks (List[Task]): List of tasks to sort
        keys (List[Tuple[SortKey, SortOrder]]): List of (field, order) tuples

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> # Sort by priority (desc), then title (asc)
        >>> sorted_tasks = sort_tasks_multi(
        ...     all_tasks,
        ...     [("priority", "desc"), ("title", "asc")]
        ... )
    """
    result = tasks.copy()

    # Apply sorts in reverse order (last key first)
    # This ensures primary sort key has final say
    for sort_key, sort_order in reversed(keys):
        result = sort_tasks(result, key=sort_key, order=sort_order)

    return result
```

---

### Template 6: Custom Sort with Predicate

**Use Case:** Sort by custom logic or calculated values

```python
from typing import List, Callable, Any
from models import Task

def sort_by_custom_key(
    tasks: List[Task],
    key_fn: Callable[[Task], Any],
    reverse: bool = False
) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks using a custom key function.

    Args:
        tasks (List[Task]): List of tasks to sort
        key_fn (Callable[[Task], Any]): Function that extracts sort key from task
        reverse (bool): True for descending order

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> # Sort by title length
        >>> sorted_tasks = sort_by_custom_key(
        ...     all_tasks,
        ...     key_fn=lambda t: len(t.title)
        ... )
        >>> # Sort by description word count
        >>> sorted_tasks = sort_by_custom_key(
        ...     all_tasks,
        ...     key_fn=lambda t: len(t.description.split())
        ... )
    """
    return sorted(tasks, key=key_fn, reverse=reverse)


def sort_by_title_length(tasks: List[Task], reverse: bool = False) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by title length.

    Args:
        tasks (List[Task]): List of tasks to sort
        reverse (bool): True for longest first

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> sorted_tasks = sort_by_title_length(all_tasks)
    """
    return sorted(tasks, key=lambda t: len(t.title), reverse=reverse)


def sort_by_urgency_score(tasks: List[Task], reverse: bool = True) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Sort tasks by calculated urgency score (priority + due date proximity).

    Args:
        tasks (List[Task]): List of tasks to sort
        reverse (bool): True for most urgent first (default)

    Returns:
        List[Task]: Sorted list of tasks

    Example:
        >>> # Most urgent tasks first
        >>> sorted_tasks = sort_by_urgency_score(all_tasks)
    """
    from datetime import date

    priority_scores = {"high": 3, "medium": 2, "low": 1}

    def calculate_urgency(task: Task) -> float:
        # Priority component (0-3)
        priority_score = priority_scores.get(
            task.priority.lower() if hasattr(task, 'priority') and task.priority else "",
            0
        )

        # Due date component (0-3 based on proximity)
        due_score = 0
        if hasattr(task, 'due_date') and task.due_date:
            days_until_due = (task.due_date - date.today()).days
            if days_until_due < 0:
                due_score = 3  # Overdue
            elif days_until_due == 0:
                due_score = 3  # Due today
            elif days_until_due <= 3:
                due_score = 2  # Due soon
            elif days_until_due <= 7:
                due_score = 1  # Due this week
            else:
                due_score = 0  # Due later

        # Completion penalty (completed tasks less urgent)
        completion_penalty = -10 if task.completed else 0

        return priority_score + due_score + completion_penalty

    return sorted(tasks, key=calculate_urgency, reverse=reverse)
```

---

## Sorting Pattern Guidelines

### Rule 1: Immutability
Always return a new sorted list; never modify the original
```python
# ✅ Good: Return new list
return sorted(tasks, key=lambda t: t.title)

# ❌ Bad: Modify in place
tasks.sort(key=lambda t: t.title)
return tasks
```

### Rule 2: Case-Insensitive String Sorting
Use `.lower()` for alphabetical sorts
```python
# ✅ Good: Case-insensitive
return sorted(tasks, key=lambda t: t.title.lower())

# ❌ Bad: Case-sensitive
return sorted(tasks, key=lambda t: t.title)
```

### Rule 3: Handle Missing Attributes
Provide fallback values for optional fields
```python
# ✅ Good: Safe with fallback
def get_priority(task: Task) -> int:
    if hasattr(task, 'priority') and task.priority:
        return priority_map.get(task.priority.lower(), 0)
    return 0

# ❌ Bad: May raise AttributeError
return sorted(tasks, key=lambda t: t.priority)
```

### Rule 4: Stable Sorting
Python's `sorted()` is stable; use this for multi-key sorts
```python
# ✅ Good: Leverage stable sort
tasks = sorted(tasks, key=lambda t: t.title)  # Secondary sort
tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)  # Primary sort

# ✅ Better: Use tuple for composite key
tasks = sorted(tasks, key=lambda t: (-t.priority, t.title))
```

### Rule 5: Meaningful Defaults
Choose sensible default sort orders
```python
# ✅ Good: Newest first makes sense for created_at
def sort_by_created_date(tasks, reverse=True):  # Newest first by default

# ✅ Good: A-Z makes sense for title
def sort_by_title(tasks, reverse=False):  # A-Z by default
```

---

## Priority Mapping Pattern

```python
# Standard priority mapping (use consistently)
PRIORITY_MAP = {
    "high": 3,
    "medium": 2,
    "low": 1,
    "none": 0,
    "": 0,
}

# For reverse priority (low to high)
REVERSE_PRIORITY_MAP = {
    "low": 3,
    "medium": 2,
    "high": 1,
    "none": 0,
    "": 0,
}
```

---

## CLI Integration Pattern

```python
# cli.py
def get_sort_options() -> tuple[str, bool]:
    """
    Prompt user for sort preferences.

    Returns:
        tuple[str, bool]: (sort_key, reverse)
    """
    print("\n--- Sort Options ---")
    print("1. Title (A-Z)")
    print("2. Priority (High to Low)")
    print("3. Created Date (Newest first)")
    print("4. Status (Pending first)")
    print("5. ID (Oldest first)")

    choice = input("\nSort by (1-5): ").strip()

    sort_map = {
        "1": ("title", False),
        "2": ("priority", True),
        "3": ("created_at", True),
        "4": ("status", False),
        "5": ("id", False),
    }

    return sort_map.get(choice, ("id", False))


# main.py
def handle_sort():
    """Handle sort command."""
    from cli import get_sort_options, display_task_list
    from task_manager import sort_tasks, get_all_tasks

    sort_key, reverse = get_sort_options()
    all_tasks = get_all_tasks()
    sorted_list = sort_tasks(all_tasks, key=sort_key, reverse=reverse)

    display_task_list(sorted_list, f"Tasks (sorted by {sort_key})")
```

---

## Testing Pattern

```python
# tests/test_task_manager.py
import pytest
from models import Task
from task_manager import sort_tasks, sort_by_priority

def test_sort_by_title():
    tasks = [
        Task(id=1, title="Zebra"),
        Task(id=2, title="Apple"),
        Task(id=3, title="Mango"),
    ]
    result = sort_tasks(tasks, key="title")
    assert result[0].title == "Apple"
    assert result[1].title == "Mango"
    assert result[2].title == "Zebra"

def test_sort_by_title_case_insensitive():
    tasks = [
        Task(id=1, title="zebra"),
        Task(id=2, title="APPLE"),
        Task(id=3, title="Mango"),
    ]
    result = sort_tasks(tasks, key="title")
    assert result[0].title == "APPLE"

def test_sort_by_priority():
    tasks = [
        Task(id=1, title="Task 1", priority="low"),
        Task(id=2, title="Task 2", priority="high"),
        Task(id=3, title="Task 3", priority="medium"),
    ]
    result = sort_by_priority(tasks, reverse=True)
    assert result[0].priority == "high"
    assert result[1].priority == "medium"
    assert result[2].priority == "low"

def test_sort_reverse():
    tasks = [
        Task(id=1, title="A"),
        Task(id=2, title="B"),
        Task(id=3, title="C"),
    ]
    result = sort_tasks(tasks, key="title", reverse=True)
    assert result[0].title == "C"
    assert result[2].title == "A"

def test_sort_returns_new_list():
    tasks = [Task(id=1, title="B"), Task(id=2, title="A")]
    result = sort_tasks(tasks, key="title")
    assert result is not tasks  # Different list object
    assert tasks[0].title == "B"  # Original unchanged
```

---

## Usage

To use this skill:

1. Identify sort requirements:
   - Which fields can be sorted?
   - What's the natural order for each field?
   - Are multi-key sorts needed?

2. Choose template:
   - Single field → Template 1-3
   - Multiple fields → Template 4
   - Type-safe API → Template 5
   - Custom logic → Template 6

3. Customize:
   - Update field references
   - Add task/spec references
   - Define priority mappings
   - Set sensible defaults

4. Add to `task_manager.py`

5. Create CLI integration in `cli.py` and `main.py`

6. Write tests in `tests/test_task_manager.py`

---

## Best Practices

1. **Immutability:** Always use `sorted()`, never `.sort()`
2. **Case-Insensitive:** Use `.lower()` for string comparisons
3. **Safe Access:** Use `hasattr()` and provide fallbacks
4. **Type Safety:** Use `Literal` types for valid sort keys
5. **Stable Sort:** Leverage Python's stable sort for multi-key
6. **Tuple Keys:** Use tuples for composite sort keys
7. **Meaningful Defaults:** Choose intuitive default orders
8. **Document Order:** Clearly state sort direction in docstrings
9. **Test Both Directions:** Test both ascending and descending
10. **Performance:** `sorted()` is O(n log n), acceptable for small lists

---

## Output Format

Generated sorting functions are ready to add to:
```
src/task_manager.py
```

With corresponding CLI integration in:
```
src/cli.py
src/main.py
```

And tests in:
```
tests/test_task_manager.py
```
