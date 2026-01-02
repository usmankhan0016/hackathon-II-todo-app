# Task: T016-T024
# Spec: specs/001-phase1-console-app/spec.md#business-logic-tests
# Purpose: Unit tests for task_manager module (all CRUD and query operations)

"""Unit tests for task_manager module."""

import pytest
from datetime import datetime
from src.phase1 import task_manager
from src.phase1.models import Task


class TestAddTask:
    """Test add_task() function - T016."""

    def test_add_task_with_minimal_fields(self, empty_task_list):
        """Test adding task with only title."""
        task = task_manager.add_task("Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == "Medium"
        assert task.tags == []
        assert len(task_manager.tasks) == 1

    def test_add_task_with_all_fields(self, empty_task_list):
        """Test adding task with all fields."""
        task = task_manager.add_task(
            title="Complete Task",
            description="Test description",
            priority="High",
            tags=["work", "urgent"],
        )

        assert task.id == 1
        assert task.title == "Complete Task"
        assert task.description == "Test description"
        assert task.priority == "High"
        assert task.tags == ["work", "urgent"]

    def test_add_multiple_tasks_generates_sequential_ids(self, empty_task_list):
        """Test that adding multiple tasks generates sequential IDs."""
        task1 = task_manager.add_task("Task 1")
        task2 = task_manager.add_task("Task 2")
        task3 = task_manager.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_sets_timestamps(self, empty_task_list):
        """Test that add_task sets created_at and updated_at timestamps."""
        task = task_manager.add_task("Test Task")

        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)
        assert task.created_at == task.updated_at  # Initially equal


class TestGetAllTasks:
    """Test get_all_tasks() function - T017."""

    def test_get_all_tasks_returns_empty_list_when_no_tasks(self, empty_task_list):
        """Test that get_all_tasks returns empty list when no tasks exist."""
        tasks = task_manager.get_all_tasks()
        assert tasks == []

    def test_get_all_tasks_returns_all_tasks(self, populated_task_list):
        """Test that get_all_tasks returns all tasks."""
        tasks = task_manager.get_all_tasks()
        assert len(tasks) == 3
        assert tasks[0].title == "Task One"
        assert tasks[1].title == "Task Two"
        assert tasks[2].title == "Task Three"

    def test_get_all_tasks_returns_copy_not_original(self, populated_task_list):
        """Test that get_all_tasks returns a copy, not the original list."""
        tasks = task_manager.get_all_tasks()
        tasks.append(Task(id=999, title="Should not affect original"))

        # Original list should still have 3 tasks
        assert len(task_manager.tasks) == 3


class TestGetTaskById:
    """Test get_task_by_id() function - T018."""

    def test_get_task_by_id_returns_correct_task(self, populated_task_list):
        """Test that get_task_by_id returns the correct task."""
        task = task_manager.get_task_by_id(2)

        assert task is not None
        assert task.id == 2
        assert task.title == "Task Two"

    def test_get_task_by_id_returns_none_for_nonexistent_id(self, populated_task_list):
        """Test that get_task_by_id returns None for non-existent ID."""
        task = task_manager.get_task_by_id(999)
        assert task is None

    def test_get_task_by_id_on_empty_list_returns_none(self, empty_task_list):
        """Test that get_task_by_id returns None on empty list."""
        task = task_manager.get_task_by_id(1)
        assert task is None


class TestUpdateTask:
    """Test update_task() function - T019."""

    def test_update_task_title_only(self, populated_task_list):
        """Test updating only the title."""
        result = task_manager.update_task(1, title="Updated Title")

        assert result is True
        task = task_manager.get_task_by_id(1)
        assert task.title == "Updated Title"
        assert task.description == "First task"  # Unchanged

    def test_update_task_description_only(self, populated_task_list):
        """Test updating only the description."""
        result = task_manager.update_task(1, description="Updated description")

        assert result is True
        task = task_manager.get_task_by_id(1)
        assert task.title == "Task One"  # Unchanged
        assert task.description == "Updated description"

    def test_update_task_both_fields(self, populated_task_list):
        """Test updating both title and description."""
        result = task_manager.update_task(
            1, title="New Title", description="New description"
        )

        assert result is True
        task = task_manager.get_task_by_id(1)
        assert task.title == "New Title"
        assert task.description == "New description"

    def test_update_task_refreshes_updated_at(self, populated_task_list):
        """Test that update_task refreshes updated_at timestamp."""
        task = task_manager.get_task_by_id(1)
        original_updated_at = task.updated_at

        # Small delay to ensure timestamp changes
        import time
        time.sleep(0.01)

        task_manager.update_task(1, title="Updated")
        task = task_manager.get_task_by_id(1)

        assert task.updated_at > original_updated_at

    def test_update_task_preserves_created_at(self, populated_task_list):
        """Test that update_task preserves created_at timestamp."""
        task = task_manager.get_task_by_id(1)
        original_created_at = task.created_at

        task_manager.update_task(1, title="Updated")
        task = task_manager.get_task_by_id(1)

        assert task.created_at == original_created_at

    def test_update_nonexistent_task_returns_false(self, populated_task_list):
        """Test that updating non-existent task returns False."""
        result = task_manager.update_task(999, title="Not exist")
        assert result is False


