# Authentication System Implementation Roadmap
**Phase 2: JWT-Based Auth with Better Auth SDK**

**Date**: 2026-01-12
**Status**: Phase 1 Complete ✅ | Phase 2-5 Ready for Agent Assignment
**Branch**: `002-user-auth`

---

## 📋 Executive Summary

The authentication system specification, plan, and tasks are **complete and ready for agent-driven implementation**. Phase 1 (project setup) has been executed successfully. Phases 2-5 are now ready for parallel agent execution.

**Total Tasks**: 62
**Completed**: 6 (Phase 1)
**Remaining**: 56 (Phases 2-5)

---

## ✅ Phase 1 Completion Report (Setup)

**Status**: COMPLETE
**Date Completed**: 2026-01-12

### Backend Setup (T001-T004) - Completed
- ✅ T001: Backend project structure created
  - `backend/src/phase2/{auth,models,middleware,handlers,routes}`
  - `backend/tests/{integration,security}`

- ✅ T002: Python project configuration (pyproject.toml)
  - Dependencies: FastAPI, python-jose, passlib, sqlmodel, asyncpg, pydantic
  - Dev dependencies: pytest, pytest-asyncio, black, ruff, mypy

- ✅ T003: Backend environment configuration (.env)
  - DATABASE_URL, BETTER_AUTH_SECRET, DEBUG, LOG_LEVEL
  - JWT expiry: 7 days (access), 30 days (refresh)

- ✅ T004: FastAPI application initialization (main.py)
  - CORS middleware configured
  - Error handlers for validation and general errors
  - Health check and root endpoints

### Frontend Setup (T005-T006) - Completed
- ✅ T005: Next.js 16 project structure
  - `frontend/src/app/(auth)/{signup,signin}`
  - `frontend/src/app/(dashboard)/{layout,tasks}`
  - `frontend/src/lib/{api,hooks}`
  - `frontend/src/components/{auth,ui,layout}`

- ✅ T006: Frontend environment configuration (.env.local)
  - NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET
  - Token refresh interval: 5 minutes
  - Feature flags for debug and logging

---

## 🎯 Phases 2-5: Agent Assignment Structure

### Phase 2: Foundational Infrastructure (7 tasks, T007-T013)
**Blocking prerequisites for all user stories**
**Primary Agent**: Backend Agent + Database Agent
**Estimated Duration**: 1-2 days

| Task | Type | Description | Agent |
|------|------|-------------|-------|
| T007 | DB | Database connection module (SQLModel, pooling, SSL) | Database Agent |
| T008 | DB | User SQLModel (fields, indexes, bcrypt utils) | Database Agent |
| T009 | API | Pydantic schemas with error codes | Backend Agent |
| T010 | DB | Database initialization on startup | Database Agent |
| T011 | Auth | JWT utilities (create/verify tokens) | Backend Agent |
| T012 | Middleware | Authentication middleware (token extraction, verification) | Backend Agent |
| T013 | Handlers | Error handlers with error codes | Backend Agent |

**Success Criteria**: All foundational tasks pass unit tests; middleware properly verifies tokens

**Blockers for Phase 3**: None - Phase 3 can start once Phase 2 completes

---

### Phase 3: User Story 1-4 Implementation (31 tasks, T014-T044)
**P1 Critical: Core authentication features**
**Can Execute in Parallel**: US1 & US2, US3 & US4
**Primary Agents**: Backend Agent, Frontend Agent, Integration Agent

#### User Story 1: Signup (10 tasks)
**Status**: Ready for assignment
**Agent Assignment**: Backend + Frontend + Integration

