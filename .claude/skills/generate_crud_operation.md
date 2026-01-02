# Generate CRUD Operation

Generate standardized Python functions for task operations with proper docstrings, type hints, and error handling.

## Instructions

When this skill is invoked, generate a complete Python function following the standardized pattern with task reference, spec reference, and proper documentation.

### Input Required
- Operation type: `add` | `view` | `update` | `delete` | `complete` | `custom`
- Task ID (e.g., T-001)
- Spec reference (e.g., specs/add-task/spec.md §2.1)
- Feature context (brief description)
- Custom parameters (if operation type is `custom`)

### Function Template Pattern

```python
def operation_name(params) -> ReturnType:
    """
    [Task]: T-XXX
    [Spec]: specs/features/[feature].md §X.X

    Brief description of what this function does.

    Args:
        param1 (type): Description of parameter
        param2 (type): Description of parameter

    Returns:
        type: Description of return value

    Raises:
        ValueError: When [specific condition]
        TypeError: When [specific condition]

    Example:
        >>> operation_name(arg1, arg2)
        expected_output
    """
    # Implementation here
```

---

## Standard Operation Patterns

### 1. ADD Operation

**Use Case:** Create and append a new task to the tasks list

**Template:**
```python
from typing import Optional, Tuple
from models import Task

def add_task(title: str, description: str = "", **kwargs) -> Tuple[Task, Optional[str]]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Create a new task and add it to the task list.

    Args:
        title (str): Task title (required, non-empty)
        description (str): Task description (optional, default: "")
        **kwargs: Additional task fields (e.g., priority, due_date)

    Returns:
        Tuple[Task, Optional[str]]:
            - Task object if successful
            - Error message if validation fails, None otherwise

    Raises:
        None: Returns errors as tuple instead of raising

    Example:
        >>> task, error = add_task("Buy groceries", "Milk and eggs")
        >>> if not error:
        ...     print(f"Task {task.id} created")
    """
    global tasks, next_id

    # Validate title
    if not title or not title.strip():
        return None, "Title cannot be empty"

    if len(title) > 100:
        return None, "Title cannot exceed 100 characters"

    # Validate description
    if len(description) > 500:
        return None, "Description cannot exceed 500 characters"

    # Create task with auto-generated ID
    task = Task(
        id=next_id,
        title=title.strip(),
        description=description.strip(),
        completed=False,
        **kwargs
    )

    # Validate task (if Task has validate method)
    is_valid, error = task.validate()
    if not is_valid:
        return None, error

    # Add to list and increment ID
    tasks.append(task)
    next_id += 1

    return task, None
```

**Variations:**
- `add_task_with_[field]()` - Add with specific additional fields
- `bulk_add_tasks()` - Add multiple tasks at once

---

### 2. VIEW Operation

**Use Case:** Display all tasks or filtered subset

**Template:**
```python
from typing import List, Optional
from models import Task

def view_all_tasks() -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Retrieve all tasks from the task list.

    Returns:
        List[Task]: List of all tasks (empty list if no tasks)

    Example:
        >>> tasks = view_all_tasks()
        >>> for task in tasks:
        ...     print(task.title)
    """
    return tasks.copy()  # Return copy to prevent external modification


def view_tasks_by_status(completed: bool) -> List[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Retrieve tasks filtered by completion status.

    Args:
        completed (bool): True for completed tasks, False for pending

    Returns:
        List[Task]: Filtered list of tasks

    Example:
        >>> pending = view_tasks_by_status(completed=False)
        >>> print(f"{len(pending)} pending tasks")
    """
    return [task for task in tasks if task.completed == completed]


def view_task_by_id(task_id: int) -> Optional[Task]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Retrieve a specific task by its ID.

    Args:
        task_id (int): Unique task identifier

    Returns:
        Optional[Task]: Task object if found, None otherwise

    Example:
        >>> task = view_task_by_id(1)
        >>> if task:
        ...     print(task.title)
        ... else:
        ...     print("Task not found")
    """
    for task in tasks:
        if task.id == task_id:
            return task
    return None
```

**Variations:**
- `view_tasks_by_[field]()` - Filter by specific field
- `search_tasks()` - Search by keyword in title/description
- `view_tasks_sorted_by_[field]()` - Return sorted results

---

### 3. UPDATE Operation

**Use Case:** Modify existing task fields

