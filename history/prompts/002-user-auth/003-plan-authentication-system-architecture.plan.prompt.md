---
id: "003"
title: "Plan Authentication System Architecture"
stage: "plan"
feature: "002-user-auth"
branch: "002-user-auth"
date: "2026-01-12"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
user: "system"
command: "/sp.plan"

labels:
  - "authentication"
  - "jwt"
  - "architecture"
  - "planning"
  - "phase2"

links:
  spec: "/specs/002-user-auth/spec.md"
  plan: "/specs/002-user-auth/plan.md"
  ticket: "null"
  adr: "null"
  pr: "null"

files:
  - "/specs/002-user-auth/plan.md"

tests: []
---

# Prompt History Record: Plan Authentication System Architecture

## Summary

Executed `/sp.plan` workflow to create comprehensive implementation architecture for JWT-based authentication system. Designed full-stack web application structure (frontend + backend + database) with 8 documented architecture decisions, detailed integration flows, testing strategy, and project structure.

## Plan Overview

### Technical Context
- **Backend**: Python 3.13+ with FastAPI, python-jose[cryptography], SQLModel, asyncpg
- **Frontend**: TypeScript 5.3+ with Next.js 16+, better-auth, @tanstack/react-query, axios
- **Database**: Neon PostgreSQL with SQLAlchemy ORM via SQLModel
- **Testing**: pytest (backend), Jest/Vitest + Playwright (frontend)
- **Performance Goals**: Signup p95 < 500ms, Signin p95 < 300ms, Token verification < 50ms
- **Constraints**: 7-day access token, 30-day refresh token, HTTPS required, 99.9% SLO

### Constitution Check (All Gates Pass)
✅ Spec-Driven Development
✅ Progressive Complexity (Phase 2)
✅ Test-First Development (TDD)
✅ User Experience Excellence
✅ Security & Authentication (JWT, user isolation)
✅ Code Quality Standards

### Project Structure

**Documentation**:
```
specs/002-user-auth/
├── spec.md ✅ (Complete)
├── plan.md ✅ (This file)
├── research.md (Phase 0 - NEXT)
├── data-model.md (Phase 1 - NEXT)
├── contracts/ (Phase 1 - NEXT)
└── tasks.md (Phase 2 - /sp.tasks)
```

**Source Code**:
```
backend/src/phase2/auth/
├── models.py (User SQLModel)
├── routes.py (POST /signup, /signin, /refresh, /logout)
├── jwt.py (JWT verification middleware)
└── schemas.py (Pydantic models)

frontend/src/app/
├── (auth)/signup/page.tsx
├── (auth)/signin/page.tsx
├── (dashboard)/layout.tsx (protected)
└── lib/auth.ts (Better Auth + JWT setup)
```

---

## Architecture Decisions Documented

### 1. JWT Algorithm & Secret Management
- **Decision**: HS256 with shared BETTER_AUTH_SECRET (32+ chars)
- **Rationale**: Symmetrical algorithm sufficient for single deployment, simpler than RS256
- **Alternative Rejected**: RS256 (adds key rotation complexity)

### 2. Token Refresh Strategy (From Clarifications)
- **Decision**: Proactive refresh when < 5 min remaining
- **Rationale**: Prevents 401 errors during active sessions
- **Implementation**: Frontend interceptor monitors expiry, calls refresh before timeout

### 3. Refresh Token Rotation (From Clarifications)
- **Decision**: Issue new refresh token with each access token refresh
- **Rationale**: Prevents replay attacks, OAuth 2.0 best practice
- **Implementation**: Backend rotates both tokens; frontend updates both

### 4. Token Storage
- **Decision**: httpOnly cookies (secure, XSS-proof)
- **Rationale**: Prevents XSS attacks, required by spec FR-020
- **Alternative Rejected**: localStorage (XSS vulnerable), sessionStorage (cleared on tab close)

### 5. Error Response Format (From Clarifications)
- **Decision**: Machine-readable error codes + generic user messages
- **Rationale**: Enables debugging while preventing information leakage
- **Format**: `{"error": "AUTH_INVALID_CREDENTIALS", "message": "Invalid credentials", "status_code": 401}`

### 6. User Isolation Enforcement
- **Decision**: Extract user_id from JWT `sub` claim; filter all queries by extracted user_id
- **Rationale**: Database-enforced security, prevents cross-user access
- **Alternative Rejected**: Frontend-only isolation (backend must verify)

