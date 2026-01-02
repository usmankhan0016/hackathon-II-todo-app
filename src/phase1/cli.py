# Task: T010
# Spec: specs/001-phase1-console-app/spec.md#cli-layer
# Purpose: User input handling and command routing

"""CLI module for Phase 1 Todo Console App.

This module handles all user input, validation, and command routing.
Coordinates between task_manager (business logic) and ui (display).
"""

from rich.prompt import Prompt, Confirm
from src.phase1 import task_manager, ui
from src.phase1.models import Task, Priority


def get_menu_choice() -> str:
    """Prompt for menu selection (1-9).

    Returns:
        str: User's menu choice

    Example:
        >>> choice = get_menu_choice()
        Choose an option (1-9): 1
    """
    return Prompt.ask("\n[cyan]Choose an option (1-9)[/cyan]", default="2")


def get_task_input() -> dict[str, str | list[str]]:
    """Prompt for new task details with validation.

    Returns:
        dict: Task details (title, description, priority, tags)

    Example:
        >>> task_data = get_task_input()
        >>> task_data['title']
        'Buy groceries'
    """
    ui.console.print("\n[cyan bold]➕ Adding New Task[/cyan bold]\n")

    title = Prompt.ask("[white]Enter task title[/white]")
    description = Prompt.ask("[white]Enter description (optional)[/white]", default="")
    priority = Prompt.ask(
        "[white]Enter priority (High/Medium/Low)[/white]",
        choices=["High", "Medium", "Low", "high", "medium", "low"],
        default="Medium",
    )
    tags_input = Prompt.ask("[white]Enter tags (comma-separated, max 5)[/white]", default="")

    # Parse tags
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()][:5]

    # Normalize priority
    priority_normalized = priority.capitalize()

    return {
        "title": title,
        "description": description,
        "priority": priority_normalized,
        "tags": tags,
    }


def get_task_id() -> int | None:
    """Prompt for task ID with integer validation.

    Returns:
        int | None: Task ID if valid, None if invalid

    Example:
        >>> task_id = get_task_id()
        Enter task ID: 1
    """
    id_input = Prompt.ask("[white]Enter task ID[/white]")
    try:
        return int(id_input)
    except ValueError:
        ui.display_error("Invalid input. Please enter a valid task ID number.")
        return None


def get_update_fields() -> dict[str, str]:
    """Prompt for fields to update (title and/or description).

    Returns:
        dict: Fields to update (empty string means no change)

    Example:
        >>> fields = get_update_fields()
        >>> fields['title']
        'New title'
    """
    ui.console.print("\n[dim]Leave blank to keep current value[/dim]\n")
    title = Prompt.ask("[white]New title (optional)[/white]", default="")
    description = Prompt.ask("[white]New description (optional)[/white]", default="")

    return {"title": title, "description": description}


def get_search_keyword() -> str:
    """Prompt for search keyword.

    Returns:
        str: Search keyword

    Example:
        >>> keyword = get_search_keyword()
        Enter search keyword: meeting
    """
    return Prompt.ask("[white]Enter search keyword[/white]")


def get_filter_criteria() -> dict[str, str]:
    """Prompt for filter criteria (status, priority, tag).

    Returns:
        dict: Filter criteria (empty string means no filter)

    Example:
        >>> criteria = get_filter_criteria()
        >>> criteria['status']
        'pending'
    """
    ui.console.print("\n[dim]Leave blank to skip filter[/dim]\n")

    status = Prompt.ask(
        "[white]Filter by status (all/pending/completed)[/white]",
        choices=["", "all", "pending", "completed"],
        default="",
    )
    priority = Prompt.ask(
        "[white]Filter by priority (High/Medium/Low)[/white]",
        choices=["", "High", "Medium", "Low"],
        default="",
    )
    tag = Prompt.ask("[white]Filter by tag[/white]", default="")

    return {"status": status or None, "priority": priority or None, "tag": tag or None}


def get_sort_options() -> tuple[str, bool]:
    """Prompt for sort field and direction.

    Returns:
        tuple[str, bool]: (sort_field, descending)

    Example:
        >>> field, desc = get_sort_options()
        >>> field
        'priority'
        >>> desc
        True
    """
    field = Prompt.ask(
        "[white]Sort by (id/title/priority/created/status)[/white]",
        choices=["id", "title", "priority", "created", "status"],
        default="id",
    )
    direction = Prompt.ask(
        "[white]Order (asc/desc)[/white]",
        choices=["asc", "desc"],
        default="asc",
    )

    return (field, direction == "desc")


def validate_title(title: str) -> str | None:
    """Validate task title.

    Args:
        title: Task title to validate

    Returns:
        str | None: Error message if invalid, None if valid

    Example:
        >>> validate_title("")
        'Task title cannot be empty. Please provide a title.'
        >>> validate_title("Valid title")
        None
    """
    if not title or title.isspace():
        return "Task title cannot be empty. Please provide a title."
    if len(title) > 200:
        return f"Task title too long ({len(title)} chars). Maximum 200 characters."
    return None


