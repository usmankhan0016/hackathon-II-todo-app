# Create Task Breakdown

Break architecture plans into atomic, independently testable tasks following SpecKit format.

## Instructions

When this skill is invoked, analyze the architecture plan and create a numbered list of small, focused tasks that can each be completed and tested independently in under 30 minutes.

### Input Required
- Architecture plan reference (path to plan.md)
- Feature name
- Spec reference (path to spec.md)

### Task Format Template

```markdown
# Tasks: [Feature Name]

**Feature:** [Feature Name]
**Spec:** `specs/[feature-name]/spec.md`
**Plan:** `specs/[feature-name]/plan.md`
**Status:** Planning | In Progress | Complete
**Created:** [YYYY-MM-DD]
**Updated:** [YYYY-MM-DD]

---

## Task List

### T-001: [Clear, Actionable Title]

**Description:**
[2-3 sentences explaining what needs to be built and why]

**Preconditions:**
- [ ] [Condition 1 that must be met before starting]
- [ ] [Condition 2 that must be met before starting]

**Outputs:**
- `path/to/file.py` - [What this file contains]
  - `function_name()` - [What this function does]
  - `ClassName` - [What this class does]

**Acceptance Criteria:**
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

**Spec Reference:** `specs/[feature-name]/spec.md` §X.X

**Dependencies:** None | T-XXX, T-XXX

**Estimated Time:** [15-30] minutes

**Test Cases:**
```python
# Test case 1
def test_[scenario]():
    # Arrange
    [setup]
    # Act
    [action]
    # Assert
    [verification]
```

**Status:** Pending | In Progress | Complete | Blocked

---

### T-002: [Next Task Title]
...
```

---

## Task Sizing Rules

### Rule 1: One Task = One Unit of Work
- ✅ **Good:** "Create Task dataclass in models.py"
- ❌ **Too Big:** "Implement entire models.py module"
- ❌ **Too Small:** "Add import statement"

### Rule 2: Must Be Independently Testable
- ✅ **Good:** "Implement add_task() function with validation"
- ❌ **Not Testable:** "Add comments to code"
- ✅ **Good:** "Create display_task() formatter function"

### Rule 3: Maximum 30 Minutes
- If a task takes longer, break it down further
- Prefer smaller tasks over larger ones
- Each task should have 3-5 acceptance criteria maximum

### Rule 4: Minimal Dependencies
- Maximum 2 dependencies per task
- If more dependencies exist, restructure tasks
- Prefer parallel tasks over sequential when possible

### Rule 5: Clear Outputs
- Must produce specific, verifiable artifacts
- File paths must be explicit
- Function/class names must be specified

---

## Standard Task Patterns

### Pattern 1: Create Data Model
```markdown
### T-XXX: Create Task Dataclass

**Description:**
Create the Task dataclass in models.py with all required fields and type hints. This serves as the core data structure for representing todo items throughout the application.

**Preconditions:**
- [ ] models.py file exists or can be created
- [ ] Python dataclasses library available

**Outputs:**
- `src/models.py`
  - `Task` dataclass with fields: id, title, description, completed
  - Type hints for all fields
  - Default values where appropriate

**Acceptance Criteria:**
- [ ] Task dataclass defined with @dataclass decorator
- [ ] All fields have type hints (int, str, bool)
- [ ] Default values set for description ("") and completed (False)
- [ ] Dataclass can be instantiated with valid data
- [ ] Fields are accessible via dot notation

**Spec Reference:** `specs/[feature]/spec.md` §3.1

**Dependencies:** None

**Estimated Time:** 15 minutes

**Test Cases:**
```python
def test_task_creation():
    task = Task(id=1, title="Test task")
    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == ""
    assert task.completed == False
```

**Status:** Pending
```

### Pattern 2: Add Validation Method
```markdown
### T-XXX: Add Task Validation Method

**Description:**
Implement the validate() method in the Task dataclass to check all field constraints. Returns a tuple of (is_valid, error_message) to enable graceful error handling.

**Preconditions:**
- [ ] T-XXX: Task dataclass exists

**Outputs:**
- `src/models.py`
  - `Task.validate()` method returning `Tuple[bool, Optional[str]]`

**Acceptance Criteria:**
- [ ] validate() method checks title is non-empty
- [ ] validate() method checks title is ≤ 100 characters
- [ ] validate() method checks description is ≤ 500 characters
- [ ] Returns (True, None) when validation passes
- [ ] Returns (False, error_message) when validation fails

**Spec Reference:** `specs/[feature]/spec.md` §3.2

**Dependencies:** T-XXX

**Estimated Time:** 20 minutes

**Test Cases:**
```python
def test_task_validation_success():
    task = Task(id=1, title="Valid title")
    is_valid, error = task.validate()
    assert is_valid == True
    assert error == None

