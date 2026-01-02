# Task: T009
# Spec: specs/001-phase1-console-app/spec.md#ui-layer
# Purpose: Rich library UI components for terminal display

"""UI module for Phase 1 Todo Console App.

This module handles all visual output using the Rich library.
Provides styled panels, tables, and colored messages.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from src.phase1.models import Task

# Global Rich console instance
console = Console()


def display_header() -> None:
    """Display application header with styled panel.

    Example:
        ┌─────────────────────────────────────────┐
        │         📝 My Todo List                 │
        └─────────────────────────────────────────┘
    """
    header = Panel(
        "[cyan bold]📝 My Todo List[/cyan bold]",
        border_style="cyan",
        padding=(0, 2),
    )
    console.print(header)


def display_menu() -> None:
    """Display main menu with numbered options.

    Example:
        ╔════════════════════════════════════════╗
        ║          📋 MAIN MENU                  ║
        ╠════════════════════════════════════════╣
        ║  1. ➕ Add Task                        ║
        ║  2. 👁️  View All Tasks                 ║
        ...
    """
    menu_text = """[cyan bold]📋 MAIN MENU[/cyan bold]

[white]1.[/white] ➕  Add Task
[white]2.[/white] 👁️  View All Tasks
[white]3.[/white] ✏️  Update Task
[white]4.[/white] ✅ Mark Task Complete/Incomplete
[white]5.[/white] 🗑️  Delete Task
[white]6.[/white] 🔍 Search Tasks
[white]7.[/white] 🏷️  Filter Tasks
[white]8.[/white] 🔄 Sort Tasks
[white]9.[/white] 🚪 Exit"""

    menu_panel = Panel(
        menu_text,
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(menu_panel)


def display_tasks_table(tasks_list: list[Task]) -> None:
    """Display tasks in a formatted table.

    Args:
        tasks_list: List of tasks to display

    Example:
        ┌────┬──────────────┬────────────────────┬──────────┬──────────┬────────┐
        │ ID │ Title        │ Description        │ Status   │ Priority │ Tags   │
        ├────┼──────────────┼────────────────────┼──────────┼──────────┼────────┤
        │ 1  │ Buy groceries│ Milk, eggs, bread  │ ✓ Done   │ High     │ home   │
        └────┴──────────────┴────────────────────┴──────────┴──────────┴────────┘
    """
    table = Table(title="Tasks", border_style="cyan", show_header=True)
    table.add_column("ID", justify="center", style="cyan", width=5)
    table.add_column("Title", style="white", width=25)
    table.add_column("Description", style="dim", width=35)
    table.add_column("Status", justify="center", width=12)
    table.add_column("Priority", justify="center", width=10)
    table.add_column("Tags", style="dim", width=15)

    for task in tasks_list:
        # Status with color coding
        if task.completed:
            status = "[green]✓ Done[/green]"
        else:
            status = "[yellow]⏳ Pending[/yellow]"

        # Priority with color coding
        if task.priority == "High":
            priority_display = "[red]High[/red]"
        elif task.priority == "Medium":
            priority_display = "[yellow]Medium[/yellow]"
        else:  # Low
            priority_display = "[blue]Low[/blue]"

        # Description - truncate if too long
        if task.description:
            desc_display = task.description[:32] + "..." if len(task.description) > 32 else task.description
        else:
            desc_display = "-"

        # Tags as comma-separated list
        tags_display = ", ".join(task.tags) if task.tags else "-"

        table.add_row(
            str(task.id),
            task.title,
            desc_display,
            status,
            priority_display,
            tags_display,
        )

    console.print(table)


def display_task_stats(stats: dict[str, int]) -> None:
    """Display task count summary panel.

    Args:
        stats: Dictionary with 'total', 'completed', 'pending' counts

    Example:
        ┌──────────────────────────────────────┐
        │ Total: 10  Completed: 3  Pending: 7  │
        └──────────────────────────────────────┘
    """
    stats_text = (
        f"[cyan]Total:[/cyan] {stats['total']}  "
        f"[green]Completed:[/green] {stats['completed']}  "
        f"[yellow]Pending:[/yellow] {stats['pending']}"
    )
    stats_panel = Panel(stats_text, border_style="dim", padding=(0, 2))
    console.print(stats_panel)


def display_success(message: str) -> None:
    """Display success message with green checkmark.

    Args:
        message: Success message to display

    Example:
        ✓ Task added successfully!
    """
    console.print(f"[green]✓[/green] {message}")


def display_error(message: str) -> None:
    """Display error message with red cross.

    Args:
        message: Error message to display

    Example:
        ✗ Task not found with ID: 5
    """
    console.print(f"[red]✗[/red] {message}")


def display_info(message: str) -> None:
    """Display info message with blue icon.

    Args:
        message: Info message to display

    Example:
        ℹ No tasks found. Add your first task to get started!
    """
    console.print(f"[blue]ℹ[/blue] {message}")


def display_warning(message: str) -> None:
    """Display warning message with yellow icon.

    Args:
        message: Warning message to display

    Example:
        ⚠ No tasks match your search
    """
    console.print(f"[yellow]⚠[/yellow] {message}")


def clear_screen() -> None:
    """Clear the terminal screen (optional utility).

    Uses Rich console clear method for cross-platform compatibility.
    """
    console.clear()
