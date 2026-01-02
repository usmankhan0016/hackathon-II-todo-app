# Tasks: Phase 1 - Todo Console App

**Input**: Design documents from `/specs/001-phase1-console-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks grouped by user story to enable independent implementation and testing

## Format: `- [ ] [TaskID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, etc.) - only for user story implementation tasks
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure (src/phase1/, tests/phase1/)
- [X] T002 Initialize pyproject.toml with UV and configure Rich dependency (>=13.7.0)
- [X] T003 [P] Create .gitignore for Python project (*.pyc, __pycache__, .venv)
- [X] T004 [P] Create README.md with project overview and setup instructions per quickstart.md
- [X] T005 [P] Create src/phase1/__init__.py package marker

**Checkpoint**: ✅ Project structure ready for module implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data model and infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create Task dataclass in src/phase1/models.py with all 8 fields (id, title, description, completed, priority, tags, created_at, updated_at)
- [X] T007 Add Priority type alias and __post_init__ validation to Task dataclass in src/phase1/models.py
- [X] T008 Create task_manager.py with global tasks list and generate_next_id() function in src/phase1/task_manager.py
- [X] T009 Create Rich Console instance and initialize ui.py module in src/phase1/ui.py
- [X] T010 Create cli.py module structure with placeholder imports in src/phase1/cli.py

**Checkpoint**: ✅ Foundation ready - TDD test setup can now begin

---

## Phase 2.5: Test Setup & Red Phase (TDD) 🧪

**Purpose**: Configure pytest and write failing tests for all CRUD operations (Red-Green-Refactor cycle)

**⚠️ CRITICAL**: Constitution Principle III mandates Test-First Development - tests MUST be written and FAIL before implementation

### Test Infrastructure Setup

- [ ] T011 Create tests/phase1/ directory structure with __init__.py and subdirectories (unit/, integration/)
- [ ] T012 Add pytest>=8.0.0 to pyproject.toml dependencies via UV
- [ ] T013 Create pytest.ini configuration file in project root (test paths, markers, output verbosity)
- [ ] T014 Create tests/phase1/conftest.py with test fixtures (sample_task, empty_task_list, populated_task_list)

### Red Phase - Write Failing Unit Tests

**⚠️ IMPORTANT**: Each test MUST fail initially (no implementation exists yet)

- [ ] T015 [P] Write tests/phase1/unit/test_models.py - test Task dataclass validation (__post_init__, field constraints, Priority type)
- [ ] T016 [P] Write tests/phase1/unit/test_task_manager.py - test add_task() function (ID generation, timestamps, task creation)
- [ ] T017 [P] Write tests/phase1/unit/test_task_manager.py - test get_all_tasks() function (returns copy, not original list)
- [ ] T018 [P] Write tests/phase1/unit/test_task_manager.py - test get_task_by_id() function (find existing, return None for non-existent)
- [ ] T019 [P] Write tests/phase1/unit/test_task_manager.py - test update_task() function (title/description update, updated_at refresh, preserve created_at)
- [ ] T020 [P] Write tests/phase1/unit/test_task_manager.py - test delete_task() function (remove from list, return True/False, ID persistence)
- [ ] T021 [P] Write tests/phase1/unit/test_task_manager.py - test toggle_complete() function (flip status, update timestamp)
- [ ] T022 [P] Write tests/phase1/unit/test_task_manager.py - test search_tasks() function (case-insensitive, title and description search)
- [ ] T023 [P] Write tests/phase1/unit/test_task_manager.py - test filter_tasks() function (status/priority/tag filtering, combined filters)
- [ ] T024 [P] Write tests/phase1/unit/test_task_manager.py - test sort_tasks() function (all sort fields, ascending/descending)
- [ ] T025 Run pytest -v and verify ALL tests FAIL with appropriate error messages (ModuleNotFoundError or AttributeError expected)

**Checkpoint**: Red phase complete - All tests written and failing ✅ Ready for Green phase (implementation)

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add new tasks with title and see them displayed in a formatted table

**Independent Test**: Launch app, add 3 tasks with different titles, view task list showing IDs and titles in formatted table

### Implementation for User Story 1 (Green Phase - Make Tests Pass)