### 7. Password Hashing
- **Decision**: bcrypt with cost ≥ 10 (via passlib[bcrypt])
- **Rationale**: Industry standard, automatic salt, slow design prevents brute force
- **Alternative Rejected**: argon2 (overkill for MVP), plaintext (security breach)

### 8. API Endpoint Structure
- **Decision**: RESTful endpoints:
  - POST /api/auth/signup → 201 Created
  - POST /api/auth/signin → 200 OK
  - POST /api/auth/refresh → 200 OK
  - POST /api/auth/logout → 204 No Content
- **Rationale**: RESTful conventions, clear semantics, standard HTTP codes
- **Alternative Rejected**: GraphQL (overkill), custom RPC (non-standard)

---

## Integration Flows Documented

### Frontend ↔ Backend Communication
```
User submits credentials → Better Auth form
    ↓
Frontend calls POST /api/auth/signup or /signin
    ↓
Backend: verify credentials, hash password, generate JWT + refresh token
    ↓
Backend: return tokens (set in httpOnly cookies)
    ↓
Frontend: store tokens, update auth state
    ↓
Subsequent requests: axios interceptor attaches JWT in Authorization header
    ↓
Backend: JWT middleware verifies token, extracts user_id
    ↓
Request proceeds with user_id in context (never from request)
    ↓
API endpoint: filters response by user_id (enforces isolation)
```

### Token Refresh Flow
```
Frontend detects access token < 5 min remaining
    ↓
Frontend: POST /api/auth/refresh
    ↓
Backend: verify refresh token, issue new access + new refresh token
    ↓
Backend: return new tokens (rotated)
    ↓
Frontend: update stored tokens
    ↓
Original request: retry with new access token → succeeds
```

### Error Handling Flow
```
User submits invalid credentials
    ↓
Backend: logs {"error": "AUTH_INVALID_CREDENTIALS", ...}
    ↓
Frontend: displays "Invalid credentials" (generic)
    ↓
Backend: logs detailed error with code for monitoring
    ↓
No information leakage (no hint about email vs password)
```

---

## Testing Strategy

### Backend Tests (pytest)
- Unit tests: Password hashing, JWT generation, token verification
- Integration tests: Signup → Signin → Protected request (complete flow)
- Security tests: User isolation (User A ≠ User B data), token validation

### Frontend Tests (Jest/Vitest + Playwright)
- Component tests: SignupForm, SigninForm rendering and validation
- Integration tests: Form submission → API call → token storage → redirect
- E2E tests: Complete journey: signup → signin → access protected page → logout

### Security Tests (Integration Agent)
- Token verification: Valid token succeeds; invalid/expired token rejected (401)
- User isolation: Cross-user access returns 403 Forbidden
- Password security: Plaintext never in logs, bcrypt hash verified
- Error messages: Generic (no enumeration), codes for debugging

---

## Success Criteria Mapping

All 10 success criteria from spec mapped to implementation/testing:

- ✅ SC-001: Signup in < 2 min (form UX design)
- ✅ SC-002: 100% token issuance (implementation validates)
- ✅ SC-003: Endpoints < 500ms p95 (performance testing)
- ✅ SC-004: Invalid credentials < 100ms (implementation validates)
- ✅ SC-005: Token expiry enforced (implementation validates)
- ✅ SC-006: Refresh < 200ms (performance testing)
- ✅ SC-007: Cross-user access blocked 403 (security testing)
- ✅ SC-008: Passwords never in plaintext (code review)
- ✅ SC-009: 95% first-attempt success (acceptance testing)
- ✅ SC-010: 1000 concurrent requests handled (load testing)

---

## Planning Artifacts Created

### Primary Deliverable
**File**: `/specs/002-user-auth/plan.md` (365 lines)

Content:
- Summary: Complete architecture overview
- Technical Context: Languages, dependencies, storage, testing, performance goals
- Constitution Check: All 6 gates pass
- Project Structure: Documentation + source code trees
- Complexity Tracking: No violations, all Phase 2 aligned
- Architecture Decisions: 8 decisions with rationale and alternatives
- Integration Points: Frontend ↔ Backend, token refresh, error handling flows
- Testing Strategy: Unit, integration, E2E, security tests
- Success Criteria: All 10 mapped to implementation
- Next Steps: Phase 0 research tasks, Phase 1 design deliverables

### Phase Completion Status