class TestDeleteTask:
    """Test delete_task() function - T020."""

    def test_delete_task_removes_from_list(self, populated_task_list):
        """Test that delete_task removes task from list."""
        result = task_manager.delete_task(2)

        assert result is True
        assert len(task_manager.tasks) == 2
        assert task_manager.get_task_by_id(2) is None

    def test_delete_nonexistent_task_returns_false(self, populated_task_list):
        """Test that deleting non-existent task returns False."""
        result = task_manager.delete_task(999)
        assert result is False
        assert len(task_manager.tasks) == 3  # No change

    def test_delete_task_preserves_other_tasks(self, populated_task_list):
        """Test that deleting one task doesn't affect others."""
        task_manager.delete_task(2)

        task1 = task_manager.get_task_by_id(1)
        task3 = task_manager.get_task_by_id(3)

        assert task1 is not None
        assert task3 is not None

    def test_id_not_reused_after_deletion(self, empty_task_list):
        """Test that IDs are not reused after deletion."""
        task_manager.add_task("Task 1")  # ID 1
        task_manager.add_task("Task 2")  # ID 2
        task_manager.delete_task(1)

        new_task = task_manager.add_task("Task 3")
        assert new_task.id == 3  # Not 1


class TestToggleComplete:
    """Test toggle_complete() function - T021."""

    def test_toggle_complete_from_pending_to_done(self, populated_task_list):
        """Test toggling task from pending to completed."""
        task = task_manager.get_task_by_id(1)
        assert task.completed is False

        result = task_manager.toggle_complete(1)

        assert result is True
        task = task_manager.get_task_by_id(1)
        assert task.completed is True

    def test_toggle_complete_from_done_to_pending(self, populated_task_list):
        """Test toggling task from completed to pending."""
        task = task_manager.get_task_by_id(2)
        assert task.completed is True

        result = task_manager.toggle_complete(2)

        assert result is True
        task = task_manager.get_task_by_id(2)
        assert task.completed is False

    def test_toggle_complete_updates_timestamp(self, populated_task_list):
        """Test that toggle_complete updates updated_at timestamp."""
        task = task_manager.get_task_by_id(1)
        original_updated_at = task.updated_at

        import time
        time.sleep(0.01)

        task_manager.toggle_complete(1)
        task = task_manager.get_task_by_id(1)

        assert task.updated_at > original_updated_at

    def test_toggle_nonexistent_task_returns_false(self, populated_task_list):
        """Test that toggling non-existent task returns False."""
        result = task_manager.toggle_complete(999)
        assert result is False


class TestSearchTasks:
    """Test search_tasks() function - T022."""

    def test_search_tasks_by_title(self, populated_task_list):
        """Test searching tasks by keyword in title."""
        results = task_manager.search_tasks("Two")

        assert len(results) == 1
        assert results[0].title == "Task Two"

    def test_search_tasks_by_description(self, populated_task_list):
        """Test searching tasks by keyword in description."""
        results = task_manager.search_tasks("First")

        assert len(results) == 1
        assert results[0].title == "Task One"

    def test_search_tasks_case_insensitive(self, populated_task_list):
        """Test that search is case-insensitive."""
        results_lower = task_manager.search_tasks("task")
        results_upper = task_manager.search_tasks("TASK")
        results_mixed = task_manager.search_tasks("TaSk")

        assert len(results_lower) == 3
        assert len(results_upper) == 3
        assert len(results_mixed) == 3

    def test_search_tasks_no_matches_returns_empty_list(self, populated_task_list):
        """Test that search with no matches returns empty list."""
        results = task_manager.search_tasks("nonexistent")
        assert results == []


