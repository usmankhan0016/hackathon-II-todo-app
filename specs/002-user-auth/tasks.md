# Implementation Tasks: Authentication System for Phase 2

**Branch**: `002-user-auth` | **Date**: 2026-01-12 | **Spec**: `specs/002-user-auth/spec.md` | **Plan**: `specs/002-user-auth/plan.md`

**Note**: All tasks follow TDD (Test-First) approach per Phase 2 constitution. Tests are provided in acceptance criteria; implementation validates tests pass.

---

## Executive Summary

**Total Tasks**: 44 implementation tasks organized in 5 phases
**Phase 1 (Setup)**: 6 tasks - Project initialization and environment setup
**Phase 2 (Foundational)**: 7 tasks - Database, shared infrastructure, core middleware
**Phase 3 (User Story 1-4 - P1 Critical)**: 17 tasks - Signup, Signin, Token Storage, Backend Verification
**Phase 4 (User Story 5-6 - P2 Important)**: 10 tasks - Logout, Token Refresh
**Phase 5 (Polish & Integration)**: 4 tasks - Error handling, logging, E2E tests

**MVP Scope Recommendation**: Complete Phase 1 + Phase 2 + Phase 3 (all P1 stories) for functional MVP (30 tasks)
**Extended Scope**: Add Phase 4 (P2 stories) for complete auth system with token refresh (40 tasks)

**Parallelization Opportunities**:
- Phase 3 US1 & US2 (signup + signin) can run parallel after foundational layer
- Phase 3 US3 & US4 (token storage + backend verification) can run parallel
- Phase 4 US5 & US6 (logout + refresh) can run parallel

---

## Phase 1: Setup & Project Initialization

**Goals**: Create project structure, configure environment, set up build tools
**Estimated Duration**: Foundational (blocking)
**Status**: PENDING

### Backend Project Setup

- [X] T001 Create backend project structure with Phase 2 directory layout: `backend/src/phase2/auth/`, `backend/src/phase2/models/`, `backend/tests/`

- [X] T002 Create Python virtual environment and setup UV for dependency management: `uv init`, add pyproject.toml with core dependencies (fastapi, python-jose, passlib, sqlmodel, asyncpg, pydantic)

- [X] T003 Create backend environment configuration file: `backend/.env` with placeholders for DATABASE_URL, BETTER_AUTH_SECRET, DEBUG flag

- [X] T004 Initialize FastAPI application in `backend/src/phase2/main.py` with CORS configuration and error handlers

### Frontend Project Setup

- [X] T005 Create Next.js 16 project structure: `frontend/src/app/(auth)/`, `frontend/src/app/(dashboard)/`, `frontend/src/lib/`, `frontend/src/components/`

- [X] T006 Create frontend environment configuration file: `frontend/.env.local` with placeholders for NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL

---

## Phase 2: Foundational Infrastructure (Blocking Prerequisites)

**Goals**: Set up database connection, core models, middleware, error handling
**Estimated Duration**: Foundational (all user stories depend on this)
**Status**: PENDING

### Database Setup

- [X] T007 Create database connection module: `backend/src/phase2/database.py` with SQLModel session factory, connection pooling (min 5, max 20), SSL configuration for Neon PostgreSQL, health check endpoint

- [X] T008 Create User SQLModel in `backend/src/phase2/models/user.py` with fields: id (UUID), email (unique, indexed), password_hash, name, created_at, updated_at. Include bcrypt password hashing utilities (verify_password, hash_password using passlib)

- [X] T009 Create Pydantic schemas in `backend/src/phase2/schemas/auth.py`: SignupRequest, SigninRequest, TokenResponse, RefreshRequest, ErrorResponse with machine-readable error codes

- [X] T010 Initialize database tables on startup: `backend/src/phase2/main.py` updated to call SQLModel.metadata.create_all() before accepting requests. Verify User table created with correct constraints and indexes.

### JWT & Authentication Infrastructure

