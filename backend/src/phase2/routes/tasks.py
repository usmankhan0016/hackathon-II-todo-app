"""
Task CRUD API endpoints with full user isolation and advanced querying.
All endpoints require JWT authentication via get_current_user_id dependency.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, desc, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..middleware.auth import get_current_user_id
from ..models.task import Task, TaskPriority, TaskStatus
from ..schemas.task import ErrorDetail, PaginatedResponse, TaskCreate, TaskResponse, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=PaginatedResponse)
async def list_tasks(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    status: Optional[TaskStatus] = Query(default=None),
    priority: Optional[TaskPriority] = Query(default=None),
    sort: str = Query(default="created_at:desc"),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    List user's tasks with pagination, filtering, and sorting.

    Query params:
    - page/limit: Pagination (default page=1, limit=20)
    - status: Filter by status (pending|in_progress|completed|cancelled)
    - priority: Filter by priority (low|medium|high|urgent)
    - sort: Comma-separated fields with direction (e.g. 'status:asc,created_at:desc')
      Allowed fields: id,title,status,priority,due_date,created_at,updated_at
    """
    user_uuid = UUID(user_id)

    # Build where clause
    where_clauses = [Task.user_id == user_uuid]
    if status:
        where_clauses.append(Task.status == status)
    if priority:
        where_clauses.append(Task.priority == priority)

    # Count total
    total_stmt = select(func.count(Task.id)).where(and_(*where_clauses))
    total = await db.scalar(total_stmt)

    # Parse sort
    allowed_fields = {
        'id', 'title', 'status', 'priority', 'due_date', 'created_at', 'updated_at'
    }
    order_by = []
    for s in sort.split(','):
        s = s.strip()
        if ':' in s:
            field, direction = s.rsplit(':', 1)
            direction = direction.lower()
        else:
            field, direction = s, 'asc'

        if field not in allowed_fields:
            raise HTTPException(
                400,
                detail=ErrorDetail(
                    error="INVALID_SORT_FIELD",
                    message=f"Invalid sort field: {field}",
                    status_code=400
                )
            )

        if direction == 'desc':
            order_by.append(desc(getattr(Task, field)))
        else:
            order_by.append(getattr(Task, field))

    # Main query
    stmt = (
        select(Task)
        .where(and_(*where_clauses))
        .order_by(*order_by)
        .offset((page - 1) * limit)
        .limit(limit)
    )

    result = await db.execute(stmt)
    tasks = result.scalars().all()

    return PaginatedResponse(
        total=total or 0,
        page=page,
        limit=limit,
        items=[TaskResponse.model_validate(task) for task in tasks]
    )


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task_in: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create new task for authenticated user."""
    task = Task(**task_in.dict(), user_id=UUID(user_id))
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return TaskResponse.model_validate(task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get single task by ID (ownership verified)."""
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=ErrorDetail(
                error="TASK_NOT_FOUND",
                message="Task not found",
                status_code=404
            )
        )
    if task.user_id != UUID(user_id):
        raise HTTPException(
            status_code=403,
            detail=ErrorDetail(
                error="TASK_NOT_AUTHORIZED",
                message="Not authorized to access this task",
                status_code=403
            )
        )
    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_in: TaskCreate,  # Full update requires all fields
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Full update/replace task (requires all fields)."""
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(404, detail={"error": "TASK_NOT_FOUND", "message": "Task not found"})
    if task.user_id != UUID(user_id):
        raise HTTPException(403, detail={"error": "TASK_NOT_AUTHORIZED", "message": "Not authorized"})

    for field, value in task_in.dict().items():
        setattr(task, field, value)
    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)
    return TaskResponse.model_validate(task)


@router.patch("/{task_id}", response_model=TaskResponse)
async def patch_task(
    task_id: UUID,
    task_in: TaskUpdate,  # Partial update
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Partial update task (only provided fields)."""
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(404, detail={"error": "TASK_NOT_FOUND", "message": "Task not found"})
    if task.user_id != UUID(user_id):
        raise HTTPException(403, detail={"error": "TASK_NOT_AUTHORIZED", "message": "Not authorized"})

    update_data = task_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)
    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Delete task (ownership verified)."""
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(404, detail={"error": "TASK_NOT_FOUND", "message": "Task not found"})
    if task.user_id != UUID(user_id):
        raise HTTPException(403, detail={"error": "TASK_NOT_AUTHORIZED", "message": "Not authorized"})

    await db.delete(task)
    await db.commit()
    return None