| Task | Type | Story | Description | Agent |
|------|------|-------|-------------|-------|
| T014 | API | US1 | Signup route POST /api/auth/signup | Backend |
| T015 | Service | US1 | Signup service (validation, user creation) | Backend |
| T016 | Service | US1 | Password constraints (>= 8 chars) | Backend |
| T017 | Service | US1 | JWT token generation on signup | Backend |
| T018 | UI | US1 | Signup page with Better Auth form | Frontend |
| T019 | UI | US1 | SignupForm component | Frontend |
| T020 | UI | US1 | Form validation UI feedback | Frontend |
| T021 | Integration | US1 | Signup form API integration | Frontend |
| T022 | UI | US1 | Error handling and toast notifications | Frontend |
| T023 | Test | US1 | Integration test: signup flow | Integration |

**Acceptance Criteria**:
- Valid signup → account created, JWT issued, redirect to dashboard
- Duplicate email → 409 Conflict
- Invalid email → 422 Unprocessable Entity
- Weak password → 422 with message "Password must be at least 8 characters"

---

#### User Story 2: Signin (9 tasks)
**Status**: Ready for assignment
**Agent Assignment**: Backend + Frontend + Integration
**Parallelization**: Can run parallel with US1

| Task | Type | Story | Description | Agent |
|------|------|-------|-------------|-------|
| T024 | API | US2 | Signin route POST /api/auth/signin | Backend |
| T025 | Service | US2 | Signin service (credentials verification) | Backend |
| T026 | Service | US2 | User lookup and password validation | Backend |
| T027 | Service | US2 | JWT token generation on signin (with refresh rotation) | Backend |
| T028 | UI | US2 | Signin page with Better Auth form | Frontend |
| T029 | UI | US2 | SigninForm component | Frontend |
| T030 | Integration | US2 | Signin form API integration | Frontend |
| T031 | UI | US2 | Error handling and generic messages (no enumeration) | Frontend |
| T032 | Test | US2 | Integration test: signin flow (no user enumeration) | Integration |

**Acceptance Criteria**:
- Valid credentials → JWT issued, user redirected
- Invalid credentials → 401 with generic message (no hint about email vs password)
- Credentials rejected in < 100ms (timing consistency)

---

#### User Story 3: Token Storage (7 tasks)
**Status**: Ready for assignment
**Agent Assignment**: Frontend + Backend
**Parallelization**: Can run parallel with US4

| Task | Type | Story | Description | Agent |
|------|------|-------|-------------|-------|
| T033 | Integration | US3 | API client setup with JWT interceptor | Frontend |
| T034 | Integration | US3 | Request interceptor (Authorization header) | Frontend |
| T035 | Integration | US3 | Response interceptor (handle 401, trigger refresh) | Frontend |
| T036 | Integration | US3 | Token storage in httpOnly cookies | Frontend |
| T037 | Middleware | US3 | Backend cookie configuration (secure flags) | Backend |
| T038 | Middleware | US3 | JWT extraction from Authorization header | Backend |
| T039 | Test | US3 | Integration test: token storage verification | Integration |

**Acceptance Criteria**:
- Tokens stored in httpOnly cookies (inaccessible to JavaScript)
- Authorization header properly formatted: "Bearer <token>"
- Secure flags set (HttpOnly, Secure, SameSite)

---

#### User Story 4: JWT Verification (5 tasks)
**Status**: Ready for assignment
**Agent Assignment**: Backend + Integration

| Task | Type | Story | Description | Agent |
|------|------|-------|-------------|-------|
| T040 | API | US4 | Protected test endpoint (requires valid JWT) | Backend |
| T041 | Middleware | US4 | JWT middleware verification on protected routes | Backend |
| T042 | Middleware | US4 | User isolation (extract user_id from JWT) | Backend |
| T043 | Handlers | US4 | 401/403 error responses for invalid/missing tokens | Backend |
| T044 | Test | US4 | Integration test: JWT verification (valid/invalid/expired) | Integration |

**Acceptance Criteria**:
- Valid JWT → request proceeds with user_id injected
- Invalid JWT → 401 Unauthorized
- Expired JWT → 401 with "Token expired" message
- Missing JWT → 401 with "Token required" message
- Cross-user access → 403 Forbidden