- [X] T011 Create JWT utilities module: `backend/src/phase2/auth/jwt.py` with functions: create_access_token (7-day expiry), create_refresh_token (30-day expiry), verify_token, extract_user_id. All use HS256 algorithm with BETTER_AUTH_SECRET

- [X] T012 [P] Create authentication middleware: `backend/src/phase2/middleware/auth.py` with HTTPBearer token extraction, JWT verification, user_id extraction and injection into request context. Returns 401 Unauthorized if token missing/invalid/expired

- [X] T013 [P] Create error handlers module: `backend/src/phase2/handlers/errors.py` with function to format errors with machine-readable error codes (AUTH_INVALID_CREDENTIALS, AUTH_EMAIL_EXISTS, AUTH_INVALID_EMAIL, AUTH_WEAK_PASSWORD, AUTH_TOKEN_EXPIRED, AUTH_TOKEN_INVALID, AUTH_TOKEN_MISSING, AUTH_FORBIDDEN). All endpoints use these error codes while showing generic messages to users.

---

## Phase 3: User Story Implementation - P1 Critical Path

**Goals**: Implement core authentication features (signup, signin, token storage, backend verification)
**Status**: PENDING
**Each story independently testable and deployable**

---

### User Story 1: User Signup (Priority P1)

**Goal**: Users can create accounts with email/password, receive JWT tokens, stored securely

**Acceptance Criteria**:
- ✅ User can signup with valid email and password → account created, JWT issued, user redirected to dashboard
- ✅ Duplicate email signup → 409 Conflict with message "Email already registered"
- ✅ Invalid email format → 422 Unprocessable Entity with message "Please enter a valid email"
- ✅ Weak password (< 8 chars) → 422 with message "Password must be at least 8 characters"

**Independent Test**: Signup page can be tested without signin or protected endpoints working. Verify database user creation, JWT issuance, and error handling.

#### Backend Tasks

- [ ] T014 [P] [US1] Create signup route in `backend/src/phase2/routes/auth.py`: POST /api/auth/signup with SignupRequest validation (email format, password >= 8 chars). Return 201 Created with TokenResponse on success. Handle duplicates (409), validation errors (422). Use error codes for logging.

- [ ] T015 [US1] Create user registration service in `backend/src/phase2/services/auth_service.py`: signup_user function that hashes password with bcrypt (cost >= 10), stores user in database atomically, raises appropriate exceptions for duplicates/validation

- [ ] T016 [US1] Update User model constraint: Add unique constraint on email field, create database index on email for query performance

- [ ] T017 [US1] Implement token generation on signup: signup_user returns (user, access_token, refresh_token). Tokens include user_id in `sub` claim and email in payload.

#### Frontend Tasks

- [ ] T018 [P] [US1] Create signup page layout: `frontend/src/app/(auth)/signup/page.tsx` with public route (no auth required), responsive layout using Tailwind CSS, error display area

- [ ] T019 [P] [US1] Create Better Auth signup form component: `frontend/src/components/auth/SignupForm.tsx` using Better Auth SDK with email input, password input, password confirmation, submit button, error display, loading state

- [ ] T020 [US1] Implement client-side validation: SignupForm validates email format (regex) and password strength (>= 8 chars) before submission, displays errors inline

- [ ] T021 [US1] Integrate signup API call: SignupForm submits to POST /api/auth/signup via axios client, receives JWT tokens, stores tokens in httpOnly cookies (set by backend Set-Cookie header), redirects to dashboard on success

- [ ] T022 [US1] Create signup error handling: SignupForm catches API errors (409, 422), extracts generic message (not error code), displays to user. Shows loading state during submission.

#### Testing Tasks

- [ ] T023 [US1] Write signup integration test: `backend/tests/integration/test_signup.py` covering valid signup, duplicate email (409), invalid email (422), weak password (422). Verify database user creation and JWT payload contents.

---

### User Story 2: User Signin (Priority P1)

**Goal**: Existing users can authenticate with email/password, receive JWT tokens with no user enumeration

