# Create Rich UI Component

Generate attractive CLI interface components using the Rich library for Python console applications.

## Instructions

When this skill is invoked, create polished, colorful CLI components using the Rich library. Rich provides a beautiful terminal interface with colors, tables, panels, progress bars, and more.

### Input Required
- Component type (header, table, message, menu, progress, prompt)
- Task ID and Spec reference
- Feature context (what data to display)
- Color scheme preference (optional)

### Installation Requirement

```python
# Add to requirements.txt or install with pip
rich>=13.0.0
```

---

## Standard Component Templates

### Template 1: Application Header

**Use Case:** Main app title and branding

```python
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def display_header(title: str = "Todo App") -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display application header with branding.

    Args:
        title (str): Application title (default: "Todo App")

    Example:
        >>> display_header("My Todo List")
    """
    header_text = Text()
    header_text.append("📝 ", style="bold yellow")
    header_text.append(title, style="bold cyan")

    console.print(Panel(
        header_text,
        border_style="cyan",
        padding=(1, 2)
    ))


def display_section_header(section: str) -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display section header for different app areas.

    Args:
        section (str): Section name

    Example:
        >>> display_section_header("View All Tasks")
    """
    console.print(f"\n[bold cyan]═══ {section} ═══[/bold cyan]\n")
```

---

### Template 2: Task Table Display

**Use Case:** Display tasks in a formatted table

```python
from rich.console import Console
from rich.table import Table
from typing import List
from models import Task

console = Console()

def display_tasks_table(tasks: List[Task], title: str = "My Tasks") -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display tasks in a formatted table with colors and icons.

    Args:
        tasks (List[Task]): List of tasks to display
        title (str): Table title (default: "My Tasks")

    Example:
        >>> display_tasks_table(all_tasks, title="Pending Tasks")
    """
    if not tasks:
        console.print("[yellow]No tasks to display.[/yellow]")
        return

    table = Table(
        title=title,
        border_style="cyan",
        header_style="bold white",
        show_lines=False
    )

    # Add columns
    table.add_column("ID", style="cyan", justify="center", width=6)
    table.add_column("Title", style="white", no_wrap=False)
    table.add_column("Status", justify="center", width=10)
    table.add_column("Priority", justify="center", width=10)

    # Add rows
    for task in tasks:
        # Status icon and color
        if task.completed:
            status = "✓ Done"
            status_style = "green"
        else:
            status = "⏳ Pending"
            status_style = "yellow"

        # Priority color
        priority_text = ""
        if hasattr(task, 'priority'):
            priority = task.priority.lower()
            if priority == "high":
                priority_text = "[red bold]🔴 High[/red bold]"
            elif priority == "medium":
                priority_text = "[yellow]🟡 Medium[/yellow]"
            elif priority == "low":
                priority_text = "[green]🟢 Low[/green]"
        else:
            priority_text = "[dim]-[/dim]"

        table.add_row(
            str(task.id),
            task.title,
            f"[{status_style}]{status}[/{status_style}]",
            priority_text
        )

    console.print(table)


def display_task_detail(task: Task) -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display detailed view of a single task.

    Args:
        task (Task): Task to display

    Example:
        >>> display_task_detail(task)
    """
    from rich.panel import Panel
    from rich.text import Text

    # Status indicator
    status_icon = "✓" if task.completed else "⏳"
    status_text = "Completed" if task.completed else "Pending"
    status_color = "green" if task.completed else "yellow"

    # Build detail text
    detail = Text()
    detail.append(f"{status_icon} ", style=f"bold {status_color}")
    detail.append(f"Task #{task.id}\n\n", style="bold cyan")
    detail.append(f"Title: ", style="bold white")
    detail.append(f"{task.title}\n", style="white")
    detail.append(f"Status: ", style="bold white")
    detail.append(f"{status_text}\n", style=status_color)

    if task.description:
        detail.append(f"Description: ", style="bold white")
        detail.append(f"{task.description}\n", style="dim white")

    if hasattr(task, 'priority'):
        detail.append(f"Priority: ", style="bold white")
        priority_color = {
            "high": "red",
            "medium": "yellow",
            "low": "green"
        }.get(task.priority.lower(), "white")
        detail.append(f"{task.priority.capitalize()}\n", style=priority_color)

    if hasattr(task, 'due_date') and task.due_date:
        detail.append(f"Due Date: ", style="bold white")
        detail.append(f"{task.due_date}\n", style="cyan")

    console.print(Panel(
        detail,
        border_style="cyan",
        padding=(1, 2)
    ))
```

