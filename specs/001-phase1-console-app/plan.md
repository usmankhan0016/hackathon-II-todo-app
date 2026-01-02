# Implementation Plan: Phase 1 - Todo Console App

**Branch**: `001-phase1-console-app` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase1-console-app/spec.md`

## Summary

Build an in-memory Python console application for task management with a modern, attractive CLI interface using the Rich library. The application implements complete CRUD operations (Create, Read, Update, Delete, Mark Complete) for tasks with optional priority levels, tags, search, filter, and sort capabilities. All data stored in-memory (Python list) with no persistence between sessions. Target users: individuals tracking personal todos via terminal.

**Technical Approach**: 5-module Python architecture (models, task_manager, ui, cli, main) with strict separation of concerns. Rich library handles all UI rendering with color-coded output, styled tables, and panels. Sequential ID generation for tasks. Type-safe implementation with full type hints and Google-style docstrings.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Rich >= 13.7.0 (terminal UI library), Python standard library (dataclasses, datetime, typing)
**Storage**: In-memory Python list (no persistence, data lost on exit)
**Testing**: pytest for unit tests (Phase 1 manual testing, automated tests in later phases)
**Target Platform**: Cross-platform terminal (Linux, macOS, Windows with WSL 2), minimum 80-character terminal width, Unicode support required
**Project Type**: Single console application
**Performance Goals**: Instant response (<100ms) for all operations, handle 100+ tasks without noticeable degradation, search/filter operations complete in <1 second
**Constraints**: No external dependencies beyond Rich library, PEP 8 compliance mandatory, type hints required on all functions, synchronous operations only (no async), Python dataclasses for Task model
**Scale/Scope**: Single-user application, 5 Python modules (~500-800 LOC total), 7 user stories (P1-P6 prioritized), 24 functional requirements, session-scoped task lists (typically <100 tasks)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Spec-Driven Development (Principle I)
- [x] Specification complete and approved (spec.md exists with all requirements)
- [x] Plan follows Specify → Plan → Tasks → Implement sequence
- [x] All code will be generated via Claude Code (no manual coding)
- [x] Task traceability enforced (every file will reference Task IDs)

### ✅ Progressive Complexity (Principle II)
- [x] Phase 1 is foundational console app (correct phase in sequence)
- [x] No dependencies on future phases (standalone system)
- [x] Follows constitution Phase 1 architecture: models.py, task_manager.py, cli.py, ui.py, main.py

### ✅ Test-First Development (Principle III)
- [x] Acceptance criteria defined in spec for all user stories
- [x] Test strategy documented (manual testing for Phase 1, pytest structure prepared)
- [x] Red-Green-Refactor cycle will be followed during implementation

### ✅ User Experience Excellence (Principle IV)
- [x] Rich library for modern terminal UI (per Phase 1 constitution standards)
- [x] Color-coded output: Green (completed), Yellow (pending), Red (error), Cyan (headers)
- [x] Visual hierarchy with emojis: 📝, ✓, ⏳, 🔴
- [x] Styled panels, bordered tables, interactive menu system

### ✅ Code Quality and Standards (Principle VI)
- [x] Python 3.13+ (constitution requirement)
- [x] PEP 8 compliance enforced
- [x] Type hints on all functions (constitution requirement)
- [x] Google-style docstrings mandatory
- [x] Dataclasses for Task model (constitution requirement)
- [x] UV for dependency management (constitution requirement)

### ✅ Architecture Standards (Principle VII)
- [x] Follows constitution Phase 1 module structure (5 modules)
- [x] Code will be placed in `src/phase1/` as per monorepo structure
- [x] Separation of concerns: models → business logic → UI → input → orchestration

### ✅ Dependency Management (Principle VIII)
- [x] Only approved Phase 1 libraries: Rich + Python standard library
- [x] No prohibited libraries (databases, async frameworks, unapproved UI tools)

### ✅ Documentation and Traceability (Principle IX)
- [x] PHR will be created after planning phase
- [x] Code comments will reference Task IDs (format: `# Task: T-XXX`)
- [x] All files will include spec section references

### ✅ Error Handling (Principle X)
- [x] Graceful handling of invalid inputs (per Phase 1 requirements)
- [x] Clear error messages with recovery suggestions
- [x] No silent failures (all errors displayed to user)
- [x] try/except blocks for exception handling