- [ ] T026 [P] [US1] Implement add_task() function in src/phase1/task_manager.py (create task with auto-generated ID and timestamps) - verify T016 passes
- [ ] T027 [P] [US1] Implement get_all_tasks() function in src/phase1/task_manager.py (return copy of tasks list) - verify T017 passes
- [ ] T028 [P] [US1] Implement display_header() function with Rich Panel in src/phase1/ui.py (show "📝 My Todo List" header)
- [ ] T029 [P] [US1] Implement display_menu() function with Rich Panel in src/phase1/ui.py (show 9 menu options)
- [ ] T030 [US1] Implement display_tasks_table() function with Rich Table in src/phase1/ui.py (columns: ID, Title, Status, Priority, Tags)
- [ ] T031 [US1] Implement display_success(), display_error(), display_info(), display_warning() message functions in src/phase1/ui.py
- [ ] T032 [US1] Implement get_task_input() function in src/phase1/cli.py (prompt for title, description, priority, tags with Rich Prompt)
- [ ] T033 [US1] Implement validate_title() function in src/phase1/cli.py (check empty, whitespace, 200 char limit)
- [ ] T034 [US1] Implement handle_add_task() command handler in src/phase1/cli.py (validate input, call add_task(), display success)
- [ ] T035 [US1] Implement handle_view_tasks() command handler in src/phase1/cli.py (get tasks, display table or "no tasks" message)
- [ ] T036 [US1] Implement get_menu_choice() function in src/phase1/cli.py (prompt for menu selection 1-9)
- [ ] T037 [US1] Create main() function with application loop in src/phase1/main.py (display header/menu, route to handlers, handle Ctrl+C)

**Checkpoint**: User Story 1 complete - users can add tasks and view them in a table

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can toggle task completion status between Pending (⏳) and Done (✓)

**Independent Test**: Pre-populate 3 tasks, mark task ID 2 as complete, verify status changes to "✓ Done" with color coding

### Implementation for User Story 2

- [ ] T038 [US2] Implement get_task_by_id() function in src/phase1/task_manager.py (return task or None) - verify T018 passes
- [ ] T039 [US2] Implement toggle_complete() function in src/phase1/task_manager.py (find task, flip completed status, update timestamp) - verify T021 passes
- [ ] T040 [US2] Implement get_task_id() function in src/phase1/cli.py (prompt for task ID, validate integer)
- [ ] T041 [US2] Implement validate_task_id() function in src/phase1/cli.py (check ID exists, return error with available IDs if not)
- [ ] T042 [US2] Implement handle_toggle_complete() command handler in src/phase1/cli.py (get ID, validate, toggle, display confirmation)
- [ ] T043 [US2] Update display_tasks_table() in src/phase1/ui.py to show status with color coding (green "✓ Done" or yellow "⏳ Pending")
- [ ] T044 [US2] Wire handle_toggle_complete() to menu option 4 in main.py

**Checkpoint**: User Story 2 complete - users can mark tasks as complete/incomplete

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can modify task titles and descriptions after creation

**Independent Test**: Create task "Call mom", update title to "Call mom about birthday dinner" and add description, verify changes appear

### Implementation for User Story 3

- [ ] T045 [US3] Implement update_task() function in src/phase1/task_manager.py (find task, update fields, refresh updated_at timestamp) - verify T019 passes
- [ ] T046 [US3] Implement get_update_fields() function in src/phase1/cli.py (prompt for new title/description, allow empty to skip)
- [ ] T047 [US3] Implement handle_update_task() command handler in src/phase1/cli.py (get ID, get fields, validate title if provided, update, display result)
- [ ] T048 [US3] Wire handle_update_task() to menu option 3 in main.py

**Checkpoint**: User Story 3 complete - users can update task details

---

## Phase 6: User Story 4 - Delete Unwanted Tasks (Priority: P3)

**Goal**: Users can remove tasks from the list with confirmation message showing task title

**Independent Test**: Create 3 tasks, delete task ID 2, verify it no longer appears and count decreases from 3 to 2

### Implementation for User Story 4

- [ ] T049 [US4] Implement delete_task() function in src/phase1/task_manager.py (find task, remove from list, return True/False) - verify T020 passes
- [ ] T050 [US4] Implement handle_delete_task() command handler in src/phase1/cli.py (get ID, validate, delete, display "Deleted task: <title>")
- [ ] T051 [US4] Add confirmation prompt to handle_delete_task() in src/phase1/cli.py (ask "Delete task '<title>'? (y/n)" before deletion)
- [ ] T052 [US4] Wire handle_delete_task() to menu option 5 in main.py

**Checkpoint**: User Story 4 complete - users can delete tasks safely

---

## Phase 7: User Story 5 - Prioritize and Categorize Tasks (Priority: P4)

**Goal**: Users can assign priority levels (High/Medium/Low) and tags to tasks with color coding

**Independent Test**: Create task with "High" priority and tags "work, urgent", verify color coding (red for High) and tags display

### Implementation for User Story 5

