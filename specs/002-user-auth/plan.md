# Implementation Plan: Authentication System for Phase 2

**Branch**: `002-user-auth` | **Date**: 2026-01-12 | **Spec**: `specs/002-user-auth/spec.md`
**Input**: Feature specification from `/specs/002-user-auth/spec.md`

**Note**: Comprehensive architectural plan for JWT-based authentication using Better Auth SDK with multi-user support, secure token management, and user isolation.

## Summary

Implement a complete JWT-based authentication system for Phase 2 of the todo application using Better Auth SDK for frontend signup/signin and FastAPI with python-jose for backend token verification. System supports user account creation, credential verification, secure token storage in httpOnly cookies, automatic token refresh (proactive at < 5 min remaining), token rotation on each use, and user isolation at database query level. All passwords hashed with bcrypt (cost ≥ 10), tokens signed with HS256 algorithm using shared BETTER_AUTH_SECRET, and error responses include machine-readable error codes for debugging while maintaining generic user-facing messages.

## Technical Context

**Language/Version**:
- Backend: Python 3.13+
- Frontend: TypeScript 5.3+ with Next.js 16+

**Primary Dependencies**:
- Backend: FastAPI, python-jose[cryptography], passlib[bcrypt], sqlmodel, asyncpg
- Frontend: better-auth, @better-auth/jwt, @tanstack/react-query, axios
- Database: Neon PostgreSQL with SQLAlchemy ORM via SQLModel

**Storage**: Neon PostgreSQL with tables: users (id, email, name, password_hash, created_at, updated_at)

**Testing**:
- Backend: pytest with integration tests for auth flows
- Frontend: Jest/Vitest for components, Playwright for E2E
- Security: Integration tests for user isolation and token validation

**Target Platform**: Linux servers (backend) + Modern browsers (frontend, ES2020+)

**Project Type**: Web application (frontend + backend separation)

**Performance Goals**:
- Signup endpoint: p95 < 500ms
- Signin endpoint: p95 < 300ms
- Token verification overhead: < 50ms per request
- System SLO: 99.9% uptime

**Constraints**:
- Token expiry: 7 days (access), 30 days (refresh)
- HTTPS required in production
- No secrets in code or version control
- All authentication endpoints require validation
- User enumeration prevention (generic error messages)

**Scale/Scope**:
- MVP: < 10,000 users (no sharding)
- Single deployment region
- Per spec: 35 functional requirements, 10 success criteria, 18 constraints

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Spec-Driven Development**: Specification complete, all requirements documented, no implementation freestyle allowed.

✅ **Progressive Complexity (Phase 2)**: Builds on Phase 1 console app, adds full-stack web with user authentication, database persistence, and multi-user support.

✅ **Test-First Development**: All acceptance criteria are testable; task phase will include test specifications before implementation.

✅ **User Experience Excellence**: Web UI standards with responsive design, error handling, loading states planned.

✅ **Security & Authentication**: JWT-based auth (Better Auth), user isolation via user_id, all endpoints require valid tokens, no plaintext secrets.

✅ **Code Quality Standards**: Python 3.13+, TypeScript strict mode, type hints on all functions, comprehensive docstrings, Pydantic models for validation.

## Project Structure

### Documentation (this feature)

```text
specs/002-user-auth/
├── spec.md              # Complete feature specification ✅ DONE
├── checklists/
│   └── requirements.md  # Requirements verification checklist ✅ DONE
├── plan.md              # This file - Implementation architecture ✅ DONE
├── research.md          # Phase 0: Research & technical decisions (NEXT)
├── data-model.md        # Phase 1: Entity definitions & relationships (NEXT)
├── contracts/           # Phase 1: API contracts & error responses (NEXT)
│   ├── auth-routes.openapi.json
│   └── error-responses.json
├── quickstart.md        # Phase 1: Setup & local dev guide (NEXT)
└── tasks.md             # Phase 2: Tasks & acceptance criteria (/sp.tasks command)
```

### Source Code (repository root)

