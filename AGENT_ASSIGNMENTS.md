# Agent Assignment Briefs
**Authentication System Phase 2 Implementation**

**Date**: 2026-01-12
**Status**: Ready for Agent Execution

---

## 🎯 Agent Assignments

### 1. Backend Agent Assignment

**Role**: Core authentication service implementation
**Primary Responsibility**: FastAPI routes, services, JWT utilities, middleware, error handling
**Total Tasks**: 24 tasks (T007-T017, T024-T027, T040-T043, T048, T054-T056, T011-T013)

#### Quick Start
1. **Read Documentation**:
   - `specs/002-user-auth/spec.md` - Feature requirements
   - `specs/002-user-auth/plan.md` - Architecture decisions
   - `specs/002-user-auth/tasks.md` - Detailed task list

2. **Set Up Environment**:
   ```bash
   cd backend
   # Verify Python 3.13+
   python --version
   # Install dependencies
   pip install -e .
   ```

3. **Start with Phase 2** (foundational, blocking for all stories):
   - T011: JWT utilities (create_access_token, create_refresh_token, verify_token, extract_user_id)
   - T012: Authentication middleware (token extraction, verification, user_id injection)
   - T013: Error handlers (8 error codes, generic messages)

#### Phase 2 Tasks (Foundational)
```
T011: JWT Utilities Module
├── Location: backend/src/phase2/auth/jwt.py
├── Functions:
│   ├── create_access_token(user_id: str, expires_delta: timedelta) → str
│   ├── create_refresh_token(user_id: str, expires_delta: timedelta) → str
│   ├── verify_token(token: str) → dict
│   └── extract_user_id(token: str) → str
├── Configuration:
│   ├── Algorithm: HS256
│   ├── Access token expiry: 7 days
│   ├── Refresh token expiry: 30 days
│   └── Secret: BETTER_AUTH_SECRET from config
└── Tests: Unit tests for token generation and verification

T012: Authentication Middleware
├── Location: backend/src/phase2/middleware/auth.py
├── Features:
│   ├── HTTPBearer token extraction
│   ├── JWT verification
│   ├── user_id extraction and context injection
│   └── 401 response for invalid/missing tokens
├── Behavior:
│   ├── Checks Authorization header: "Bearer <token>"
│   ├── Verifies token signature and expiry
│   ├── Injects user_id into request.state.user_id
│   └── Returns 401 if verification fails
└── Integration: Add to FastAPI app with app.add_middleware()

T013: Error Handlers
├── Location: backend/src/phase2/handlers/errors.py
├── Error Codes (8 total):
│   ├── AUTH_INVALID_CREDENTIALS (401)
│   ├── AUTH_EMAIL_EXISTS (409)
│   ├── AUTH_INVALID_EMAIL (422)
│   ├── AUTH_WEAK_PASSWORD (422)
│   ├── AUTH_TOKEN_EXPIRED (401)
│   ├── AUTH_TOKEN_INVALID (401)
│   ├── AUTH_TOKEN_MISSING (401)
│   └── AUTH_FORBIDDEN (403)
├── Response Format:
│   └── {"error": "CODE", "message": "Generic message", "status_code": 401}
└── Usage: All endpoints use these handlers
```

#### Phase 3 Backend Tasks (User Stories)
```
US1 - Signup (T014-T017):
├── T014: POST /api/auth/signup route
│   ├── Request: {email, password, name}
│   ├── Response: {access_token, refresh_token, user}
│   ├── Status codes: 201 (success), 409 (exists), 422 (invalid)
│   └── Validation: email format, password >= 8 chars
├── T015: Signup service business logic
│   ├── Hash password with bcrypt (cost >= 10)
│   ├── Create User record
│   ├── Check for duplicates
│   └── Return standardized response
├── T016: Password constraints enforcement
│   ├── Minimum 8 characters
│   ├── Return 422 if too weak
│   └── Include error code in response
└── T017: JWT token generation on signup
    ├── Create access token (7 days)
    ├── Create refresh token (30 days)
    └── Return both in response

US2 - Signin (T024-T027):
├── T024: POST /api/auth/signin route
│   ├── Request: {email, password}
│   ├── Response: {access_token, refresh_token, user}
│   ├── Status code: 200 (success), 401 (invalid)
│   └── Validation: email format
├── T025: Signin service business logic
│   ├── Look up user by email
│   ├── Verify password with bcrypt
│   ├── Return 401 with generic message if invalid
│   └── Prevent user enumeration (same timing)
├── T026: User lookup and password validation
│   ├── Query: SELECT * FROM users WHERE email = ?
│   ├── Verify: bcrypt.verify(password, password_hash)
│   └── Security: Return generic error (no "email not found")
└── T027: JWT token generation on signin (with rotation)
    ├── Create new access token
    ├── Create new refresh token (rotated)
    └── Return both in response

US3 - Token Storage (T037-T038):
├── T037: Backend cookie configuration
│   ├── Set cookies with flags: HttpOnly, Secure, SameSite=Strict
│   ├── Path: /
│   ├── Domain: localhost (or production domain)
│   └── Expiry: Same as token expiry
└── T038: JWT extraction from Authorization header
    ├── Header format: "Bearer <token>"
    ├── Parse and extract token
    └── Fallback to cookies if header missing

US4 - JWT Verification (T040-T043):
├── T040: Protected test endpoint
│   ├── Route: GET /api/protected/test
│   ├── Requires: Valid JWT middleware
│   ├── Response: {message: "success", user_id: "..."}
│   └── Status: 200 (success), 401 (invalid token)
├── T041: JWT middleware on protected routes
│   ├── Apply middleware to /api/* routes
│   ├── Skip: /api/auth/signup, /api/auth/signin
│   └── Enforce: All other endpoints
├── T042: User isolation enforcement
│   ├── Extract user_id from JWT
│   ├── Filter all queries: WHERE user_id = $1
│   ├── Never use user_id from request
│   └── Return 403 if accessing other user's data
└── T043: 401/403 error responses
    ├── 401: Missing or invalid token
    ├── 401: Token expired
    ├── 403: Cross-user access attempt
    └── Use error handlers from T013
```

