# Task: T014
# Spec: specs/001-phase1-console-app/spec.md#testing-infrastructure
# Purpose: Pytest fixtures for Phase 1 tests

"""Pytest fixtures for Phase 1 Todo Console App tests.

Provides reusable test data and setup/teardown logic.
"""

import pytest
from datetime import datetime
from src.phase1.models import Task
from src.phase1 import task_manager


@pytest.fixture
def sample_task():
    """Create a sample task for testing.

    Returns:
        Task: A task with id=1, title="Test Task"
    """
    return Task(
        id=1,
        title="Test Task",
        description="Test description",
        completed=False,
        priority="Medium",
        tags=["test"],
        created_at=datetime(2026, 1, 1, 10, 0, 0),
        updated_at=datetime(2026, 1, 1, 10, 0, 0),
    )


@pytest.fixture
def empty_task_list():
    """Ensure task list is empty before test.

    Yields:
        None: Clears task list, yields, then clears again after test
    """
    task_manager.tasks.clear()
    yield
    task_manager.tasks.clear()


@pytest.fixture
def populated_task_list(empty_task_list):
    """Create a populated task list with 3 tasks.

    Returns:
        list[Task]: List of 3 sample tasks
    """
    tasks = [
        Task(
            id=1,
            title="Task One",
            description="First task",
            completed=False,
            priority="High",
            tags=["work", "urgent"],
        ),
        Task(
            id=2,
            title="Task Two",
            description="Second task",
            completed=True,
            priority="Medium",
            tags=["personal"],
        ),
        Task(
            id=3,
            title="Task Three",
            description="Third task",
            completed=False,
            priority="Low",
            tags=["work"],
        ),
    ]
    task_manager.tasks.extend(tasks)
    return tasks
