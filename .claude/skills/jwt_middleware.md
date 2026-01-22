---
name: jwt-middleware
description: Implement JWT token verification middleware with user isolation and token extraction. Use when securing FastAPI endpoints with authentication.
---

# JWT Middleware Skill - Token Verification & User Isolation

## Instructions

Implement JWT verification middleware and dependency injection for FastAPI to enforce authentication and user isolation across all protected endpoints.

### 1. **Token Extraction**
   - Extract token from Authorization header
   - Expected format: `Authorization: Bearer <token>`
   - Handle missing Authorization header (401 Unauthorized)
   - Handle missing or malformed Bearer token (401 Unauthorized)
   - Support token from cookies as fallback (optional)
   - Trim whitespace from token

### 2. **JWT Verification**
   - Use `BETTER_AUTH_SECRET` for signature verification
   - Use HS256 algorithm for decoding
   - Verify token signature validity
   - Check token expiration (exp claim)
   - Extract user_id from `sub` claim
   - Extract email from `email` claim
   - Validate required claims present
   - Handle expired token: 401 Unauthorized with "Token expired"
   - Handle invalid signature: 401 Unauthorized with "Invalid token"

### 3. **User Isolation Enforcement**
   - Extract user_id from token
   - Inject user_id as dependency for protected endpoints
   - Validate user_id matches resource ownership
   - Return 403 Forbidden for cross-user access attempts
   - Query database to verify user still exists
   - Check user account not deleted/disabled

### 4. **Error Handling & Messages**
   - Missing token: 401 "Authentication required"
   - Expired token: 401 "Token expired"
   - Invalid signature: 401 "Invalid token"
   - Malformed header: 401 "Invalid Authorization header"
   - Invalid claims: 401 "Invalid token claims"
   - Generic 401 for security (no user enumeration)

### 5. **Optional Middleware Features**
   - Rate limiting by user_id
   - Token refresh on expiry (optional)
   - Logging of authentication failures
   - Metrics collection (auth attempts, failures)
   - Request context with user_id
   - Correlation IDs for tracing

## Example Implementation

### JWT Utilities (jwt_utils.py)
```python
import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")

if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable not set")

def create_jwt_token(
    user_id: str,
    email: str,
    expires_in_hours: int = 168
) -> str:
    """Create JWT token with user claims."""
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=expires_in_hours),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        raise ValueError("Token expired")
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {str(e)}")
        raise ValueError("Invalid token")

def create_refresh_token(
    user_id: str,
    expires_in_days: int = 30
) -> str:
    """Create refresh token with longer expiry."""
    payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=expires_in_days),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
```

### Dependency Injection (auth_dependencies.py)
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthenticationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User
from jwt_utils import verify_jwt_token
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer(
    scheme_name="Bearer",
    description="JWT token in Authorization header"
)

async def get_current_user(
    credentials: HTTPAuthenticationCredentials = Depends(security)
) -> str:
    """Extract and verify JWT token, return user_id."""
    token = credentials.credentials

    try:
        payload = verify_jwt_token(token)
    except ValueError as e:
        logger.warning(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id: Optional[str] = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user_id

async def get_current_user_with_db(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from database, verify user exists."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user

async def verify_user_ownership(
    resource_user_id: str,
    current_user_id: str = Depends(get_current_user)
) -> str:
    """Verify current user owns the resource."""
    if resource_user_id != current_user_id:
        logger.warning(
            f"Unauthorized access attempt: user {current_user_id} "
            f"accessing resource owned by {resource_user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    return current_user_id
```

### FastAPI Integration (main.py)
```python
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from auth_dependencies import get_current_user, get_current_user_with_db
from models import Task
from sqlalchemy.orm import Session
from database import get_db

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="Task management API with JWT authentication"
)

# Protected endpoint example
@app.get("/api/tasks")
async def list_tasks(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all tasks for authenticated user."""
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks

# Endpoint with full user verification
@app.get("/api/profile")
async def get_profile(
    current_user = Depends(get_current_user_with_db)
):
    """Get current user profile."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name
    }
```

### Middleware Option (Global Token Logging)
```python
from fastapi import Request
from fastapi.middleware.base import BaseHTTPMiddleware
from time import time
import logging

logger = logging.getLogger(__name__)

class AuthLoggingMiddleware(BaseHTTPMiddleware):
    """Log authentication attempts and failures."""

    async def dispatch(self, request: Request, call_next):
        start_time = time()

        # Extract token for logging
        auth_header = request.headers.get("authorization", "")
        has_token = bool(auth_header.startswith("Bearer "))

        response = await call_next(request)

        process_time = time() - start_time

        logger.info(
            f"Path: {request.url.path} | "
            f"Method: {request.method} | "
            f"Status: {response.status_code} | "
            f"Auth: {has_token} | "
            f"Duration: {process_time:.3f}s"
        )

        return response

app.add_middleware(AuthLoggingMiddleware)
```

### Rate Limiting by User
```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.util import get_remote_address
import redis.asyncio as redis

# Initialize rate limiter (in startup)
redis_client = await redis.from_url("redis://localhost")
await FastAPILimiter.init(redis_client)

@app.post("/api/auth/signin")
@limiter.limit("5/15 minutes")  # 5 attempts per 15 minutes per user
async def signin(request: Request, credentials: SigninRequest):
    """Signin with rate limiting."""
    # ... signin logic ...
```

### Test Example
```python
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_protected_endpoint_without_token():
    """Test 401 when no token provided."""
    response = client.get("/api/tasks")
    assert response.status_code == 401

def test_protected_endpoint_with_valid_token():
    """Test 200 with valid token."""
    token = create_jwt_token("test-user-id", "test@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/tasks", headers=headers)
    assert response.status_code == 200

def test_protected_endpoint_with_expired_token():
    """Test 401 with expired token."""
    # Create token with 0 hour expiry
    payload = {"sub": "test-user", "email": "test@example.com", "exp": datetime.utcnow()}
    expired_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/api/tasks", headers=headers)
    assert response.status_code == 401
```

## Acceptance Criteria
- [ ] HTTPBearer dependency extracts token from Authorization header
- [ ] JWT token verified with HS256 algorithm
- [ ] Signature validation using BETTER_AUTH_SECRET
- [ ] Token expiration checked (exp claim)
- [ ] User ID extracted from sub claim
- [ ] 401 returned for missing token
- [ ] 401 returned for expired token
- [ ] 401 returned for invalid signature
- [ ] 403 returned for cross-user access
- [ ] User isolation enforced on all protected endpoints
- [ ] get_current_user dependency working
- [ ] get_current_user_with_db dependency working
- [ ] Authentication errors logged
- [ ] All tests passing (valid/expired/invalid tokens)

## Dependencies
- **FastAPI**: Web framework
- **python-jose**: JWT token verification
- **pydantic**: Request/response models
- **SQLAlchemy**: User database lookups
- **fastapi-limiter**: Rate limiting (optional)
- **redis**: For rate limiting backend (optional)

## Related Skills
- `task_crud` – Protected endpoints using this middleware
- `auth_routes` – Token generation (pairs with verification)
- `error_handling` – Exception handling for auth errors
