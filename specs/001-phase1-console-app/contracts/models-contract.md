# Module Contract: models.py

**Module**: `src.phase1.models`
**Purpose**: Define Task data structure and type definitions
**Dependencies**: None (Python standard library only)

## Exports

### Task Dataclass
```python
@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "Medium"
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
```

### Type Aliases
```python
Priority = Literal["High", "Medium", "Low"]
```

## Responsibilities
- Define Task data structure
- Validate field values in `__post_init__`
- Provide type hints for other modules
- No business logic (pure data)

## Usage Example
```python
from src.phase1.models import Task

task = Task(id=1, title="Buy groceries")
```
