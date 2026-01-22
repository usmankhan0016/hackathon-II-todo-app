---
name: auth-setup
description: Configure Better Auth with JWT plugin and shared secret for Phase 2+ authentication. Use when setting up authentication infrastructure.
---

# Auth Setup Skill - Better Auth Configuration

## Instructions

Configure Better Auth as the authentication provider with JWT token support and shared secret management across frontend and backend.

### 1. **Better Auth Installation & Configuration**
   - Install Better Auth package in backend (FastAPI)
   - Configure JWT plugin with HS256 algorithm
   - Set up shared `BETTER_AUTH_SECRET` environment variable
   - Initialize auth instance with database adapter

### 2. **JWT Plugin Setup**
   - Enable JWT token generation on login
   - Set token expiration (recommended: 7 days for access, 30 days for refresh)
   - Configure token signing with `BETTER_AUTH_SECRET`
   - Include user ID and email in JWT claims
   - Implement token refresh mechanism

### 3. **Shared Secret Management**
   - Define `BETTER_AUTH_SECRET` in `.env` (backend)
   - Mirror `BETTER_AUTH_SECRET` in frontend environment
   - Ensure 32+ character cryptographically secure random string
   - Document secret rotation procedure
   - Never commit secrets to version control

### 4. **Database Adapter Configuration**
   - SQLModel ORM for database access
   - Neon PostgreSQL connection pooling
   - User table with: id, email, password_hash, created_at, updated_at
   - Session tracking for token management
   - Proper indexing on email and user_id

### 5. **Error Handling**
   - Invalid secret: 500 Server Error
   - Database connection failure: 503 Service Unavailable
   - Token generation failure: 500 Server Error with logging

## Example Configuration

### Backend Setup (.env)
```env
DATABASE_URL=postgresql://user:password@neon-endpoint/dbname
BETTER_AUTH_SECRET=your-32-character-cryptographically-secure-random-string
JWT_ALGORITHM=HS256
TOKEN_EXPIRY_HOURS=168
REFRESH_TOKEN_EXPIRY_DAYS=30
```

### Better Auth Instance (Python/FastAPI)
```python
from better_auth import BetterAuth, JWTPlugin
from sqlmodel import SQLModel, create_engine, Session

auth = BetterAuth(
    database_url=os.getenv("DATABASE_URL"),
    secret=os.getenv("BETTER_AUTH_SECRET"),
    plugins=[
        JWTPlugin(
            algorithm="HS256",
            expiry_hours=int(os.getenv("TOKEN_EXPIRY_HOURS", "168")),
            refresh_expiry_days=int(os.getenv("REFRESH_TOKEN_EXPIRY_DAYS", "30"))
        )
    ]
)
```

### Frontend Environment (.env.local)
```env
NEXT_PUBLIC_BETTER_AUTH_SECRET=same-secret-as-backend
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Acceptance Criteria
- [ ] Better Auth package installed and configured
- [ ] JWT plugin enabled with HS256 algorithm
- [ ] Shared secret defined in both backend and frontend
- [ ] Database adapter properly configured
- [ ] Token generation working (verified via tests)
- [ ] Token validation on protected endpoints
- [ ] Environment variables properly isolated (never in code)
- [ ] Error handling for auth failures

## Dependencies
- **Phase 2+**: FastAPI backend, Neon PostgreSQL, Better Auth SDK
- **Frontend**: Next.js environment variables configured
- **Database**: User table schema created with auth fields

## Related Skills
- `auth_routes` – Implement signup/signin endpoints
- `create_task_breakdown` – Break down auth feature
- `generate_crud_operation` – Create user CRUD operations
