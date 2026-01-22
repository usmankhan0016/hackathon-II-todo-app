---
name: error-handling
description: Implement comprehensive error handling with HTTPException, validation errors, and standard status codes. Use when building robust FastAPI endpoints.
---

# Error Handling Skill - HTTPException & Validation

## Instructions

Implement comprehensive error handling across FastAPI endpoints with proper HTTP status codes, validation, exception handling, and meaningful error messages.

### 1. **HTTP Status Codes**
   - **200 OK**: Successful GET, general success
   - **201 Created**: Successful POST with new resource
   - **204 No Content**: Successful DELETE (no response body)
   - **400 Bad Request**: Validation error, malformed request
   - **401 Unauthorized**: Missing/invalid authentication
   - **403 Forbidden**: Authenticated but unauthorized (wrong user)
   - **404 Not Found**: Resource doesn't exist
   - **409 Conflict**: Duplicate resource (email already exists)
   - **422 Unprocessable Entity**: Semantic validation error (pydantic)
   - **429 Too Many Requests**: Rate limit exceeded
   - **500 Internal Server Error**: Unexpected server error
   - **503 Service Unavailable**: Database connection failed

### 2. **HTTPException Usage**
   - Use FastAPI HTTPException for all errors
   - Include meaningful detail message
   - Include appropriate status_code
   - Add headers when needed (WWW-Authenticate for 401)
   - Never expose internal stack traces to client
   - Log full error details server-side

### 3. **Validation Error Handling**
   - Pydantic validates request bodies automatically
   - FastAPI returns 422 Unprocessable Entity for validation errors
   - Custom validators for business logic
   - Return detailed validation error messages
   - Include field names in error details
   - Suggest corrections when possible

### 4. **Database Error Handling**
   - Catch IntegrityError for unique constraint violations
   - Catch OperationalError for connection failures
   - Catch NoResultFound for missing resources
   - Translate to appropriate HTTP status codes
   - Log database errors with full context
   - Return generic message to client

### 5. **Global Exception Handlers**
   - Register custom exception handlers
   - Handle unexpected exceptions gracefully
   - Log exceptions with request context
   - Return 500 with generic message
   - Never expose sensitive error details
   - Include request ID for tracing

## Example Implementation

### Error Response Model
```python
from pydantic import BaseModel
from typing import Optional, Any, Dict

class ErrorDetail(BaseModel):
    """Standard error response."""
    error: str  # Error code or message
    message: str  # Human-readable message
    status_code: int
    detail: Optional[str] = None  # Additional details
    field: Optional[str] = None  # Field with error (validation only)
    request_id: Optional[str] = None  # For tracing

class ValidationError(BaseModel):
    """Validation error response."""
    error: str = "validation_error"
    message: str = "Validation failed"
    status_code: int = 422
    errors: Dict[str, Any]  # Field-level errors
    request_id: Optional[str] = None
```

### HTTPException Usage Examples
```python
from fastapi import HTTPException, status

# 404 Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task not found"
)

# 401 Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

# 403 Forbidden
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Forbidden"
)

# 409 Conflict (duplicate)
raise HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Email already registered"
)

# 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid request data"
)
```

### Database Error Handling
```python
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import NoResultFound
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import logging

logger = logging.getLogger(__name__)

@app.post("/api/tasks")
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create task with database error handling."""
    try:
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    except IntegrityError as e:
        """Handle unique constraint violations."""
        db.rollback()
        logger.error(f"Integrity error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Resource already exists"
        )

    except OperationalError as e:
        """Handle database connection errors."""
        db.rollback()
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable"
        )

    except Exception as e:
        """Handle unexpected errors."""
        db.rollback()
        logger.error(f"Unexpected error creating task: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

### Pydantic Custom Validators
```python
from pydantic import BaseModel, field_validator, ValidationError
from datetime import datetime