#### Phase 4 Backend Tasks
```
US5 - Logout (T048):
├── Optional POST /api/auth/logout endpoint
├── Request: {refresh_token} or just authenticated
├── Response: {message: "logged out"}
├── Status: 204 No Content
└── Note: Frontend clears tokens; backend optional

US6 - Token Refresh (T054-T056):
├── T054: POST /api/auth/refresh endpoint
│   ├── Request: {refresh_token}
│   ├── Response: {access_token, refresh_token}
│   ├── Status: 200 (success), 401 (invalid)
│   └── Return new tokens (both rotated)
├── T055: Refresh token rotation
│   ├── On each refresh, issue new refresh token
│   ├── Old token invalidated (optional)
│   ├── Return new access + new refresh
│   └── Frontend updates both
└── T056: Backend refresh test
    ├── Verify new tokens issued
    ├── Verify old refresh token no longer works
    ├── Check token rotation
    └── Performance: < 200ms
```

#### Development Flow
1. **TDD Approach**: Write tests first, implement after
2. **Database**: Phase 2 Database Agent handles User schema (you use it)
3. **Configuration**: Use settings from `backend/src/phase2/config.py`
4. **Error Handling**: Always use handlers from `backend/src/phase2/handlers/errors.py`
5. **User Isolation**: Always extract user_id from JWT, never from request

#### Code Quality Standards
- Python 3.13+ with type hints on all functions
- PEP 8 compliant
- All functions documented with docstrings
- Pydantic models for validation
- Pytest for unit/integration tests
- Coverage goal: >80%

#### Key Files to Create/Modify
```
backend/src/phase2/
├── auth/
│   ├── jwt.py              (T011)
│   └── routes/auth.py      (T014, T024, T040, T048, T054)
├── services/
│   ├── auth_service.py     (T015, T025, T027, T055)
│   └── user_service.py     (T026)
├── middleware/
│   ├── auth.py             (T012, T038, T042)
│   └── __init__.py
├── handlers/
│   ├── errors.py           (T013, T043)
│   └── __init__.py
├── models/
│   ├── user.py             (T008 - Database Agent creates this)
│   └── __init__.py
├── schemas/
│   ├── auth.py             (T009 - may be partially Database Agent)
│   └── __init__.py
└── main.py                 (updated with routes, middleware)
```

#### Testing Strategy
```bash
# Run backend tests
pytest backend/tests/

# Run with coverage
pytest backend/tests/ --cov=backend/src --cov-report=term-missing

# Run specific test file
pytest backend/tests/test_auth.py -v

# Run with markers
pytest backend/tests/ -m "integration"
```

---

### 2. Frontend Agent Assignment

**Role**: User interface and API client implementation
**Primary Responsibility**: Next.js pages, forms, API client, interceptors, auth context
**Total Tasks**: 20 tasks (T018-T022, T028-T031, T033-T036, T045-T047, T050-T053, T058-T062)

#### Quick Start
1. **Read Documentation**:
   - `specs/002-user-auth/spec.md` - Feature requirements
   - `specs/002-user-auth/plan.md` - Architecture decisions
   - `specs/002-user-auth/tasks.md` - Detailed task list

2. **Set Up Environment**:
   ```bash
   cd frontend
   # Verify Node 18+
   node --version
   npm --version
   # Install dependencies
   npm install
   # Start dev server
   npm run dev
   # Visit http://localhost:3000
   ```

3. **Start with Phase 3** (after backend Phase 2 complete):
   - T018-T022: Signup page and form
   - T028-T031: Signin page and form
   - T033-T036: API client with interceptors