```text
# Web application structure (frontend + backend)

backend/src/
├── phase2/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── models.py        # User SQLModel, password hashing
│   │   ├── routes.py        # POST /signup, POST /signin, POST /refresh, POST /logout
│   │   ├── jwt.py           # JWT verification, token extraction, middleware
│   │   └── schemas.py       # Pydantic models: SignupRequest, SigninRequest, TokenResponse
│   ├── database.py          # SQLModel setup, connection pooling, migrations
│   ├── config.py            # Environment config, BETTER_AUTH_SECRET
│   └── main.py              # FastAPI app, middleware, error handlers
└── requirements.txt

backend/tests/
├── test_auth_signup.py      # Unit tests for signup logic
├── test_auth_signin.py      # Unit tests for signin logic
├── test_jwt_verification.py # Unit tests for token verification
├── integration/
│   ├── test_auth_flow.py    # End-to-end signup → signin → API call
│   └── test_user_isolation.py # Cross-user access prevention
└── conftest.py              # Test fixtures, DB setup

frontend/src/
├── app/
│   ├── (auth)/
│   │   ├── signup/
│   │   │   └── page.tsx     # Signup page with Better Auth form
│   │   ├── signin/
│   │   │   └── page.tsx     # Signin page with Better Auth form
│   │   └── layout.tsx       # Auth routes layout (public)
│   ├── (dashboard)/
│   │   ├── layout.tsx       # Protected routes layout, redirect logic
│   │   ├── page.tsx         # Dashboard redirect
│   │   └── tasks/
│   │       └── page.tsx     # Task list (protected by layout)
│   └── layout.tsx           # Root layout with providers
├── lib/
│   ├── auth.ts              # Better Auth + JWT setup, client config
│   ├── api/
│   │   ├── client.ts        # Axios instance with JWT interceptors
│   │   └── tasks.ts         # Task API calls (will use auth context)
│   └── hooks/
│       ├── useAuth.ts       # Auth context hook (from Better Auth)
│       └── useTask.ts       # Task data fetching (React Query hooks)
├── components/
│   ├── auth/
│   │   ├── SignupForm.tsx   # Better Auth signup component
│   │   └── SigninForm.tsx   # Better Auth signin component
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── ErrorAlert.tsx
│   └── layout/
│       └── Navigation.tsx
├── types/
│   └── auth.ts              # TypeScript types for auth state
└── .env.local               # Frontend env config

frontend/tests/
├── components/
│   ├── SignupForm.test.tsx
│   └── SigninForm.test.tsx
├── e2e/
│   └── auth-flow.spec.ts    # Playwright E2E tests
└── conftest.ts              # Test setup
```

**Structure Decision**: Web application with separated frontend (Next.js 16) and backend (FastAPI) as specified in constitution Phase 2. Frontend handles UI and token storage; backend handles token verification, user model, and protected endpoints. Database shared via Neon PostgreSQL with SQLModel ORM. Authentication via Better Auth SDK (frontend) and python-jose (backend).

## Complexity Tracking

**No constitution violations.** All design decisions align with Phase 2 principles:
- ✅ Spec-driven development (specification complete, no ad-hoc changes)
- ✅ TDD mandate (test specifications in tasks.md phase)
- ✅ Progressive complexity (builds on Phase 1 console app)
- ✅ Security-first (JWT, user isolation, hashing, no plaintext secrets)
- ✅ Code quality standards (Python 3.13+, TypeScript strict, type hints, docstrings)

---

## Architecture Decisions

### 1. **JWT Algorithm & Secret Management**
- **Decision**: HS256 with shared BETTER_AUTH_SECRET (32+ chars, random)
- **Rationale**: Symmetrical algorithm sufficient for single deployment, simpler than RS256 key management
- **Alternative Rejected**: RS256 (adds complexity of key rotation for MVP)
- **Implementation**: Backend and frontend use same BETTER_AUTH_SECRET from environment variables