**Template:**
```python
from typing import Optional, Tuple

def update_task(task_id: int, **kwargs) -> Tuple[bool, Optional[str]]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Update one or more fields of an existing task.

    Args:
        task_id (int): Unique task identifier
        **kwargs: Fields to update (e.g., title="New title", completed=True)

    Returns:
        Tuple[bool, Optional[str]]:
            - True if update successful, False otherwise
            - Error message if failed, None if successful

    Example:
        >>> success, error = update_task(1, title="Updated title")
        >>> if success:
        ...     print("Task updated")
        ... else:
        ...     print(f"Error: {error}")
    """
    # Find task
    task = view_task_by_id(task_id)
    if not task:
        return False, f"Task with ID {task_id} not found"

    # Validate updates
    if 'title' in kwargs:
        title = kwargs['title']
        if not title or not title.strip():
            return False, "Title cannot be empty"
        if len(title) > 100:
            return False, "Title cannot exceed 100 characters"
        task.title = title.strip()

    if 'description' in kwargs:
        description = kwargs['description']
        if len(description) > 500:
            return False, "Description cannot exceed 500 characters"
        task.description = description.strip()

    if 'completed' in kwargs:
        if not isinstance(kwargs['completed'], bool):
            return False, "Completed must be a boolean value"
        task.completed = kwargs['completed']

    # Update additional fields
    for key, value in kwargs.items():
        if key not in ['title', 'description', 'completed']:
            if hasattr(task, key):
                setattr(task, key, value)
            else:
                return False, f"Invalid field: {key}"

    # Validate updated task
    is_valid, error = task.validate()
    if not is_valid:
        return False, error

    return True, None


def update_task_title(task_id: int, new_title: str) -> Tuple[bool, Optional[str]]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Update only the title of a task.

    Args:
        task_id (int): Unique task identifier
        new_title (str): New task title

    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)

    Example:
        >>> success, error = update_task_title(1, "New Title")
    """
    return update_task(task_id, title=new_title)
```

**Variations:**
- `update_task_[field]()` - Update specific field only
- `bulk_update_tasks()` - Update multiple tasks at once

---

### 4. DELETE Operation

**Use Case:** Remove task from the list

**Template:**
```python
from typing import Tuple, Optional

def delete_task(task_id: int) -> Tuple[bool, Optional[str]]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Delete a task from the task list.

    Args:
        task_id (int): Unique task identifier

    Returns:
        Tuple[bool, Optional[str]]:
            - True if deletion successful, False otherwise
            - Error message if failed, None if successful

    Example:
        >>> success, error = delete_task(1)
        >>> if success:
        ...     print("Task deleted")
        ... else:
        ...     print(f"Error: {error}")
    """
    global tasks

    # Find task index
    task_index = None
    for i, task in enumerate(tasks):
        if task.id == task_id:
            task_index = i
            break

    if task_index is None:
        return False, f"Task with ID {task_id} not found"

    # Remove task
    deleted_task = tasks.pop(task_index)

    return True, None


def delete_all_completed_tasks() -> Tuple[int, Optional[str]]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Delete all completed tasks from the list.

    Returns:
        Tuple[int, Optional[str]]:
            - Number of tasks deleted
            - Error message if failed, None if successful

    Example:
        >>> count, error = delete_all_completed_tasks()
        >>> print(f"Deleted {count} completed tasks")
    """
    global tasks

    initial_count = len(tasks)
    tasks = [task for task in tasks if not task.completed]
    deleted_count = initial_count - len(tasks)

    return deleted_count, None


def delete_all_tasks() -> Tuple[int, Optional[str]]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Delete all tasks from the list (with confirmation in CLI).

    Returns:
        Tuple[int, Optional[str]]:
            - Number of tasks deleted
            - Error message if failed, None if successful

    Warning:
        This operation cannot be undone. Ensure CLI prompts for confirmation.

    Example:
        >>> count, error = delete_all_tasks()
        >>> print(f"Deleted {count} tasks")
    """
    global tasks, next_id

    count = len(tasks)
    tasks.clear()
    next_id = 1  # Reset ID counter

    return count, None
```

**Variations:**
- `delete_tasks_by_[criteria]()` - Delete multiple tasks matching criteria
- `soft_delete_task()` - Mark as deleted without removing

---

### 5. COMPLETE Operation

**Use Case:** Toggle or set task completion status