**Acceptance Criteria**:
- ✅ Valid credentials signin → JWT issued (7-day expiry), user redirected to dashboard
- ✅ Wrong password → 401 Unauthorized with generic message "Invalid credentials"
- ✅ Nonexistent email → 401 Unauthorized with generic message "Invalid credentials" (no user enumeration)
- ✅ Token expires after 7 days → 401 on next protected request, user redirected to signin

**Independent Test**: Signin page tested independently; verify credential verification, token issuance, and generic error messages prevent user enumeration.

#### Backend Tasks

- [ ] T024 [P] [US2] Create signin route in `backend/src/phase2/routes/auth.py`: POST /api/auth/signin with SigninRequest (email, password). Return 200 OK with TokenResponse on success. Return 401 with generic "Invalid credentials" for both wrong password AND nonexistent email (no differentiation). Use error codes for backend logging only.

- [ ] T025 [US2] Create authentication service: `backend/src/phase2/services/auth_service.py` signin_user function that queries user by email, verifies password hash, handles both invalid email and wrong password with same error (no enumeration), generates access + refresh tokens

- [ ] T026 [US2] Implement token generation on signin: Tokens include user_id in `sub` claim, email in payload, access token with 7-day expiry, refresh token with 30-day expiry

- [ ] T027 [US2] Add refresh token rotation on signin: Each signin issues new access token AND new refresh token (both rotated). Old tokens remain valid until expiry (no immediate invalidation).

#### Frontend Tasks

- [ ] T028 [P] [US2] Create signin page layout: `frontend/src/app/(auth)/signin/page.tsx` with public route, responsive layout, error display

- [ ] T029 [P] [US2] Create Better Auth signin form component: `frontend/src/components/auth/SigninForm.tsx` with email input, password input, submit button, error display, loading state

- [ ] T030 [US2] Integrate signin API call: SigninForm submits to POST /api/auth/signin, receives tokens (stored in httpOnly cookies by Set-Cookie header), redirects to dashboard on success

- [ ] T031 [US2] Create signin error handling: Catches 401 error, displays generic message "Invalid credentials" to user (no information about email vs password). Shows loading state during submission.

#### Testing Tasks

- [ ] T032 [US2] Write signin integration test: `backend/tests/integration/test_signin.py` covering valid credentials (200), wrong password (401 generic), nonexistent email (401 generic), verify no user enumeration via error messages

---

### User Story 3: Secure Token Storage (Priority P1)

**Goal**: JWT tokens stored in httpOnly cookies, inaccessible to JavaScript, automatically attached to API requests

**Acceptance Criteria**:
- ✅ JWT token stored in httpOnly cookie (not localStorage)
- ✅ Token automatically attached in Authorization header to API requests
- ✅ httpOnly cookie inaccessible via JavaScript (verified in browser DevTools)

**Independent Test**: Token storage verified by checking HTTP response headers (Set-Cookie with HttpOnly flag), verifying cookie visible in browser DevTools but inaccessible to JavaScript.

#### Frontend Tasks

- [ ] T033 [US3] Create API client: `frontend/src/lib/api/client.ts` using axios with default base URL (NEXT_PUBLIC_API_URL), default headers, error handling

- [ ] T034 [US3] Implement axios request interceptor: `frontend/src/lib/api/client.ts` updated to attach JWT token in Authorization header (Bearer scheme) for all requests. Token extracted from httpOnly cookie automatically (browser sends cookie in request).

- [ ] T035 [US3] Implement response error handling: axios response interceptor catches 401 Unauthorized, redirects to signin page (token expired or invalid)

- [ ] T036 [US3] Create axios instance export: `frontend/src/lib/api/client.ts` exports configured axios instance for use in API calls throughout application

#### Backend Tasks

- [ ] T037 [US3] Update signin/signup routes to set secure cookies: `backend/src/phase2/routes/auth.py` updated to set response cookies with flags: HttpOnly=true, Secure=true (HTTPS only), SameSite=Strict, Path=/api, MaxAge set according to token expiry

