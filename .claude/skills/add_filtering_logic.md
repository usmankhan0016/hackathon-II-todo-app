# Add Filtering Logic

Generate standard filtering functions for task lists with multiple criteria support.

## Instructions

When this skill is invoked, create a complete filtering function that allows users to filter tasks by various criteria. The function should be flexible, composable, and follow functional programming principles.

### Input Required
- Filter criteria needed (status, priority, tag, search, date, custom fields)
- Task model structure (which fields are available)
- Feature context (what filtering scenario is needed)
- Task ID and Spec reference

### Core Filtering Pattern

```python
def filter_tasks(
    tasks: list[Task],
    status: str | None = None,
    priority: str | None = None,
    tag: str | None = None,
    search: str | None = None
) -> list[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Filter tasks by multiple criteria.

    Args:
        tasks (list[Task]): List of Task objects to filter
        status (str | None): "pending" or "completed" (optional)
        priority (str | None): "high", "medium", or "low" (optional)
        tag (str | None): Tag to search for (optional)
        search (str | None): Keyword search in title/description (optional)

    Returns:
        list[Task]: Filtered list of tasks (new list, original unchanged)

    Example:
        >>> filtered = filter_tasks(all_tasks, status="pending", priority="high")
        >>> for task in filtered:
        ...     print(task.title)
    """
    # Start with full list (create copy to avoid mutation)
    filtered = tasks.copy()

    # Apply status filter
    if status is not None:
        status_lower = status.lower()
        if status_lower == "pending":
            filtered = [t for t in filtered if not t.completed]
        elif status_lower == "completed":
            filtered = [t for t in filtered if t.completed]

    # Apply priority filter
    if priority is not None:
        priority_lower = priority.lower()
        filtered = [t for t in filtered if hasattr(t, 'priority') and t.priority.lower() == priority_lower]

    # Apply tag filter
    if tag is not None:
        tag_lower = tag.lower()
        filtered = [t for t in filtered if hasattr(t, 'tags') and tag_lower in [tag.lower() for tag in t.tags]]

    # Apply search filter (case-insensitive)
    if search is not None:
        search_lower = search.lower()
        filtered = [
            t for t in filtered
            if search_lower in t.title.lower() or search_lower in t.description.lower()
        ]

    return filtered
```

---

## Standard Filter Templates

### Template 1: Basic Status Filter

**Use Case:** Filter by completion status only

```python
from typing import List
from models import Task

def filter_by_status(tasks: List[Task], completed: bool) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Filter tasks by completion status.

    Args:
        tasks (List[Task]): List of tasks to filter
        completed (bool): True for completed tasks, False for pending

    Returns:
        List[Task]: Filtered list of tasks

    Example:
        >>> pending = filter_by_status(all_tasks, completed=False)
        >>> print(f"Found {len(pending)} pending tasks")
    """
    return [task for task in tasks if task.completed == completed]


def get_pending_tasks(tasks: List[Task]) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Get all pending (incomplete) tasks.

    Args:
        tasks (List[Task]): List of tasks

    Returns:
        List[Task]: All pending tasks

    Example:
        >>> pending = get_pending_tasks(all_tasks)
    """
    return filter_by_status(tasks, completed=False)


def get_completed_tasks(tasks: List[Task]) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Get all completed tasks.

    Args:
        tasks (List[Task]): List of tasks

    Returns:
        List[Task]: All completed tasks

    Example:
        >>> completed = get_completed_tasks(all_tasks)
    """
    return filter_by_status(tasks, completed=True)
```

---

### Template 2: Priority Filter

**Use Case:** Filter by priority level