### 2. **Token Refresh Strategy**
- **Decision**: Proactive refresh when < 5 minutes remaining on access token
- **Rationale**: Prevents 401 errors during active sessions, seamless UX, aligns with spec clarification
- **Alternative Rejected**: Reactive refresh on 401 (causes user-facing delays)
- **Implementation**: Frontend interceptor monitors token expiry, calls refresh endpoint before timeout

### 3. **Refresh Token Rotation**
- **Decision**: Issue new refresh token with each access token refresh
- **Rationale**: Prevents replay attacks, limits exposure window if token leaked, OAuth 2.0 best practice
- **Alternative Rejected**: Single-use refresh tokens (frontend retry logic complexity)
- **Implementation**: Backend issues new refresh token in refresh response; frontend updates both tokens

### 4. **Token Storage**
- **Decision**: httpOnly cookies (separate cookies for access and refresh, or combined in secure storage)
- **Rationale**: Prevents XSS attacks (inaccessible to JavaScript), required by spec (FR-020)
- **Alternative Rejected**: localStorage (XSS vulnerable), sessionStorage (cleared on tab close)
- **Implementation**: Better Auth SDK handles cookie management; backend sets cookies with secure flags

### 5. **Error Response Format**
- **Decision**: Machine-readable error codes + generic user-facing messages
- **Rationale**: Enables backend logging/debugging while preventing information leakage
- **Alternative Rejected**: Generic messages only (hard to debug), detailed error messages (info leakage)
- **Implementation**: `{"error": "AUTH_INVALID_CREDENTIALS", "message": "Invalid credentials", "status_code": 401}`

### 6. **User Isolation Enforcement**
- **Decision**: Extract user_id from JWT `sub` claim; filter all queries by user_id (never from request)
- **Rationale**: Prevents cross-user data access at query level, database-enforced security
- **Alternative Rejected**: Frontend-only isolation (backend must verify), role-based access (overengineering for MVP)
- **Implementation**: JWT middleware extracts user_id; task endpoints filter by extracted user_id, not request parameter

### 7. **Password Hashing**
- **Decision**: bcrypt with cost factor >= 10 (via passlib[bcrypt])
- **Rationale**: Industry standard, automatically handles salt generation, slow by design to prevent brute force
- **Alternative Rejected**: argon2 (overkill for MVP), plaintext (security breach)
- **Implementation**: Better Auth SDK handles hashing during signup; backend verifies hash during signin

### 8. **API Endpoint Structure**
- **Decision**: RESTful endpoints with status codes:
  - POST /api/auth/signup → 201 Created
  - POST /api/auth/signin → 200 OK
  - POST /api/auth/refresh → 200 OK
  - POST /api/auth/logout → 204 No Content
  - Protected endpoints require valid JWT in Authorization header