#### Phase 3 Frontend Tasks
```
US1 - Signup (T018-T022):
├── T018: Signup page component
│   ├── Location: frontend/src/app/(auth)/signup/page.tsx
│   ├── Layout: Form with email, password, confirm password fields
│   ├── Styling: Tailwind CSS with responsive design
│   ├── Components: Use SignupForm component
│   └── Accessibility: WCAG AA compliant labels, error text
├── T019: SignupForm component
│   ├── Location: frontend/src/components/auth/SignupForm.tsx
│   ├── Using: Better Auth SDK for form handling
│   ├── Fields:
│   │   ├── Email input (type="email", validation)
│   │   ├── Password input (type="password", minlength=8)
│   │   ├── Confirm password (match validation)
│   │   └── Submit button (loading state)
│   ├── Validation: Client-side with zod/Better Auth
│   └── Error display: Toast notifications
├── T020: Form validation UI feedback
│   ├── Real-time validation: Email format, password strength
│   ├── Error messages: Below each field
│   ├── Success state: Disable submit, show loading
│   └── Styling: Red for errors, green for success
├── T021: Signup form API integration
│   ├── Call: POST /api/auth/signup with {email, password, name}
│   ├── Handle: 201 (success), 409 (exists), 422 (invalid)
│   ├── On success: Store tokens, redirect to /dashboard
│   └── On error: Show error message, keep form data
└── T022: Error handling and toast notifications
    ├── Toast library: (pick sonner, react-toastify, or similar)
    ├── Success toast: "Account created! Redirecting..."
    ├── Error toast: Generic message (e.g., "Email already registered")
    ├── Duration: 5 seconds
    └── Position: Top-right

US2 - Signin (T028-T031):
├── T028: Signin page component
│   ├── Location: frontend/src/app/(auth)/signin/page.tsx
│   ├── Layout: Form with email, password fields
│   ├── Styling: Same as signup (consistent design)
│   └── Components: Use SigninForm component
├── T029: SigninForm component
│   ├── Location: frontend/src/components/auth/SigninForm.tsx
│   ├── Using: Better Auth SDK
│   ├── Fields:
│   │   ├── Email input (type="email")
│   │   ├── Password input (type="password")
│   │   ├── Remember me checkbox (optional)
│   │   └── Submit button
│   ├── Validation: Email format only (server validates password)
│   └── Error display: Toast notifications
├── T030: Signin form API integration
│   ├── Call: POST /api/auth/signin with {email, password}
│   ├── Handle: 200 (success), 401 (invalid)
│   ├── On success: Store tokens, redirect to /dashboard
│   └── On error: Show generic error (never hint if email exists)
└── T031: Error handling and generic messages
    ├── Always show: "Invalid email or password"
    ├── Never show: "Email not registered" (prevents enumeration)
    ├── Show only once per attempt
    └── Clear error on retry

US3 - Token Storage (T033-T036):
├── T033: API client setup with JWT interceptor
│   ├── Location: frontend/src/lib/api/client.ts
│   ├── Library: axios with interceptors
│   ├── Base URL: NEXT_PUBLIC_API_URL from env
│   ├── Default headers: Content-Type: application/json
│   └── Export: axiosInstance for use in other modules
├── T034: Request interceptor (Authorization header)
│   ├── Before each request:
│   │   ├── Get token from cookies
│   │   ├── Add Authorization header: "Bearer <token>"
│   │   └── Skip auth routes (/signup, /signin)
│   ├── Error handling: No-op if token missing (handled by response)
│   └── Refresh logic: Integrated with response interceptor
├── T035: Response interceptor (handle 401, trigger refresh)
│   ├── On 401 Unauthorized:
│   │   ├── Check if refresh token exists
│   │   ├── Call POST /api/auth/refresh
│   │   ├── Update stored tokens
│   │   ├── Retry original request with new token
│   │   └── If refresh fails: redirect to /signin
│   ├── On other errors: Pass through
│   └── Automatic retry: Transparent to calling code
└── T036: Token storage in httpOnly cookies
    ├── Handled by: Better Auth SDK and server cookies
    ├── Frontend responsibility: Don't manually set cookies
    ├── Read tokens: Use Better Auth SDK methods
    └── Verification: Inspect with DevTools (Network → Cookies)

US4 - JWT Verification (implicit):
└── Handled by: Backend middleware + response interceptor
```

#### Phase 4 Frontend Tasks
```
US5 - Logout (T045-T047):
├── T045: Logout button component
│   ├── Location: frontend/src/components/auth/LogoutButton.tsx
│   ├── Placement: Navigation bar or sidebar
│   ├── Appearance: Button with logout icon/text
│   ├── Styling: Consistent with app theme
│   └── Accessibility: Proper button semantics
├── T046: Logout function
│   ├── Location: frontend/src/lib/auth.ts
│   ├── Function: logout() → Promise<void>
│   ├── Actions:
│   │   ├── Clear tokens from cookies (Better Auth)
│   │   ├── Clear auth context/state
│   │   └── Optional: Call POST /api/auth/logout
│   └── Completion: Redirect to /signin
└── T047: Navigation redirect after logout
    ├── Hook: useRouter from next/navigation
    ├── Redirect: Push to /signin
    ├── Preserve: Redirect URL for post-login return (optional)
    └── Timing: Immediately after token clear

US6 - Token Refresh (T050-T053):
├── T050: Proactive token expiry check (< 5 min remaining)
│   ├── Location: frontend/src/lib/hooks/useAuth.ts or useTokenRefresh.ts
│   ├── Logic:
│   │   ├── Get token from cookies
│   │   ├── Decode token (without verification)
│   │   ├── Extract exp claim (expiry timestamp)
│   │   ├── Calculate time remaining: exp - now
│   │   └── Return: isExpiringSoon (< 5 minutes)
│   ├── Usage: In effect hook to trigger refresh
│   └── Frequency: Check on app mount and after each request
├── T051: Refresh token request and retry logic
│   ├── Call: POST /api/auth/refresh with refresh token
│   ├── Handle success:
│   │   ├── Update stored tokens (access + refresh rotated)
│   │   ├── Queue any pending requests
│   │   └── Retry queued requests with new token
│   ├── Handle failure:
│   │   ├── Clear tokens
│   │   ├── Redirect to /signin
│   │   └── Show error toast: "Your session expired"
│   └── Timeout: 5 seconds per refresh attempt
├── T052: Frontend interceptor triggers refresh automatically
│   ├── Integration with T035 (response interceptor)
│   ├── On 401 + refresh_token exists:
│   │   ├── Trigger refresh function from T051
│   │   ├── Wait for new tokens
│   │   ├── Retry original request
│   │   └── Return updated response
│   ├── On 401 + no refresh_token:
│   │   ├── Clear auth state
│   │   └── Redirect to /signin
│   └── No user-visible pause (seamless experience)
└── T053: Token rotation (new tokens on refresh)
    ├── Handled by: Backend (T055)
    ├── Frontend responsibility:
    │   ├── Receive both new_access_token and new_refresh_token
    │   ├── Update both in cookies
    │   ├── Don't reuse old refresh token
    │   └── Verify tokens different from previous
```