```python
from typing import List, Optional
from models import Task

def filter_by_priority(tasks: List[Task], priority: str) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Filter tasks by priority level.

    Args:
        tasks (List[Task]): List of tasks to filter
        priority (str): Priority level ("high", "medium", "low")

    Returns:
        List[Task]: Tasks matching the priority level

    Raises:
        ValueError: If priority is not "high", "medium", or "low"

    Example:
        >>> urgent = filter_by_priority(all_tasks, "high")
        >>> print(f"{len(urgent)} high-priority tasks")
    """
    valid_priorities = ["high", "medium", "low"]
    priority_lower = priority.lower()

    if priority_lower not in valid_priorities:
        raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")

    return [
        task for task in tasks
        if hasattr(task, 'priority') and task.priority.lower() == priority_lower
    ]


def get_high_priority_tasks(tasks: List[Task]) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Get all high-priority tasks.

    Args:
        tasks (List[Task]): List of tasks

    Returns:
        List[Task]: All high-priority tasks
    """
    return filter_by_priority(tasks, "high")
```

---

### Template 3: Search Filter

**Use Case:** Keyword search in title and description

```python
from typing import List
from models import Task

def search_tasks(tasks: List[Task], keyword: str) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Search tasks by keyword in title or description (case-insensitive).

    Args:
        tasks (List[Task]): List of tasks to search
        keyword (str): Keyword to search for

    Returns:
        List[Task]: Tasks containing the keyword

    Example:
        >>> results = search_tasks(all_tasks, "urgent")
        >>> for task in results:
        ...     print(f"Found: {task.title}")
    """
    if not keyword:
        return tasks.copy()

    keyword_lower = keyword.lower()
    return [
        task for task in tasks
        if keyword_lower in task.title.lower() or keyword_lower in task.description.lower()
    ]
```

---

### Template 4: Tag Filter

**Use Case:** Filter by tags/labels

```python
from typing import List
from models import Task

def filter_by_tag(tasks: List[Task], tag: str) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Filter tasks that have a specific tag.

    Args:
        tasks (List[Task]): List of tasks to filter
        tag (str): Tag to search for (case-insensitive)

    Returns:
        List[Task]: Tasks containing the tag

    Example:
        >>> work_tasks = filter_by_tag(all_tasks, "work")
        >>> print(f"{len(work_tasks)} work-related tasks")
    """
    if not tag:
        return tasks.copy()

    tag_lower = tag.lower()
    return [
        task for task in tasks
        if hasattr(task, 'tags') and tag_lower in [t.lower() for t in task.tags]
    ]


def filter_by_any_tag(tasks: List[Task], tags: List[str]) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Filter tasks that have any of the specified tags.

    Args:
        tasks (List[Task]): List of tasks to filter
        tags (List[str]): List of tags to search for

    Returns:
        List[Task]: Tasks containing at least one of the tags

    Example:
        >>> tagged = filter_by_any_tag(all_tasks, ["work", "urgent"])
    """
    if not tags:
        return tasks.copy()

    tags_lower = [tag.lower() for tag in tags]
    return [
        task for task in tasks
        if hasattr(task, 'tags') and any(t.lower() in tags_lower for t in task.tags)
    ]


def filter_by_all_tags(tasks: List[Task], tags: List[str]) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Filter tasks that have all of the specified tags.

    Args:
        tasks (List[Task]): List of tasks to filter
        tags (List[str]): List of tags that must all be present

    Returns:
        List[Task]: Tasks containing all of the tags

    Example:
        >>> tagged = filter_by_all_tags(all_tasks, ["work", "urgent"])
    """
    if not tags:
        return tasks.copy()

    tags_lower = [tag.lower() for tag in tags]
    return [
        task for task in tasks
        if hasattr(task, 'tags') and all(t in [tag.lower() for tag in task.tags] for t in tags_lower)
    ]
```

---

### Template 5: Date Range Filter

**Use Case:** Filter by due date or creation date