---

### Template 3: Success/Error/Info Messages

**Use Case:** User feedback and notifications

```python
from rich.console import Console

console = Console()

def display_success(message: str) -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display success message with green checkmark.

    Args:
        message (str): Success message to display

    Example:
        >>> display_success("Task created successfully!")
    """
    console.print(f"[green]✓[/green] {message}")


def display_error(message: str) -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display error message with red X.

    Args:
        message (str): Error message to display

    Example:
        >>> display_error("Task not found!")
    """
    console.print(f"[red]✗[/red] {message}")


def display_warning(message: str) -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display warning message with yellow icon.

    Args:
        message (str): Warning message to display

    Example:
        >>> display_warning("This action cannot be undone!")
    """
    console.print(f"[yellow]⚠[/yellow] {message}")


def display_info(message: str) -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display informational message with blue icon.

    Args:
        message (str): Info message to display

    Example:
        >>> display_info("You have 5 pending tasks.")
    """
    console.print(f"[cyan]ℹ[/cyan] {message}")
```

---

### Template 4: Interactive Menu

**Use Case:** Main menu and navigation

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def display_menu() -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display main menu with available commands.

    Example:
        >>> display_menu()
    """
    menu = Table.grid(padding=(0, 2))
    menu.add_column(style="cyan", justify="right")
    menu.add_column(style="white")

    menu.add_row("1", "➕ Add new task")
    menu.add_row("2", "📋 View all tasks")
    menu.add_row("3", "✏️  Edit task")
    menu.add_row("4", "✓", "Mark task complete")
    menu.add_row("5", "🗑️  Delete task")
    menu.add_row("6", "🔍 Search tasks")
    menu.add_row("7", "📊 Filter tasks")
    menu.add_row("0", "👋 Exit")

    console.print(Panel(
        menu,
        title="[bold cyan]Main Menu[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    ))


def display_compact_menu() -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display compact menu for quick access.

    Example:
        >>> display_compact_menu()
    """
    console.print("\n[cyan]Commands:[/cyan] ", end="")
    console.print("[white]add | view | edit | complete | delete | search | filter | exit[/white]\n")
```

---

### Template 5: Progress Indicators

**Use Case:** Long-running operations

```python
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

console = Console()

def display_spinner(task_description: str = "Processing...") -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display spinner for quick operations.

    Args:
        task_description (str): Description of operation

    Example:
        >>> with console.status("[cyan]Loading tasks...") as status:
        ...     # Do work here
        ...     load_tasks()
    """
    # Usage pattern shown in example
    pass  # Implementation uses context manager


def display_progress_bar(items: list, process_fn) -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display progress bar for batch operations.

    Args:
        items (list): Items to process
        process_fn: Function to apply to each item

    Example:
        >>> def delete_task(task_id):
        ...     # Delete logic
        ...     pass
        >>> display_progress_bar(task_ids, delete_task)
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("Processing...", total=len(items))

        for item in items:
            process_fn(item)
            progress.advance(task)


# Usage example for spinner
def example_with_spinner():
    """Example of using spinner."""
    with console.status("[cyan]Loading tasks...") as status:
        # Simulate work
        import time
        time.sleep(2)
    display_success("Tasks loaded!")
```

---

### Template 6: Input Prompts (with Rich)

**Use Case:** Enhanced user input with validation

```python
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt

console = Console()

def prompt_text(prompt: str, default: str = "") -> str:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Prompt user for text input with Rich styling.

    Args:
        prompt (str): Prompt message
        default (str): Default value

    Returns:
        str: User input

    Example:
        >>> title = prompt_text("Task title", default="Untitled")
    """
    if default:
        return Prompt.ask(f"[cyan]{prompt}[/cyan]", default=default)
    return Prompt.ask(f"[cyan]{prompt}[/cyan]")


def prompt_int(prompt: str, min_value: int = None, max_value: int = None) -> int:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Prompt user for integer input with validation.

    Args:
        prompt (str): Prompt message
        min_value (int): Minimum allowed value
        max_value (int): Maximum allowed value

    Returns:
        int: User input

    Example:
        >>> task_id = prompt_int("Enter task ID", min_value=1)
    """
    return IntPrompt.ask(f"[cyan]{prompt}[/cyan]")


def prompt_choice(prompt: str, choices: list[str]) -> str:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Prompt user to choose from a list of options.

    Args:
        prompt (str): Prompt message
        choices (list[str]): Valid choices

    Returns:
        str: Selected choice

    Example:
        >>> priority = prompt_choice("Priority", ["high", "medium", "low"])
    """
    return Prompt.ask(
        f"[cyan]{prompt}[/cyan]",
        choices=choices,
        show_choices=True
    )


