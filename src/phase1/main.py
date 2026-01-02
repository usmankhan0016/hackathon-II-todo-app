# Task: T037
# Spec: specs/001-phase1-console-app/spec.md#user-story-1
# Purpose: Main application entry point with command loop

"""Main application module for Phase 1 Todo Console App.

This module contains the main application loop that:
- Displays header and menu
- Gets user input
- Routes to command handlers
- Handles graceful exit
"""

from src.phase1 import ui, cli


def main() -> None:
    """Main application loop.

    Displays menu, handles user input, and routes to appropriate command handlers.
    Exits gracefully on Ctrl+C or when user selects Exit option.
    """
    try:
        ui.display_header()
        ui.console.print(
            "\n[dim]Welcome to your Todo List! Manage your tasks efficiently.[/dim]\n"
        )

        while True:
            ui.display_menu()
            choice = cli.get_menu_choice()

            # Route to command handlers
            if choice == "1":
                cli.handle_add_task()
            elif choice == "2":
                cli.handle_view_tasks()
            elif choice == "3":
                cli.handle_update_task()
            elif choice == "4":
                cli.handle_toggle_complete()
            elif choice == "5":
                cli.handle_delete_task()
            elif choice == "6":
                cli.handle_search_tasks()
            elif choice == "7":
                cli.handle_filter_tasks()
            elif choice == "8":
                cli.handle_sort_tasks()
            elif choice == "9":
                ui.console.print("\n[cyan]👋 Goodbye! Your tasks are saved for this session.[/cyan]\n")
                break
            else:
                ui.display_warning(
                    f"Invalid choice: '{choice}'. Please select a number between 1 and 9."
                )

            ui.console.print()  # Add spacing between operations

    except KeyboardInterrupt:
        ui.console.print("\n\n[yellow]⚠️  Application interrupted by user (Ctrl+C)[/yellow]")
        ui.console.print("[cyan]👋 Goodbye! Your tasks are saved for this session.[/cyan]\n")
    except Exception as e:
        ui.display_error(f"Unexpected error occurred: {str(e)}")
        ui.console.print("\n[dim]Please report this issue if it persists.[/dim]\n")


if __name__ == "__main__":
    main()
