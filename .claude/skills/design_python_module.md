# Design Python Module

Generate a clean Python module architecture plan for the console todo app.

## Instructions

When this skill is invoked, create a technical architecture plan that defines the structure and responsibilities of four core modules: models, task_manager, cli, and main.

### Input Required
- Feature specification reference (path to spec.md)
- Feature name
- Brief description of functionality to implement

### Template Structure

```markdown
# Architecture Plan: [Feature Name]

## Overview
[1-2 sentences describing the technical approach and module changes needed]

## Feature Reference
**Spec:** `specs/[feature-name]/spec.md`
**Status:** Planning
**Created:** [Date]

---

## Module Architecture

### 1. models.py
**Purpose:** Data structures and validation logic

#### Dataclass Definitions

```python
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class Task:
    """Represents a todo task item."""
    id: int
    title: str
    description: str = ""
    completed: bool = False
    # [Add new fields for this feature]
    # field_name: type = default_value

    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate task data.

        Returns:
            tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        # [Add validation logic]
        pass

    # [Add any feature-specific methods]
```

#### New Classes (if needed)
```python
# [Define any additional dataclasses needed for this feature]
```

#### Validation Rules
- **title:** [validation rules]
- **description:** [validation rules]
- **[new_field]:** [validation rules]

#### Methods to Add/Modify
| Method | Purpose | Parameters | Returns |
|--------|---------|------------|---------|
| `validate()` | [description] | `self` | `tuple[bool, Optional[str]]` |
| [method_name] | [description] | [params] | [return type] |

---

### 2. task_manager.py
**Purpose:** Business logic and data operations

#### Storage Structure
```python
from typing import List
from models import Task

# In-memory storage
tasks: List[Task] = []
next_id: int = 1
```

#### CRUD Operations

##### Create
```python
def create_task(title: str, description: str = "", **kwargs) -> tuple[Task, Optional[str]]:
    """
    Create a new task.

    Args:
        title: Task title
        description: Task description
        **kwargs: Additional fields for the task

    Returns:
        tuple[Task, Optional[str]]: (created_task, error_message)

    Raises:
        None (returns error in tuple instead)
    """
    # Implementation notes:
    # 1. [Step 1]
    # 2. [Step 2]
    # 3. [Step 3]
    pass
```

##### Read
```python
def get_task(task_id: int) -> Optional[Task]:
    """
    Retrieve a task by ID.

    Args:
        task_id: Unique task identifier

    Returns:
        Optional[Task]: Task if found, None otherwise
    """
    pass

def get_all_tasks() -> List[Task]:
    """
    Retrieve all tasks.

    Returns:
        List[Task]: List of all tasks
    """
    pass

# [Add feature-specific read functions]
def [filter_function_name]([params]) -> List[Task]:
    """
    [Description of filtering logic]

    Args:
        [param]: [description]

    Returns:
        List[Task]: Filtered task list
    """
    pass
```

##### Update
```python
def update_task(task_id: int, **kwargs) -> tuple[bool, Optional[str]]:
    """
    Update task fields.

    Args:
        task_id: Task identifier
        **kwargs: Fields to update

    Returns:
        tuple[bool, Optional[str]]: (success, error_message)
    """
    # Implementation notes:
    # 1. [Step 1]
    # 2. [Step 2]
    pass

# [Add feature-specific update functions]
def [specific_update_function]([params]) -> tuple[bool, Optional[str]]:
    """
    [Description]

    Args:
        [params]: [description]

    Returns:
        tuple[bool, Optional[str]]: (success, error_message)
    """
    pass
```

##### Delete
```python
def delete_task(task_id: int) -> tuple[bool, Optional[str]]:
    """
    Delete a task by ID.

    Args:
        task_id: Task identifier

    Returns:
        tuple[bool, Optional[str]]: (success, error_message)
    """
    pass
```

#### Business Logic Functions
```python
# [Add feature-specific business logic functions]

def [business_logic_function]([params]) -> [return_type]:
    """
    [Description of business logic]

    Args:
        [params]: [description]

    Returns:
        [return_type]: [description]

    Business Rules:
        - [Rule 1]
        - [Rule 2]
    """
    pass
```

#### Helper Functions
```python
def _[helper_function]([params]) -> [return_type]:
    """
    [Private helper function description]

    Args:
        [params]: [description]

    Returns:
        [return_type]: [description]
    """
    pass