def test_task_validation_empty_title():
    task = Task(id=1, title="")
    is_valid, error = task.validate()
    assert is_valid == False
    assert "empty" in error.lower()
```

**Status:** Pending
```

### Pattern 3: Implement CRUD Function
```markdown
### T-XXX: Implement add_task() Function

**Description:**
Create the add_task() function in task_manager.py that validates input, creates a Task object, assigns an auto-incremented ID, and appends it to the tasks list.

**Preconditions:**
- [ ] T-XXX: Task dataclass exists
- [ ] T-XXX: Task.validate() method exists
- [ ] task_manager.py has tasks list and next_id initialized

**Outputs:**
- `src/task_manager.py`
  - `add_task(title: str, description: str = "") -> Tuple[Task, Optional[str]]`

**Acceptance Criteria:**
- [ ] Function validates title and description
- [ ] Function creates Task with auto-incremented ID
- [ ] Function calls Task.validate() before adding
- [ ] Function appends task to global tasks list
- [ ] Function returns (task, None) on success
- [ ] Function returns (None, error_message) on failure

**Spec Reference:** `specs/[feature]/spec.md` §4.1

**Dependencies:** T-XXX, T-XXX

**Estimated Time:** 25 minutes

**Test Cases:**
```python
def test_add_task_success():
    task, error = add_task("Test task", "Description")
    assert error is None
    assert task.id == 1
    assert task.title == "Test task"
    assert len(tasks) == 1

def test_add_task_empty_title():
    task, error = add_task("")
    assert task is None
    assert "empty" in error.lower()
```

**Status:** Pending
```

### Pattern 4: Create Display Function
```markdown
### T-XXX: Create display_task() Function

**Description:**
Implement display_task() in cli.py to format and print a single task with consistent styling, including ID, title, status indicator, and description.

**Preconditions:**
- [ ] T-XXX: Task dataclass exists
- [ ] cli.py file exists or can be created

**Outputs:**
- `src/cli.py`
  - `display_task(task: Task) -> None`

**Acceptance Criteria:**
- [ ] Function prints task ID, title, and status on first line
- [ ] Function uses checkmark symbol (✓) for completed tasks
- [ ] Function uses empty box (☐) for incomplete tasks
- [ ] Function prints description indented on second line
- [ ] Output matches format specified in spec

**Spec Reference:** `specs/[feature]/spec.md` §5.1

**Dependencies:** T-XXX

**Estimated Time:** 20 minutes

**Test Cases:**
```python
def test_display_task_incomplete(capsys):
    task = Task(id=1, title="Test", description="Desc", completed=False)
    display_task(task)
    captured = capsys.readouterr()
    assert "☐" in captured.out
    assert "Test" in captured.out

def test_display_task_complete(capsys):
    task = Task(id=1, title="Test", description="Desc", completed=True)
    display_task(task)
    captured = capsys.readouterr()
    assert "✓" in captured.out
```

**Status:** Pending
```