**Phase 0 (Research) - Pending**
- [ ] Better Auth SDK JWT plugin research
- [ ] JWT payload structure documentation
- [ ] python-jose compatibility verification
- [ ] httpOnly cookie security best practices
- [ ] BETTER_AUTH_SECRET rotation strategy

**Phase 1 (Design) - Pending**
- [ ] research.md with technical findings
- [ ] data-model.md with User entity, relationships
- [ ] contracts/auth-routes.openapi.json
- [ ] contracts/error-responses.json
- [ ] quickstart.md with dev setup
- [ ] Agent context updates

**Phase 2 (Tasks) - Pending**
- [ ] Generate tasks.md via `/sp.tasks`
- [ ] Detail implementation tasks with acceptance criteria
- [ ] Assign to agents (Backend, Frontend, Database, Integration)

**Phase 3 (Implementation) - Future**
- [ ] Backend Agent: auth routes, JWT middleware, User model
- [ ] Database Agent: User schema, indexes, relationships
- [ ] Frontend Agent: signup/signin pages, API client, token management
- [ ] Integration Agent: E2E tests, security validation

---

## Key Planning Decisions

### 1. No Research Phase Required (Phase 0 Skipped)
- **Reason**: All architectural decisions already clarified via `/sp.clarify`
- **Rationale**: Specification included technical requirements from user input
- **Alternative**: Could conduct research, but would be redundant
- **Justification**: Proceeding to Phase 1 (Design) or Phase 2 (Tasks) is appropriate next step

### 2. Project Type: Web Application (Frontend + Backend)
- **Architecture**: Separated frontend (Next.js) and backend (FastAPI)
- **Integration**: HTTP REST API with JWT authentication
- **Rationale**: Aligns with Phase 2 constitutional requirement for full-stack web
- **Alternative Rejected**: Monolithic backend (loses frontend flexibility)

### 3. Security-First Design
- **Decisions**: JWT, httpOnly cookies, user isolation, bcrypt, token rotation
- **Rationale**: All decisions prioritize security (from phase 2 constitution)
- **Alternative Rejected**: Simpler but less secure approaches documented

---

## Decision Logic

### Why HS256 (Not RS256)?
- MVP doesn't need asymmetric key management
- Shared secret simpler for single deployment
- Can migrate to RS256 in later phases

### Why Proactive Refresh (Not Reactive)?
- Prevents user-facing 401 errors during active sessions
- Better UX (no unexpected logouts)
- Spec clarification confirmed this approach

### Why Refresh Token Rotation?
- Security best practice (prevents replay attacks)
- OAuth 2.0 standard pattern
- Limits exposure window if token leaked

### Why httpOnly Cookies?
- XSS attack prevention (inaccessible to JavaScript)
- Spec mandates this (FR-020)
- Industry standard for token storage

---

## Next Command Recommendation

**Option 1: Continue Planning (Recommended)**
- Run `/sp.plan --phase 0` to generate research.md
- Then `/sp.plan --phase 1` to generate data-model.md and contracts

**Option 2: Skip to Tasks**
- Run `/sp.tasks` to generate tasks.md with implementation tasks
- Skip research/design artifacts if confident in architecture

**Option 3: Start Implementation**
- Use agents directly to implement from this plan
- Agents reference this plan for architecture guidance

**Recommended**: Option 1 (Complete planning artifacts for traceability)

---

## Validation Checklist

- [x] Technical context fully specified
- [x] Constitution check: All gates pass
- [x] Project structure defined (frontend, backend, database)
- [x] Architecture decisions: 8 documented with rationale
- [x] Integration flows: Frontend ↔ Backend detailed
- [x] Testing strategy: Unit, integration, E2E, security
- [x] Success criteria: All 10 mapped to implementation
- [x] Phase gates: Ready for Phase 0 or Phase 2
- [x] No critical ambiguities remaining
- [x] All clarifications (Q1, Q2, Q3) incorporated

---

**Plan Status**: ✅ COMPLETE AND READY FOR NEXT PHASE

**Plan Quality**: Comprehensive, architecture-driven, testable, security-focused

**Recommended Next Step**: Proceed to `/sp.tasks` for task generation OR continue with Phase 0/1 research/design artifacts

---

**Record Date**: 2026-01-12
**Plan Complete**: Yes
**Tasks Ready**: Pending /sp.tasks
**Implementation Ready**: Pending /sp.tasks + agent assignment
**Feature Branch**: `002-user-auth`
