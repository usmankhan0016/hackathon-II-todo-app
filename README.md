# Task: T004
# Spec: specs/001-phase1-console-app/spec.md#project-overview
# Purpose: Project documentation and setup instructions

# Evolution of Todo - Phase 1: Console App

In-memory Python console application for task management with a modern, attractive CLI interface using the Rich library.

## Features

- ✅ Create and view tasks
- ✅ Mark tasks complete/incomplete
- ✅ Update task details
- ✅ Delete tasks
- ✅ Assign priorities (High/Medium/Low) and tags
- ✅ Search and filter tasks
- ✅ Sort tasks by multiple criteria
- 📝 Rich terminal UI with color coding
- ⏳ Session-scoped in-memory storage

## Requirements

- Python 3.13+
- UV package manager
- Terminal with Unicode support (80+ character width)

## Installation

```bash
# Clone repository
git clone <repo-url>
cd todo-app

# Checkout Phase 1 branch
git checkout 001-phase1-console-app

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

## Usage

```bash
# Run the application
python -m src.phase1.main

# Run tests
pytest

# Run type checking
mypy src/phase1

# Format code
black src/phase1 tests/phase1
```

## Project Structure

```
src/phase1/
├── __init__.py          # Package marker
├── models.py            # Task dataclass definitions
├── task_manager.py      # In-memory CRUD operations
├── ui.py                # Rich library UI components
├── cli.py               # User input and command routing
└── main.py              # Application entry point

tests/phase1/
├── unit/                # Unit tests for all modules
└── integration/         # End-to-end integration tests
```

## Development

This project follows Test-Driven Development (TDD) with pytest. All code is generated from specifications following the Spec-Driven Development workflow.

See `specs/001-phase1-console-app/` for complete specifications, plans, and task breakdowns.

## License

MIT
