---
name: db-connection
description: Initialize Neon PostgreSQL connection pool and session management for FastAPI. Use when setting up database layer for Phase 2+ applications.
---

# DB Connection Skill - Neon PostgreSQL Setup

## Instructions

Configure persistent, pooled Neon PostgreSQL connections with proper session management, connection pooling, and error handling for FastAPI backend.

### 1. **Neon PostgreSQL Connection Setup**
   - Parse DATABASE_URL environment variable
   - Use psycopg2 or psycopg3 async driver
   - Connection pooling (min 5, max 20 connections)
   - Timeout handling (connect timeout 10s, query timeout 30s)
   - SSL/TLS verification for Neon (sslmode=require)
   - Automatic connection retry logic
   - Connection health checks

### 2. **SQLModel & SQLAlchemy Integration**
   - Create SQLAlchemy engine with Neon dialect
   - Configure connection pool class (QueuePool)
   - Set pool recycle to 3600s (1 hour)
   - Enable echo logging in development only
   - Proper engine disposal on shutdown
   - Connection pool monitoring

### 3. **Session Management**
   - SessionLocal factory for dependency injection
   - Session context manager for transactions
   - Automatic rollback on exceptions
   - Proper session cleanup
   - Scoped sessions for thread-safety
   - FastAPI Depends integration

### 4. **Database Initialization**
   - Create all tables on application startup
   - Schema validation on boot
   - Migration strategy (Alembic integration)
   - Seed default data if needed
   - Health check endpoint (`/health/db`)

### 5. **Error Handling & Resilience**
   - Connection failures: retry with exponential backoff
   - Timeout errors: graceful degradation
   - Connection pool exhaustion: queue timeout
   - Network errors: circuit breaker pattern
   - Database unavailable: 503 Service Unavailable
   - Transaction rollback on errors

## Example Implementation

### Environment Configuration (.env)
```env
DATABASE_URL=postgresql://user:password@ep-xyz123.us-east-1.aws.neon.tech/dbname
DB_POOL_MIN=5
DB_POOL_MAX=20
DB_POOL_RECYCLE=3600
DB_CONNECT_TIMEOUT=10
DB_QUERY_TIMEOUT=30
```

### Database Module (database.py)
```python
import os
from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

# Parse connection parameters
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Ensure SSL for Neon
if "neon.tech" in DATABASE_URL and "sslmode" not in DATABASE_URL:
    DATABASE_URL = f"{DATABASE_URL}?sslmode=require"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=pool.QueuePool,
    pool_size=int(os.getenv("DB_POOL_MIN", "5")),
    max_overflow=int(os.getenv("DB_POOL_MAX", "20")),
    pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "3600")),
    connect_args={
        "timeout": int(os.getenv("DB_CONNECT_TIMEOUT", "10")),
    },
    echo=os.getenv("DEBUG") == "true",  # Log SQL in development
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@contextmanager
def get_session() -> Session:
    """Context manager for database sessions with automatic cleanup."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        session.close()

def get_db() -> Session:
    """Dependency injection for FastAPI endpoints."""
    db = SessionLocal()
    try:
        yield db
    except OperationalError as e:
        logger.error(f"Database connection error: {str(e)}")
        raise
    finally:
        db.close()
```

### FastAPI Integration (main.py)
```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from database import engine, get_db, SessionLocal
from models import SQLModel

# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    yield
    # Shutdown
    logger.info("Closing database connections...")
    engine.dispose()
    logger.info("Database connections closed")

app = FastAPI(lifespan=lifespan)

@app.get("/health/db")
async def health_check_db(db: Session = Depends(get_db)):
    """Health check endpoint for database connectivity."""
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}, 503
```

### Connection Pool Monitoring
```python
from sqlalchemy.pool import QueuePool

def get_pool_stats() -> dict:
    """Get current connection pool statistics."""
    pool_obj = engine.pool
    if isinstance(pool_obj, QueuePool):
        return {
            "checked_out": pool_obj.checkedout(),
            "size": pool_obj.size(),
            "checked_in": pool_obj.size() - pool_obj.checkedout(),
            "queue_size": pool_obj.queue.qsize(),
        }
    return {}

@app.get("/admin/db/pool-stats")
async def pool_stats():
    """Monitor connection pool statistics (admin only)."""
    return get_pool_stats()
```

### Migration Setup with Alembic
```python
# Initialize Alembic (one-time)
# alembic init migrations

# In alembic/env.py
from models import SQLModel
target_metadata = SQLModel.metadata

# Generate migration after schema changes
# alembic revision --autogenerate -m "Add users and tasks tables"

# Apply migrations on startup
# alembic upgrade head
```

### Error Handling & Retry Logic
```python
from sqlalchemy.exc import OperationalError
import time
from functools import wraps

def retry_on_db_error(max_retries=3, backoff_factor=2):
    """Decorator for retrying database operations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except OperationalError as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = backoff_factor ** attempt
                    logger.warning(f"DB error, retrying in {wait_time}s: {str(e)}")
                    time.sleep(wait_time)
        return wrapper
    return decorator
```

## Acceptance Criteria
- [ ] DATABASE_URL properly configured from environment
- [ ] SSL/TLS enabled for Neon connection
- [ ] Connection pool configured (min 5, max 20, recycle 3600s)
- [ ] SessionLocal factory created for dependency injection
- [ ] get_db() dependency working in FastAPI endpoints
- [ ] All tables created on application startup
- [ ] Health check endpoint (`/health/db`) returning correct status
- [ ] Connection errors handled gracefully
- [ ] Transaction rollback on exceptions
- [ ] Connection pool stats available (admin endpoint)
- [ ] Alembic migrations configured
- [ ] Database operations tested with pytest
- [ ] Connection timeouts configured (10s connect, 30s query)

## Dependencies
- **SQLAlchemy**: Database abstraction layer
- **psycopg2-binary** or **psycopg**: PostgreSQL driver
- **SQLModel**: ORM with Pydantic integration
- **alembic**: Database migrations
- **fastapi**: Web framework for dependency injection
- **python-dotenv**: Environment variable loading

## Related Skills
- `schema_design` – Define User and Task models
- `auth_setup` – Extend connection for auth layer
- `generate_crud_operation` – Create endpoints using db sessions
