# Feature Specification: Phase 1 - Todo Console App

**Feature Branch**: `001-phase1-console-app`
**Created**: 2026-01-02
**Status**: Draft
**Input**: User description: "Phase 1: Todo Console App - Create a comprehensive specification for Phase 1 of the Todo application: an in-memory Python console app with an attractive CLI interface."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and View Tasks (Priority: P1)

As a user, I want to add new tasks and see them displayed in an organized list, so that I can start tracking my todos immediately.

**Why this priority**: This is the core MVP - without the ability to create and view tasks, the application has no value. This represents the minimum viable functionality.

**Independent Test**: Can be fully tested by launching the app, adding 3 tasks with different titles, and verifying they appear in a formatted table with auto-generated IDs and timestamps. Delivers immediate value as a basic task tracker.

**Acceptance Scenarios**:

1. **Given** the app is running and showing the main menu, **When** I select "Add Task" and enter a title "Buy groceries", **Then** the task is created with ID 1, displays success confirmation, and appears in the task list
2. **Given** I have added 2 tasks, **When** I select "View All Tasks", **Then** I see a formatted table showing both tasks with ID, Title, Status (⏳ Pending), and a count summary "Total: 2 tasks (0 completed, 2 pending)"
3. **Given** no tasks exist, **When** I select "View All Tasks", **Then** I see a friendly message "No tasks found. Add your first task to get started!"

---

### User Story 2 - Mark Tasks Complete (Priority: P2)

As a user, I want to mark tasks as complete or incomplete, so that I can track my progress and see what's been accomplished.

**Why this priority**: This adds the critical "done" state that makes a todo list functional. Without this, users can only accumulate tasks without closure.

**Independent Test**: Can be tested independently by pre-populating 3 tasks, marking task ID 2 as complete, and verifying the status changes from "⏳ Pending" to "✓ Done" with visual confirmation. Delivers the satisfaction of task completion.

**Acceptance Scenarios**:

1. **Given** I have a task with ID 1 in pending status, **When** I select "Mark Task Complete" and enter ID 1, **Then** the task status changes to "✓ Done" and I see confirmation "Task 1 marked as complete"
2. **Given** I have a task with ID 2 already completed, **When** I select "Mark Task Complete" and enter ID 2, **Then** the task status toggles back to "⏳ Pending" and I see "Task 2 marked as pending"
3. **Given** I mark task 3 as complete, **When** I view all tasks, **Then** the task count shows "Total: 3 tasks (1 completed, 2 pending)"

---

### User Story 3 - Update Task Details (Priority: P3)

As a user, I want to modify task titles and descriptions after creation, so that I can correct mistakes or update details as tasks evolve.

**Why this priority**: This provides flexibility but isn't critical for basic functionality. Users can work around this by deleting and recreating tasks if needed.

**Independent Test**: Can be tested by creating a task "Call mom", updating the title to "Call mom about birthday dinner" and adding description "Ask about menu preferences", then verifying changes appear in the task list.

**Acceptance Scenarios**:

1. **Given** I have a task with ID 1 titled "Buy groceries", **When** I select "Update Task", enter ID 1, and provide new title "Buy groceries and household items", **Then** the task title updates and I see "Task 1 updated successfully"
2. **Given** task ID 2 has no description, **When** I update it to add description "Call before 5pm", **Then** the description is saved and the updated_at timestamp refreshes
3. **Given** I try to update task ID 99 which doesn't exist, **When** I submit the update, **Then** I see error "Task not found with ID: 99. Available task IDs: 1, 2, 3"

---

### User Story 4 - Delete Unwanted Tasks (Priority: P3)

As a user, I want to remove tasks I no longer need, so that my task list stays clean and relevant.

**Why this priority**: This is useful for housekeeping but not essential for core functionality. Users can ignore unwanted tasks if deletion isn't available.

**Independent Test**: Can be tested by creating 3 tasks, deleting task ID 2, and verifying it no longer appears in the list and the task count decreases from 3 to 2.

**Acceptance Scenarios**:

1. **Given** I have 3 tasks and want to remove task ID 2 titled "Old task", **When** I select "Delete Task" and enter ID 2, **Then** the task is removed and I see "Deleted task: Old task"
2. **Given** I delete task ID 1, **When** I view all tasks, **Then** task ID 1 no longer appears and the count shows "Total: 2 tasks"
3. **Given** I try to delete task ID 99 which doesn't exist, **When** I submit the delete request, **Then** I see error "Task not found with ID: 99. Available task IDs: 1, 2, 3"

---

### User Story 5 - Prioritize and Categorize Tasks (Priority: P4)

As a user, I want to assign priority levels (High/Medium/Low) and tags to tasks, so that I can organize and focus on what's most important.

**Why this priority**: This is an enhancement that adds organization capabilities but isn't required for basic task tracking. Users can manually indicate priority in task titles if needed.