- [ ] T038 [P] [US3] Implement Authorization header parsing in middleware: `backend/src/phase2/middleware/auth.py` extracts JWT from Authorization header (Bearer scheme), validates signature, extracts user_id. Middleware applies to all /api/* routes except /api/auth/signup and /api/auth/signin

#### Testing Tasks

- [ ] T039 [US3] Write token storage test: `frontend/tests/integration/test_token_storage.test.tsx` verifies Set-Cookie header present in signup/signin responses with HttpOnly flag, token attached to subsequent requests in Authorization header

---

### User Story 4: JWT Verification on Backend (Priority P1)

**Goal**: Backend verifies JWT tokens on protected endpoints, enforces user_id extraction, prevents unauthorized access

**Acceptance Criteria**:
- ✅ Valid JWT token → request proceeds, user_id extracted from token
- ✅ Invalid/tampered JWT token → 401 Unauthorized
- ✅ Expired JWT token → 401 Unauthorized
- ✅ Missing JWT token → 401 Unauthorized

**Independent Test**: Create test endpoint requiring JWT; test with valid, invalid, expired, and no tokens. Verify user_id correctly extracted for valid tokens.

#### Backend Tasks

- [ ] T040 [P] [US4] Create protected test endpoint: `backend/src/phase2/routes/test.py` with GET /api/test endpoint that requires valid JWT (applies auth middleware), returns current user_id from extracted JWT. Used for testing token verification.

- [ ] T041 [US4] Implement JWT verification middleware: `backend/src/phase2/middleware/auth.py` verify_token function uses python-jose to verify JWT signature (HS256 with BETTER_AUTH_SECRET), checks token expiration, extracts user_id from `sub` claim

- [ ] T042 [US4] Add middleware to protected routes: All endpoints except /api/auth/* require auth middleware. Middleware adds user_id to request context (never allow user_id from request body/query).

- [ ] T043 [US4] Implement 401 error responses: Token verification failures return 401 Unauthorized with generic error message (no details about why token invalid). Machine-readable error codes for backend logging.

#### Testing Tasks

- [ ] T044 [US4] Write JWT verification integration test: `backend/tests/integration/test_jwt_verification.py` covering valid token (succeeds), invalid signature (401), expired token (401), missing token (401). Verify user_id correctly extracted from valid tokens.

---

## Phase 4: User Story Implementation - P2 Important

**Goals**: Implement logout and token refresh for improved UX
**Status**: PENDING
**Can proceed after Phase 3 (P1) stories complete**

---

### User Story 5: User Logout (Priority P2)

**Goal**: Users can explicitly end sessions by logging out, tokens cleared from storage

**Acceptance Criteria**:
- ✅ Logout button clears tokens and redirects to signin page
- ✅ After logout, protected pages redirect to signin
- ✅ Old tokens cannot access protected endpoints (401)

**Independent Test**: Test logout, verify tokens cleared, attempt protected request returns 401.

#### Frontend Tasks

- [ ] T045 [P] [US5] Create logout button component: `frontend/src/components/layout/LogoutButton.tsx` with button that calls logout function, displays loading state during logout

- [ ] T046 [US5] Implement logout function: `frontend/src/lib/auth.ts` logout function clears tokens from httpOnly cookies (frontend can set empty value), updates auth state, redirects to signin page using Next.js router

- [ ] T047 [US5] Add logout button to navigation: `frontend/src/components/layout/Navigation.tsx` includes LogoutButton for authenticated users

#### Backend Tasks

- [ ] T048 [P] [US5] Create logout endpoint: `backend/src/phase2/routes/auth.py` POST /api/auth/logout (optional backend logout tracking, clears server-side token tracking if implemented). Returns 204 No Content.

#### Testing Tasks

- [ ] T049 [US5] Write logout integration test: `frontend/tests/integration/test_logout.test.tsx` verifies logout clears tokens, redirects to signin, subsequent protected requests receive 401

---

### User Story 6: Token Refresh (Priority P2)

**Goal**: Automatically refresh expired access tokens using refresh tokens, maintain sessions

**Acceptance Criteria**:
- ✅ When access token < 5 min remaining, automatic refresh happens on next API request
- ✅ New access token issued with 7-day expiry
- ✅ New refresh token issued (rotation) with 30-day expiry
- ✅ If refresh token expired, user redirected to signin

**Independent Test**: Test token refresh by simulating expiry (mocking clock), verify new tokens issued and rotated.

#### Frontend Tasks

- [ ] T050 [P] [US6] Create token refresh check function: `frontend/src/lib/auth.ts` function shouldRefreshToken checks if access token expiry < 5 minutes, returns boolean

- [ ] T051 [US6] Implement request interceptor with refresh logic: axios request interceptor (in `frontend/src/lib/api/client.ts`) checks if token should refresh, calls refresh endpoint before original request if needed

- [ ] T052 [US6] Create refresh endpoint call: Frontend calls POST /api/auth/refresh with refresh token in request body, receives new access token + new refresh token (rotated), updates stored tokens

- [ ] T053 [US6] Implement automatic retry after refresh: After successful token refresh, original failed request is retried with new access token. If refresh fails (401), redirect to signin.

#### Backend Tasks

- [ ] T054 [P] [US6] Create refresh endpoint: `backend/src/phase2/routes/auth.py` POST /api/auth/refresh with RefreshRequest (refresh_token in body). Verify refresh token signature and expiry. Generate new access token (7-day expiry) + new refresh token (30-day expiry, rotation). Return 200 OK with new tokens.

- [ ] T055 [US6] Implement refresh token rotation: Each refresh request issues NEW refresh token. Old refresh token becomes invalid after rotation. Frontend must update stored refresh token after each refresh.

- [ ] T056 [US6] Add refresh endpoint error handling: If refresh token invalid/expired, return 401 Unauthorized with generic message. No user enumeration.

#### Testing Tasks

- [ ] T057 [US6] Write token refresh integration test: `backend/tests/integration/test_token_refresh.py` verifies valid refresh token (200 with new tokens), invalid refresh token (401), token rotation (new token different from old). Verify new tokens work for subsequent requests.

- [ ] T058 [US6] Write frontend refresh interceptor test: `frontend/tests/integration/test_refresh_interceptor.test.tsx` verifies automatic refresh when token < 5 min remaining, original request retried after refresh, redirect to signin if refresh fails (401)

---

## Phase 5: Polish & Cross-Cutting Concerns

**Goals**: Complete testing, logging, error handling, security validation
**Status**: PENDING
**Execute after core user stories complete**

### Integration & Security

- [ ] T059 Complete end-to-end flow test: `backend/tests/integration/test_auth_flow_e2e.py` covering signup → signin → protected request → logout → verify cannot access. Verify all status codes, error messages, user isolation.

- [ ] T060 [P] User isolation security test: `backend/tests/security/test_user_isolation.py` creates User A and User B, verifies User A cannot query/modify User B's data. Tests cross-user access attempts return 403 Forbidden.

- [ ] T061 [P] Password security test: `backend/tests/security/test_password_security.py` verifies passwords hashed with bcrypt (never plaintext), same plaintext produces different hashes, hashes cannot be reversed, plaintext never in logs

- [ ] T062 Frontend end-to-end test: `frontend/tests/e2e/auth-flow.spec.ts` using Playwright, covers complete user journey: signup → signin → access protected page → logout → verify redirected to signin

---

## Task Dependencies & Execution Strategy

### Critical Path (Blocking Order)

```
Phase 1 Setup (T001-T006)
    ↓
Phase 2 Foundational (T007-T013)
    ↓
Phase 3 User Stories (T014-T044)
    ├─ US1: Signup (T014-T023)
    ├─ US2: Signin (T024-T032)
    ├─ US3: Token Storage (T033-T039)
    └─ US4: Backend Verification (T040-T044)
    ↓
Phase 4 User Stories (T045-T058)
    ├─ US5: Logout (T045-T049)
    └─ US6: Token Refresh (T050-T058)
    ↓
Phase 5 Polish (T059-T062)
```

### Parallelization Opportunities

**After Phase 2 Foundational:**
- T014-T023 (US1 Backend) can run parallel with T033-T039 (US3 Frontend/Backend Setup)
- T024-T032 (US2 Backend) can run parallel with T018-T022 (US1 Frontend)

**After T023 (US1 Complete):**
- T024-T032 (US2) and T033-T039 (US3) can run in parallel
- T040-T044 (US4) can start after T012 (auth middleware complete)

**Independent Parallel Phases:**
- Phase 4 US5 & US6 can run in parallel after Phase 3 complete

### Recommended Execution Phases

**MVP (Phase 1-3)**: 30 tasks
- Setup (T001-T006)
- Foundational (T007-T013)
- All P1 stories (T014-T044)
- **Result**: Functional authentication system with signup, signin, token management, backend verification

**Extended (Phase 1-4)**: 40 tasks
- All above + Logout & Token Refresh
- **Result**: Complete auth system with logout and automatic token refresh

**Production (Phase 1-5)**: 44 tasks
- All above + Complete testing, security validation, E2E tests
- **Result**: Production-ready authentication system with comprehensive tests

---

## Implementation Notes

### Architecture Patterns

1. **Dependency Injection**: All services receive database session and config via constructor
2. **Error Handling**: All endpoints return consistent error response format with error codes
3. **User Isolation**: user_id always extracted from JWT (never from request), used to filter queries
4. **Token Management**: Both access and refresh tokens issued, refresh token rotates on each use
5. **Security**: All passwords hashed with bcrypt (cost >= 10), no plaintext secrets in code, environment variables only

### Testing Strategy (TDD)

All acceptance criteria provided in each user story can serve as test cases. Recommended approach:
1. Read acceptance criteria
2. Write test cases covering each scenario
3. Implement to make tests pass
4. Verify all tests pass before task completion

### Code Organization

- **Backend**: Modular structure by concern (auth, models, services, routes, middleware, handlers)
- **Frontend**: Component-based with separate concerns (pages, components, lib/services)
- **Tests**: Parallel structure to source (backend/tests mirrors backend/src structure)

### Development Workflow

1. **Per Task**: Developer reads task, implements, writes tests
2. **Per User Story**: Team lead verifies all tasks in story complete, acceptance criteria met
3. **Per Phase**: QA performs integration testing across all tasks in phase
4. **Release**: After Phase 5 complete, full E2E testing before production deployment

---

## Success Metrics

- ✅ All 44 tasks completed and tested
- ✅ All 10 success criteria from spec verified
- ✅ All 6 user stories independently testable and deployable
- ✅ All 35 functional requirements (FR-001 through FR-035) implemented
- ✅ Security constraints (8 constraints) verified via tests
- ✅ Performance targets (p95 latency) validated
- ✅ Zero user enumeration vulnerabilities
- ✅ Zero plaintext password storage
- ✅ User isolation enforced (cross-user access blocked)
- ✅ 100% end-to-end flow coverage

---

## Next Steps

1. **Assign Tasks**: Allocate tasks to Backend, Frontend, Database, and Integration agents
2. **Start Phase 1**: Execute setup tasks (T001-T006)
3. **Proceed to Phase 2**: Foundation tasks (T007-T013) - no user story tasks can run until these complete
4. **Parallel Phase 3**: After Phase 2, run User Story 1-4 tasks in parallel per parallelization strategy
5. **Phase 4**: After Phase 3 complete, run Logout and Token Refresh (Phase 4)
6. **Phase 5**: Final polish, security tests, E2E validation
7. **Deploy**: After all phases complete, deploy to production

---

**Tasks Status**: ✅ READY FOR ASSIGNMENT AND IMPLEMENTATION

**Recommended Execution**: Start with Phase 1 (Setup), then Phase 2 (Foundational), then Phase 3 (P1 User Stories in parallel where possible)