- [ ] T053 [US5] Implement validate_priority() function in src/phase1/cli.py (normalize High/Medium/Low, case-insensitive, default to Medium on invalid)
- [ ] T054 [US5] Implement validate_tags() function in src/phase1/cli.py (parse comma-separated, max 5 tags, max 20 chars each)
- [ ] T055 [US5] Update get_task_input() in src/phase1/cli.py to include priority and tags validation
- [ ] T056 [US5] Update display_tasks_table() in src/phase1/ui.py to show priority with color coding (red=High, yellow=Medium, blue=Low)
- [ ] T057 [US5] Update display_tasks_table() in src/phase1/ui.py to show tags as comma-separated list in Tags column

**Checkpoint**: User Story 5 complete - users can set priorities and tags with visual feedback

---

## Phase 8: User Story 6 - Search and Filter Tasks (Priority: P5)

**Goal**: Users can search by keyword and filter by status, priority, or tags to find specific tasks

**Independent Test**: Create 10 tasks with various attributes, search for keyword "meeting", verify only matching tasks appear

### Implementation for User Story 6

- [ ] T058 [P] [US6] Implement search_tasks() function in src/phase1/task_manager.py (case-insensitive keyword search in title and description) - verify T022 passes
- [ ] T059 [P] [US6] Implement filter_tasks() function in src/phase1/task_manager.py (filter by status, priority, and/or tag) - verify T023 passes
- [ ] T060 [US6] Implement get_search_keyword() function in src/phase1/cli.py (prompt for search keyword)
- [ ] T061 [US6] Implement get_filter_criteria() function in src/phase1/cli.py (prompt for status/priority/tag filters)
- [ ] T062 [US6] Implement handle_search_tasks() command handler in src/phase1/cli.py (get keyword, search, display results or "no matches" warning)
- [ ] T063 [US6] Implement handle_filter_tasks() command handler in src/phase1/cli.py (get criteria, filter, display results)
- [ ] T064 [US6] Wire handle_search_tasks() to menu option 6 and handle_filter_tasks() to menu option 7 in main.py

**Checkpoint**: User Story 6 complete - users can search and filter tasks

---

## Phase 9: User Story 7 - Sort Tasks (Priority: P6)

**Goal**: Users can sort tasks by title, priority, creation date, or status with persistent sort during session

**Independent Test**: Create 5 tasks with different priorities, select "Sort by Priority" (high to low), verify high-priority tasks at top

### Implementation for User Story 7

- [ ] T065 [US7] Implement sort_tasks() function in src/phase1/task_manager.py (sort by id/title/priority/created/status, ascending or descending) - verify T024 passes
- [ ] T066 [US7] Add global current_sort state to task_manager.py (track sort field and direction for session persistence)
- [ ] T067 [US7] Implement get_sort_options() function in src/phase1/cli.py (prompt for sort field and direction)
- [ ] T068 [US7] Implement handle_sort_tasks() command handler in src/phase1/cli.py (get options, update global sort, display sorted results)
- [ ] T069 [US7] Update handle_view_tasks() in src/phase1/cli.py to apply current_sort before displaying tasks
- [ ] T070 [US7] Wire handle_sort_tasks() to menu option 8 in main.py

**Checkpoint**: User Story 7 complete - users can sort tasks with persistent session preferences

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements, error handling, and validation across all user stories

- [ ] T071 [P] Implement get_task_stats() function in src/phase1/task_manager.py (return dict with total, completed, pending counts)
- [ ] T072 [P] Implement display_task_stats() function in src/phase1/ui.py (show task count summary panel)
- [ ] T073 Update handle_view_tasks() in src/phase1/cli.py to display task stats after table
- [ ] T074 Add empty state handling to handle_view_tasks() in src/phase1/cli.py (show "No tasks found. Add your first task to get started!")
- [ ] T075 Add invalid menu choice handling to main.py (re-prompt without crashing on invalid input)
- [ ] T076 Add KeyboardInterrupt exception handling to main.py (graceful exit message on Ctrl+C)
- [ ] T077 Add general exception handling to main.py (catch-all for unexpected errors with error display)
- [ ] T078 Implement clear_screen() utility function in src/phase1/ui.py (optional - clear terminal between operations)
- [ ] T079 Add error handling for non-existent IDs across all command handlers in cli.py (display helpful error with available IDs)
- [ ] T080 Add validation for empty task list operations in cli.py (prevent update/delete/toggle on empty list)
- [ ] T081 Manual testing: Run all acceptance scenarios from spec.md User Stories 1-7
- [ ] T082 Manual testing: Run all edge case tests from spec.md (empty title, long title, invalid ID, special characters, 100+ tasks)
- [ ] T083 Update README.md with complete usage examples and troubleshooting section
- [ ] T084 Verify all success criteria SC-001 to SC-010 from spec.md are met
- [ ] T085 Final code review: Check all functions have type hints and Google-style docstrings

