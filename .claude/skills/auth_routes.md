---
name: auth-routes
description: Implement signup/signin endpoints with token generation and user isolation. Use when building authentication REST API routes.
---

# Auth Routes Skill - Signup/Signin Endpoints

## Instructions

Implement FastAPI endpoints for user registration and authentication with JWT token generation and user-scoped task access.

### 1. **Signup Endpoint** (`POST /api/auth/signup`)
   - Accept email and password in request body
   - Validate email format and password strength (min 8 chars, mixed case, numbers)
   - Hash password using bcrypt or argon2
   - Create user in database with unique email constraint
   - Generate JWT token on successful signup
   - Return token and user info (id, email)
   - Handle duplicate email: 409 Conflict

### 2. **Signin Endpoint** (`POST /api/auth/signin`)
   - Accept email and password
   - Query user by email
   - Verify password hash
   - Generate new JWT token on success
   - Return token and user info
   - Handle invalid credentials: 401 Unauthorized (generic message)
   - Rate limit to prevent brute force (max 5 attempts per 15 minutes)

### 3. **Token Management**
   - Generate JWT with `sub` (user_id) claim
   - Include `email` in token payload
   - Set `exp` (expiration) claim correctly
   - Implement token refresh endpoint: `POST /api/auth/refresh`
   - Refresh tokens valid for extended period (30 days)
   - Access tokens valid for shorter period (7 days)

### 4. **User Isolation**
   - Extract user_id from JWT `sub` claim in protected routes
   - Validate user_id matches resource ownership
   - All task endpoints require valid JWT token
   - Implement middleware: `verify_token()` decorator
   - Return 401 for missing/invalid tokens
   - Return 403 for unauthorized access (wrong user)

### 5. **Protected Endpoint Pattern**
   - Require Authorization header: `Bearer <token>`
   - Extract and validate token
   - Inject user_id into endpoint handler
   - Filter all queries by user_id
   - No cross-user data leakage

## Example Implementation

### Request/Response Models
```python
from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    email: EmailStr
    password: str  # min 8 chars

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    email: str
    token_type: str = "bearer"

class TokenRefreshRequest(BaseModel):
    refresh_token: str
```

### Signup Endpoint
```python
from fastapi import HTTPException, status

@app.post("/api/auth/signup", response_model=AuthResponse)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Hash password and create user
    hashed_pwd = hash_password(request.password)
    user = User(email=request.email, password_hash=hashed_pwd)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate tokens
    access_token = create_jwt_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=str(user.id),
        email=user.email
    )
```

### Signin Endpoint
```python
@app.post("/api/auth/signin", response_model=AuthResponse)
async def signin(request: SigninRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_jwt_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=str(user.id),
        email=user.email
    )
```

### Token Verification Middleware
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthenticationCredentials

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthenticationCredentials = Depends(security)) -> str:
    try:
        payload = jwt.decode(
            credentials.credentials,
            os.getenv("BETTER_AUTH_SECRET"),
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/api/tasks")
async def list_tasks(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks
```

## Acceptance Criteria
- [ ] Signup endpoint creates user and returns valid JWT
- [ ] Signin endpoint authenticates user and returns JWT
- [ ] Email validation prevents invalid formats
- [ ] Password hashing implemented securely
- [ ] Duplicate email rejected (409 Conflict)
- [ ] Invalid credentials return 401 (no user enumeration)
- [ ] Token refresh endpoint works correctly
- [ ] Protected endpoints require valid JWT
- [ ] User isolation enforced (no cross-user access)
- [ ] All endpoints tested with pytest
- [ ] Rate limiting implemented for signin

## Dependencies
- **FastAPI**: Web framework
- **SQLModel**: ORM for user persistence
- **python-jose**: JWT token creation/verification
- **passlib**: Password hashing
- **pydantic**: Request/response validation
- **Better Auth**: Authentication SDK

## Related Skills
- `auth_setup` – Configure Better Auth and secrets
- `generate_crud_operation` – Create task CRUD endpoints
- `create_task_breakdown` – Plan auth feature tasks