**Constitution Compliance**: PASS - All gates satisfied, no violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-console-app/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (Rich library patterns, Python best practices)
├── data-model.md        # Phase 1 output (Task dataclass, validation rules)
├── quickstart.md        # Phase 1 output (setup, run, usage instructions)
├── contracts/           # Phase 1 output (internal module contracts)
│   ├── models-contract.md
│   ├── task-manager-contract.md
│   ├── ui-contract.md
│   └── cli-contract.md
├── checklists/
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/phase1/
├── __init__.py          # Package marker
├── models.py            # Task dataclass, type definitions
├── task_manager.py      # In-memory CRUD operations, business logic
├── ui.py                # Rich library UI components (tables, panels, messages)
├── cli.py               # User input handling, validation, command routing
└── main.py              # Application entry point, main loop

tests/phase1/
├── __init__.py
├── unit/
│   ├── test_models.py
│   ├── test_task_manager.py
│   └── test_validation.py
└── integration/
    └── test_end_to_end.py

pyproject.toml           # UV project configuration, Rich dependency
README.md                # Project overview, setup instructions
.gitignore               # Python standard ignores
```

**Structure Decision**: Single project structure selected (Option 1 from template) because this is a standalone console application with no frontend/backend split or mobile components. All Phase 1 code isolated in `src/phase1/` to support future multi-phase monorepo structure. Clear module separation aligns with constitution's Phase 1 architecture requirements.

## Complexity Tracking

> **Not Applicable** - No constitution violations detected. All requirements satisfied within constitutional constraints.
## Phase 0: Research & Technical Decisions

### Rich Library UI Patterns

**Decision**: Use Rich library's high-level components (Table, Panel, Prompt) for all UI rendering

**Rationale**:
- Rich provides production-ready terminal UI components with minimal code
- Built-in color support, Unicode handling, and responsive layouts
- Active maintenance and wide adoption in Python CLI tools
- Declarative API aligns with clean code principles

**Alternatives Considered**:
1. **curses** (Python standard library) - Rejected: Low-level, complex API, harder to maintain
2. **Click** (command framework) - Rejected: Focused on argument parsing, not rich UI rendering
3. **Textual** (Rich successor) - Rejected: Too complex for Phase 1, async-based (violates constraints)

**Implementation Pattern**:
```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

# Pattern 1: Styled panels for headers
header = Panel("[cyan]📝 My Todo List[/cyan]", border_style="cyan")
console.print(header)

# Pattern 2: Tables for task lists
table = Table(title="Tasks", border_style="cyan")
table.add_column("ID", justify="center", width=5)
table.add_column("Title", style="white", width=30)
table.add_column("Status", justify="center", width=10)
table.add_row("1", "Buy groceries", "[green]✓ Done[/green]")

# Pattern 3: Prompts for user input
title = Prompt.ask("Enter task title")
```

### Sequential ID Generation Strategy

**Decision**: Use `max([t.id for t in tasks], default=0) + 1` for ID generation

**Rationale**:
- Simple, predictable ID assignment
- Works correctly even after task deletions
- IDs never reused within a session (per spec requirement A-010)
- Single expression, easy to test

**Alternatives Considered**:
1. **Counter variable** - Rejected: Requires state management, can drift from actual max ID
2. **UUID** - Rejected: Not sequential, harder for users to reference tasks by ID
3. **enumerate() with offset** - Rejected: Breaks after deletions

**Implementation Pattern**:
```python
def generate_next_id(tasks: list[Task]) -> int:
    """Generate next sequential task ID.
    
    Args:
        tasks: Current list of tasks
        
    Returns:
        Next available ID (1 if list empty, max_id + 1 otherwise)
    """
    return max([t.id for t in tasks], default=0) + 1
```

### Input Validation Strategy

**Decision**: Validate at CLI layer before passing to business logic

**Rationale**:
- Separation of concerns: CLI handles input validation, task_manager handles business rules
- Immediate feedback to user (fail fast)
- task_manager functions can assume valid input (cleaner code)
- Easier to test: validation logic isolated in CLI module

**Validation Rules**:
```python
# Title validation
def validate_title(title: str) -> str | None:
    """Validate task title.
    
    Returns:
        Error message if invalid, None if valid
    """
    if not title or title.isspace():
        return "Task title cannot be empty. Please provide a title."
    if len(title) > 200:
        return f"Task title too long ({len(title)} chars). Maximum 200 characters."
    return None

