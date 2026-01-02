# Task: T015
# Spec: specs/001-phase1-console-app/spec.md#data-model-validation
# Purpose: Unit tests for Task dataclass validation

"""Unit tests for Task dataclass and validation logic."""

import pytest
from datetime import datetime
from src.phase1.models import Task, Priority


class TestTaskCreation:
    """Test Task dataclass creation and initialization."""

    def test_create_task_with_minimal_fields(self):
        """Test creating task with only required fields (id, title)."""
        task = Task(id=1, title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False
        assert task.priority == "Medium"
        assert task.tags == []
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_create_task_with_all_fields(self):
        """Test creating task with all fields populated."""
        created = datetime(2026, 1, 1, 10, 0, 0)
        updated = datetime(2026, 1, 1, 11, 0, 0)

        task = Task(
            id=1,
            title="Complete Task",
            description="Test description",
            completed=True,
            priority="High",
            tags=["work", "urgent"],
            created_at=created,
            updated_at=updated,
        )

        assert task.id == 1
        assert task.title == "Complete Task"
        assert task.description == "Test description"
        assert task.completed is True
        assert task.priority == "High"
        assert task.tags == ["work", "urgent"]
        assert task.created_at == created
        assert task.updated_at == updated


class TestTaskValidation:
    """Test Task validation in __post_init__."""

    def test_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title="")

    def test_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(id=1, title="   ")

    def test_title_exceeding_200_chars_raises_error(self):
        """Test that title >200 characters raises ValueError."""
        long_title = "x" * 201
        with pytest.raises(ValueError, match="Task title too long"):
            Task(id=1, title=long_title)

    def test_description_exceeding_1000_chars_raises_error(self):
        """Test that description >1000 characters raises ValueError."""
        long_desc = "x" * 1001
        with pytest.raises(ValueError, match="Description too long"):
            Task(id=1, title="Test", description=long_desc)

    def test_invalid_priority_raises_error(self):
        """Test that invalid priority raises ValueError."""
        with pytest.raises(ValueError, match="Invalid priority"):
            Task(id=1, title="Test", priority="Critical")

    def test_too_many_tags_raises_error(self):
        """Test that >5 tags raises ValueError."""
        too_many_tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"]
        with pytest.raises(ValueError, match="Too many tags"):
            Task(id=1, title="Test", tags=too_many_tags)

    def test_tag_exceeding_20_chars_raises_error(self):
        """Test that tag >20 characters raises ValueError."""
        long_tag = "x" * 21
        with pytest.raises(ValueError, match="Tag too long"):
            Task(id=1, title="Test", tags=[long_tag])


class TestTaskFieldConstraints:
    """Test Task field constraints and edge cases."""

    def test_title_exactly_200_chars_is_valid(self):
        """Test that title of exactly 200 characters is valid."""
        title_200 = "x" * 200
        task = Task(id=1, title=title_200)
        assert len(task.title) == 200

    def test_description_exactly_1000_chars_is_valid(self):
        """Test that description of exactly 1000 characters is valid."""
        desc_1000 = "x" * 1000
        task = Task(id=1, title="Test", description=desc_1000)
        assert len(task.description) == 1000

    def test_exactly_5_tags_is_valid(self):
        """Test that exactly 5 tags is valid."""
        five_tags = ["tag1", "tag2", "tag3", "tag4", "tag5"]
        task = Task(id=1, title="Test", tags=five_tags)
        assert len(task.tags) == 5

    def test_tag_exactly_20_chars_is_valid(self):
        """Test that tag of exactly 20 characters is valid."""
        tag_20 = "x" * 20
        task = Task(id=1, title="Test", tags=[tag_20])
        assert len(task.tags[0]) == 20

    def test_all_priority_levels_are_valid(self):
        """Test that all priority levels (High/Medium/Low) are valid."""
        for priority in ["High", "Medium", "Low"]:
            task = Task(id=1, title="Test", priority=priority)
            assert task.priority == priority