class TestFilterTasks:
    """Test filter_tasks() function - T023."""

    def test_filter_by_status_pending(self, populated_task_list):
        """Test filtering by pending status."""
        results = task_manager.filter_tasks(status="pending")

        assert len(results) == 2
        assert all(not t.completed for t in results)

    def test_filter_by_status_completed(self, populated_task_list):
        """Test filtering by completed status."""
        results = task_manager.filter_tasks(status="completed")

        assert len(results) == 1
        assert all(t.completed for t in results)

    def test_filter_by_priority(self, populated_task_list):
        """Test filtering by priority level."""
        results = task_manager.filter_tasks(priority="High")

        assert len(results) == 1
        assert results[0].priority == "High"

    def test_filter_by_tag(self, populated_task_list):
        """Test filtering by tag."""
        results = task_manager.filter_tasks(tag="work")

        assert len(results) == 2
        assert all("work" in t.tags for t in results)

    def test_filter_by_multiple_criteria(self, populated_task_list):
        """Test filtering by multiple criteria combined."""
        results = task_manager.filter_tasks(status="pending", tag="work")

        assert len(results) == 2
        assert all(not t.completed and "work" in t.tags for t in results)

    def test_filter_all_status_returns_all_tasks(self, populated_task_list):
        """Test that status='all' returns all tasks."""
        results = task_manager.filter_tasks(status="all")
        assert len(results) == 3


class TestSortTasks:
    """Test sort_tasks() function - T024."""

    def test_sort_by_id_ascending(self, populated_task_list):
        """Test sorting by ID in ascending order."""
        tasks = task_manager.get_all_tasks()
        sorted_tasks = task_manager.sort_tasks(tasks, by="id", descending=False)

        assert [t.id for t in sorted_tasks] == [1, 2, 3]

    def test_sort_by_id_descending(self, populated_task_list):
        """Test sorting by ID in descending order."""
        tasks = task_manager.get_all_tasks()
        sorted_tasks = task_manager.sort_tasks(tasks, by="id", descending=True)

        assert [t.id for t in sorted_tasks] == [3, 2, 1]

    def test_sort_by_title(self, populated_task_list):
        """Test sorting by title alphabetically."""
        tasks = task_manager.get_all_tasks()
        sorted_tasks = task_manager.sort_tasks(tasks, by="title", descending=False)

        assert [t.title for t in sorted_tasks] == ["Task One", "Task Three", "Task Two"]

    def test_sort_by_priority_descending(self, populated_task_list):
        """Test sorting by priority (High to Low)."""
        tasks = task_manager.get_all_tasks()
        sorted_tasks = task_manager.sort_tasks(tasks, by="priority", descending=True)

        assert [t.priority for t in sorted_tasks] == ["High", "Medium", "Low"]

    def test_sort_by_status(self, populated_task_list):
        """Test sorting by completion status."""
        tasks = task_manager.get_all_tasks()
        sorted_tasks = task_manager.sort_tasks(tasks, by="status", descending=False)

        # False (pending) comes before True (completed) when ascending
        completed_count = sum(1 for t in sorted_tasks if t.completed)
        assert completed_count == 1
        assert sorted_tasks[-1].completed is True  # Completed task at end

    def test_sort_returns_new_list(self, populated_task_list):
        """Test that sort_tasks returns a new list (doesn't modify original)."""
        tasks = task_manager.get_all_tasks()
        original_order = [t.id for t in tasks]

        sorted_tasks = task_manager.sort_tasks(tasks, by="id", descending=True)

        # Original should be unchanged
        assert [t.id for t in tasks] == original_order
        # Sorted should be different
        assert [t.id for t in sorted_tasks] == [3, 2, 1]

    def test_sort_by_invalid_field_raises_error(self, populated_task_list):
        """Test that sorting by invalid field raises ValueError."""
        tasks = task_manager.get_all_tasks()

        with pytest.raises(ValueError, match="Invalid sort field"):
            task_manager.sort_tasks(tasks, by="invalid_field")


class TestGetTaskStats:
    """Test get_task_stats() function (for T071 but tested here)."""

    def test_get_task_stats_with_no_tasks(self, empty_task_list):
        """Test stats with empty task list."""
        stats = task_manager.get_task_stats()

        assert stats["total"] == 0
        assert stats["completed"] == 0
        assert stats["pending"] == 0

    def test_get_task_stats_with_populated_list(self, populated_task_list):
        """Test stats with populated task list."""
        stats = task_manager.get_task_stats()

        assert stats["total"] == 3
        assert stats["completed"] == 1
        assert stats["pending"] == 2