# ID validation
def validate_task_id(id_input: str, tasks: list[Task]) -> tuple[int | None, str | None]:
    """Validate and parse task ID.
    
    Returns:
        (parsed_id, error_message) - one will be None
    """
    try:
        task_id = int(id_input)
    except ValueError:
        return None, "Invalid input. Please enter a valid task ID number."
    
    if not any(t.id == task_id for t in tasks):
        available = ", ".join(str(t.id) for t in tasks)
        return None, f"Task not found with ID: {task_id}. Available task IDs: {available}"
    
    return task_id, None

# Priority validation
def validate_priority(priority: str) -> str:
    """Validate and normalize priority input.
    
    Returns normalized priority (High/Medium/Low) or raises ValueError
    """
    priority_map = {
        "high": "High",
        "medium": "Medium",
        "low": "Low",
        "h": "High",
        "m": "Medium",
        "l": "Low"
    }
    normalized = priority_map.get(priority.lower())
    if not normalized:
        raise ValueError("Invalid priority. Choose: High, Medium, or Low")
    return normalized
```

### Error Message Formatting

**Decision**: Use Rich markup with consistent icon prefixes for all messages

**Message Patterns**:
```python
# Success messages (green)
"[green]✓[/green] Task added successfully!"
"[green]✓[/green] Task {id} marked as complete"

# Error messages (red)
"[red]✗[/red] Task not found with ID: {id}"
"[red]✗[/red] Task title cannot be empty"

# Info messages (blue)
"[blue]ℹ[/blue] Showing {count} pending tasks"
"[blue]ℹ[/blue] No tasks found. Add your first task to get started!"