**Template:**
```python
from typing import Tuple, Optional

def complete_task(task_id: int) -> Tuple[bool, Optional[str]]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Mark a task as completed.

    Args:
        task_id (int): Unique task identifier

    Returns:
        Tuple[bool, Optional[str]]:
            - True if operation successful, False otherwise
            - Error message if failed, None if successful

    Example:
        >>> success, error = complete_task(1)
        >>> if success:
        ...     print("Task marked as completed")
    """
    task = view_task_by_id(task_id)
    if not task:
        return False, f"Task with ID {task_id} not found"

    if task.completed:
        return False, f"Task {task_id} is already completed"

    task.completed = True
    return True, None


def uncomplete_task(task_id: int) -> Tuple[bool, Optional[str]]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Mark a completed task as incomplete.

    Args:
        task_id (int): Unique task identifier

    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)

    Example:
        >>> success, error = uncomplete_task(1)
        >>> if success:
        ...     print("Task marked as incomplete")
    """
    task = view_task_by_id(task_id)
    if not task:
        return False, f"Task with ID {task_id} not found"

    if not task.completed:
        return False, f"Task {task_id} is already incomplete"

    task.completed = False
    return True, None


def toggle_task_completion(task_id: int) -> Tuple[bool, Optional[str]]:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Toggle the completion status of a task.

    Args:
        task_id (int): Unique task identifier

    Returns:
        Tuple[bool, Optional[str]]:
            - True if toggle successful, False otherwise
            - Error message if failed, None if successful

    Example:
        >>> success, error = toggle_task_completion(1)
        >>> if success:
        ...     print("Task completion toggled")
    """
    task = view_task_by_id(task_id)
    if not task:
        return False, f"Task with ID {task_id} not found"

    task.completed = not task.completed
    return True, None
```

**Variations:**
- `complete_all_tasks()` - Mark all tasks as completed
- `complete_tasks_by_[criteria]()` - Batch completion

---

### 6. CUSTOM Operation

**Use Case:** Feature-specific operations not covered by standard CRUD

**Template:**
```python
from typing import [appropriate types]

def custom_operation_name(params) -> ReturnType:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    [Description of what this custom operation does]

    Args:
        param1 (type): Description
        param2 (type): Description

    Returns:
        ReturnType: Description

    Raises:
        ExceptionType: When [condition]

    Business Rules:
        - [Rule 1]
        - [Rule 2]

    Example:
        >>> result = custom_operation_name(arg1, arg2)
        >>> print(result)
    """
    # Validation
    # Business logic
    # Return result
    pass
```

---

## Error Handling Patterns

### Pattern 1: Tuple Return (Preferred)
```python
def operation() -> Tuple[bool, Optional[str]]:
    """Returns (success, error_message)"""
    if error_condition:
        return False, "Descriptive error message"
    return True, None
```

### Pattern 2: Optional Return
```python
def operation() -> Optional[ReturnType]:
    """Returns result or None if not found"""
    if not found:
        return None
    return result
```

### Pattern 3: Result with Data
```python
def operation() -> Tuple[Optional[Data], Optional[str]]:
    """Returns (data, error_message)"""
    if error:
        return None, "Error message"
    return data, None
```

---

## Standard Imports

```python
from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass
from models import Task
```

---

## Validation Rules

### Title Validation
```python
if not title or not title.strip():
    return False, "Title cannot be empty"
if len(title) > 100:
    return False, "Title cannot exceed 100 characters"
```

### Description Validation
```python
if len(description) > 500:
    return False, "Description cannot exceed 500 characters"
```

### ID Validation
```python
if task_id <= 0:
    return False, "Task ID must be a positive integer"
```

### Existence Check
```python
task = view_task_by_id(task_id)
if not task:
    return False, f"Task with ID {task_id} not found"
```

---

## Usage

To use this skill:

1. Specify operation type: add, view, update, delete, complete, or custom
2. Provide task ID (e.g., T-001)
3. Provide spec reference (e.g., specs/add-task/spec.md §2.1)
4. Describe the feature context
5. For custom operations, provide:
   - Function name
   - Parameters needed
   - Return type
   - Business logic description

The skill will generate:
- Complete function with proper signature
- Full docstring with task/spec references
- Type hints for all parameters and returns
- Error handling following standard patterns
- Example usage in docstring
- Validation logic where appropriate

## Output Format

```python
# Generated function ready to add to task_manager.py
# Includes all imports, docstrings, and implementation
```

## Best Practices

1. **Type Hints:** Always include complete type hints
2. **Docstrings:** Follow Google/NumPy style with Task and Spec references
3. **Error Handling:** Use tuple returns (success, error) pattern
4. **Validation:** Validate at the function level, not just in models
5. **Immutability:** Return copies of lists to prevent external modification
6. **Global State:** Only modify global `tasks` and `next_id` when necessary
7. **Examples:** Include realistic usage examples in docstrings
8. **Consistency:** Follow the same patterns across all CRUD operations

## Quality Checklist

- [ ] Function has type hints for all parameters and return
- [ ] Docstring includes [Task] and [Spec] references
- [ ] Docstring includes Args, Returns, and Example sections
- [ ] Error cases return tuple with descriptive message
- [ ] Validation is performed before state changes
- [ ] Global variables are modified safely
- [ ] Function follows single responsibility principle
- [ ] Edge cases are handled (empty list, not found, duplicates)
- [ ] Example in docstring is executable and accurate