```

---

### 3. cli.py
**Purpose:** User interface and display formatting

#### Input Handling

```python
def get_user_input(prompt: str, required: bool = True) -> Optional[str]:
    """
    Get input from user with validation.

    Args:
        prompt: Prompt message to display
        required: Whether input is required

    Returns:
        Optional[str]: User input or None if not required and empty
    """
    pass

def get_[specific_input]() -> [return_type]:
    """
    Get [specific type] input from user.

    Returns:
        [return_type]: Validated input

    Prompts:
        - [Prompt 1]
        - [Prompt 2]
    """
    pass
```

#### Display Functions

```python
def display_task(task: Task) -> None:
    """
    Display a single task in formatted output.

    Args:
        task: Task object to display

    Output Format:
        [Example output format]
    """
    pass

def display_task_list(tasks: List[Task], header: str = "Tasks") -> None:
    """
    Display a list of tasks.

    Args:
        tasks: List of tasks to display
        header: Header text for the list

    Output Format:
        [Example output format]
    """
    pass

def display_[feature_specific_view]([params]) -> None:
    """
    Display [specific view] for this feature.

    Args:
        [params]: [description]

    Output Format:
        [Example output format]
    """
    pass
```

#### Formatting Helpers

```python
def format_[data_type]([params]) -> str:
    """
    Format [data type] for display.

    Args:
        [params]: [description]

    Returns:
        str: Formatted string

    Format:
        [Example format]
    """
    pass
```

#### Menu System

```python
def display_menu() -> None:
    """
    Display the main menu options.

    Menu Options:
        [Option 1]: [Description]
        [Option 2]: [Description]
        [New Option]: [Description for this feature]
    """
    pass

def display_[submenu]() -> None:
    """
    Display [submenu] for this feature.

    Menu Options:
        [Option 1]: [Description]
        [Option 2]: [Description]
    """
    pass
```

#### Error/Success Messages

```python
def show_success(message: str) -> None:
    """Display success message."""
    pass

def show_error(message: str) -> None:
    """Display error message."""
    pass

def show_info(message: str) -> None:
    """Display informational message."""
    pass
```

---

### 4. main.py
**Purpose:** Application entry point and command routing

#### Main Loop

```python
from cli import display_menu, get_user_input, show_error
from task_manager import [import required functions]

def main() -> None:
    """
    Main application loop.

    Flow:
        1. Display menu
        2. Get user command
        3. Route to handler
        4. Display result
        5. Repeat until exit
    """
    print("=== Todo App ===\n")

    while True:
        display_menu()
        command = get_user_input("Enter command: ", required=True)

        if command == "exit":
            print("Goodbye!")
            break

        # [Add new command routing for this feature]
        handle_command(command)

if __name__ == "__main__":
    main()
```

#### Command Handlers

```python
def handle_command(command: str) -> None:
    """
    Route command to appropriate handler.

    Args:
        command: User command string

    Commands:
        [command1]: [description]
        [command2]: [description]
        [new_command]: [description for this feature]
    """
    command = command.lower().strip()

    # [Map commands to handlers]
    command_map = {
        "[command1]": handle_[command1],
        "[command2]": handle_[command2],
        # [Add new command mappings]
    }

    handler = command_map.get(command)
    if handler:
        handler()
    else:
        show_error(f"Unknown command: {command}")

def handle_[command_name]() -> None:
    """
    Handle [command name] command.

    Flow:
        1. [Step 1]
        2. [Step 2]
        3. [Step 3]

    User Interaction:
        - Prompts: [list prompts]
        - Output: [describe output]
    """
    # Implementation notes:
    # 1. [Detail 1]
    # 2. [Detail 2]
    pass
