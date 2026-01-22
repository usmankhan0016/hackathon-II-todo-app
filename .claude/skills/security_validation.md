---
name: security-validation
description: Validate user ID matching, data isolation, and cross-user access prevention. Use when implementing and testing security boundaries.
---

# Security Validation Skill - User Isolation & Data Access Control

## Instructions

Implement comprehensive security validation to prevent cross-user data access, enforce user ownership verification, and maintain data isolation across the application.

### 1. **User ID Validation**
   - Extract user_id from JWT token `sub` claim
   - Compare token user_id with request resource ownership
   - Verify user exists in database before granting access
   - Validate user_id is UUID format (if using UUIDs)
   - Reject requests with mismatched user_id
   - Return 403 Forbidden (not 404) to avoid information leakage
   - Log unauthorized access attempts with details

### 2. **Data Isolation at Query Level**
   - All queries filter by user_id from token
   - Queries MUST NOT return other users' data
   - Example: `SELECT * FROM tasks WHERE user_id = ? AND id = ?`
   - Never: `SELECT * FROM tasks WHERE id = ?` (missing user_id filter)
   - Validate result ownership after database query
   - Return 404 if task doesn't exist OR doesn't belong to user
   - Consistent error response (403 is safer than 404)

### 3. **Endpoint-Level Access Control**
   - All protected endpoints require valid JWT
   - Extract user_id from token in middleware
   - Pass user_id to endpoint handler
   - Endpoint handler validates resource ownership
   - Never trust user_id from query parameters
   - Never trust user_id from request body
   - Always extract from token claims

### 4. **Cross-User Access Prevention**
   - Cannot view other users' tasks
   - Cannot edit other users' tasks
   - Cannot delete other users' tasks
   - Cannot transfer task ownership
   - Cannot access other users' profile data
   - Cannot see other users' task metadata
   - Cannot filter by other user_id (returns 403)
   - Cannot update user_id field on existing tasks

### 5. **Relationship & Cascade Security**
   - Deleting user cascades to user's tasks only
   - Updating user only affects that user's data
   - Querying relationships filtered by user_id
   - Foreign key constraints enforced at database level
   - Cannot move task between users via batch operations

### 6. **Frontend Security Validation**
   - Verify JWT token before making requests
   - Extract user_id from token and validate
   - Store only current user's data in state
   - Don't cache other users' data
   - Validate API responses contain expected user_id
   - Redirect to login if token invalid
   - Clear all user data on logout

## Example Implementation