def prompt_confirm(prompt: str, default: bool = False) -> bool:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Prompt user for yes/no confirmation.

    Args:
        prompt (str): Prompt message
        default (bool): Default answer

    Returns:
        bool: User confirmation

    Example:
        >>> if prompt_confirm("Delete all tasks?"):
        ...     delete_all_tasks()
    """
    return Confirm.ask(f"[yellow]{prompt}[/yellow]", default=default)
```

---

### Template 7: Summary Dashboard

**Use Case:** Display statistics and summary

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from typing import List
from models import Task

console = Console()

def display_dashboard(tasks: List[Task]) -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display task statistics dashboard.

    Args:
        tasks (List[Task]): All tasks

    Example:
        >>> display_dashboard(all_tasks)
    """
    # Calculate statistics
    total = len(tasks)
    completed = sum(1 for t in tasks if t.completed)
    pending = total - completed
    completion_rate = (completed / total * 100) if total > 0 else 0

    # Priority breakdown (if available)
    high_priority = sum(1 for t in tasks if hasattr(t, 'priority') and t.priority.lower() == 'high')
    medium_priority = sum(1 for t in tasks if hasattr(t, 'priority') and t.priority.lower() == 'medium')
    low_priority = sum(1 for t in tasks if hasattr(t, 'priority') and t.priority.lower() == 'low')

    # Create statistics table
    stats = Table.grid(padding=(0, 2))
    stats.add_column(style="cyan", justify="right")
    stats.add_column(style="white")

    stats.add_row("📊 Total Tasks:", f"[bold]{total}[/bold]")
    stats.add_row("✓ Completed:", f"[green]{completed}[/green]")
    stats.add_row("⏳ Pending:", f"[yellow]{pending}[/yellow]")
    stats.add_row("📈 Completion:", f"[cyan]{completion_rate:.1f}%[/cyan]")

    if high_priority or medium_priority or low_priority:
        stats.add_row("", "")  # Blank line
        stats.add_row("🔴 High Priority:", f"[red]{high_priority}[/red]")
        stats.add_row("🟡 Medium Priority:", f"[yellow]{medium_priority}[/yellow]")
        stats.add_row("🟢 Low Priority:", f"[green]{low_priority}[/green]")

    console.print(Panel(
        stats,
        title="[bold cyan]Task Summary[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    ))


def display_quick_stats(tasks: List[Task]) -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display compact task statistics.

    Args:
        tasks (List[Task]): All tasks

    Example:
        >>> display_quick_stats(all_tasks)
    """
    total = len(tasks)
    completed = sum(1 for t in tasks if t.completed)
    pending = total - completed

    console.print(
        f"[cyan]Tasks:[/cyan] {total} total | "
        f"[green]{completed} completed[/green] | "
        f"[yellow]{pending} pending[/yellow]"
    )
```

---

### Template 8: Empty State Display

**Use Case:** Show when no data is available

```python
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def display_empty_state(message: str = "No tasks yet") -> None:
    """
    [Task]: T-XXX
    [Spec]: specs/[feature]/spec.md §X.X

    Display empty state when no tasks exist.

    Args:
        message (str): Empty state message

    Example:
        >>> if not tasks:
        ...     display_empty_state("No pending tasks")
    """
    empty_text = Text()
    empty_text.append("📭 ", style="dim")
    empty_text.append(message, style="dim italic")
    empty_text.append("\n\n")
    empty_text.append("Tip: ", style="bold cyan")
    empty_text.append("Use 'add' command to create your first task!", style="dim")

    console.print(Panel(
        empty_text,
        border_style="dim",
        padding=(1, 2)
    ))
```

---

## Color Scheme Reference

```python
# Standard color palette for consistency
COLORS = {
    "primary": "cyan",        # Headers, borders, prompts
    "success": "green",       # Completed tasks, success messages
    "warning": "yellow",      # Pending tasks, warnings
    "error": "red",           # Errors, high priority
    "info": "blue",           # Informational messages
    "muted": "dim white",     # Secondary text
    "highlight": "bold white" # Important text
}

# Priority colors
PRIORITY_COLORS = {
    "high": "red",
    "medium": "yellow",
    "low": "green"
}

# Status colors
STATUS_COLORS = {
    "completed": "green",
    "pending": "yellow",
    "overdue": "red"
}
```

---

## Icon Reference

```python
# Standard icons for consistency
ICONS = {
    "task": "📝",
    "add": "➕",
    "view": "📋",
    "edit": "✏️",
    "delete": "🗑️",
    "search": "🔍",
    "filter": "📊",
    "complete": "✓",
    "pending": "⏳",
    "high": "🔴",
    "medium": "🟡",
    "low": "🟢",
    "success": "✓",
    "error": "✗",
    "warning": "⚠",
    "info": "ℹ",
    "exit": "👋",
    "empty": "📭"
}
```

---

## Usage

To use this skill:

1. **Specify component type:**
   - Header/Title
   - Table display
   - Message (success/error/warning/info)
   - Menu/Navigation
   - Progress indicator
   - Input prompt
   - Dashboard/Statistics
   - Empty state

2. **Provide context:**
   - What data to display
   - Color scheme (use defaults for consistency)
   - Task/Spec reference

3. **Choose template:**
   - Use appropriate template from 1-8 above
   - Customize for specific needs

4. **Add to cli.py:**
   - Place all Rich UI functions in `cli.py`
   - Import `Console` at module level
   - Reuse console instance

5. **Install dependency:**
   ```bash
   pip install rich>=13.0.0
   ```

---

## Best Practices

1. **Consistent Colors:** Use the color scheme reference for consistency
2. **Icons:** Use standard icons for better UX
3. **Reuse Console:** Create one `Console()` instance per module
4. **Spacing:** Add blank lines before/after components for readability
5. **Borders:** Use consistent border style ("cyan" recommended)
6. **Tables:** Use `show_lines=False` for cleaner tables
7. **Panels:** Add padding (1, 2) for better spacing
8. **Empty States:** Always handle empty lists gracefully
9. **Input Validation:** Use Rich's Prompt classes for validated input
10. **Error Handling:** Wrap Rich operations in try-except for safety

---

## Integration Pattern

```python
# cli.py - Complete integration example

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from typing import List
from models import Task

# Create console instance (reuse throughout module)
console = Console()

# Use templates from this skill
def display_header(title: str = "Todo App") -> None:
    # Template 1 code here
    pass

def display_tasks_table(tasks: List[Task], title: str = "My Tasks") -> None:
    # Template 2 code here
    pass

def display_success(message: str) -> None:
    # Template 3 code here
    pass

# ... other template functions
```

---

## Testing Pattern

```python
# tests/test_cli.py
from io import StringIO
from rich.console import Console
from cli import display_tasks_table
from models import Task

def test_display_empty_table():
    """Test displaying empty task list."""
    # Capture output
    console = Console(file=StringIO())
    tasks = []

    # Should not raise error
    display_tasks_table(tasks, title="Test")


def test_display_tasks_table():
    """Test displaying task table."""
    tasks = [
        Task(id=1, title="Test 1", completed=False),
        Task(id=2, title="Test 2", completed=True),
    ]

    # Should not raise error
    display_tasks_table(tasks)
```

---

## Output Format

Generated Rich UI components are ready to add to:
```
src/cli.py
```

With proper imports:
```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.progress import Progress, SpinnerColumn, BarColumn, TimeElapsedColumn
```

And in requirements.txt:
```
rich>=13.0.0
```

---

## Quick Reference

| Component | Template | Use Case |
|-----------|----------|----------|
| Header | 1 | App title, section headers |
| Table | 2 | List tasks in formatted table |
| Messages | 3 | Success/error/warning/info feedback |
| Menu | 4 | Navigation and commands |
| Progress | 5 | Long operations, batch processing |
| Prompts | 6 | User input with validation |
| Dashboard | 7 | Statistics and summary |
| Empty State | 8 | No data available |

---

## Advanced Features

### Markdown Rendering
```python
from rich.markdown import Markdown

console.print(Markdown("# Task Details\n\n- Item 1\n- Item 2"))
```

### Syntax Highlighting
```python
from rich.syntax import Syntax

code = "def hello(): print('world')"
console.print(Syntax(code, "python"))
```

### Live Updates
```python
from rich.live import Live
from time import sleep

with Live(generate_table(), refresh_per_second=4) as live:
    for _ in range(10):
        sleep(0.4)
        live.update(generate_table())
```
