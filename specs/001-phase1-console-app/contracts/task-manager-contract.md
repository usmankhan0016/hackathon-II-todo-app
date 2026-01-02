# Module Contract: task_manager.py

**Module**: `src.phase1.task_manager`
**Purpose**: Business logic for task CRUD operations
**Dependencies**: `models.Task`

## Global State
```python
tasks: list[Task] = []  # In-memory task storage
```

## Functions

### CRUD Operations
```python
def add_task(title: str, description: str = "", priority: str = "Medium", tags: list[str] = []) -> Task
def get_all_tasks() -> list[Task]
def get_task_by_id(task_id: int) -> Task | None
def update_task(task_id: int, title: str | None = None, description: str | None = None) -> bool
def delete_task(task_id: int) -> bool
def toggle_complete(task_id: int) -> bool
```

### Query Operations
```python
def search_tasks(keyword: str) -> list[Task]
def filter_tasks(status: str | None = None, priority: str | None = None, tag: str | None = None) -> list[Task]
def sort_tasks(tasks: list[Task], by: str = "id", descending: bool = False) -> list[Task]
```

### Statistics
```python
def get_task_stats() -> dict[str, int]  # {"total": 10, "completed": 3, "pending": 7}
```

## Responsibilities
- Manage global task list
- Generate sequential task IDs
- Implement business logic
- No UI or input handling