#### Phase 5 Frontend Tasks (E2E Tests with Playwright)
```
T062: Playwright E2E test
├── Location: frontend/tests/e2e/auth-flow.spec.ts
├── Scenarios:
│   ├── Scenario 1: Complete signup flow
│   │   ├── Navigate to /signup
│   │   ├── Fill email, password, confirm password
│   │   ├── Submit form
│   │   ├── Verify redirect to /dashboard
│   │   └── Verify dashboard content visible
│   ├── Scenario 2: Signin with existing account
│   │   ├── Navigate to /signin
│   │   ├── Fill email, password
│   │   ├── Submit form
│   │   ├── Verify redirect to /dashboard
│   │   └── Verify user greeting appears
│   ├── Scenario 3: Logout
│   │   ├── Click logout button
│   │   ├── Verify redirect to /signin
│   │   ├── Verify cannot access /dashboard (protected)
│   │   └── Verify must signin again
│   └── Scenario 4: Token refresh
│       ├── Signin to get tokens
│       ├── Make API request (triggers refresh if needed)
│       ├── Verify request succeeds
│       └── Verify no interruption to user
├── Performance:
│   ├── Measure signup time (< 2 seconds)
│   ├── Measure signin time (< 2 seconds)
│   └── Report in test output
└── Cleanup:
    ├── Delete test user after tests
    ├── Clear cookies
    └── Reset app state
```

#### Development Flow
1. **TDD Approach**: Write component tests first, build components after
2. **API Communication**: Backend must be running for integration
3. **Token Management**: Better Auth SDK handles most of it; implement interceptors
4. **User Experience**: Prevent loading states and provide feedback
5. **Accessibility**: All forms WCAG AA compliant

#### Code Quality Standards
- TypeScript strict mode, no any
- React 18+ with hooks
- Type safety on all components and hooks
- Prettier formatting (npm run format)
- ESLint compliance (npm run lint)
- Jest/Vitest for component tests

#### Key Files to Create/Modify
```
frontend/src/
├── app/
│   ├── (auth)/
│   │   ├── signup/
│   │   │   └── page.tsx           (T018)
│   │   └── signin/
│   │       └── page.tsx           (T028)
│   ├── (dashboard)/
│   │   └── page.tsx               (protected, redirect logic)
│   ├── layout.tsx                 (root layout, providers)
│   └── globals.css                (Tailwind)
├── components/
│   ├── auth/
│   │   ├── SignupForm.tsx         (T019)
│   │   ├── SigninForm.tsx         (T029)
│   │   └── LogoutButton.tsx       (T045)
│   └── ui/
│       ├── Button.tsx
│       ├── Input.tsx
│       └── Toast.tsx
├── lib/
│   ├── auth.ts                    (T046, auth context)
│   ├── api/
│   │   └── client.ts              (T033, interceptors)
│   └── hooks/
│       ├── useAuth.ts             (auth state)
│       └── useTokenRefresh.ts     (T050-T052, refresh logic)
├── types/
│   └── auth.ts                    (TypeScript types)
└── env.ts                         (environment validation)

frontend/tests/
├── components/
│   ├── SignupForm.test.tsx
│   └── SigninForm.test.tsx
└── e2e/
    └── auth-flow.spec.ts          (T062)
```

#### Testing Strategy
```bash
# Run frontend tests
npm test

# Run with coverage
npm test -- --coverage

# Run E2E tests
npm run e2e

# Run E2E with UI
npm run e2e:headed

# Type checking
npm run type-check

# Linting
npm run lint

# Formatting
npm run format
```

---

### 3. Database Agent Assignment

**Role**: Data persistence and schema management
**Primary Responsibility**: User model, database connection, schema initialization
**Total Tasks**: 4 tasks (T007-T010)

#### Quick Start
1. **Read Documentation**:
   - `specs/002-user-auth/plan.md` - Database schema design
   - `specs/002-user-auth/tasks.md` - Database tasks
   - Backend project structure

2. **Environment Setup**:
   ```bash
   # Verify PostgreSQL is running locally or use Neon
   # Set DATABASE_URL in backend/.env
   DATABASE_URL=postgresql://user:password@localhost:5432/todo_app_dev
   ```