**Checkpoint**: Phase 1 complete and ready for demo

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories and tests
- **Test Setup & Red Phase (Phase 2.5)**: Depends on Foundational - MUST complete before implementation (TDD mandate)
- **User Story 1 (Phase 3)**: Depends on Test Setup (Phase 2.5) - MVP delivery point - GREEN PHASE (make tests pass)
- **User Story 2 (Phase 4)**: Depends on Test Setup - Can run parallel to US1 (if different developers)
- **User Story 3 (Phase 5)**: Depends on Test Setup - Can run parallel to US1/US2
- **User Story 4 (Phase 6)**: Depends on Test Setup - Can run parallel to US1/US2/US3
- **User Story 5 (Phase 7)**: Depends on Test Setup - Can run parallel to other stories
- **User Story 6 (Phase 8)**: Depends on Test Setup - Can run parallel to other stories
- **User Story 7 (Phase 9)**: Depends on Test Setup - Can run parallel to other stories
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

All user stories (US1-US7) are **independently testable** after Foundational phase:

- **US1 (Create/View)**: Foundation only - No other story dependencies
- **US2 (Toggle Complete)**: Foundation only - No other story dependencies (works on tasks created by US1 but doesn't require US1 code)
- **US3 (Update)**: Foundation only - No other story dependencies
- **US4 (Delete)**: Foundation only - No other story dependencies
- **US5 (Priority/Tags)**: Foundation only - Enhances US1 display but doesn't depend on it
- **US6 (Search/Filter)**: Foundation only - Works on any tasks regardless of how they were created
- **US7 (Sort)**: Foundation only - Works on any tasks regardless of how they were created

### Within Each User Story

- Models/functions in task_manager.py marked [P] can run in parallel (different functions)
- UI functions marked [P] can run in parallel (different display functions)
- CLI input functions can run before or parallel to handlers
- Handlers depend on their corresponding task_manager functions
- Menu wiring happens after handler implementation

### Parallel Opportunities

**Phase 1 - Setup**: T003, T004, T005 can run in parallel (different files)

**Phase 2 - Foundational**: All tasks sequential (T006→T007→T008→T009→T010) due to dependencies

**Phase 2.5 - Test Setup & Red Phase**:
- T011-T014 sequential (pytest setup)
- T015-T024 can ALL run in parallel (different test files, all marked [P])
- T025 sequential after all tests written (verify they fail)

**Phase 3 - User Story 1**:
- T026, T027 parallel (different functions in task_manager.py)
- T028, T029, T031 parallel (different functions in ui.py)
- T030 depends on T028/T029 (needs header/menu first)

**Phase 4 - User Story 2**: T038, T040 can run parallel

**Phase 5 - User Story 3**: All sequential (T045→T046→T047→T048)

**Phase 6 - User Story 4**: T049, T050 can run parallel

**Phase 7 - User Story 5**: T053, T054 parallel (different validation functions)

**Phase 8 - User Story 6**: T058, T059 parallel (different task_manager functions)

**Phase 10 - Polish**: T071, T072 parallel (different modules)

**Across User Stories** (after Test Setup complete):
- US1 (Phase 3) can run parallel to US2 (Phase 4) with different developers
- US3, US4, US5, US6, US7 can all run in parallel after Test Setup phase

---

## Parallel Example: Test Phase (Phase 2.5)

```bash
# After Foundational phase (T006-T010) is complete, run pytest setup sequentially:
T011: Create tests/phase1/ directory structure
T012: Add pytest>=8.0.0 to pyproject.toml
T013: Create pytest.ini configuration
T014: Create conftest.py with fixtures

# Then write ALL test files in parallel (RED PHASE):
# Developer A - Models & Core Functions:
T015: Write test_models.py
T016: Write test for add_task()
T017: Write test for get_all_tasks()

# Developer B - CRUD Operations:
T018: Write test for get_task_by_id()
T019: Write test for update_task()
T020: Write test for delete_task()
T021: Write test for toggle_complete()

# Developer C - Query Operations:
T022: Write test for search_tasks()
T023: Write test for filter_tasks()
T024: Write test for sort_tasks()

# Finally, verify all tests FAIL:
T025: Run pytest -v (expect all failures)
```

## Parallel Example: Implementation (Phase 3)

```bash
# After Test Setup phase is complete, these tasks can run in parallel:

# Developer A works on task_manager functions (GREEN PHASE):
T026: Implement add_task() in task_manager.py - make T016 pass
T027: Implement get_all_tasks() in task_manager.py - make T017 pass

# Developer B works on UI functions:
T028: Implement display_header() in ui.py
T029: Implement display_menu() in ui.py
T031: Implement message functions in ui.py

# Developer C works on CLI validation:
T032: Implement get_task_input() in cli.py
T033: Implement validate_title() in cli.py
```

---

## Implementation Strategy

### TDD MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T010) ⚠️ BLOCKS everything
3. Complete Phase 2.5: **RED PHASE** (T011-T025) - Write failing tests ⚠️ **TDD MANDATE**
4. Complete Phase 3: **GREEN PHASE** (T026-T037) - US1: Make tests pass ✅
5. **STOP and VALIDATE**: Run pytest to verify all tests pass, test US1 acceptance scenarios
6. Deploy/demo if ready ✅ **MVP DELIVERED**

**Why stop here?** User Story 1 provides immediate value - users can create and view tasks, which is the core todo list functionality.

### Incremental Delivery (Recommended TDD Workflow)

1. **Foundation** (T001-T010) → Project structure ready
2. **RED PHASE** (T011-T025) → All tests written and failing ✅
3. **GREEN: MVP** (T026-T037) → US1: Create & View → Tests pass → Demo ✅
4. **GREEN: Enhancement 1** (T038-T044) → US2: Toggle Complete → Tests pass → Demo ✅
5. **GREEN: Enhancement 2** (T045-T048) → US3: Update → Tests pass → Demo ✅
6. **GREEN: Enhancement 3** (T049-T052) → US4: Delete → Tests pass → Demo ✅
7. **GREEN: Enhancement 4** (T053-T057) → US5: Priority/Tags → Tests pass → Demo ✅
8. **GREEN: Enhancement 5** (T058-T064) → US6: Search/Filter → Tests pass → Demo ✅
9. **GREEN: Enhancement 6** (T065-T070) → US7: Sort → Tests pass → Demo ✅
10. **REFACTOR: Polish** (T071-T085) → Final refinements → Full demo ✅

Each increment follows Red-Green-Refactor cycle and is independently testable.

### Parallel Team Strategy

With 3 developers after Foundational phase:

1. **All**: Complete Setup (T001-T005) and Foundational (T006-T010) together
2. **RED PHASE**: Complete Test Setup (T011-T025) together - all tests written and failing
3. Once RED phase is done (**constitution compliance checkpoint**):
   - **Developer A**: User Story 1 (T026-T037) - MVP (make tests pass)
   - **Developer B**: User Story 2 (T038-T044) + User Story 3 (T045-T048)
   - **Developer C**: User Story 4 (T049-T052) + User Story 5 (T053-T057)
4. **Integration**: Wire all handlers to main.py menu
5. **All**: User Story 6 (T058-T064) and User Story 7 (T065-T070) as needed
6. **All**: Polish & Testing (T071-T085)

---

## Task Format Validation

All tasks follow the required format:

✅ **Checkbox**: Every task starts with `- [ ]`
✅ **Task ID**: Sequential T001, T002, T003... T085 (85 total tasks)
✅ **[P] marker**: Included only for parallelizable tasks (different files, no dependencies)
✅ **[Story] label**: Included for user story implementation tasks (US1-US7)
✅ **Description**: Clear action with exact file path

**Examples from this file**:
- ✅ `- [ ] T001 Create project directory structure (src/phase1/, tests/phase1/)`
- ✅ `- [ ] T003 [P] Create .gitignore for Python project`
- ✅ `- [ ] T015 [P] Write tests/phase1/unit/test_models.py` (Red Phase - TDD)
- ✅ `- [ ] T026 [P] [US1] Implement add_task() function in src/phase1/task_manager.py` (Green Phase - TDD)
- ✅ `- [ ] T042 [US2] Implement handle_toggle_complete() command handler in src/phase1/cli.py`

---

## Notes

- **[P] tasks** = Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story] labels** = Map tasks to user stories from spec.md for traceability
- **✅ TDD Compliance** = Phase 2.5 (T011-T025) adds pytest tests per Constitution Principle III
- **Red-Green-Refactor Cycle**: T011-T025 (Red - tests fail) → T026-T070 (Green - tests pass) → T071-T085 (Refactor - polish)
- Each user story is **independently testable** after Test Setup phase
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently and run pytest
- **MVP = User Story 1** (Create and View Tasks) with passing pytest tests - 37 tasks total (T001-T037)