```python
from typing import List, Optional
from datetime import datetime, date
from models import Task

def filter_by_due_date(
    tasks: List[Task],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Filter tasks by due date range.

    Args:
        tasks (List[Task]): List of tasks to filter
        start_date (Optional[date]): Minimum due date (inclusive)
        end_date (Optional[date]): Maximum due date (inclusive)

    Returns:
        List[Task]: Tasks within the date range

    Example:
        >>> from datetime import date
        >>> today = date.today()
        >>> due_soon = filter_by_due_date(all_tasks, end_date=today)
    """
    filtered = tasks.copy()

    if start_date is not None:
        filtered = [
            task for task in filtered
            if hasattr(task, 'due_date') and task.due_date and task.due_date >= start_date
        ]

    if end_date is not None:
        filtered = [
            task for task in filtered
            if hasattr(task, 'due_date') and task.due_date and task.due_date <= end_date
        ]

    return filtered


def get_overdue_tasks(tasks: List[Task]) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Get all tasks that are past their due date and not completed.

    Args:
        tasks (List[Task]): List of tasks

    Returns:
        List[Task]: Overdue tasks

    Example:
        >>> overdue = get_overdue_tasks(all_tasks)
        >>> print(f"You have {len(overdue)} overdue tasks!")
    """
    today = date.today()
    return [
        task for task in tasks
        if hasattr(task, 'due_date')
        and task.due_date
        and task.due_date < today
        and not task.completed
    ]


def get_due_today(tasks: List[Task]) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Get all tasks due today.

    Args:
        tasks (List[Task]): List of tasks

    Returns:
        List[Task]: Tasks due today

    Example:
        >>> today_tasks = get_due_today(all_tasks)
    """
    today = date.today()
    return [
        task for task in tasks
        if hasattr(task, 'due_date') and task.due_date == today
    ]
```

---

### Template 6: Multi-Criteria Filter (Composable)

**Use Case:** Filter by any combination of criteria

```python
from typing import List, Optional
from datetime import date
from models import Task

def filter_tasks(
    tasks: List[Task],
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    due_before: Optional[date] = None,
    due_after: Optional[date] = None
) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Filter tasks by multiple criteria (all filters are optional and composable).

    Args:
        tasks (List[Task]): List of tasks to filter
        completed (Optional[bool]): Filter by completion status
        priority (Optional[str]): Filter by priority ("high", "medium", "low")
        tag (Optional[str]): Filter by tag (case-insensitive)
        search (Optional[str]): Keyword search in title/description
        due_before (Optional[date]): Filter tasks due before this date
        due_after (Optional[date]): Filter tasks due after this date

    Returns:
        List[Task]: Filtered list of tasks matching all criteria

    Example:
        >>> # Get high-priority pending tasks containing "report"
        >>> filtered = filter_tasks(
        ...     all_tasks,
        ...     completed=False,
        ...     priority="high",
        ...     search="report"
        ... )
        >>> print(f"Found {len(filtered)} matching tasks")
    """
    # Start with copy of all tasks
    filtered = tasks.copy()

    # Apply completion status filter
    if completed is not None:
        filtered = [t for t in filtered if t.completed == completed]

    # Apply priority filter
    if priority is not None:
        priority_lower = priority.lower()
        valid_priorities = ["high", "medium", "low"]
        if priority_lower not in valid_priorities:
            return []  # Invalid priority returns empty list
        filtered = [
            t for t in filtered
            if hasattr(t, 'priority') and t.priority.lower() == priority_lower
        ]

    # Apply tag filter
    if tag is not None:
        tag_lower = tag.lower()
        filtered = [
            t for t in filtered
            if hasattr(t, 'tags') and tag_lower in [tag.lower() for tag in t.tags]
        ]

    # Apply search filter
    if search is not None:
        search_lower = search.lower()
        filtered = [
            t for t in filtered
            if search_lower in t.title.lower() or search_lower in t.description.lower()
        ]

    # Apply due_before filter
    if due_before is not None:
        filtered = [
            t for t in filtered
            if hasattr(t, 'due_date') and t.due_date and t.due_date <= due_before
        ]

    # Apply due_after filter
    if due_after is not None:
        filtered = [
            t for t in filtered
            if hasattr(t, 'due_date') and t.due_date and t.due_date >= due_after
        ]

    return filtered
```

---

### Template 7: Custom Field Filter (Generic)

**Use Case:** Filter by any custom field

