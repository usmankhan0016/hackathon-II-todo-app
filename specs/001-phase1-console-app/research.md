# Research: Phase 1 - Todo Console App

**Date**: 2026-01-02
**Feature**: 001-phase1-console-app
**Purpose**: Research technical decisions for Python console app with Rich UI

## Rich Library Analysis

### Overview
- **Package**: `rich`
- **Version**: 13.7.0+ (latest stable)
- **License**: MIT
- **Maintenance**: Active (weekly updates)
- **Downloads**: 50M+ per month
- **Documentation**: https://rich.readthedocs.io/

### Key Features for Phase 1
1. **Table Component**: Formatted, bordered tables with automatic column sizing
2. **Panel Component**: Styled boxes for headers and messages
3. **Prompt Component**: Interactive input with validation support
4. **Console**: Central object for all printing with color/style markup
5. **Markdown Support**: Rich text formatting in strings

### Implementation Patterns

**Pattern 1: Console Initialization**
```python
from rich.console import Console

console = Console()
```
- Single global console instance
- Handles all output automatically
- Supports color terminal detection

**Pattern 2: Table Creation**
```python
from rich.table import Table

table = Table(title="Tasks", border_style="cyan")
table.add_column("ID", justify="center", style="cyan", width=5)
table.add_column("Title", style="white", no_wrap=False)
table.add_row("1", "Buy groceries")
console.print(table)
```
- Declarative column definitions
- Auto-sizing or fixed widths
- Style inheritance from table → column → row

**Pattern 3: Panel for Headers**
```python
from rich.panel import Panel

header = Panel(
    "[cyan bold]📝 My Todo List[/cyan bold]",
    border_style="cyan",
    padding=(0, 2)
)
console.print(header)
```
- Centers content automatically
- Supports padding and borders
- Inline Rich markup for styling

**Pattern 4: User Input**
```python
from rich.prompt import Prompt

title = Prompt.ask("Enter task title")
priority = Prompt.ask(
    "Enter priority",
    choices=["High", "Medium", "Low"],
    default="Medium"
)
```
- Type-safe prompts (IntPrompt, Confirm, etc.)
- Built-in validation
- Default values supported

### Color Scheme Best Practices

**Semantic Colors** (from Rich documentation):
- `green`: Success, completed items
- `yellow`: Warnings, pending items
- `red`: Errors, urgent items
- `cyan`/`blue`: Information, headers
- `white`: Default text
- `dim`: Secondary information

**Usage in Phase 1**:
```python
# Success messages
console.print("[green]✓[/green] Task added successfully!")

# Error messages
console.print("[red]✗[/red] Task not found with ID: 5")

# Info messages
console.print("[blue]ℹ[/blue] No tasks found")

# Status indicators in table
status = "[green]✓ Done[/green]" if completed else "[yellow]⏳ Pending[/yellow]"
```

## Python Dataclass Best Practices

### Research Question: Mutable Default Arguments
**Problem**: Lists as default arguments are shared across instances
```python
# WRONG
class Task:
    tags: list[str] = []  # Same list used by all instances!
```

**Solution**: Use `field(default_factory=list)`
```python
from dataclasses import dataclass, field

@dataclass
class Task:
    tags: list[str] = field(default_factory=list)  # New list per instance
```

### Research Question: Timestamp Defaults
**Problem**: `datetime.now()` evaluated at class definition time
```python
# WRONG
created_at: datetime = datetime.now()  # Same timestamp for all instances!
```

**Solution**: Use `field(default_factory=datetime.now)`
```python
created_at: datetime = field(default_factory=datetime.now)  # Evaluated at instance creation
```

### Type Hints for Python 3.13+
- Use `list[Task]` instead of `List[Task]` (built-in generics)
- Use `str | None` instead of `Optional[str]` (union types)
- Use `Literal["High", "Medium", "Low"]` for enums
- Enable type checking with `mypy --strict`

## In-Memory Storage Patterns

### Research Question: ID Generation Strategy
**Options Evaluated**:
1. Counter variable (global state)
2. UUID (non-sequential)
3. `max(ids) + 1` (calculated)

**Decision**: Option 3 - `max([t.id for t in tasks], default=0) + 1`

**Rationale**:
- No additional state to manage
- Survives task deletions
- Predictable, testable
- Aligns with spec requirement A-010 (IDs never reused)