**Independent Test**: Can be tested by creating a task, assigning it "High" priority and tags "work, urgent", then viewing the task list to verify priority and tags display correctly with color coding.

**Acceptance Scenarios**:

1. **Given** I'm creating a new task "Finish project report", **When** I assign priority "High" and tags "work, deadline", **Then** the task is created with High priority (color-coded red) and displays tags in the task list
2. **Given** I have a task with Medium priority, **When** I view all tasks, **Then** I see the task with yellow color coding and "Medium" label
3. **Given** I try to set an invalid priority "Critical", **When** I submit, **Then** I see error "Invalid priority. Choose: High, Medium, or Low" and the system defaults to "Medium"

---

### User Story 6 - Search and Filter Tasks (Priority: P5)

As a user, I want to search tasks by keyword and filter by status, priority, or tags, so that I can quickly find specific tasks in a large list.

**Why this priority**: This becomes valuable only when users have many tasks. For initial use with few tasks, it's not essential.

**Independent Test**: Can be tested by creating 10 tasks with various priorities and tags, searching for keyword "meeting", and verifying only matching tasks appear with a count like "Showing 3 matching tasks".

**Acceptance Scenarios**:

1. **Given** I have 10 tasks including 3 with "meeting" in the title, **When** I search for "meeting", **Then** I see only the 3 matching tasks and a message "Showing 3 matching tasks"
2. **Given** I have 5 tasks with 2 marked as High priority, **When** I filter by "High" priority, **Then** I see only the 2 high-priority tasks
3. **Given** I search for "nonexistent", **When** no matches are found, **Then** I see warning "⚠ No tasks match your search"

---

### User Story 7 - Sort Tasks (Priority: P6)

As a user, I want to sort tasks by title, priority, creation date, or status, so that I can view them in my preferred order.

**Why this priority**: This is a convenience feature that enhances usability but isn't critical. Tasks can be scanned visually in the default order.

**Independent Test**: Can be tested by creating 5 tasks with different priorities and dates, selecting "Sort by Priority" (high to low), and verifying tasks reorder with high-priority tasks at the top.

**Acceptance Scenarios**:

1. **Given** I have 5 tasks with mixed priorities, **When** I sort by priority (high to low), **Then** tasks reorder with High priority first, Medium second, Low last
2. **Given** I sort by title alphabetically, **When** I view tasks, **Then** they appear in A-Z order and the sort persists during the session
3. **Given** I sort by creation date (newest first), **When** I add a new task, **Then** it appears at the top of the list

---

### Edge Cases

- **Empty title submission**: What happens when user submits a task with only whitespace or empty string? System should reject with error "Task title cannot be empty. Please provide a title."
- **Very long title (>200 characters)**: System should truncate at 200 characters or reject with validation error
- **Invalid ID input**: When user enters "abc" instead of a number for task ID, system should show "Invalid input. Please enter a valid task ID number."
- **Rapid task creation**: When user quickly adds 100+ tasks, system should handle without performance degradation (in-memory list should scale)
- **Special characters in title**: System should properly display emojis, international characters, and special symbols without breaking the table formatting
- **Session persistence**: Data is lost when app exits (expected behavior for Phase 1) - user should be aware this is in-memory only

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create new tasks with a required title (1-200 characters) and optional description (max 1000 characters)
- **FR-002**: System MUST auto-generate sequential task IDs starting from 1 and incrementing for each new task
- **FR-003**: System MUST timestamp each task with creation time (created_at) and last modification time (updated_at)
- **FR-004**: System MUST display all tasks in a formatted table showing ID, Title, Status, Priority, and Tags
- **FR-005**: System MUST allow users to toggle task completion status between "Pending" (⏳) and "Done" (✓)
- **FR-006**: System MUST allow users to update task title and description while preserving the original created_at timestamp
- **FR-007**: System MUST allow users to delete tasks by ID and confirm deletion with the task title
- **FR-008**: System MUST validate that task IDs exist before performing update, delete, or status change operations
- **FR-009**: System MUST display task count summary showing total tasks, completed count, and pending count
- **FR-010**: System MUST store all tasks in-memory using a Python list with no persistence between sessions
- **FR-011**: System MUST provide a menu-driven interface with numbered options (1-9) for all operations
- **FR-012**: System MUST use Rich library for all UI output including panels, tables, and colored messages
- **FR-013**: System MUST color-code tasks and messages: Green (completed/success), Yellow (pending/warning), Red (error), Cyan (headers)
- **FR-014**: System MUST display visual status indicators: ✓ for completed tasks, ⏳ for pending tasks
- **FR-015**: System MUST validate task title is not empty or whitespace-only before creation
- **FR-016**: System MUST allow users to assign priority levels (High, Medium, Low) to tasks with Medium as default
- **FR-017**: System MUST allow users to assign multiple tags (max 5) to tasks, each tag max 20 characters
- **FR-018**: System MUST support case-insensitive keyword search across task titles and descriptions
- **FR-019**: System MUST allow filtering tasks by status (all, pending, completed), priority level, and tags
- **FR-020**: System MUST allow sorting tasks by title, priority, creation date, or status in ascending/descending order
- **FR-021**: System MUST persist sort preference during the current session (until app exits)
- **FR-022**: System MUST display friendly error messages with actionable suggestions when operations fail
- **FR-023**: System MUST show available task IDs in error messages when a non-existent ID is referenced
- **FR-024**: System MUST handle invalid menu selections by re-prompting the user without crashing