# Warning messages (yellow)
"[yellow]⚠[/yellow] No tasks match your search"
```

**Rationale**: Consistent visual language improves UX, color-coded feedback aids rapid comprehension

### Data Structure Decisions

**Decision**: Use Python dataclass with field() defaults for mutable fields

**Implementation**:
```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    """Represents a single todo task.
    
    Attributes:
        id: Unique task identifier (sequential)
        title: Task title (1-200 characters)
        description: Optional task description (max 1000 characters)
        completed: Completion status (False = pending, True = done)
        priority: Priority level (High/Medium/Low)
        tags: List of category tags (max 5 tags, 20 chars each)
        created_at: Timestamp when task was created
        updated_at: Timestamp of last modification
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "Medium"
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
```

**Rationale**:
- Dataclass reduces boilerplate (auto-generates `__init__`, `__repr__`, `__eq__`)
- `field(default_factory=list)` prevents mutable default argument bug
- `field(default_factory=datetime.now)` generates timestamp at instance creation time
- Type hints enable static type checking with mypy
- Aligns with constitution requirement C-004

## Phase 1: Design & Contracts

### Data Model

*Full data model documented in [data-model.md](./data-model.md)*

**Core Entity: Task**

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| id | int | Yes | Auto-generated | Positive integer, unique within session |
| title | str | Yes | - | 1-200 characters, not empty/whitespace |
| description | str | No | "" | Max 1000 characters |
| completed | bool | No | False | Boolean (pending/done) |
| priority | str | No | "Medium" | One of: "High", "Medium", "Low" |
| tags | list[str] | No | [] | Max 5 tags, each max 20 chars |
| created_at | datetime | Yes | Auto-generated | Immutable after creation |
| updated_at | datetime | Yes | Auto-generated | Refreshed on modification |

**State Transitions**:
```
[New] --create--> [Pending] --complete--> [Completed]
                     ↑                          |
                     +---------uncomplete-------+
                     
[Pending/Completed] --update--> [Pending/Completed] (status preserved)
[Pending/Completed] --delete--> [Deleted/Removed from list]
```

### Module Contracts

#### models.py Contract
*Full contract: [contracts/models-contract.md](./contracts/models-contract.md)*

**Exports**:
- `Task` dataclass
- `Priority` type alias: `Literal["High", "Medium", "Low"]`

**Responsibilities**:
- Define Task data structure
- Provide type definitions for domain objects
- No business logic (pure data)

**Dependencies**: None (only Python standard library)

#### task_manager.py Contract
*Full contract: [contracts/task-manager-contract.md](./contracts/task-manager-contract.md)*

**Exports**:
```python
# Global state
tasks: list[Task] = []

# CRUD operations
def add_task(title: str, description: str = "", priority: str = "Medium", tags: list[str] = []) -> Task
def get_all_tasks() -> list[Task]
def get_task_by_id(task_id: int) -> Task | None
def update_task(task_id: int, title: str | None = None, description: str | None = None) -> bool
def delete_task(task_id: int) -> bool
def toggle_complete(task_id: int) -> bool

# Query operations
def search_tasks(keyword: str) -> list[Task]
def filter_tasks(status: str | None = None, priority: str | None = None, tag: str | None = None) -> list[Task]
def sort_tasks(tasks: list[Task], by: str = "id", descending: bool = False) -> list[Task]

# Statistics
def get_task_stats() -> dict[str, int]  # {"total": 10, "completed": 3, "pending": 7}
```

**Responsibilities**:
- Manage global task list (in-memory storage)
- Implement business logic for CRUD operations
- Handle ID generation
- Provide query and filter capabilities
- No UI or input handling

**Dependencies**: `models.Task`

#### ui.py Contract
*Full contract: [contracts/ui-contract.md](./contracts/ui-contract.md)*

**Exports**:
```python
# Display functions
def display_header() -> None
def display_menu() -> None
def display_tasks_table(tasks: list[Task]) -> None
def display_task_stats(stats: dict[str, int]) -> None

# Message functions
def display_success(message: str) -> None
def display_error(message: str) -> None
def display_info(message: str) -> None
def display_warning(message: str) -> None

# Utility
def clear_screen() -> None
```

**Responsibilities**:
- Render all UI components using Rich library
- Format task data for display
- Display status messages with consistent styling
- No business logic or data manipulation

**Dependencies**: `models.Task`, `rich.console.Console`, `rich.table.Table`, `rich.panel.Panel`

#### cli.py Contract
*Full contract: [contracts/cli-contract.md](./contracts/cli-contract.md)*

**Exports**:
```python
# Input functions
def get_task_input() -> dict[str, str | list[str]]
def get_task_id() -> int | None
def get_update_fields() -> dict[str, str]
def get_search_keyword() -> str
def get_filter_criteria() -> dict[str, str]
def get_sort_options() -> tuple[str, bool]

# Command handlers
def handle_add_task() -> None
def handle_view_tasks() -> None
def handle_update_task() -> None
def handle_delete_task() -> None
def handle_toggle_complete() -> None
def handle_search_tasks() -> None
def handle_filter_tasks() -> None
def handle_sort_tasks() -> None

# Menu routing
def get_menu_choice() -> str
```

**Responsibilities**:
- Handle all user input (keyboard input via Rich Prompt)
- Validate input before passing to business logic
- Route menu choices to appropriate handlers
- Coordinate between task_manager and ui modules
- Display results of operations

**Dependencies**: `task_manager` (all functions), `ui` (all functions), `models.Task`, `rich.prompt.Prompt`

#### main.py Contract

**Exports**:
```python
def main() -> None
```

**Responsibilities**:
- Initialize Rich console
- Run main application loop
- Handle graceful exit (Ctrl+C)
- Top-level exception handling

**Dependencies**: `cli.get_menu_choice`, `cli` (all handlers), `ui.display_header`, `ui.display_info`

### Quickstart Guide

*Full guide: [quickstart.md](./quickstart.md)*

**Setup**:
```bash
# Clone repository
git clone <repo-url>
cd todo-app

# Checkout Phase 1 branch
git checkout 001-phase1-console-app

# Install dependencies with UV
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install rich

# Run application
python -m src.phase1.main
```

**Basic Usage**:
1. Launch app → Main menu appears
2. Press `1` → Add new task
3. Press `2` → View all tasks
4. Press `4` → Mark task complete
5. Press `9` → Exit

**Example Session**:
```
┌─────────────────────────────────────────┐
│         📝 My Todo List                 │
└─────────────────────────────────────────┘

╔════════════════════════════════════════╗
║          📋 MAIN MENU                  ║
╠════════════════════════════════════════╣
║  1. ➕ Add Task                        ║
║  2. 👁️  View All Tasks                 ║
║  3. ✏️  Update Task                    ║
║  4. ✅ Mark Task Complete              ║
║  5. 🗑️  Delete Task                    ║
║  6. 🔍 Search Tasks                    ║
║  7. 🏷️  Filter by Priority/Tag        ║
║  8. 🔄 Sort Tasks                      ║
║  9. 🚪 Exit                            ║
╚════════════════════════════════════════╝

Choose an option (1-9): 1

➕ Adding New Task

Enter task title: Buy groceries
Enter description (optional): Milk, eggs, bread
Enter priority (High/Medium/Low) [Medium]: High
Enter tags (comma-separated, max 5) []: home, urgent

✓ Task added successfully!
  ID: 1
  Title: Buy groceries
  Priority: High
  Tags: home, urgent
```

## Implementation Sequence

### Wave 1: Foundation (Tasks T-001 to T-010)
**Goal**: Get basic app structure running with core create/view functionality

1. **T-001**: Create `models.py` with Task dataclass
2. **T-002**: Create `task_manager.py` with global tasks list
3. **T-003**: Implement `add_task()` function in task_manager
4. **T-004**: Implement `get_all_tasks()` function in task_manager
5. **T-005**: Implement `generate_next_id()` helper in task_manager
6. **T-006**: Create `ui.py` with Rich console initialization
7. **T-007**: Implement `display_header()` and `display_menu()` in ui
8. **T-008**: Implement `display_tasks_table()` in ui
9. **T-009**: Implement message functions in ui (success, error, info, warning)
10. **T-010**: Create `main.py` with basic loop structure

**Checkpoint**: Can launch app, see menu, but no handlers wired yet

### Wave 2: Core CRUD (Tasks T-011 to T-020)
**Goal**: Wire all basic CRUD operations end-to-end

11. **T-011**: Implement `update_task()` in task_manager
12. **T-012**: Implement `delete_task()` in task_manager
13. **T-013**: Implement `toggle_complete()` in task_manager
14. **T-014**: Create `cli.py` with input functions
15. **T-015**: Implement `handle_add_task()` command handler
16. **T-016**: Implement `handle_view_tasks()` command handler
17. **T-017**: Implement `handle_update_task()` command handler
18. **T-018**: Implement `handle_delete_task()` command handler
19. **T-019**: Implement `handle_toggle_complete()` command handler
20. **T-020**: Wire all handlers to menu routing in main.py

**Checkpoint**: All 5 basic CRUD operations functional (US-1 to US-4 complete)

### Wave 3: Validation & Error Handling (Tasks T-021 to T-025)
**Goal**: Make app robust against invalid input

21. **T-021**: Implement validation functions in cli.py (title, ID, priority)
22. **T-022**: Add input validation to all CLI handlers
23. **T-023**: Implement error display patterns in ui.py
24. **T-024**: Add empty state handling (no tasks, no search results)
25. **T-025**: Add exception handling in main.py (KeyboardInterrupt, general exceptions)

**Checkpoint**: App handles all error scenarios gracefully

### Wave 4: Intermediate Features (Tasks T-026 to T-035)
**Goal**: Add priority, tags, search, filter, sort capabilities

26. **T-026**: Add priority field support to Task model (already in dataclass)
27. **T-027**: Add tags field support to Task model (already in dataclass)
28. **T-028**: Implement `filter_tasks()` function in task_manager
29. **T-029**: Implement `search_tasks()` function in task_manager
30. **T-030**: Implement `sort_tasks()` function in task_manager
31. **T-031**: Implement `handle_search_tasks()` command in cli
32. **T-032**: Implement `handle_filter_tasks()` command in cli
33. **T-033**: Implement `handle_sort_tasks()` command in cli
34. **T-034**: Update UI to display priority with color coding
35. **T-035**: Update UI to display tags in task table

**Checkpoint**: All intermediate features working (US-5, US-6, US-7 complete)

### Wave 5: Polish & Testing (Tasks T-036 to T-040)
**Goal**: Final refinements and comprehensive testing

36. **T-036**: Implement `get_task_stats()` in task_manager
37. **T-037**: Implement `display_task_stats()` in ui
38. **T-038**: Add confirmation prompts for destructive actions (delete)
39. **T-039**: Manual testing of all happy paths (spec scenarios 1-3 for each US)
40. **T-040**: Manual testing of all edge cases and error scenarios

**Checkpoint**: Phase 1 complete, ready for demo

## Dependency Graph

```
main.py
  ├─> cli.py
  │     ├─> task_manager.py
  │     │     └─> models.py
  │     ├─> ui.py
  │     │     └─> models.py
  │     └─> models.py (for type hints)
  └─> ui.py (for header display)

Implementation order (bottom-up):
1. models.py (no dependencies)
2. task_manager.py (depends on models)
3. ui.py (depends on models)
4. cli.py (depends on task_manager, ui, models)
5. main.py (depends on cli, ui)
```

## Testing Strategy

### Manual Testing Checklist
*Automated tests deferred to later phases per constitution*

**Wave 1 - Happy Paths** (After T-020):
- [ ] Launch app and see main menu
- [ ] Add task with title only → Task created with ID 1
- [ ] Add task with title + description → Task created with ID 2
- [ ] View tasks → See formatted table with both tasks
- [ ] Mark task 1 complete → Status changes to ✓
- [ ] Update task 2 title → Title changes, updated_at refreshes
- [ ] Delete task 1 → Task removed from list
- [ ] Exit app → Graceful shutdown

**Wave 2 - Edge Cases** (After T-025):
- [ ] Try to add task with empty title → Error displayed
- [ ] Try to add task with 250-char title → Error or truncation
- [ ] Try to update non-existent task (ID 999) → Error with available IDs
- [ ] Try to delete non-existent task → Error message
- [ ] View tasks when list is empty → "No tasks found" message
- [ ] Enter invalid menu choice (0, 10, "abc") → Re-prompt without crash
- [ ] Press Ctrl+C during operation → Graceful exit

**Wave 3 - Intermediate Features** (After T-035):
- [ ] Add task with High priority → Shows red color
- [ ] Add task with tags "work, urgent" → Tags display in table
- [ ] Search for "meeting" → Only matching tasks shown
- [ ] Filter by High priority → Only high-priority tasks shown
- [ ] Filter by tag "work" → Only tasks with "work" tag shown
- [ ] Sort by title A-Z → Tasks alphabetically ordered
- [ ] Sort by priority High→Low → High tasks first
- [ ] Add task after sorting → New task appears in sorted position

**Wave 4 - Performance** (After T-040):
- [ ] Add 50 tasks rapidly → No lag or crashes
- [ ] View 50-task list → Table renders correctly
- [ ] Search across 50 tasks → Results appear in <1 second
- [ ] Filter 50 tasks by priority → Results appear instantly

## Success Criteria Verification

*Map to spec Success Criteria SC-001 to SC-010*

- **SC-001** (task creation in <10 seconds): Verify during Wave 1 testing
- **SC-002** (all CRUD operations work): Verify during Wave 1 testing
- **SC-003** (handle 100+ tasks): Verify during Wave 4 performance testing
- **SC-004** (100% operations show confirmation): Verify all handlers display success/error messages
- **SC-005** (visual distinction of status): Verify color coding in display_tasks_table
- **SC-006** (errors display in <1 second): Verify during Wave 2 testing
- **SC-007** (table formats correctly): Verify with 50-task list in Wave 4
- **SC-008** (menu is self-explanatory): User feedback during final demo
- **SC-009** (task count accurate): Verify after every add/delete/complete operation
- **SC-010** (search in <1 second): Verify during Wave 3 testing with 100-task list

## Next Steps

1. ✅ **Planning Complete** - This document (plan.md)
2. **Generate Tasks** - Run `/sp.tasks` to create tasks.md with detailed task breakdown
3. **Implement** - Run `/sp.implement` to execute tasks sequentially
4. **Validate** - Manual testing against acceptance criteria
5. **Demo** - Record 90-second walkthrough video

**Ready for**: `/sp.tasks` command to generate atomic implementation tasks
