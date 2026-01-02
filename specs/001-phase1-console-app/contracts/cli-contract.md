# Module Contract: cli.py

**Module**: `src.phase1.cli`
**Purpose**: User input handling and command routing
**Dependencies**: `task_manager.*`, `ui.*`, `models.Task`, `rich.prompt.Prompt`

## Input Functions
```python
def get_task_input() -> dict[str, str | list[str]]
def get_task_id() -> int | None
def get_update_fields() -> dict[str, str]
def get_search_keyword() -> str
def get_filter_criteria() -> dict[str, str]
def get_sort_options() -> tuple[str, bool]
```

## Command Handlers
```python
def handle_add_task() -> None
def handle_view_tasks() -> None
def handle_update_task() -> None
def handle_delete_task() -> None
def handle_toggle_complete() -> None
def handle_search_tasks() -> None
def handle_filter_tasks() -> None
def handle_sort_tasks() -> None
```

## Menu Routing
```python
def get_menu_choice() -> str
```

## Responsibilities
- Handle all user input via Rich Prompt
- Validate input before passing to task_manager
- Route menu choices to handlers
- Coordinate between task_manager and ui
- Display operation results