#### Phase 2 Database Tasks
```
T007: Database connection module
├── Location: backend/src/phase2/database.py
├── Features:
│   ├── SQLModel session factory
│   ├── Connection pooling: min 5, max 20
│   ├── SSL configuration (for Neon PostgreSQL)
│   ├── Health check function
│   └── Database initialization
├── Implementation:
│   ├── Use SQLAlchemy engine with asyncpg
│   ├── Create session maker with Session class
│   ├── Export: engine, SessionLocal, get_db (dependency)
│   └── Add health_check() function to verify connection
└── Error handling:
    ├── Graceful failure if DB unavailable
    ├── Retry logic with exponential backoff
    └── Logging of connection issues

T008: User SQLModel
├── Location: backend/src/phase2/models/user.py
├── Fields:
│   ├── id: UUID, primary key, auto-generated
│   ├── email: str, unique, indexed, not null
│   ├── password_hash: str, not null (bcrypt)
│   ├── name: str, optional
│   ├── created_at: datetime, default=now()
│   ├── updated_at: datetime, default=now(), onupdate=now()
│   └── is_active: bool, default=True (optional)
├── Indexes:
│   ├── idx_users_email (email)
│   ├── idx_users_created_at (created_at)
│   └── idx_users_is_active (is_active) - optional
├── Constraints:
│   ├── UNIQUE(email)
│   ├── NOT NULL(email, password_hash)
│   └── CHECK(email ~ pattern) - email validation
├── Utilities:
│   ├── hash_password(password: str) → str (bcrypt, cost >= 10)
│   ├── verify_password(password: str, hash: str) → bool
│   └── Both use passlib.context
└── Methods:
    ├── __repr__() for debugging
    └── to_dict() for serialization (exclude password_hash)

T009: Pydantic schemas
├── Location: backend/src/phase2/schemas/auth.py
├── Schemas:
│   ├── SignupRequest
│   │   ├── email: str (EmailStr)
│   │   ├── password: str (min_length=8)
│   │   └── name: str (optional)
│   ├── SigninRequest
│   │   ├── email: str (EmailStr)
│   │   └── password: str
│   ├── RefreshRequest
│   │   └── refresh_token: str
│   ├── TokenResponse
│   │   ├── access_token: str
│   │   ├── refresh_token: str
│   │   ├── token_type: str = "bearer"
│   │   └── expires_in: int (in seconds)
│   ├── UserResponse
│   │   ├── id: str (UUID)
│   │   ├── email: str
│   │   ├── name: str
│   │   └── created_at: datetime
│   └── ErrorResponse
│       ├── error: str (error code)
│       ├── message: str (user-facing)
│       └── status_code: int
├── Validation:
│   ├── Email format validation
│   ├── Password length enforcement (>= 8)
│   └── All fields required unless Optional
└── Example:
    ```python
    class SignupRequest(BaseModel):
        email: EmailStr
        password: str = Field(..., min_length=8)
        name: Optional[str] = None
    ```

T010: Database table initialization on startup
├── Location: backend/src/phase2/main.py (startup event)
├── Steps:
│   ├── On app startup:
│   │   ├── Call SQLModel.metadata.create_all(engine)
│   │   ├── Log: "Database tables created/verified"
│   │   └── Continue startup
│   ├── Verify User table:
│   │   ├── Columns present and correct type
│   │   ├── Indexes created
│   │   └── Constraints applied
│   └── Error handling:
│       ├── If migration fails: Log error, raise exception
│       └── If migration succeeds: Continue normally
├── Implementation:
│   ├── Use lifespan context manager (from main.py)
│   ├── Call create_all during startup
│   ├── Verify with simple query: SELECT COUNT(*) FROM users
│   └── Handle exceptions appropriately
└── Testing:
    ├── Verify User table exists
    ├── Verify columns and types
    ├── Verify indexes created
    └── Verify can insert/query data
```

#### Development Approach
1. **Database-First**: Create models before services
2. **Migrations**: Simple for MVP (create_all), upgrade to Alembic later
3. **Testing**: Use test database (separate from dev)
4. **Indexes**: Create on frequently queried columns (email, created_at)

#### Key Files
```
backend/src/phase2/
├── database.py              (T007)
├── models/
│   ├── user.py             (T008)
│   └── __init__.py
└── schemas/
    ├── auth.py             (T009)
    └── __init__.py

backend/
├── pyproject.toml          (dependencies updated in T002)
└── .env                    (DATABASE_URL configured in T003)
```

#### Testing Strategy
```python
# Verify database connection
def test_database_connection():
    assert engine is not None
    with Session(engine) as session:
        session.exec(text("SELECT 1"))

# Verify User model
def test_user_model_creation():
    user = User(email="test@example.com", password_hash="hash")
    session.add(user)
    session.commit()
    assert user.id is not None

# Verify password hashing
def test_password_hashing():
    hashed = hash_password("password123")
    assert verify_password("password123", hashed)
    assert not verify_password("wrong", hashed)
```

---

### 4. Integration Agent Assignment

**Role**: Testing and system integration validation
**Primary Responsibility**: Integration tests, E2E tests, security tests, performance validation
**Total Tasks**: 10 tasks (T023, T032, T039, T044, T049, T056-T062)

#### Quick Start
1. **Read Documentation**:
   - `specs/002-user-auth/spec.md` - Success criteria and constraints
   - `specs/002-user-auth/plan.md` - Testing strategy
   - `specs/002-user-auth/tasks.md` - Test specifications

2. **Environment Setup**:
   ```bash
   # Backend running
   cd backend && python -m uvicorn src.phase2.main:app --reload

   # Frontend running (separate terminal)
   cd frontend && npm run dev

   # Test runner ready
   cd backend && pytest
   cd frontend && npm test
   cd frontend && npm run e2e
   ```