### Key Entities *(include if feature involves data)*

- **Task**: Represents a single todo item. Key attributes: unique ID (integer), title (string, required), description (string, optional), completion status (boolean), priority level (High/Medium/Low), tags (list of strings), creation timestamp, last update timestamp. Each task is independently identifiable by its ID.

- **TaskList**: Represents the in-memory collection of all tasks. This is a Python list that maintains task order and supports sequential ID generation. Relationship: contains zero or more Task entities. State is lost when application exits (no persistence).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a new task and see it in the task list in under 10 seconds from menu selection
- **SC-002**: Users can complete all 5 basic CRUD operations (Create, Read, Update, Delete, Mark Complete) without encountering errors
- **SC-003**: The application handles at least 100 tasks without noticeable performance degradation (list operations remain responsive)
- **SC-004**: 100% of task operations (add, update, delete, complete) provide immediate visual confirmation with color-coded success/error messages
- **SC-005**: Users can visually distinguish between completed and pending tasks at a glance through color coding and status symbols
- **SC-006**: All error scenarios (invalid ID, empty title, non-existent task) display helpful error messages within 1 second
- **SC-007**: The task table displays properly formatted with aligned columns, borders, and readable text for lists up to 50 tasks
- **SC-008**: Users can navigate the menu system without needing to reference external documentation (menu is self-explanatory)
- **SC-009**: Task count summary accurately reflects current state after every add, delete, or status change operation
- **SC-010**: Search operations return filtered results in under 1 second for task lists up to 100 items

### Assumptions

- **A-001**: Users have Python 3.13+ installed on their system
- **A-002**: Users will run the application from a terminal that supports Unicode characters (for emojis and special symbols)
- **A-003**: Users understand that data is not persisted between sessions (in-memory only for Phase 1)
- **A-004**: Users have the UV package manager available for dependency installation
- **A-005**: Terminal width is at least 80 characters to properly display the task table
- **A-006**: Users will interact with the application sequentially (one operation at a time, no concurrent operations expected)
- **A-007**: Task list size will typically be under 100 items during Phase 1 usage
- **A-008**: Users are comfortable with keyboard-based menu navigation (no mouse interaction)
- **A-009**: Default priority of "Medium" is acceptable when users don't specify priority explicitly
- **A-010**: Task IDs remain unique within a session even after deletions (IDs are not reused)

### Constraints

- **C-001**: Must use Python 3.13+ (no backward compatibility with older Python versions)
- **C-002**: Must use Rich library for all UI output (no alternative UI libraries)
- **C-003**: Must use UV for dependency management (no pip or other package managers)
- **C-004**: Must use Python dataclasses for Task model (no plain dictionaries or custom classes)
- **C-005**: Must use in-memory Python list for storage (no databases, files, or external storage)
- **C-006**: Must follow PEP 8 code style guidelines strictly
- **C-007**: Must include type hints on all functions and methods
- **C-008**: Must include docstrings (Google style) on all functions
- **C-009**: Must reference task IDs in code comments for traceability (format: `# Task: T-XXX`)
- **C-010**: No external dependencies beyond Rich library and Python standard library
- **C-011**: No async/await patterns (synchronous operations only)
- **C-012**: No file persistence or database connections
- **C-013**: Application must run entirely in the terminal (no GUI components)
- **C-014**: Must handle errors with try/except blocks (no uncaught exceptions that crash the app)

### Non-Goals (Out of Scope for Phase 1)

- **NG-001**: Data persistence between sessions (will be added in Phase 2 with database)
- **NG-002**: Multi-user support or user authentication (Phase 2)
- **NG-003**: Web interface or API endpoints (Phase 2)
- **NG-004**: Due dates, reminders, or recurring tasks (future enhancement)
- **NG-005**: Task attachments or file uploads
- **NG-006**: Collaborative features or task sharing
- **NG-007**: Export to external formats (CSV, JSON, PDF)
- **NG-008**: Integration with calendar or email systems
- **NG-009**: Mobile app or responsive web design
- **NG-010**: Cloud synchronization or backup
- **NG-011**: Advanced analytics or reporting dashboards
- **NG-012**: Keyboard shortcuts or command-line arguments (only menu-driven for now)