def validate_task_id(task_id: int | None) -> tuple[int | None, str | None]:
    """Validate task ID exists.

    Args:
        task_id: Task ID to validate

    Returns:
        tuple[int | None, str | None]: (task_id, error_message) - one will be None

    Example:
        >>> validate_task_id(1)
        (1, None)
        >>> validate_task_id(999)
        (None, 'Task not found with ID: 999. Available task IDs: 1, 2, 3')
    """
    if task_id is None:
        return (None, "Invalid task ID")

    task = task_manager.get_task_by_id(task_id)
    if not task:
        available_ids = [str(t.id) for t in task_manager.get_all_tasks()]
        if available_ids:
            ids_list = ", ".join(available_ids)
            return (None, f"Task not found with ID: {task_id}. Available task IDs: {ids_list}")
        else:
            return (None, "No tasks available")

    return (task_id, None)


def validate_priority(priority: str) -> str:
    """Normalize and validate priority input.

    Args:
        priority: Priority input (case-insensitive)

    Returns:
        str: Normalized priority (High/Medium/Low)

    Raises:
        ValueError: If priority is invalid
    """
    priority_map = {
        "high": "High",
        "medium": "Medium",
        "low": "Low",
        "h": "High",
        "m": "Medium",
        "l": "Low",
    }
    normalized = priority_map.get(priority.lower())
    if not normalized:
        ui.display_warning(
            "Invalid priority. Choose: High, Medium, or Low. Defaulting to Medium."
        )
        return "Medium"
    return normalized


def validate_tags(tags_input: str) -> list[str]:
    """Parse and validate tags input.

    Args:
        tags_input: Comma-separated tags

    Returns:
        list[str]: Validated tags (max 5, each max 20 chars)

    Example:
        >>> validate_tags("work, urgent, home")
        ['work', 'urgent', 'home']
    """
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    if len(tags) > 5:
        ui.display_warning("Too many tags. Using first 5.")
        tags = tags[:5]

    # Truncate tags longer than 20 characters
    tags = [tag[:20] if len(tag) > 20 else tag for tag in tags]

    return tags


# Command handlers will be implemented in later tasks
# (T019, T020, T027, T032, T035, T042, T047, T048, T053)


def handle_add_task() -> None:
    """Handle 'Add Task' command.

    Prompts user for task details, validates input, creates task, and displays success message.
    """
    task_data = get_task_input()

    # Validate title
    title_error = validate_title(task_data["title"])
    if title_error:
        ui.display_error(title_error)
        return

    # Create task
    try:
        task = task_manager.add_task(
            title=task_data["title"],
            description=task_data["description"],
            priority=task_data["priority"],
            tags=task_data["tags"],
        )
        ui.display_success(f"Task created successfully! (ID: {task.id})")
    except ValueError as e:
        ui.display_error(f"Failed to create task: {str(e)}")


def handle_view_tasks() -> None:
    """Handle 'View All Tasks' command.

    Retrieves all tasks, applies current sort preference, and displays them in a formatted table.
    Shows task statistics after the table. Shows a message if no tasks exist.
    """
    tasks = task_manager.get_all_tasks()

    if not tasks:
        ui.display_info("No tasks found. Add your first task to get started!")
        return

    # Apply current sort preference
    sorted_tasks = task_manager.sort_tasks(
        tasks,
        by=task_manager.current_sort["by"],
        descending=task_manager.current_sort["descending"],
    )

    ui.display_tasks_table(sorted_tasks)

    # Display task statistics
    stats = task_manager.get_task_stats()
    ui.console.print()  # Add spacing
    ui.display_task_stats(stats)


def handle_update_task() -> None:
    """Handle 'Update Task' command.

    Prompts for task ID, validates it exists, prompts for new values, updates task, and displays confirmation.
    """
    ui.console.print("\n[cyan bold]✏️  Update Task[/cyan bold]\n")

    task_id = get_task_id()
    if task_id is None:
        return

    # Validate task exists
    validated_id, error = validate_task_id(task_id)
    if error:
        ui.display_error(error)
        return

    # Show current task details
    task = task_manager.get_task_by_id(validated_id)
    ui.console.print(f"\n[dim]Current title:[/dim] {task.title}")
    ui.console.print(f"[dim]Current description:[/dim] {task.description or '(none)'}\n")

    # Get update fields
    fields = get_update_fields()

    # Only update if at least one field provided
    if not fields["title"] and not fields["description"]:
        ui.display_info("No changes made.")
        return

    # Update task
    success = task_manager.update_task(
        validated_id,
        title=fields["title"] if fields["title"] else None,
        description=fields["description"] if fields["description"] else None,
    )

    if success:
        ui.display_success(f"Task ID {validated_id} updated successfully!")
    else:
        ui.display_error(f"Failed to update task ID: {validated_id}")