#### Phase 3 Integration Tests
```
T023: Signup integration test (Backend)
├── Location: backend/tests/integration/test_signup.py
├── Test cases:
│   ├── Test 1: Valid signup
│   │   ├── Send: POST /api/auth/signup
│   │   │   {email: "user@example.com", password: "password123", name: "User"}
│   │   ├── Expect: 201 Created
│   │   ├── Response includes: access_token, refresh_token
│   │   ├── User in database: id, email, password_hash set
│   │   └── Verify: password_hash != password (hashed)
│   ├── Test 2: Duplicate email
│   │   ├── Create first user
│   │   ├── Attempt signup with same email
│   │   ├── Expect: 409 Conflict
│   │   ├── Message: "Email already registered"
│   │   └── One user in database (not duplicated)
│   ├── Test 3: Invalid email format
│   │   ├── Send: email = "invalid-email"
│   │   ├── Expect: 422 Unprocessable Entity
│   │   └── Message: "Please enter a valid email"
│   ├── Test 4: Weak password (< 8 chars)
│   │   ├── Send: password = "short"
│   │   ├── Expect: 422 Unprocessable Entity
│   │   └── Message: "Password must be at least 8 characters"
│   └── Test 5: Missing required fields
│       ├── Send: {password: "password123"} (no email)
│       ├── Expect: 422 Unprocessable Entity
│       └── Message indicates missing field
├── Utilities:
│   ├── test_client from fastapi.testclient
│   ├── Database fixture (per-test cleanup)
│   └── Helper: create_user(email, password, name)
└── Assertions:
    ├── Status code correct
    ├── Response schema valid
    ├── Database updated correctly
    ├── No sensitive data in response (no password_hash)
    └── Performance: < 500ms (SC-001)

T032: Signin integration test (Backend)
├── Location: backend/tests/integration/test_signin.py
├── Setup:
│   ├── Create test user: email, hashed password
│   ├── Pre-populate database
│   └── Ready for signin attempts
├── Test cases:
│   ├── Test 1: Valid signin
│   │   ├── Send: POST /api/auth/signin
│   │   │   {email: "user@example.com", password: "password123"}
│   │   ├── Expect: 200 OK
│   │   ├── Response includes: access_token, refresh_token
│   │   └── Tokens valid (can decode, have user_id)
│   ├── Test 2: Invalid credentials
│   │   ├── Send: correct email, wrong password
│   │   ├── Expect: 401 Unauthorized
│   │   └── Message: "Invalid credentials" (generic, no hint)
│   ├── Test 3: User not found
│   │   ├── Send: non-existent email
│   │   ├── Expect: 401 Unauthorized
│   │   └── Message: "Invalid credentials" (same as wrong password)
│   ├── Test 4: Invalid email format
│   │   ├── Send: email = "invalid"
│   │   ├── Expect: 422 Unprocessable Entity
│   │   └── Message: "Please enter a valid email"
│   ├── Test 5: Timing consistency
│   │   ├── Measure signin time for valid credentials
│   │   ├── Measure signin time for invalid credentials
│   │   ├── Expect: < 100ms (SC-004)
│   │   └── Expect: Similar timing (prevent enumeration)
│   └── Test 6: No user enumeration
│       ├── Attempt multiple signin failures
│       ├── Measure if timing varies by email existence
│       ├── Expect: Same timing for all invalid attempts
│       └── Verify: No info leakage about email validity
├── Utilities:
│   ├── test_client from fastapi
│   ├── Database fixture with pre-populated user
│   ├── Helper: timeit for performance measurement
│   └── Helper: signin(email, password)
└── Assertions:
    ├── Valid signin: 200, tokens present, decodable
    ├── Invalid: 401, generic message
    ├── Timing: < 100ms for all attempts
    └── Tokens include correct user_id

T039: Token storage integration test (Frontend)
├── Location: frontend/tests/integration/test_token_storage.test.tsx
├── Test setup:
│   ├── Mock backend API responses
│   ├── Mount component that calls signup/signin
│   └── Verify token storage behavior
├── Test cases:
│   ├── Test 1: Tokens stored in httpOnly cookies
│   │   ├── After signup: verify Set-Cookie headers
│   │   ├── Check: HttpOnly flag set
│   │   ├── Check: Secure flag set (HTTPS)
│   │   ├── Check: SameSite=Strict set
│   │   └── Verify: Cannot access from JavaScript
│   ├── Test 2: API client includes token in requests
│   │   ├── Make API call (e.g., GET /api/protected)
│   │   ├── Intercept request
│   │   ├── Verify: Authorization header = "Bearer <token>"
│   │   └── Token matches stored token
│   ├── Test 3: Token refresh updates both tokens
│   │   ├── Initial signin: get tokens A and B
│   │   ├── Trigger refresh: POST /api/auth/refresh
│   │   ├── Expect: New tokens C and D
│   │   ├── Verify: C != A (token rotated)
│   │   └── Verify: D != B (refresh token rotated)
│   └── Test 4: Logout clears tokens
│       ├── After signup: tokens present
│       ├── Call logout function
│       ├── Verify: Token cookie deleted or empty
│       └── Subsequent requests: No Authorization header
├── Utilities:
│   ├── @testing-library/react for component testing
│   ├── jest.mock for API interception
│   └── document.cookie for verification
└── Assertions:
    ├── Cookies have secure flags
    ├── Authorization header properly formatted
    ├── Token refresh provides new tokens
    └── Logout removes tokens

T044: JWT verification integration test (Backend)
├── Location: backend/tests/integration/test_jwt_verification.py
├── Test cases:
│   ├── Test 1: Valid JWT passes middleware
│   │   ├── Create valid token for user ID
│   │   ├── Make request with Authorization: Bearer <token>
│   │   ├── Middleware validates token
│   │   ├── Expect: Request proceeds (200 OK)
│   │   └── Response includes user data (not password_hash)
│   ├── Test 2: Missing JWT returns 401
│   │   ├── Make request without Authorization header
│   │   ├── Middleware rejects
│   │   ├── Expect: 401 Unauthorized
│   │   └── Message: "Token required"
│   ├── Test 3: Invalid JWT format returns 401
│   │   ├── Authorization: "Bearer invalid-token-string"
│   │   ├── Middleware fails to verify
│   │   ├── Expect: 401 Unauthorized
│   │   └── Message: "Invalid token"
│   ├── Test 4: Expired JWT returns 401
│   │   ├── Create token with past expiry
│   │   ├── Make request with expired token
│   │   ├── Middleware detects expiry
│   │   ├── Expect: 401 Unauthorized
│   │   └── Message: "Token expired"
│   ├── Test 5: User isolation enforced
│   │   ├── Create two users (A and B)
│   │   ├── Get token for User A
│   │   ├── Make request to access User B's data with User A's token
│   │   ├── Expect: 403 Forbidden
│   │   └── Message: "Access denied" (or similar)
│   └── Test 6: Token claims verified
│       ├── Create valid token with correct claims
│       ├── Make request
│       ├── Verify user_id extracted correctly
│       ├── Verify iat (issued at) within reasonable time
│       └── Verify exp (expiry) correct
├── Utilities:
│   ├── test_client from fastapi
│   ├── Helper: create_test_token(user_id, expires_delta)
│   ├── Helper: create_expired_token()
│   └── Mock database fixture
└── Assertions:
    ├── Valid token: Request succeeds (200)
    ├── Missing: 401 "Token required"
    ├── Invalid format: 401 "Invalid token"
    ├── Expired: 401 "Token expired"
    ├── Cross-user: 403 "Access denied"
    └── Claims: Correct extraction and validation
```