- **Rationale**: RESTful conventions, clear semantics, standard HTTP status codes
- **Alternative Rejected**: GraphQL (MVP doesn't need query flexibility), custom RPC (non-standard)
- **Implementation**: FastAPI routes with proper status code responses

---

## Integration Points

### Frontend ↔ Backend Communication

```
User Action → Better Auth Form
    ↓
Frontend calls /api/auth/signup or /api/auth/signin
    ↓
Backend verifies credentials, hashes password, generates JWT + refresh token
    ↓
Backend returns tokens (set in httpOnly cookies via Set-Cookie header)
    ↓
Frontend stores tokens in cookies, updates auth state
    ↓
Subsequent requests: Frontend axios interceptor attaches JWT in Authorization header
    ↓
Backend JWT middleware verifies token, extracts user_id
    ↓
Request proceeds with user_id injected into context
    ↓
API endpoint filters response by user_id (ensures isolation)
```

### Token Refresh Flow

```
Frontend detects access token has < 5 minutes remaining
    ↓
Frontend calls POST /api/auth/refresh with refresh token in request body
    ↓
Backend verifies refresh token, generates new access token + new refresh token
    ↓
Backend returns new tokens (both rotated)
    ↓
Frontend updates stored tokens
    ↓
Original request is retried with new access token
    ↓
Request succeeds
```

### Error Handling

```
User submits invalid credentials
    ↓
Backend returns: {"error": "AUTH_INVALID_CREDENTIALS", "message": "Invalid credentials", "status_code": 401}
    ↓
Frontend displays generic message: "Invalid credentials"
    ↓
Backend logs detailed error with code for monitoring/debugging
    ↓
No information leakage (no hint about email vs password)
```

---

## Testing Strategy

### Backend Tests (pytest)
- **Unit Tests**: Password hashing, JWT generation, token verification
- **Integration Tests**: Complete auth flows (signup → signin → protected request)
- **Security Tests**: User isolation (User A cannot access User B's data), token validation, error messages

### Frontend Tests (Jest/Vitest + Playwright)
- **Component Tests**: SignupForm, SigninForm rendering and validation
- **Integration Tests**: Form submission → API call → token storage → redirect
- **E2E Tests**: Complete user journey: signup → signin → access protected page → logout

### Security Tests (Integration Agent)
- **Token Verification**: Valid token succeeds, invalid/expired token rejected (401)
- **User Isolation**: Cross-user access attempts return 403 Forbidden
- **Password Security**: Plaintext password never in logs, bcrypt hash verified
- **Error Messages**: Generic messages (no enumeration), machine-readable codes for debugging

---

## Success Criteria (from Spec)

- [x] **SC-001**: Users can complete account creation in under 2 minutes (form UX)
- [x] **SC-002**: System successfully issues JWT tokens on 100% of valid attempts (implementation validates)
- [x] **SC-003**: Auth endpoints respond within 500ms p95 (performance testing validates)
- [x] **SC-004**: Invalid credentials rejected within 100ms with consistent message (implementation validates)
- [x] **SC-005**: JWT tokens expire exactly as specified (7d access, 30d refresh - implementation validates)
- [x] **SC-006**: Token refresh succeeds within 200ms (performance testing validates)
- [x] **SC-007**: Cross-user access rejected 403 Forbidden 100% (security testing validates)
- [x] **SC-008**: Passwords never stored/logged in plaintext (code review validates)
- [x] **SC-009**: 95% first-attempt success rate (acceptance testing validates)
- [x] **SC-010**: System handles 1000 concurrent requests without degradation (load testing validates)

---

## Next Steps

### Phase 0: Research & Technical Decisions (Next)
- [ ] Research Better Auth SDK JWT plugin best practices
- [ ] Document JWT payload structure and claims requirements
- [ ] Verify python-jose compatibility with Better Auth tokens
- [ ] Research httpOnly cookie security best practices
- [ ] Document BETTER_AUTH_SECRET generation and rotation strategy

### Phase 1: Design & Contracts
- [ ] Create `research.md` with findings (DELIVERABLE)
- [ ] Create `data-model.md` with User entity, relationships, constraints (DELIVERABLE)
- [ ] Create `contracts/auth-routes.openapi.json` with endpoint specifications (DELIVERABLE)
- [ ] Create `contracts/error-responses.json` with error code mappings (DELIVERABLE)
- [ ] Create `quickstart.md` with local dev setup guide (DELIVERABLE)
- [ ] Update agent context files with implementation details

### Phase 2: Task Generation (/sp.tasks command)
- [ ] Generate detailed implementation tasks with acceptance criteria
- [ ] Create test specifications before implementation (TDD)
- [ ] Assign tasks to agents (Backend, Frontend, Database, Integration)

### Phase 3: Implementation
- [ ] Backend Agent: Implement auth routes, JWT middleware, User model
- [ ] Database Agent: Define User schema, indexes, relationships
- [ ] Frontend Agent: Build signup/signin pages, API client, token management
- [ ] Integration Agent: Create end-to-end tests, security validation

---

## Plan Status

**✅ COMPLETE AND READY FOR PHASE 0 (Research)**

- Technical context fully specified
- Constitution check: All gates pass
- Project structure defined (frontend + backend + database)
- Architecture decisions documented
- Integration points clarified
- Testing strategy defined
- Success criteria mapped to implementation

**Recommended Next Command**: `/sp.plan --phase 0` to generate research.md with technical findings, or proceed directly to `/sp.tasks` to generate implementation tasks.