---

### Phase 4: User Story 5-6 Implementation (10 tasks, T045-T054)
**P2 Important: Logout & Token Refresh**
**Depends on**: Phase 3 completion
**Can Execute in Parallel**: US5 & US6
**Primary Agents**: Frontend Agent, Backend Agent, Integration Agent

#### User Story 5: Logout (5 tasks)
**Status**: Ready for assignment (after Phase 3)
**Agent Assignment**: Frontend + Backend + Integration

| Task | Type | Story | Description | Agent |
|------|------|-------|-------------|-------|
| T045 | UI | US5 | Logout button component | Frontend |
| T046 | Integration | US5 | Logout function (clear tokens) | Frontend |
| T047 | Integration | US5 | Navigation redirect after logout | Frontend |
| T048 | API | US5 | Optional logout endpoint POST /api/auth/logout | Backend |
| T049 | Test | US5 | Integration test: logout flow | Integration |

**Acceptance Criteria**:
- Logout button visible in dashboard
- Clicking logout clears tokens and redirects to signin
- All protected routes require re-authentication after logout

---

#### User Story 6: Token Refresh (5 tasks)
**Status**: Ready for assignment (after Phase 3)
**Agent Assignment**: Frontend + Backend + Integration
**Parallelization**: Can run parallel with US5

| Task | Type | Story | Description | Agent |
|------|------|-------|-------------|-------|
| T050 | Integration | US6 | Proactive token expiry check (< 5 min remaining) | Frontend |
| T051 | Integration | US6 | Refresh token request and retry logic | Frontend |
| T052 | Integration | US6 | Frontend interceptor triggers refresh automatically | Frontend |
| T053 | Integration | US6 | Token rotation (new tokens on refresh) | Frontend |
| T054 | API | US6 | Backend refresh endpoint POST /api/auth/refresh | Backend |
| T055 | Service | US6 | Refresh token rotation implementation | Backend |
| T056 | Test | US6 | Backend refresh test (new tokens issued) | Integration |
| T057 | Test | US6 | Frontend interceptor test | Integration |

**Acceptance Criteria**:
- Frontend detects token < 5 min remaining
- Automatically calls refresh endpoint
- New tokens returned (both access and refresh rotated)
- Original request retried with new token
- Refresh succeeds within 200ms

---

### Phase 5: Polish & Integration (8 tasks, T058-T062)
**Cross-cutting: End-to-end tests, security validation**
**Depends on**: All phases complete
**Primary Agents**: Integration Agent

| Task | Type | Description | Agent |
|------|------|-------------|-------|
| T058 | Test | E2E flow test: signup → signin → logout | Integration |
| T059 | Test | E2E flow test: signup → signin → request refresh | Integration |
| T060 | Test | Security test: user isolation (cross-user prevention) | Integration |
| T061 | Test | Security test: password security (bcrypt, no plaintext) | Integration |
| T062 | Test | Playwright E2E test: complete user journey | Integration |

**Acceptance Criteria**:
- All auth flows work end-to-end
- User A cannot access User B's data (403 Forbidden)
- Passwords stored with bcrypt, never in plaintext
- 95% first-attempt success rate achieved

---

## 🚀 Execution Strategy

### Sequential Phases
1. **Phase 2** (Blocking): Complete first - all user stories depend on this
2. **Phase 3** (Parallel): US1 & US2 can run parallel, US3 & US4 can run parallel
3. **Phase 4** (Parallel): US5 & US6 can run parallel after Phase 3
4. **Phase 5** (Sequential): Run after all phases complete

### Agent Coordination
- **Backend Agent**: T007-T017, T024-T027, T040-T043, T048, T054-T056
- **Frontend Agent**: T005-T006, T018-T022, T028-T031, T033-T036, T045-T047, T050-T053, T058-T062
- **Database Agent**: T007-T010
- **Integration Agent**: T023, T032, T039, T044, T049, T057, T060-T062