#### Phase 4 Integration Tests
```
T049: Logout integration test (Backend/Frontend)
├── Location: backend/tests/integration/test_logout.py (optional)
├── Scenarios:
│   ├── Frontend: Click logout button → tokens cleared, redirect /signin
│   ├── Backend: POST /api/auth/logout → 204 No Content
│   └── Verify: User must signin again to access protected routes

T056: Refresh token test (Backend)
├── Location: backend/tests/integration/test_refresh.py
├── Test cases:
│   ├── Test 1: Valid refresh token returns new tokens
│   │   ├── POST /api/auth/refresh with valid refresh_token
│   │   ├── Expect: 200 OK
│   │   ├── Response: new access_token, new refresh_token
│   │   ├── Verify: Old refresh_token no longer works (rotation)
│   │   └── Performance: < 200ms (SC-006)
│   ├── Test 2: Invalid refresh token returns 401
│   │   ├── POST /api/auth/refresh with invalid token
│   │   ├── Expect: 401 Unauthorized
│   │   └── Message: "Invalid refresh token"
│   └── Test 3: Refresh rotation
│       ├── Get initial tokens (access_1, refresh_1)
│       ├── Call refresh → get (access_2, refresh_2)
│       ├── Verify: access_2 != access_1 (new token)
│       ├── Verify: refresh_2 != refresh_1 (rotated)
│       └── Verify: refresh_1 no longer valid (can't reuse)

T057: Frontend interceptor test (Frontend)
├── Location: frontend/tests/integration/test_refresh_interceptor.test.tsx
├── Scenarios:
│   ├── Scenario 1: On 401 response
│   │   ├── Make API request
│   │   ├── Backend returns 401 (token expired)
│   │   ├── Interceptor calls refresh
│   │   ├── Gets new tokens
│   │   ├── Retries original request
│   │   └── Request succeeds (200 OK)
│   ├── Scenario 2: Proactive refresh on < 5 min expiry
│   │   ├── Decode token, check expiry
│   │   ├── If < 5 minutes: Trigger refresh proactively
│   │   ├── Update tokens before they expire
│   │   └── User never sees 401
│   └── Scenario 3: Multiple concurrent requests
│       ├── Send 3 requests concurrently
│       ├── Token expires during requests
│       ├── Only one refresh call made (no race condition)
│       ├── All 3 requests retry and succeed
│       └── Verify: Refresh called once (not 3x)
```

