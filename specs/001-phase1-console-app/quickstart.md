# Quickstart Guide: Phase 1 - Todo Console App

**Date**: 2026-01-02
**Feature**: 001-phase1-console-app

## Prerequisites

- **Python**: 3.13 or higher
- **UV**: Package manager (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Terminal**: Unicode support for emojis (most modern terminals)
- **OS**: Linux, macOS, or Windows with WSL 2

## Installation

```bash
# 1. Clone repository
git clone <repo-url>
cd todo-app

# 2. Checkout Phase 1 branch
git checkout 001-phase1-console-app

# 3. Create virtual environment
uv venv

# 4. Activate virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows (WSL):
source .venv/bin/activate

# 5. Install dependencies
uv pip install "rich>=13.7.0"

# 6. Run application
python -m src.phase1.main
```

## Basic Usage

### Launch App
```bash
python -m src.phase1.main
```

You'll see the main menu:
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

Choose an option (1-9):
```

### Core Operations

#### 1. Add Task
```
Choose an option (1-9): 1

➕ Adding New Task

Enter task title: Buy groceries
Enter description (optional): Milk, eggs, bread
Enter priority (High/Medium/Low) [Medium]: High
Enter tags (comma-separated, max 5) []: home, shopping

✓ Task added successfully!
  ID: 1
  Title: Buy groceries
  Priority: High
  Tags: home, shopping
```

#### 2. View All Tasks
```
Choose an option (1-9): 2

┏━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ ID┃ Title            ┃ Status ┃Priority┃ Tags     ┃
┡━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ 1 │ Buy groceries    │ ⏳ Todo│  High  │home,shop │
│ 2 │ Call mom         │ ✓ Done │ Medium │personal  │
└───┴──────────────────┴────────┴────────┴──────────┘

Total: 2 tasks (1 completed, 1 pending)
```

#### 3. Mark Task Complete
```
Choose an option (1-9): 4

✅ Mark Task Complete

Enter task ID: 1

✓ Task 1 marked as complete
```

#### 4. Search Tasks
```
Choose an option (1-9): 6

🔍 Search Tasks

Enter search keyword: groceries

┏━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ ID┃ Title            ┃ Status ┃Priority┃ Tags     ┃
┡━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ 1 │ Buy groceries    │ ✓ Done │  High  │home,shop │
└───┴──────────────────┴────────┴────────┴──────────┘

ℹ Showing 1 matching task
```

#### 5. Exit
```
Choose an option (1-9): 9

👋 Goodbye! Your tasks will be lost (in-memory only).
```

## Keyboard Shortcuts

- **Ctrl+C**: Exit application immediately
- **Enter**: Accept default value in prompts
- **1-9**: Select menu option

## Tips & Tricks

1. **Quick Task Entry**: Leave description empty by pressing Enter
2. **Default Priority**: Press Enter to use Medium priority
3. **Multiple Tags**: Separate with commas: `work, urgent, deadline`
4. **Case-Insensitive Search**: "MEETING" finds "meeting" and "Meeting"
5. **Empty List**: View tasks shows "No tasks found" message with helpful prompt

## Common Errors & Solutions

### Error: "Task title cannot be empty"
**Solution**: Enter at least one non-whitespace character

### Error: "Task not found with ID: 5"
**Solution**: Check available task IDs in the error message, use one of those

### Error: "Invalid priority"
**Solution**: Enter exactly "High", "Medium", or "Low" (case-insensitive)

### Error: "ModuleNotFoundError: No module named 'rich'"
**Solution**: Install Rich library: `uv pip install rich`

### Issue: Terminal doesn't show colors
**Solution**: Use a modern terminal (iTerm2, Windows Terminal, GNOME Terminal)

### Issue: Emojis don't display correctly
**Solution**: Ensure terminal has Unicode support and a font with emoji glyphs

## Data Persistence

⚠️ **Important**: Phase 1 uses in-memory storage. All tasks are lost when the application exits.

To save your work:
1. Take a screenshot before exiting
2. Copy task details to a text file
3. Wait for Phase 2 (database persistence)

## Performance

- **Startup**: <1 second
- **Add Task**: <1 second
- **View Tasks**: <1 second (up to 100 tasks)
- **Search**: <1 second (up to 100 tasks)

## Troubleshooting

### Application won't start
```bash
# Check Python version
python --version  # Should be 3.13+

# Check virtual environment
which python  # Should point to .venv/bin/python

# Reinstall dependencies
uv pip install --force-reinstall rich
```

### Unicode errors
```bash
# Set UTF-8 encoding
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

## Next Steps

- Try adding 10+ tasks to test the interface
- Practice search and filter operations
- Test error handling (empty title, invalid ID)
- Provide feedback for Phase 2 enhancements

## Support

- **GitHub Issues**: <repo-url>/issues
- **Documentation**: See `specs/001-phase1-console-app/`
- **Demo Video**: See `docs/phase1-demo.mp4` (after completion)