def handle_delete_task() -> None:
    """Handle 'Delete Task' command.

    Prompts for task ID, validates it exists, confirms deletion, deletes task, and displays confirmation.
    """
    ui.console.print("\n[cyan bold]🗑️  Delete Task[/cyan bold]\n")

    task_id = get_task_id()
    if task_id is None:
        return

    # Validate task exists
    validated_id, error = validate_task_id(task_id)
    if error:
        ui.display_error(error)
        return

    # Show task details and confirm
    task = task_manager.get_task_by_id(validated_id)
    ui.console.print(f"\n[dim]Task to delete:[/dim] {task.title}")

    confirm = Confirm.ask("[yellow]Are you sure you want to delete this task?[/yellow]", default=False)

    if not confirm:
        ui.display_info("Deletion cancelled.")
        return

    # Delete task
    success = task_manager.delete_task(validated_id)
    if success:
        ui.display_success(f"Task '{task.title}' (ID: {validated_id}) deleted successfully!")
    else:
        ui.display_error(f"Failed to delete task ID: {validated_id}")


def handle_toggle_complete() -> None:
    """Handle 'Mark Complete/Incomplete' command.

    Prompts for task ID, validates it exists, toggles completion status, and displays confirmation.
    """
    ui.console.print("\n[cyan bold]✅ Toggle Task Completion[/cyan bold]\n")

    task_id = get_task_id()
    if task_id is None:
        return

    # Validate task exists
    validated_id, error = validate_task_id(task_id)
    if error:
        ui.display_error(error)
        return

    # Get task before toggling to show old status
    task = task_manager.get_task_by_id(validated_id)
    old_status = "✓ Done" if task.completed else "⏳ Pending"

    # Toggle completion
    success = task_manager.toggle_complete(validated_id)
    if success:
        task = task_manager.get_task_by_id(validated_id)
        new_status = "✓ Done" if task.completed else "⏳ Pending"
        ui.display_success(
            f"Task '{task.title}' status changed from {old_status} to {new_status}"
        )
    else:
        ui.display_error(f"Failed to toggle completion status for task ID: {validated_id}")


def handle_search_tasks() -> None:
    """Handle 'Search Tasks' command.

    Prompts for search keyword, searches tasks, and displays matching results or 'no matches' message.
    """
    ui.console.print("\n[cyan bold]🔍 Search Tasks[/cyan bold]\n")

    keyword = get_search_keyword()
    results = task_manager.search_tasks(keyword)

    if not results:
        ui.display_warning(f"No tasks match your search: '{keyword}'")
        return

    ui.console.print(f"\n[dim]Found {len(results)} task(s) matching '{keyword}':[/dim]\n")
    ui.display_tasks_table(results)


def handle_filter_tasks() -> None:
    """Handle 'Filter Tasks' command.

    Prompts for filter criteria (status/priority/tag), filters tasks, and displays matching results.
    """
    ui.console.print("\n[cyan bold]🏷️  Filter Tasks[/cyan bold]\n")

    criteria = get_filter_criteria()

    # Apply filters
    results = task_manager.filter_tasks(
        status=criteria["status"],
        priority=criteria["priority"],
        tag=criteria["tag"],
    )

    if not results:
        ui.display_warning("No tasks match your filter criteria.")
        return

    # Build filter description
    filters_applied = []
    if criteria["status"]:
        filters_applied.append(f"status={criteria['status']}")
    if criteria["priority"]:
        filters_applied.append(f"priority={criteria['priority']}")
    if criteria["tag"]:
        filters_applied.append(f"tag={criteria['tag']}")

    filter_desc = ", ".join(filters_applied) if filters_applied else "none"
    ui.console.print(f"\n[dim]Found {len(results)} task(s) with filters: {filter_desc}[/dim]\n")
    ui.display_tasks_table(results)


def handle_sort_tasks() -> None:
    """Handle 'Sort Tasks' command.

    Prompts for sort field and direction, updates global sort state, and displays sorted tasks.
    """
    ui.console.print("\n[cyan bold]🔄 Sort Tasks[/cyan bold]\n")

    field, descending = get_sort_options()

    # Update global sort state
    task_manager.current_sort["by"] = field
    task_manager.current_sort["descending"] = descending

    # Get and sort tasks
    tasks = task_manager.get_all_tasks()
    if not tasks:
        ui.display_info("No tasks to sort.")
        return

    sorted_tasks = task_manager.sort_tasks(tasks, by=field, descending=descending)

    order_desc = "descending" if descending else "ascending"
    ui.console.print(f"\n[dim]Tasks sorted by {field} ({order_desc}):[/dim]\n")
    ui.display_tasks_table(sorted_tasks)
    ui.console.print(f"\n[dim]Sort preference saved for this session.[/dim]")