#### Phase 5 Polish Tests
```
T058: E2E flow test: signup → signin → logout
├── Location: backend/tests/integration/test_auth_flow_e2e.py
├── Flow:
│   ├── Step 1: POST /api/auth/signup
│   │   ├── Response: 201, tokens
│   │   └── User created in database
│   ├── Step 2: GET /api/protected/test
│   │   ├── Use access_token from signup
│   │   ├── Response: 200, protected data
│   │   └── Verify user_id matches
│   ├── Step 3: POST /api/auth/logout (optional)
│   │   ├── Response: 204 No Content
│   │   └── Verify tokens invalidated
│   └── Step 4: GET /api/protected/test
│       ├── No token
│       ├── Response: 401 Unauthorized
│       └── Cannot access protected resource

T059: E2E flow test: signup → signin → request refresh
├── Location: backend/tests/integration/test_auth_flow_refresh.py
├── Flow:
│   ├── Step 1: POST /api/auth/signup
│   │   └── Get initial tokens
│   ├── Step 2: POST /api/auth/refresh
│   │   ├── Use refresh_token
│   │   └── Get new tokens (rotated)
│   ├── Step 3: GET /api/protected/test
│   │   ├── Use new access_token
│   │   ├── Response: 200
│   │   └── Success (new token valid)
│   └── Step 4: GET /api/protected/test with old token
│       ├── Use original access_token
│       ├── Response: 401 (original expired or invalidated)
│       └── Verify: Tokens properly rotated

T060: Security test: User isolation
├── Location: backend/tests/security/test_user_isolation.py
├── Setup:
│   ├── Create User A with email a@example.com
│   ├── Create User B with email b@example.com
│   ├── Get tokens for both users
│   └── Test cross-user access
├── Test cases:
│   ├── Test 1: User A cannot access User B's data
│   │   ├── Token: User A's access_token
│   │   ├── Request: GET /api/protected/test?user_id=<User B ID>
│   │   ├── Expect: 403 Forbidden or filtered response
│   │   └── Verify: No User B data leaks
│   ├── Test 2: User isolation enforced at DB level
│   │   ├── Token: User A
│   │   ├── Direct database query attempt: SELECT * FROM users WHERE user_id != A
│   │   ├── Endpoint: Returns empty or 403 (enforced by middleware)
│   │   └── Verify: Middleware filters correctly
│   └── Test 3: User B cannot modify User A's account
│       ├── Token: User B
│       ├── Request: PUT /api/user/<User A ID> with new data
│       ├── Expect: 403 Forbidden
│       └── Verify: No modification occurred

T061: Security test: Password security
├── Location: backend/tests/security/test_password_security.py
├── Test cases:
│   ├── Test 1: Passwords stored as bcrypt hashes
│   │   ├── Signup user with password "password123"
│   │   ├── Query database: SELECT password_hash FROM users
│   │   ├── Verify: password_hash != "password123"
│   │   ├── Verify: password_hash starts with "$2b$" (bcrypt signature)
│   │   └── Verify: Hash length ~60 chars
│   ├── Test 2: Password verification works
│   │   ├── Hash: bcrypt.hashpw(b"password123")
│   │   ├── Verify: bcrypt.checkpw(b"password123", hash) = True
│   │   ├── Verify: bcrypt.checkpw(b"wrong", hash) = False
│   │   └── Timing: Consistent for both
│   ├── Test 3: No plaintext passwords in logs
│   │   ├── Trigger signup with password
│   │   ├── Capture all log output
│   │   ├── Verify: Password string not in logs
│   │   ├── Verify: Only hashes or "***" in logs
│   │   └── Verify: Error messages don't expose password
│   └── Test 4: Bcrypt cost factor >= 10
│       ├── Extract cost factor from password_hash
│       ├── Verify: Cost >= 10 (slow enough)
│       ├── Verify: Hashing takes > 10ms
│       └── Verify: Brute force not feasible

T062: Playwright E2E test (Frontend)
├── Location: frontend/tests/e2e/auth-flow.spec.ts
├── (See Frontend Agent assignment for details)
```

#### Test Execution Strategy
```bash
# Run all backend tests
pytest backend/tests/ -v

# Run integration tests only
pytest backend/tests/integration/ -v

# Run security tests only
pytest backend/tests/security/ -v

# Run with coverage
pytest backend/tests/ --cov=backend/src --cov-report=term-missing

# Run frontend tests
npm test

# Run E2E tests
npm run e2e

# Run E2E with headed browser
npm run e2e:headed
```

#### Key Success Criteria
- ✅ All 62 tasks marked complete
- ✅ All tests passing (unit, integration, E2E, security)
- ✅ No critical security issues found
- ✅ User isolation verified and enforced
- ✅ Password security validated
- ✅ Performance targets met (< 500ms signup, < 200ms refresh)
- ✅ 95% first-attempt success rate

---

## 🎯 Execution Timeline

**Phase 2** (Blocking - starts immediately):
- Database Agent: T007-T010 (1 day)
- Backend Agent: T011-T013 (1 day)

**Phase 3** (Parallel - after Phase 2):
- Backend US1 & Frontend US1: T014-T023 (2-3 days)
- Backend US2 & Frontend US2: T024-T032 (2-3 days, parallel with US1)
- Frontend US3 & Backend US3: T033-T039 (1-2 days, parallel with US2)
- Backend US4 & Integration US4: T040-T044 (1-2 days, parallel with US3)

**Phase 4** (Parallel - after Phase 3):
- Frontend US5 & Backend US5: T045-T049 (1 day)
- Frontend US6 & Backend US6: T050-T057 (1-2 days, parallel with US5)

**Phase 5** (Sequential - after Phases 3-4):
- Integration Agent: T058-T062 (1-2 days)

**Total Estimated Duration**: 10-14 days

---

## 📧 Questions & Support

If you have questions about:
- **Backend tasks**: Refer to Backend Agent assignment
- **Frontend tasks**: Refer to Frontend Agent assignment
- **Database design**: Refer to Database Agent assignment
- **Testing approach**: Refer to Integration Agent assignment
- **Specifications**: Review `specs/002-user-auth/spec.md`
- **Architecture**: Review `specs/002-user-auth/plan.md`

---

**Document Status**: ✅ READY FOR AGENT ASSIGNMENT
**Last Updated**: 2026-01-12
**Next Step**: Assign agents and begin Phase 2 execution