### Pattern 5: Add Command Handler
```markdown
### T-XXX: Add Command Handler for [Action]

**Description:**
Create handle_[action]() function in main.py that prompts for user input, calls the appropriate task_manager function, and displays the result using cli functions.

**Preconditions:**
- [ ] T-XXX: [required task_manager function] exists
- [ ] T-XXX: [required cli function] exists
- [ ] main.py has command routing infrastructure

**Outputs:**
- `src/main.py`
  - `handle_[action]() -> None`

**Acceptance Criteria:**
- [ ] Function prompts user for required input
- [ ] Function validates user input before processing
- [ ] Function calls task_manager function with validated input
- [ ] Function displays success message on successful operation
- [ ] Function displays error message on failure
- [ ] Function handles edge cases gracefully

**Spec Reference:** `specs/[feature]/spec.md` §6.1

**Dependencies:** T-XXX, T-XXX

**Estimated Time:** 25 minutes

**Test Cases:**
```python
def test_handle_[action]_success(monkeypatch, capsys):
    # Mock user input
    inputs = iter(["Test input"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    handle_[action]()

    captured = capsys.readouterr()
    assert "success" in captured.out.lower()
```

**Status:** Pending
```

### Pattern 6: Update Menu System
```markdown
### T-XXX: Add [Feature] Option to Menu

**Description:**
Update display_menu() in cli.py to include the new [feature] command option and update handle_command() in main.py to route the command to the appropriate handler.

**Preconditions:**
- [ ] T-XXX: handle_[action]() exists
- [ ] cli.py has display_menu() function
- [ ] main.py has handle_command() function

**Outputs:**
- `src/cli.py`
  - Updated `display_menu()` with new option
- `src/main.py`
  - Updated `handle_command()` with new route

**Acceptance Criteria:**
- [ ] Menu displays new command option with description
- [ ] Command is added to command_map dictionary
- [ ] Entering command triggers correct handler
- [ ] Menu formatting remains consistent
- [ ] Command help text is clear and concise

**Spec Reference:** `specs/[feature]/spec.md` §6.2

**Dependencies:** T-XXX

**Estimated Time:** 15 minutes

**Test Cases:**
```python
def test_menu_includes_new_option(capsys):
    display_menu()
    captured = capsys.readouterr()
    assert "[command]" in captured.out.lower()

def test_command_routing(monkeypatch):
    # Test that command routes to correct handler
    pass
```

**Status:** Pending
```

### Pattern 7: Write Unit Tests
```markdown
### T-XXX: Write Unit Tests for [Component]

**Description:**
Create comprehensive unit tests for [component] covering all success paths, error cases, and edge cases using pytest framework.

**Preconditions:**
- [ ] T-XXX: [Component to test] is implemented
- [ ] pytest is installed and configured

**Outputs:**
- `tests/test_[component].py`
  - Test class with 5-10 test methods
  - Fixtures for common test data
  - Tests for success, failure, and edge cases

**Acceptance Criteria:**
- [ ] All public functions have at least one test
- [ ] Success paths are tested
- [ ] Error cases are tested
- [ ] Edge cases (empty input, invalid data) are tested
- [ ] All tests pass when run with pytest
- [ ] Test coverage is > 80% for the module

**Spec Reference:** `specs/[feature]/spec.md` §7.1

**Dependencies:** T-XXX

**Estimated Time:** 30 minutes

**Test Cases:**
```python
# The tests themselves are the test cases
class TestComponent:
    def test_success_case(self):
        pass

    def test_error_case(self):
        pass

    def test_edge_case(self):
        pass
```

**Status:** Pending
```

---

## Task Organization Strategy

### Phase 1: Foundation (Models & Data)
Tasks that create core data structures with no dependencies
- T-001: Create dataclasses
- T-002: Add validation methods
- T-003: Add any model helper methods

### Phase 2: Business Logic (Task Manager)
Tasks that implement CRUD and business rules
- T-004: Initialize storage (tasks list, next_id)
- T-005: Implement add function
- T-006: Implement view functions
- T-007: Implement update function
- T-008: Implement delete function
- T-009: Implement feature-specific logic

### Phase 3: User Interface (CLI)
Tasks that handle display and input
- T-010: Create display functions
- T-011: Create input handling functions
- T-012: Create formatting helpers
- T-013: Update menu display

### Phase 4: Integration (Main)
Tasks that wire everything together
- T-014: Create command handlers
- T-015: Update command routing
- T-016: Add error handling

### Phase 5: Testing & Quality
Tasks that verify correctness
- T-017: Write model tests
- T-018: Write task_manager tests
- T-019: Write cli tests
- T-020: Write integration tests
- T-021: Manual testing and bug fixes

---

## Dependency Management

### Good Dependency Example
```markdown
**Dependencies:** T-001, T-002
```
- Clear which tasks must complete first
- Maximum 2 dependencies
- Dependencies are from earlier phases

### Bad Dependency Example
```markdown
**Dependencies:** T-001, T-002, T-003, T-005, T-007
```
- ❌ Too many dependencies (> 2)
- Should be restructured or split

### Parallel Tasks (No Dependencies)
```markdown
**Dependencies:** None
```
- Can be worked on simultaneously
- Ideal for team collaboration
- Faster overall completion

---

## Acceptance Criteria Guidelines

### Good Acceptance Criteria
- [ ] Function returns tuple (bool, Optional[str])
- [ ] Title validation checks for empty string
- [ ] Description is trimmed of whitespace
- [ ] Task is appended to global tasks list
- [ ] next_id is incremented after adding

**Why Good:**
- Specific and measurable
- Can be checked with unit tests
- Clearly defines "done"

### Bad Acceptance Criteria
- [ ] Function works correctly
- [ ] Code is clean
- [ ] Everything is tested

**Why Bad:**
- Too vague
- Not measurable
- Not testable

---

## Usage

To use this skill:

1. Read the architecture plan from `specs/[feature]/plan.md`
2. Identify all functions, classes, and components to create
3. Break each component into a separate task
4. Order tasks by dependency (foundation → logic → UI → integration)
5. Ensure each task:
   - Has clear outputs (files and functions)
   - Takes < 30 minutes
   - Has ≤ 2 dependencies
   - Has 3-5 testable acceptance criteria
   - Includes test case examples
6. Number tasks sequentially (T-001, T-002, ...)
7. Save to `specs/[feature]/tasks.md`

## Task Breakdown Process

### Step 1: Extract Components from Plan
Read plan.md and list all:
- Dataclasses to create
- Functions to implement
- Display functions needed
- Command handlers required

### Step 2: Create Task for Each Component
Each item becomes one task following the appropriate pattern

### Step 3: Add Validation Tasks
For each dataclass/function, add validation task if needed

### Step 4: Add Test Tasks
Create test tasks for each module (models, task_manager, cli)

### Step 5: Add Integration Tasks
Create tasks for command handlers and menu updates

### Step 6: Order by Dependencies
Arrange tasks so dependencies come before dependents

### Step 7: Verify Task Size
Ensure each task is < 30 minutes; split if necessary

### Step 8: Add Spec References
Link each task to the relevant section in spec.md

---

## Output Format

Save the completed task breakdown as:
```
specs/[feature-name]/tasks.md
```

Where `[feature-name]` matches the spec and plan directory names.

---

## Quality Checklist

For each task, verify:
- [ ] Has unique sequential ID (T-XXX)
- [ ] Title is one clear sentence
- [ ] Description is 2-3 sentences
- [ ] Preconditions are explicit and checkable
- [ ] Outputs list specific files and functions
- [ ] Acceptance criteria are testable (3-5 items)
- [ ] Spec reference links to correct section
- [ ] Dependencies listed (≤ 2) or None
- [ ] Estimated time is 15-30 minutes
- [ ] Test cases included with example code
- [ ] Status field present (Pending/In Progress/Complete/Blocked)

For the overall task list, verify:
- [ ] Tasks are ordered by dependencies
- [ ] No circular dependencies exist
- [ ] Parallel tasks are identified
- [ ] Total estimated time is reasonable
- [ ] All plan components are covered
- [ ] Tasks follow phase organization (models → logic → UI → integration → testing)

---

## Best Practices

1. **Start with Data Models:** Always begin with Task dataclass and validation
2. **One Function Per Task:** Don't combine multiple functions into one task
3. **Test as You Go:** Create test tasks immediately after implementation tasks
4. **Clear Outputs:** Always specify exact file paths and function names
5. **Minimal Dependencies:** Prefer tasks that can be done in parallel
6. **Concrete Examples:** Include actual test code in task descriptions
7. **Consistent Naming:** Use same terminology as spec and plan
8. **Realistic Estimates:** Be honest about 30-minute limit
9. **Checkable Criteria:** Every acceptance criterion must be verifiable
10. **Complete Coverage:** Every function in the plan should have a task

---

## Common Pitfalls to Avoid

❌ **Too Large:** "Implement entire task_manager.py" → Split into one task per function
❌ **Too Vague:** "Make it work" → Define specific outputs and criteria
❌ **Too Many Dependencies:** Task depends on 5 others → Restructure or split
❌ **Not Testable:** "Improve code quality" → Define measurable criteria
❌ **Missing Outputs:** No file paths specified → Always list exact files
❌ **No Examples:** No test cases shown → Always include test code
❌ **Wrong Order:** UI task before data model task → Order by dependencies
❌ **Unrealistic Time:** Task takes 2 hours → Split into smaller tasks