```python
from typing import List, Any, Callable
from models import Task

def filter_by_field(
    tasks: List[Task],
    field_name: str,
    value: Any,
    comparison: str = "equals"
) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Generic filter by any task field with comparison operators.

    Args:
        tasks (List[Task]): List of tasks to filter
        field_name (str): Name of the field to filter by
        value (Any): Value to compare against
        comparison (str): Comparison operator ("equals", "contains", "gt", "lt", "gte", "lte")

    Returns:
        List[Task]: Tasks matching the filter criteria

    Example:
        >>> # Get tasks with priority "high"
        >>> high = filter_by_field(all_tasks, "priority", "high")
        >>> # Get tasks with ID greater than 5
        >>> recent = filter_by_field(all_tasks, "id", 5, "gt")
    """
    def matches(task: Task) -> bool:
        if not hasattr(task, field_name):
            return False

        field_value = getattr(task, field_name)

        if comparison == "equals":
            return field_value == value
        elif comparison == "contains":
            return value.lower() in str(field_value).lower()
        elif comparison == "gt":
            return field_value > value
        elif comparison == "lt":
            return field_value < value
        elif comparison == "gte":
            return field_value >= value
        elif comparison == "lte":
            return field_value <= value
        else:
            return False

    return [task for task in tasks if matches(task)]


def filter_by_predicate(tasks: List[Task], predicate: Callable[[Task], bool]) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Filter tasks using a custom predicate function.

    Args:
        tasks (List[Task]): List of tasks to filter
        predicate (Callable[[Task], bool]): Function that returns True for tasks to include

    Returns:
        List[Task]: Tasks for which predicate returns True

    Example:
        >>> # Get tasks with long descriptions
        >>> long_desc = filter_by_predicate(
        ...     all_tasks,
        ...     lambda t: len(t.description) > 100
        ... )
        >>> # Get high-priority incomplete tasks
        >>> urgent = filter_by_predicate(
        ...     all_tasks,
        ...     lambda t: hasattr(t, 'priority') and t.priority == "high" and not t.completed
        ... )
    """
    return [task for task in tasks if predicate(task)]
```

---

## Filter Pattern Guidelines

### Rule 1: Immutability
Always return a new list; never modify the original
```python
# ✅ Good: Return new list
filtered = tasks.copy()
return [t for t in filtered if condition]

# ❌ Bad: Modify original
for task in tasks:
    if not condition:
        tasks.remove(task)
return tasks
```

### Rule 2: Case-Insensitive String Matching
Always use `.lower()` for string comparisons
```python
# ✅ Good: Case-insensitive
search_lower = search.lower()
filtered = [t for t in tasks if search_lower in t.title.lower()]

# ❌ Bad: Case-sensitive
filtered = [t for t in tasks if search in t.title]
```

### Rule 3: Handle Missing Attributes
Use `hasattr()` before accessing optional fields
```python
# ✅ Good: Check attribute exists
filtered = [t for t in tasks if hasattr(t, 'priority') and t.priority == "high"]

# ❌ Bad: Assume attribute exists
filtered = [t for t in tasks if t.priority == "high"]  # May raise AttributeError
```

### Rule 4: Composability
Filters should be composable and chainable
```python
# ✅ Good: Composable
pending = filter_by_status(tasks, completed=False)
high_priority = filter_by_priority(pending, "high")
recent = filter_by_due_date(high_priority, start_date=last_week)

# ✅ Also Good: Single multi-criteria filter
filtered = filter_tasks(tasks, completed=False, priority="high", due_after=last_week)
```

### Rule 5: Empty Filter Returns All
If no criteria provided, return copy of all items
```python
# ✅ Good: No filter returns all
if search is None or search == "":
    return tasks.copy()

# ❌ Bad: No filter returns empty
if search is None:
    return []
```

---

## Usage

To use this skill:

1. Identify what filtering criteria are needed:
   - Status (completed/pending)
   - Priority levels
   - Tags/labels
   - Keyword search
   - Date ranges
   - Custom fields

2. Choose the appropriate template:
   - Single criterion → Use specific filter (Template 1-5)
   - Multiple criteria → Use multi-criteria filter (Template 6)
   - Dynamic criteria → Use generic filter (Template 7)

