---
name: schema-design
description: Design SQLModel data models (Task, User) with proper relationships and constraints. Use when defining database schema for Phase 2+ applications.
---

# Schema Design Skill - SQLModel Models & Relationships

## Instructions

Design efficient, maintainable SQLModel ORM models with proper relationships, constraints, and type safety for todo application.

### 1. **User Model Definition**
   - UUID primary key with auto-generation
   - Unique email constraint
   - Password hash field (never store plain text)
   - Timestamps: created_at, updated_at
   - Optional fields: name, avatar_url, theme_preference
   - One-to-Many relationship with Task
   - SQLAlchemy indexes on email for fast lookups
   - Proper datetime handling with timezone awareness

### 2. **Task Model Definition**
   - UUID primary key with auto-generation
   - Foreign key to User (user_id)
   - Title (required, 1-255 chars)
   - Description (optional)
   - Status enum: pending, completed, overdue
   - Priority enum: low, medium, high
   - Due date (optional, with timezone)
   - Timestamps: created_at, updated_at
   - Optional fields: tags, completion_date, estimated_hours
   - Cascade delete relationship (deleting user deletes tasks)

### 3. **Relationship Configuration**
   - User has many Tasks (one-to-many)
   - Task belongs to User (many-to-one)
   - Cascade delete: delete user → delete all user's tasks
   - Lazy loading strategy optimized for queries
   - Proper foreign key constraint enforcement
   - Back-references for bidirectional access

### 4. **Data Validation & Constraints**
   - Email validation (format + uniqueness)
   - Password hash minimum length (60 chars for bcrypt)
   - Title non-empty and length bounds
   - Due date must be future or present (validation in model)
   - Status and priority limited to enum values
   - Hours estimated as positive integers
   - Soft deletes optional for audit trail

### 5. **Indexing & Performance**
   - Primary key indexes (automatic)
   - Unique index on User.email
   - Composite index on (user_id, status) for filtering
   - Composite index on (user_id, due_date) for sorting
   - No over-indexing to maintain write performance

## Example Implementation

### User Model
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid

class User(SQLModel, table=True):
    """User account for todo application."""
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(min_length=60)  # bcrypt hash
    name: Optional[str] = Field(default=None, max_length=255)
    avatar_url: Optional[str] = Field(default=None, max_length=500)
    theme_preference: str = Field(default="light", max_length=10)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email})"
```

### Task Model
```python
from enum import Enum
from typing import Optional, List

class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    OVERDUE = "overdue"

class TaskPriority(str, Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(SQLModel, table=True):
    """Task item linked to user."""
    __tablename__ = "tasks"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255, min_length=1)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.PENDING, index=True)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = Field(default=None, index=True)
    completion_date: Optional[datetime] = Field(default=None)
    estimated_hours: Optional[int] = Field(default=None, ge=0)
    tags: Optional[str] = Field(default=None, max_length=500)  # comma-separated
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional[User] = Relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self.title}, status={self.status})"
```

### Composite Index Definition
```python
from sqlalchemy import Index

# Add to SQLModel table configuration
__table_args__ = (
    Index('idx_user_status', 'user_id', 'status'),
    Index('idx_user_due_date', 'user_id', 'due_date'),
)
```

### Model Creation in Task Model
```python
class Task(SQLModel, table=True):
    """Task item linked to user."""
    __tablename__ = "tasks"
    __table_args__ = (
        Index('idx_user_status', 'user_id', 'status'),
        Index('idx_user_due_date', 'user_id', 'due_date'),
    )
    # ... fields ...
```

## Acceptance Criteria
- [ ] User model with UUID, email (unique), password_hash, timestamps
- [ ] Task model with UUID, user_id (FK), title, status, priority, due_date
- [ ] Status and priority enums properly defined
- [ ] One-to-many relationship (User → Tasks)
- [ ] Cascade delete configured
- [ ] Indexes on email, (user_id, status), (user_id, due_date)
- [ ] Timezone-aware datetime handling
- [ ] Type hints on all fields
- [ ] Docstrings on all models
- [ ] Field constraints (length, nullability, format)
- [ ] Schema migration script generated
- [ ] Models tested in isolation

## Dependencies
- **SQLModel**: ORM and validation
- **SQLAlchemy**: Database abstraction layer
- **pydantic**: Data validation
- **psycopg2-binary**: PostgreSQL driver (for Neon)
- **uuid**: Built-in Python for ID generation
- **datetime**: Built-in Python for timestamps

## Related Skills
- `db_connection` – Initialize Neon PostgreSQL connection
- `auth_setup` – Extend User model for auth fields
- `generate_crud_operation` – Create Task CRUD endpoints