### Daily Standup Template
```
Phase: [Phase Number]
Completed Tasks: [T### description - status]
In Progress: [T### description - % complete]
Blockers: [Any blocking issues]
Next: [Next task to start]
```

---

## 📊 Success Metrics

### Phase 2 (Foundational)
- [ ] All 7 tasks pass unit tests
- [ ] Database successfully initializes with User table
- [ ] JWT utilities create/verify tokens correctly
- [ ] Middleware properly extracts and verifies tokens

### Phase 3 (User Stories 1-4)
- [ ] Signup creates accounts and issues JWTs
- [ ] Signin validates credentials and issues JWTs
- [ ] Tokens stored securely in httpOnly cookies
- [ ] Protected endpoints enforce JWT verification
- [ ] User isolation prevents cross-user access
- [ ] All 4 user stories have passing integration tests

### Phase 4 (User Stories 5-6)
- [ ] Logout clears tokens and redirects
- [ ] Token refresh works before expiry
- [ ] New tokens issued on refresh (rotation)
- [ ] Automatic retry on 401 works seamlessly

### Phase 5 (Polish)
- [ ] E2E flow tests cover signup → signin → logout
- [ ] Security tests verify user isolation
- [ ] 95% first-attempt success rate achieved
- [ ] All 62 tasks marked complete

---

## 📝 Implementation Notes

### Testing Approach (TDD)
1. Write test file with acceptance criteria
2. Implement feature to make test pass
3. Refactor if needed while keeping tests green

### Error Handling
- Use error codes for backend logging (e.g., AUTH_INVALID_CREDENTIALS)
- Show generic messages to users (no information leakage)
- Include error codes in responses: `{"error": "AUTH_INVALID_CREDENTIALS", "message": "Invalid credentials", "status_code": 401}`

### User Isolation
- **Rule**: Extract user_id from JWT `sub` claim
- **Never**: Use user_id from request parameter
- **Always**: Filter queries by extracted user_id

### Security Checklist
- [ ] BETTER_AUTH_SECRET >= 32 characters
- [ ] Bcrypt cost factor >= 10
- [ ] Tokens stored in httpOnly cookies
- [ ] All endpoints HTTPS in production
- [ ] No plaintext passwords in logs
- [ ] No user enumeration (generic error messages)

---

## 🔄 Next Steps

### For Backend Agent
1. Read `specs/002-user-auth/plan.md` (architecture overview)
2. Read `specs/002-user-auth/tasks.md` (detailed tasks)
3. Start with Phase 2 foundational tasks (T007-T013)
4. Proceed with Phase 3 backend tasks (T014-T017, T024-T027, T040-T043)
5. Finish with Phase 4 backend tasks (T054-T056)

### For Frontend Agent
1. Read `specs/002-user-auth/plan.md` (architecture overview)
2. Read `specs/002-user-auth/tasks.md` (detailed tasks)
3. Set up frontend dependencies after Phase 1 (npm install)
4. Implement Phase 3 frontend tasks (T018-T022, T028-T031, T033-T036)
5. Implement Phase 4 frontend tasks (T045-T047, T050-T053)

### For Database Agent
1. Read `specs/002-user-auth/plan.md` (database schema)
2. Implement Phase 2 tasks (T007-T010)
3. Verify User table schema and indexes

### For Integration Agent
1. Read all specs (spec.md, plan.md, tasks.md)
2. Start writing tests after feature implementations
3. Run integration tests at end of each phase
4. Execute Phase 5 end-to-end and security tests

---

## 📞 Communication

**Branch**: `002-user-auth` (keep all work on this branch)
**Documentation**: All specs in `specs/002-user-auth/`
**Status**: Updated in this file as phases complete
**Issues**: Track blockers and dependencies

---

**Implementation Status**: ✅ READY FOR AGENT ASSIGNMENT
**Last Updated**: 2026-01-12
**Next Milestone**: Phase 2 Completion