class TaskCreate(BaseModel):
    """Task creation with validation."""
    title: str
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        """Validate title is not empty."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        if len(v) > 255:
            raise ValueError("Title must be 255 characters or less")
        return v.strip()

    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v):
        """Validate due date is in future."""
        if v and v < datetime.utcnow():
            raise ValueError("Due date must be in the future")
        return v

# Usage in endpoint
@app.post("/api/tasks")
async def create_task(task_data: TaskCreate):
    """Create task (validation errors auto-return 422)."""
    return task_data
```

### Global Exception Handler
```python
from fastapi import Request
from fastapi.responses import JSONResponse
import uuid
import logging

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions globally."""
    request_id = str(uuid.uuid4())

    logger.error(
        f"Unhandled exception (ID: {request_id}) | "
        f"Path: {request.url.path} | "
        f"Method: {request.method} | "
        f"Error: {str(exc)}",
        exc_info=True
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred",
            "status_code": 500,
            "request_id": request_id
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTPException handler with request ID."""
    request_id = str(uuid.uuid4())

    # Log 4xx errors as warnings, 5xx as errors
    if exc.status_code >= 500:
        logger.error(f"HTTP Error {exc.status_code}: {exc.detail} (ID: {request_id})")
    else:
        logger.warning(f"HTTP Error {exc.status_code}: {exc.detail} (ID: {request_id})")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "message": exc.detail,
            "status_code": exc.status_code,
            "request_id": request_id
        },
        headers=exc.headers
    )
```

### Business Logic Validation
```python
from datetime import datetime

async def validate_task_update(
    task: Task,
    update_data: TaskUpdate,
    db: Session
) -> None:
    """Validate business logic for task updates."""

    # Cannot set due_date in the past
    if update_data.due_date and update_data.due_date < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Due date cannot be in the past"
        )

    # Cannot complete overdue task
    if update_data.status == TaskStatus.COMPLETED and task.status == TaskStatus.OVERDUE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot complete overdue tasks, archive instead"
        )

    # Cannot change user_id
    if update_data.user_id and update_data.user_id != task.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change task ownership"
        )

@app.patch("/api/tasks/{task_id}")
async def update_task(
    task_id: str,
    update_data: TaskUpdate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update task with validation."""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Validate business logic
    await validate_task_update(task, update_data, db)

    # Apply update
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task
```

### Test Example
```python
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_task_validation_error():
    """Test 400 for invalid title."""
    headers = {"Authorization": f"Bearer {valid_token}"}
    response = client.post(
        "/api/tasks",
        json={"title": ""},  # Empty title
        headers=headers
    )
    assert response.status_code == 422  # Validation error
    assert "title" in response.json()

def test_create_task_duplicate_conflict():
    """Test 409 for duplicate resource."""
    headers = {"Authorization": f"Bearer {valid_token}"}
    response = client.post(
        "/api/auth/signup",
        json={"email": "existing@example.com", "password": "SecurePass123"}
    )
    assert response.status_code == 409  # Conflict

def test_get_task_not_found():
    """Test 404 for missing task."""
    headers = {"Authorization": f"Bearer {valid_token}"}
    response = client.get(
        "/api/tasks/nonexistent-id",
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["error"] == "Task not found"

def test_unauthorized_access():
    """Test 401 without token."""
    response = client.get("/api/tasks")
    assert response.status_code == 401
```

## Acceptance Criteria
- [ ] All endpoints return appropriate HTTP status codes
- [ ] HTTPException used for all error cases
- [ ] Validation errors return 422 with field details
- [ ] Database errors caught and translated to HTTP errors
- [ ] 404 for missing resources
- [ ] 403 for cross-user access
- [ ] 401 for authentication failures
- [ ] 409 for duplicate resources
- [ ] Global exception handler for unexpected errors
- [ ] Error responses include request_id for tracing
- [ ] Internal errors logged, generic message to client
- [ ] Pydantic validators working correctly
- [ ] Business logic validation implemented
- [ ] All tests passing (error scenarios covered)

## Dependencies
- **FastAPI**: Web framework
- **pydantic**: Validation models
- **SQLAlchemy**: Database exceptions
- **python-jose**: JWT errors
- **logging**: Error logging
- **uuid**: Request tracking

## Related Skills
- `task_crud` – Implement errors in endpoints
- `jwt_middleware` – Authentication errors
- `auth_routes` – Validation in signup/signin