```

---

## Implementation Order

### Phase 1: Data Layer
1. Update `models.py` with new fields/classes
2. Add validation methods
3. Write unit tests for models

### Phase 2: Business Logic
1. Implement CRUD operations in `task_manager.py`
2. Add business logic functions
3. Write unit tests for task manager

### Phase 3: User Interface
1. Create display functions in `cli.py`
2. Add input handling
3. Test display output manually

### Phase 4: Integration
1. Add command handlers to `main.py`
2. Update menu system
3. Test end-to-end flow

---

## Function Signature Summary

### models.py
- `Task.validate() -> tuple[bool, Optional[str]]`
- [Additional methods]

### task_manager.py
- `create_task(title: str, description: str = "", **kwargs) -> tuple[Task, Optional[str]]`
- `get_task(task_id: int) -> Optional[Task]`
- `get_all_tasks() -> List[Task]`
- `update_task(task_id: int, **kwargs) -> tuple[bool, Optional[str]]`
- `delete_task(task_id: int) -> tuple[bool, Optional[str]]`
- [Feature-specific functions]

### cli.py
- `get_user_input(prompt: str, required: bool = True) -> Optional[str]`
- `display_task(task: Task) -> None`
- `display_task_list(tasks: List[Task], header: str = "Tasks") -> None`
- `display_menu() -> None`
- `show_success(message: str) -> None`
- `show_error(message: str) -> None`
- [Feature-specific functions]

### main.py
- `main() -> None`
- `handle_command(command: str) -> None`
- [Command handler functions]

---

## Dependencies

### Standard Library
```python
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from datetime import datetime  # [if needed]
```

### Internal Modules
```python
from models import Task  # [and other classes]
from task_manager import [functions]
from cli import [functions]
```

### External Packages
```
# [List any pip packages needed]
# Example: pytest==7.4.0 (for testing)
```

---

## Testing Strategy

### Unit Tests
- `test_models.py`: Test Task validation and methods
- `test_task_manager.py`: Test CRUD operations and business logic
- `test_cli.py`: Test formatting functions (not interactive input)

### Integration Tests
- `test_integration.py`: Test command flow end-to-end with mocked input

### Manual Testing
- Test console output formatting
- Test user input handling
- Test error scenarios

---

## Error Handling Strategy

### Validation Errors
- Caught at model level
- Returned as tuple (success, error_message)
- Displayed to user via cli.show_error()

### Business Logic Errors
- Caught at task_manager level
- Returned as tuple (success, error_message)
- Clear, actionable error messages

### User Input Errors
- Handled at cli level
- Re-prompt for valid input
- Show helpful error messages

---

## Code Quality Checklist

- [ ] All functions have type hints
- [ ] All functions have docstrings
- [ ] Error cases return tuples with error messages
- [ ] No global state except tasks list in task_manager
- [ ] Private helpers prefixed with underscore
- [ ] Consistent naming conventions (snake_case)
- [ ] Input validation at appropriate layers
- [ ] Clear separation of concerns between modules

---

## Notes

### Design Decisions
- [Key architectural decision 1]
- [Key architectural decision 2]

### Assumptions
- [Assumption 1]
- [Assumption 2]

### Future Considerations
- [Potential extension 1]
- [Potential extension 2]
```

## Usage

To use this skill:

1. User provides feature specification reference
2. Read the spec to understand requirements
3. Ask clarifying questions:
   - What new fields need to be added to Task?
   - What CRUD operations are needed?
   - What commands should be added to the menu?
   - How should data be displayed?
4. Fill in the template with specific function signatures
5. Define clear implementation order
6. Save to `specs/[feature-name]/plan.md`

## Best Practices

- **Type Hints:** All functions must have complete type hints
- **Error Handling:** Use tuple returns (success, error) pattern
- **Docstrings:** Follow Google/NumPy docstring format
- **Separation of Concerns:** Keep modules focused on single responsibility
- **Testability:** Design functions to be easily unit tested
- **Consistency:** Follow existing patterns in the codebase
- **Private Functions:** Use underscore prefix for internal helpers
- **Immutability:** Prefer dataclasses over mutable dicts

## Module Responsibilities

### models.py
✅ DO: Define data structures, validation logic, data-related methods
❌ DON'T: Business logic, I/O operations, external dependencies

### task_manager.py
✅ DO: CRUD operations, business rules, data transformations
❌ DON'T: User input, display formatting, application flow

### cli.py
✅ DO: Display formatting, input collection, menu display
❌ DON'T: Business logic, data storage, validation rules

### main.py
✅ DO: Command routing, application flow, integration
❌ DON'T: Business logic, complex formatting, data manipulation

## Output Format

Save the completed architecture plan as:
```
specs/[feature-name]/plan.md
```

Where `[feature-name]` matches the spec directory name.
