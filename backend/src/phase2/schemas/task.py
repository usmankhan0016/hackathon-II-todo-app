"""
Pydantic models for Task API endpoints.
Separate create/update/response models for validation and serialization.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator

from ..models.task import TaskPriority, TaskStatus


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    status: TaskStatus = Field(TaskStatus.PENDING)
    priority: TaskPriority = Field(TaskPriority.MEDIUM)
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = Field(default_factory=list)


class TaskCreate(TaskBase):
    """Model for POST /api/tasks - create new task."""
    pass


class TaskUpdate(BaseModel):
    """Model for PUT/PATCH /api/tasks/{id} - update task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None

    @validator('tags', pre=True, each_item=True)
    def validate_tags(cls, v):
        if isinstance(v, str) and len(v) > 50:
            raise ValueError('Tag too long')
        return v


class TaskResponse(TaskBase):
    """Model for task responses - includes ID and timestamps."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    """Wrapper for paginated task lists."""
    total: int
    page: int
    limit: int
    items: List[TaskResponse]


class ErrorDetail(BaseModel):
    """Standard error response format."""
    error: str
    message: str
    status_code: int