### Middleware User Extraction
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthenticationCredentials
from jwt_utils import verify_jwt_token
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthenticationCredentials = Depends(security)
) -> str:
    """Extract and verify user_id from JWT token."""
    try:
        payload = verify_jwt_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Missing user_id in token")
        return user_id
    except Exception as e:
        logger.warning(f"Failed to extract user_id: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

### User Ownership Validation
```python
from sqlalchemy.orm import Session
from models import Task, User

def verify_task_ownership(
    task_id: str,
    user_id: str,
    db: Session
) -> Task:
    """Verify task belongs to user."""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id  # CRITICAL: Filter by user_id
    ).first()

    if not task:
        logger.warning(f"User {user_id} attempted to access task {task_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"  # Don't reveal if task exists
        )

    return task

def verify_user_exists(user_id: str, db: Session) -> User:
    """Verify user exists and is active."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.error(f"User {user_id} not found in database")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
```

### Query-Level Data Isolation
```python
from sqlalchemy.orm import Session

async def get_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> Task:
    """Get task with user_id filter at query level."""
    # CORRECT: Filter by both task_id AND user_id
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id  # Must include user_id filter
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    return task

async def list_tasks(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """List only user's own tasks."""
    # CORRECT: Filter by user_id automatically
    tasks = db.query(Task).filter(
        Task.user_id == user_id  # Only this user's tasks
    ).all()

    return tasks

async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> Task:
    """Create task for current user only."""
    # CORRECT: Always set user_id from token, never from request body
    task = Task(
        user_id=user_id,  # From token, not request
        title=task_data.title,
        description=task_data.description
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task
```

### Update with Ownership Verification
```python
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> Task:
    """Update task with ownership verification."""
    task = verify_task_ownership(task_id, user_id, db)

    # CRITICAL: Prevent user_id change
    if task_data.user_id and task_data.user_id != user_id:
        logger.warning(
            f"User {user_id} attempted to change task ownership to {task_data.user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change task ownership"
        )

    # Update allowed fields only
    update_dict = task_data.model_dump(exclude_unset=True)
    # Ensure user_id is not in the update dict
    update_dict.pop('user_id', None)

    for field, value in update_dict.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task
```

### Delete with Ownership Verification
```python
async def delete_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete task with ownership verification."""
    task = verify_task_ownership(task_id, user_id, db)

    db.delete(task)
    db.commit()

    return None  # 204 No Content
```

### Batch Operations with Isolation
```python
async def bulk_delete_tasks(
    task_ids: List[str],
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete multiple tasks with user_id filter."""
    # CRITICAL: Filter by user_id to prevent cross-user deletion
    tasks = db.query(Task).filter(
        Task.id.in_(task_ids),
        Task.user_id == user_id  # Must include user_id filter
    ).all()

    if len(tasks) != len(task_ids):
        logger.warning(
            f"User {user_id} attempted to delete tasks outside their ownership"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Some tasks cannot be deleted"
        )

    for task in tasks:
        db.delete(task)

    db.commit()

    return {"deleted": len(tasks)}
```

### Frontend Security Validation
```typescript
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getToken, getUserIdFromToken } from '@/lib/auth';
import { fetchTasks } from '@/lib/api/tasks';
import { Task } from '@/lib/types';

export default function TasksPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadTasks() {
      try {
        // 1. Verify token exists
        const token = getToken();
        if (!token) {
          router.push('/login');
          return;
        }

        // 2. Extract user_id from token
        const currentUserId = getUserIdFromToken();
        if (!currentUserId) {
          // Invalid token, redirect to login
          router.push('/login');
          return;
        }

        // 3. Fetch tasks
        const response = await fetchTasks();

        // 4. Validate response contains only current user's tasks
        const validTasks = response.items.filter((task: Task) => {
          if (task.user_id !== currentUserId) {
            console.error(
              `Security violation: Task ${task.id} belongs to different user`
            );
            return false;
          }
          return true;
        });

        // 5. If any tasks failed validation, redirect to login
        if (validTasks.length !== response.items.length) {
          console.error('API returned data from other users');
          router.push('/login');
          return;
        }

        setTasks(validTasks);
      } catch (error) {
        console.error('Failed to load tasks:', error);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    }

    loadTasks();
  }, [router]);

  return (
    <div>
      {/* Render tasks */}
    </div>
  );
}
```

### Security Testing
```python
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_cannot_access_other_users_task():
    """Test user cannot access another user's task."""
    # Create user 1 and task
    user1_response = client.post("/api/auth/signup", json={
        "email": "user1@example.com",
        "password": "Pass123"
    })
    user1_token = user1_response.json()["access_token"]
    user1_id = user1_response.json()["user_id"]

    task_response = client.post(
        "/api/tasks",
        json={"title": "User 1 Task"},
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    task_id = task_response.json()["id"]

    # Create user 2
    user2_response = client.post("/api/auth/signup", json={
        "email": "user2@example.com",
        "password": "Pass123"
    })
    user2_token = user2_response.json()["access_token"]
    user2_id = user2_response.json()["user_id"]

    # User 2 tries to access user 1's task
    response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )

    # Must return 403, not 404 (to avoid information leakage)
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"

def test_cannot_modify_other_users_task():
    """Test user cannot modify another user's task."""
    # User 1 creates task
    user1_response = client.post("/api/auth/signup", json={
        "email": "user1@example.com",
        "password": "Pass123"
    })
    user1_token = user1_response.json()["access_token"]

    task_response = client.post(
        "/api/tasks",
        json={"title": "Original Title"},
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    task_id = task_response.json()["id"]

    # User 2 tries to update user 1's task
    user2_response = client.post("/api/auth/signup", json={
        "email": "user2@example.com",
        "password": "Pass123"
    })
    user2_token = user2_response.json()["access_token"]

    response = client.patch(
        f"/api/tasks/{task_id}",
        json={"title": "Hacked Title"},
        headers={"Authorization": f"Bearer {user2_token}"}
    )

    assert response.status_code == 403

    # Verify task was not modified
    verify_response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert verify_response.json()["title"] == "Original Title"

def test_cannot_delete_other_users_task():
    """Test user cannot delete another user's task."""
    # User 1 creates task
    user1_response = client.post("/api/auth/signup", json={
        "email": "user1@example.com",
        "password": "Pass123"
    })
    user1_token = user1_response.json()["access_token"]

    task_response = client.post(
        "/api/tasks",
        json={"title": "Vulnerable Task"},
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    task_id = task_response.json()["id"]

    # User 2 tries to delete user 1's task
    user2_response = client.post("/api/auth/signup", json={
        "email": "user2@example.com",
        "password": "Pass123"
    })
    user2_token = user2_response.json()["access_token"]

    response = client.delete(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )

    assert response.status_code == 403

    # Verify task still exists for user 1
    verify_response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert verify_response.status_code == 200

def test_list_tasks_only_shows_own_tasks():
    """Test list endpoint only returns user's own tasks."""
    # Create user 1 with tasks
    user1_response = client.post("/api/auth/signup", json={
        "email": "user1@example.com",
        "password": "Pass123"
    })
    user1_token = user1_response.json()["access_token"]

    for i in range(3):
        client.post(
            "/api/tasks",
            json={"title": f"User 1 Task {i}"},
            headers={"Authorization": f"Bearer {user1_token}"}
        )

    # Create user 2 with tasks
    user2_response = client.post("/api/auth/signup", json={
        "email": "user2@example.com",
        "password": "Pass123"
    })
    user2_token = user2_response.json()["access_token"]

    for i in range(2):
        client.post(
            "/api/tasks",
            json={"title": f"User 2 Task {i}"},
            headers={"Authorization": f"Bearer {user2_token}"}
        )

    # User 1 lists tasks
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    assert response.status_code == 200
    tasks = response.json()["items"]
    assert len(tasks) == 3
    assert all("User 1 Task" in t["title"] for t in tasks)

    # User 2 lists tasks
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {user2_token}"}
    )

    tasks = response.json()["items"]
    assert len(tasks) == 2
    assert all("User 2 Task" in t["title"] for t in tasks)

def test_cannot_transfer_task_ownership():
    """Test user cannot change task owner."""
    # User 1 creates task
    user1_response = client.post("/api/auth/signup", json={
        "email": "user1@example.com",
        "password": "Pass123"
    })
    user1_token = user1_response.json()["access_token"]
    user1_id = user1_response.json()["user_id"]

    task_response = client.post(
        "/api/tasks",
        json={"title": "Transferable Task"},
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    task_id = task_response.json()["id"]

    # User 2
    user2_response = client.post("/api/auth/signup", json={
        "email": "user2@example.com",
        "password": "Pass123"
    })
    user2_token = user2_response.json()["access_token"]
    user2_id = user2_response.json()["user_id"]

    # User 1 tries to transfer ownership to user 2
    response = client.patch(
        f"/api/tasks/{task_id}",
        json={"user_id": user2_id},
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    assert response.status_code == 400
    assert "ownership" in response.json()["detail"]

    # Verify ownership unchanged
    verify_response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert verify_response.json()["user_id"] == user1_id
```

## Acceptance Criteria
- [ ] User ID extracted from JWT token (never from request)
- [ ] All queries filter by user_id from token
- [ ] Cannot view other users' tasks (403 Forbidden)
- [ ] Cannot edit other users' tasks (403 Forbidden)
- [ ] Cannot delete other users' tasks (403 Forbidden)
- [ ] Cannot transfer task ownership (400 Bad Request)
- [ ] List endpoint only returns current user's tasks
- [ ] Task creation sets user_id from token
- [ ] User existence verified before granting access
- [ ] Cross-user access attempts logged
- [ ] 403 returned instead of 404 (no information leakage)
- [ ] Batch operations respect user_id filter
- [ ] Frontend validates response user_id matches token
- [ ] Frontend redirects on security violation
- [ ] All security tests passing

## Dependencies
- **pytest**: Backend testing
- **FastAPI**: Dependency injection
- **SQLAlchemy**: Query filtering
- **JWT/python-jose**: Token extraction
- **@testing-library/react**: Frontend testing
- **jest**: JavaScript testing

## Related Skills
- `auth_flow` – End-to-end auth scenario testing
- `jwt_middleware` – Token verification
- `task_crud` – Endpoints with security
- `api_client` – Frontend security validation