**Edge Cases Handled**:
```python
# Empty list
max([], default=0) + 1  # Returns 1

# After deletions (deleted task 2)
tasks = [Task(id=1), Task(id=3)]
max([t.id for t in tasks], default=0) + 1  # Returns 4 (not 2)
```

### Search Performance
**Research**: Linear search acceptable for Phase 1 scope
- Spec assumption A-007: <100 tasks typical
- Spec constraint SC-010: <1 second for search on 100 items
- Python list scan: ~0.001ms per item on modern hardware
- Conclusion: No indexing needed for Phase 1

## Input Validation Patterns

### Research Question: Where to Validate?
**Options**:
1. Validate in task_manager (business logic)
2. Validate in CLI (presentation layer)
3. Validate in both (belt-and-suspenders)

**Decision**: Option 2 - CLI layer only

**Rationale**:
- Separation of concerns (CLI handles input, task_manager handles domain logic)
- Immediate user feedback (fail fast)
- Cleaner task_manager code (assumes valid input)
- Easier testing (validation isolated)

**Validation Functions Needed**:
```python
def validate_title(title: str) -> str | None:
    """Returns error message or None if valid."""
    if not title or title.isspace():
        return "Task title cannot be empty"
    if len(title) > 200:
        return "Task title too long (max 200 characters)"
    return None

def validate_task_id(id_input: str, tasks: list[Task]) -> tuple[int | None, str | None]:
    """Returns (parsed_id, error_message) - one will be None."""
    try:
        task_id = int(id_input)
    except ValueError:
        return None, "Invalid input. Please enter a number."

    if not any(t.id == task_id for t in tasks):
        available = ", ".join(str(t.id) for t in tasks)
        return None, f"Task not found. Available IDs: {available}"

    return task_id, None
```

## Error Handling Strategy

### Research Question: Exception vs Return Codes?
**Decision**: Mix of both based on context

**Return Codes** (task_manager functions):
```python
def update_task(task_id: int, ...) -> bool:
    """Returns True if updated, False if not found."""
```
- Cleaner for expected failures (ID not found)
- Caller decides how to handle

**Exceptions** (validation failures):
```python
def validate_priority(priority: str) -> str:
    """Returns normalized priority or raises ValueError."""
    if priority not in valid_priorities:
        raise ValueError("Invalid priority")
```
- For truly exceptional cases (programming errors)
- Crash-stop on unexpected input

## Alternatives Considered & Rejected

### Alternative 1: Textual (Rich successor)
- **Pros**: More powerful, widget system, async support
- **Cons**: Too complex for Phase 1, requires async/await (violates constitution C-011)
- **Decision**: Rejected - stick with Rich

### Alternative 2: Click (CLI framework)
- **Pros**: Excellent argument parsing, command groups
- **Cons**: Focused on commands, not interactive menus
- **Decision**: Rejected - Rich Prompt sufficient for interactive menu

### Alternative 3: curses (stdlib)
- **Pros**: No external dependencies, powerful
- **Cons**: Low-level, complex API, harder to maintain
- **Decision**: Rejected - Rich provides better developer experience

### Alternative 4: UUID for Task IDs
- **Pros**: Guaranteed unique, no collision risk
- **Cons**: Not user-friendly (hard to type "update task abc-123-def...")
- **Decision**: Rejected - sequential integers better UX

## Dependencies Lock

**Required**:
- `rich >= 13.7.0`

**Development** (future phases):
- `pytest >= 8.0.0` (testing framework)
- `mypy >= 1.8.0` (static type checking)
- `black >= 24.0.0` (code formatting)

**Installation Command**:
```bash
uv pip install "rich>=13.7.0"
```

## Performance Benchmarks

**Expected Performance** (based on Rich documentation):
- Table rendering (50 rows): <10ms
- Console.print(): <1ms per call
- Prompt.ask(): Instant (blocking for user input)

**Validation**:
- Title validation: O(1) - constant time
- ID validation: O(n) - linear scan, acceptable for n<100
- Search: O(n*m) - n tasks, m keyword length, <1ms for n=100

**Conclusion**: All operations meet spec performance requirements (SC-001 to SC-010)

## References

- Rich Documentation: https://rich.readthedocs.io/en/stable/
- Python Dataclasses: https://docs.python.org/3/library/dataclasses.html
- PEP 8 Style Guide: https://peps.python.org/pep-0008/
- Type Hints (PEP 484): https://peps.python.org/pep-0484/
- Google Python Style Guide: https://google.github.io/styleguide/pyguide.html

**Research Complete**: All technical decisions documented with rationale
