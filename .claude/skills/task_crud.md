---
name: task-crud
description: Implement 6 REST endpoints (GET, POST, PUT, PATCH, DELETE) for task management with user isolation. Use when building task CRUD API operations.
---

# Task CRUD Skill - REST Endpoints

## Instructions

Implement complete CRUD operations for tasks with RESTful API endpoints, proper HTTP methods, user isolation, and pagination.

### 1. **GET /api/tasks** - List User Tasks
   - Retrieve all tasks for authenticated user
   - Query parameters: page (default 1), limit (default 20, max 100)
   - Filter by status: `?status=pending,completed`
   - Filter by priority: `?priority=high,medium,low`
   - Sort options: `?sort=created_at,-due_date` (- for descending)
   - Response: paginated list with metadata (total, page, limit)
   - HTTP 200 OK with array of tasks
   - Only return user's own tasks (enforce user_id isolation)

### 2. **GET /api/tasks/{task_id}** - Retrieve Single Task
   - Get specific task by ID
   - Verify task belongs to authenticated user
   - Return full task object with all fields
   - HTTP 200 OK on success
   - HTTP 404 Not Found if task doesn't exist
   - HTTP 403 Forbidden if user not authorized
   - Include related user info (optional sub-resource)

### 3. **POST /api/tasks** - Create Task
   - Create new task for authenticated user
   - Required fields: title
   - Optional fields: description, priority, due_date, estimated_hours, tags
   - Auto-set: user_id (from token), created_at, updated_at, status=pending
   - Validate title length (1-255 chars)
   - Validate due_date is present/future
   - Return created task with generated ID
   - HTTP 201 Created with Location header: `/api/tasks/{task_id}`
   - HTTP 400 Bad Request for validation errors

### 4. **PUT /api/tasks/{task_id}** - Replace Task (Full Update)
   - Replace entire task object
   - Requires all required fields in request body
   - Verify task ownership
   - Update all fields except created_at
   - Update updated_at timestamp
   - Validate all constraints
   - Return updated task object
   - HTTP 200 OK on success
   - HTTP 404 Not Found if task doesn't exist
   - HTTP 400 Bad Request for validation errors

### 5. **PATCH /api/tasks/{task_id}** - Partial Update
   - Partial update of task fields
   - Only provided fields are updated
   - Preserve unspecified fields
   - Verify task ownership
   - Update updated_at timestamp
   - Validate provided fields only
   - Common use: mark complete, change status, update due_date
   - Return updated task object
   - HTTP 200 OK on success
   - HTTP 404 Not Found if task doesn't exist
   - HTTP 400 Bad Request for validation errors

### 6. **DELETE /api/tasks/{task_id}** - Delete Task
   - Delete task permanently
   - Verify task ownership
   - Cascade delete any related data (if applicable)
   - HTTP 204 No Content on success (empty response)
   - HTTP 404 Not Found if task doesn't exist
   - HTTP 403 Forbidden if user not authorized

## Example Implementation

### Request/Response Models
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    OVERDUE = "overdue"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskCreate(BaseModel):
    """Request model for creating task."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    estimated_hours: Optional[int] = Field(None, ge=0)
    tags: Optional[str] = Field(None, max_length=500)

class TaskUpdate(BaseModel):
    """Request model for updating task (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[int] = Field(None, ge=0)
    tags: Optional[str] = Field(None, max_length=500)

class TaskResponse(BaseModel):
    """Response model for task."""
    id: str
    user_id: str
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime]
    completion_date: Optional[datetime]
    estimated_hours: Optional[int]
    tags: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    total: int
    page: int
    limit: int
    items: List[TaskResponse]
```

### LIST Endpoint with Pagination & Filtering
```python
from fastapi import FastAPI, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from database import get_db

app = FastAPI()

@app.get("/api/tasks", response_model=PaginatedResponse)
async def list_tasks(
    user_id: str = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    sort: str = Query("-created_at"),
    db: Session = Depends(get_db)
):
    """List all tasks for authenticated user with pagination."""
    # Base query filtered by user
    query = db.query(Task).filter(Task.user_id == user_id)

    # Apply status filter
    if status:
        statuses = status.split(",")
        query = query.filter(Task.status.in_(statuses))

    # Apply priority filter
    if priority:
        priorities = priority.split(",")
        query = query.filter(Task.priority.in_(priorities))

    # Get total count before pagination
    total = query.count()

    # Apply sorting
    for sort_field in sort.split(","):
        if sort_field.startswith("-"):
            field_name = sort_field[1:]
            query = query.order_by(desc(getattr(Task, field_name)))
        else:
            query = query.order_by(asc(getattr(Task, sort_field)))

    # Apply pagination
    offset = (page - 1) * limit
    tasks = query.offset(offset).limit(limit).all()

    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        items=tasks
    )
```

### GET Single Task
```python
@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve single task by ID."""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task
```

### CREATE Task
```python
from fastapi import Response

@app.post("/api/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    response: Response = None
):
    """Create new task for authenticated user."""
    # Create task object
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date,
        estimated_hours=task_data.estimated_hours,
        tags=task_data.tags,
        status=TaskStatus.PENDING
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    # Set Location header
    response.headers["Location"] = f"/api/tasks/{task.id}"

    return task
```

### UPDATE Task (PUT - Full Replace)
```python
@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Replace entire task (PUT)."""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update all fields except created_at
    task.title = task_data.title
    task.description = task_data.description
    task.priority = task_data.priority
    task.due_date = task_data.due_date
    task.estimated_hours = task_data.estimated_hours
    task.tags = task_data.tags
    task.updated_at = datetime.utcnow()

    db.add(task)
    db.commit()
    db.refresh(task)

    return task
```

### PATCH Task (Partial Update)
```python
@app.patch("/api/tasks/{task_id}", response_model=TaskResponse)
async def partial_update_task(
    task_id: str,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Partially update task (PATCH)."""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    db.add(task)
    db.commit()
    db.refresh(task)

    return task
```

### DELETE Task
```python
@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete task permanently."""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return None
```

## Acceptance Criteria
- [ ] GET /api/tasks returns paginated list with filters
- [ ] GET /api/tasks/{id} returns single task or 404
- [ ] POST /api/tasks creates task with 201 status
- [ ] PUT /api/tasks/{id} replaces entire task
- [ ] PATCH /api/tasks/{id} partially updates task
- [ ] DELETE /api/tasks/{id} deletes task (204)
- [ ] All endpoints enforce user isolation (user_id check)
- [ ] Pagination working (page, limit parameters)
- [ ] Sorting working (multi-field sort, ascending/descending)
- [ ] Filtering by status and priority working
- [ ] Validation errors return 400 with details
- [ ] Authorization errors return 403
- [ ] All endpoints tested with pytest
- [ ] Response models match TaskResponse schema

## Dependencies
- **FastAPI**: Web framework
- **SQLModel**: ORM for database access
- **pydantic**: Request/response validation
- **SQLAlchemy**: Query building
- **python-jose**: JWT token handling (from auth)

## Related Skills
- `jwt_middleware` – Verify tokens and extract user_id
- `error_handling` – Handle validation and HTTP errors
- `schema_design` – Task model definition