3. Customize the template:
   - Update Task field references
   - Add task/spec references
   - Adjust validation logic
   - Add examples specific to use case

4. Add to `task_manager.py` module

5. Create corresponding CLI functions in `cli.py` to prompt for filter criteria

6. Add command handlers in `main.py` to wire up the filters

---

## CLI Integration Pattern

```python
# cli.py
def get_filter_criteria() -> dict:
    """
    Prompt user for filter criteria.

    Returns:
        dict: Filter criteria to pass to filter_tasks()
    """
    print("\n--- Filter Tasks ---")
    print("Leave blank to skip a filter\n")

    criteria = {}

    # Status filter
    status = input("Status (pending/completed): ").strip()
    if status:
        criteria['completed'] = status.lower() == "completed"

    # Priority filter
    priority = input("Priority (high/medium/low): ").strip()
    if priority:
        criteria['priority'] = priority

    # Search filter
    search = input("Search keyword: ").strip()
    if search:
        criteria['search'] = search

    return criteria


# main.py
def handle_filter():
    """Handle filter command."""
    from cli import get_filter_criteria, display_task_list
    from task_manager import filter_tasks, get_all_tasks

    criteria = get_filter_criteria()
    all_tasks = get_all_tasks()
    filtered = filter_tasks(all_tasks, **criteria)

    if filtered:
        display_task_list(filtered, "Filtered Tasks")
    else:
        print("No tasks match your criteria.")
```

---

## Testing Pattern

```python
# tests/test_task_manager.py
import pytest
from models import Task
from task_manager import filter_tasks

def test_filter_by_status_pending():
    tasks = [
        Task(id=1, title="Task 1", completed=False),
        Task(id=2, title="Task 2", completed=True),
        Task(id=3, title="Task 3", completed=False),
    ]
    result = filter_tasks(tasks, completed=False)
    assert len(result) == 2
    assert all(not t.completed for t in result)

def test_filter_by_search():
    tasks = [
        Task(id=1, title="Buy groceries", description="Milk and eggs"),
        Task(id=2, title="Write report", description="Q4 summary"),
        Task(id=3, title="Call mom", description=""),
    ]
    result = filter_tasks(tasks, search="report")
    assert len(result) == 1
    assert result[0].title == "Write report"

def test_filter_case_insensitive():
    tasks = [Task(id=1, title="URGENT Task", description="Important")]
    result = filter_tasks(tasks, search="urgent")
    assert len(result) == 1

def test_filter_multiple_criteria():
    tasks = [
        Task(id=1, title="Task 1", completed=False, priority="high"),
        Task(id=2, title="Task 2", completed=True, priority="high"),
        Task(id=3, title="Task 3", completed=False, priority="low"),
    ]
    result = filter_tasks(tasks, completed=False, priority="high")
    assert len(result) == 1
    assert result[0].id == 1

def test_filter_no_criteria_returns_all():
    tasks = [Task(id=1, title="Task 1"), Task(id=2, title="Task 2")]
    result = filter_tasks(tasks)
    assert len(result) == 2

def test_filter_returns_copy():
    tasks = [Task(id=1, title="Task 1")]
    result = filter_tasks(tasks, search="nonexistent")
    assert result is not tasks  # Different list objects
```

---

## Best Practices

1. **Always Return New List:** Never modify the input list
2. **Case-Insensitive:** Use `.lower()` for all string comparisons
3. **Check Attributes:** Use `hasattr()` before accessing optional fields
4. **Validate Input:** Check for valid filter values before applying
5. **Empty Criteria:** Return copy of all items when no filters applied
6. **List Comprehensions:** Prefer list comprehensions over loops for clarity
7. **Composable:** Design filters to work together
8. **Type Hints:** Include proper type hints for all parameters
9. **Docstrings:** Document all parameters and return values
10. **Examples:** Include usage examples in docstrings

---

## Output Format

Generated filtering functions are ready to add to:
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
