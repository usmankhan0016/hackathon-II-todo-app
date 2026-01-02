# Module Contract: ui.py

**Module**: `src.phase1.ui`
**Purpose**: Rich library UI components and display functions
**Dependencies**: `models.Task`, `rich.*`

## Functions

### Display Functions
```python
def display_header() -> None
def display_menu() -> None
def display_tasks_table(tasks: list[Task]) -> None
def display_task_stats(stats: dict[str, int]) -> None
```

### Message Functions
```python
def display_success(message: str) -> None  # Green with ✓
def display_error(message: str) -> None    # Red with ✗
def display_info(message: str) -> None     # Blue with ℹ
def display_warning(message: str) -> None  # Yellow with ⚠
```

### Utility
```python
def clear_screen() -> None
```

## Responsibilities
- Render all UI using Rich library
- Format task data for display
- Display status messages
- No business logic
