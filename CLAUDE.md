# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

---

# Phase II: Todo Full-Stack Web Application

## Project Overview

Transform the Phase 1 console app into a modern, multi-user web application with persistent storage using the Agentic Development Stack workflow.

**Phase II Objective:** Implement a responsive web application with user authentication, RESTful API endpoints, and persistent data storage.

### Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 16+ (App Router) |
| **Backend** | Python FastAPI |
| **ORM** | SQLModel |
| **Database** | Neon Serverless PostgreSQL |
| **Authentication** | Better Auth + JWT |
| **Development** | Claude Code + Spec-Kit Plus (No manual coding) |

### Phase II Features (Basic Level)

1. **User Authentication** – Signup/signin with Better Auth
2. **Persistent Storage** – PostgreSQL via Neon
3. **RESTful API** – 6 task endpoints with JWT validation
4. **Responsive UI** – Next.js with Tailwind CSS
5. **Data Isolation** – User-scoped task management

## Specialized Agents for Phase II

Use these agents for their respective domains:

### 1. **Auth Agent** (`auth-agent`)
**Responsible for:** Authentication infrastructure and setup

**When to Use:**
- Setting up Better Auth configuration
- Implementing JWT token generation
- Configuring shared secrets (BETTER_AUTH_SECRET)
- Testing signup/signin flows

**Skills Used:** `auth_setup`, `auth_routes`

**Key Deliverables:**
- Better Auth configured with JWT plugin
- Signup endpoint: `POST /api/auth/signup` (201 Created)
- Signin endpoint: `POST /api/auth/signin` (200 OK)
- Refresh endpoint: `POST /api/auth/refresh`
- Tokens contain user_id in `sub` claim

**Output to Expect:**
- Environment variables configured
- Token generation working
- 11+ auth flow tests passing
- No secrets in code

---

### 2. **Database Agent** (`database-agent`)
**Responsible for:** Data modeling and database setup

**When to Use:**
- Designing User and Task models
- Setting up Neon PostgreSQL connection
- Creating indexes for performance
- Configuring connection pooling

**Skills Used:** `schema_design`, `db_connection`

**Key Deliverables:**
- User model (UUID, email unique, password_hash)
- Task model (UUID, user_id FK, title, status, priority)
- One-to-many relationship with cascade delete
- Indexes on (user_id, status) and (user_id, due_date)
- Health check endpoint: `GET /health/db`
- Alembic migrations configured

**Output to Expect:**
- Schema created and validated
- Connection pooling: min 5, max 20
- Migration scripts generated
- 17+ integration tests passing

---

### 3. **API Agent** (`api-agent`)
**Responsible for:** REST endpoint implementation and error handling

**When to Use:**
- Implementing 6 CRUD endpoints
- Adding JWT middleware to endpoints
- Setting up error handling and validation
- Creating request/response models

**Skills Used:** `task_crud`, `jwt_middleware`, `error_handling`

**Key Deliverables:**
- GET /api/tasks (list, paginated, filtered)
- GET /api/tasks/{id} (single task)
- POST /api/tasks (create, 201)
- PUT /api/tasks/{id} (full update)
- PATCH /api/tasks/{id} (partial update)
- DELETE /api/tasks/{id} (204)
- JWT validation on all endpoints
- Pydantic models for validation
- Error responses with proper status codes

**Output to Expect:**
- 6 endpoints fully functional
- 45+ endpoint tests passing
- 100% user isolation verified
- OpenAPI/Swagger documentation

---

### 4. **Frontend Agent** (`frontend-agent`)
**Responsible for:** Next.js page structure and React components

**When to Use:**
- Creating page structure with App Router
- Building TaskList, TaskForm, TaskItem components
- Setting up React Query for data fetching
- Implementing responsive design

**Skills Used:** `nextjs_pages`, `ui_components`, `api_client`

**Key Deliverables:**
- Root layout with providers (QueryClient, Theme)
- Auth routes: /login, /signup
- Dashboard routes: /tasks, /tasks/[id]
- TaskList component (pagination, filtering, sorting)
- TaskForm component (create/edit modal)
- TaskItem component (display with actions)
- API client with automatic JWT attachment
- React Query hooks for data fetching
- Dark mode support
- Mobile-responsive design

**Output to Expect:**
- 7+ pages created
- 32+ component tests passing
- React Query caching working
- Tailwind + ShadCN UI integrated
- Lighthouse score > 90

---

### 5. **Integration Agent** (`integration-agent`)
**Responsible for:** End-to-end testing and security validation

**When to Use:**
- Testing complete auth flows (signup → login → logout)
- Validating user isolation across layers
- Performing security audits
- Testing integration between components

**Skills Used:** `auth_flow`, `security_validation`

**Key Deliverables:**
- Complete auth flow tests (11+ tests)
- User isolation tests (15+ tests)
- Cross-user access prevention verified
- Security vulnerability audit
- Integration tests (8+ tests)
- No hardcoded secrets
- No plaintext passwords
- Proper error messages (no enumeration)

**Output to Expect:**
- 34+ integration tests passing
- 0 security vulnerabilities
- Security audit report
- Recommendations for improvements

---

## Development Workflow for Phase II

### Step 1: Specification Phase
```bash
# Create feature specifications using Claude Code
# Run: /sp.specify
# Defines: Requirements, acceptance criteria, user stories
```

### Step 2: Planning Phase
```bash
# Generate architectural plan
# Run: /sp.plan
# Produces: Architecture decisions, data models, API contracts
```

### Step 3: Task Breakdown Phase
```bash
# Break plan into testable tasks
# Run: /sp.tasks
# Generates: Task IDs, dependencies, acceptance criteria
```

### Step 4: Implementation Phase (Agent-Driven)

#### a. Database Setup (DB Agent)
```bash
# Launch database-agent to set up schema
# Agent uses: schema_design, db_connection skills
# Outputs: Models, migrations, connection pooling
```

#### b. Authentication Setup (Auth Agent)
```bash
# Launch auth-agent to implement auth
# Agent uses: auth_setup, auth_routes skills
# Outputs: Signup/signin endpoints, token generation
```

#### c. API Implementation (API Agent)
```bash
# Launch api-agent to implement CRUD endpoints
# Agent uses: task_crud, jwt_middleware, error_handling skills
# Outputs: 6 endpoints, validation, error handling
```

#### d. Frontend Development (Frontend Agent)
```bash
# Launch frontend-agent to build UI
# Agent uses: nextjs_pages, ui_components, api_client skills
# Outputs: Pages, components, data fetching
```

#### e. Integration Testing (Integration Agent)
```bash
# Launch integration-agent for end-to-end validation
# Agent uses: auth_flow, security_validation skills
# Outputs: Test results, security audit, recommendations
```

### Step 5: Validation Phase
```bash
# Verify all acceptance criteria met
# Run all tests (unit, integration, E2E)
# Security audit complete
# Performance validated (Lighthouse > 90)
```

### Step 6: Documentation Phase
```bash
# Create PHR (Prompt History Records)
# Generate ADRs for architectural decisions
# Document API endpoints (Swagger)
# Create user guide
```

---

## API Endpoints Overview

### Authentication Endpoints
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | /api/auth/signup | Create user account | 201 Created |
| POST | /api/auth/signin | Login with credentials | 200 OK |
| POST | /api/auth/refresh | Refresh access token | 200 OK |

### Task CRUD Endpoints
| Method | Endpoint | Description | Status | User Isolation |
|--------|----------|-------------|--------|-----------------|
| GET | /api/tasks | List user's tasks | 200 OK | Filtered by user_id |
| POST | /api/tasks | Create new task | 201 Created | user_id from JWT |
| GET | /api/tasks/{id} | Get task details | 200 OK | Ownership verified |
| PUT | /api/tasks/{id} | Replace task | 200 OK | Ownership verified |
| PATCH | /api/tasks/{id} | Partial update | 200 OK | Ownership verified |
| DELETE | /api/tasks/{id} | Delete task | 204 No Content | Ownership verified |

---

## Authentication Flow (Better Auth + FastAPI)

### Challenge: Cross-Layer Authentication
Better Auth (JavaScript/TypeScript) runs on Next.js frontend. FastAPI backend (Python) must verify JWT tokens.

### Solution: JWT Tokens
1. **Frontend (Next.js):** Better Auth issues JWT on login
2. **Token Content:** Includes user_id (`sub` claim), email, expiration
3. **API Integration:** Frontend attaches token to every request
   ```
   Authorization: Bearer <jwt_token>
   ```
4. **Backend Validation:** FastAPI middleware verifies token signature using shared secret
5. **User Isolation:** Extract user_id from token, filter all queries

### Security Contract
- **Secret Sharing:** BETTER_AUTH_SECRET in both frontend and backend .env
- **No Manual Token:** Tokens auto-generated by Better Auth
- **No Secrets in Code:** All secrets in .env (never committed)
- **Token Refresh:** Auto-refresh on 401, retry original request
- **User Isolation:** All database queries filtered by user_id from token

---

## Critical Implementation Rules for Phase II

### 1. Authentication
- ✅ Use Better Auth for signup/signin
- ✅ JWT tokens contain user_id in `sub` claim
- ✅ Share BETTER_AUTH_SECRET between frontend and backend
- ❌ NEVER hardcode tokens or secrets
- ❌ NEVER skip JWT verification

### 2. User Isolation
- ✅ Extract user_id from JWT token (never from request)
- ✅ Filter ALL queries by user_id
- ✅ Verify resource ownership before returning/modifying
- ✅ Return 403 Forbidden (not 404) for cross-user access
- ❌ NEVER return other users' data

### 3. Database
- ✅ Use Neon PostgreSQL via SQLModel
- ✅ Create proper indexes (user_id, status, due_date)
- ✅ Enforce unique constraints (email)
- ✅ Set up connection pooling (5-20)
- ❌ NEVER store plaintext passwords

### 4. API Design
- ✅ Use RESTful conventions (GET, POST, PUT, PATCH, DELETE)
- ✅ Return proper HTTP status codes
- ✅ Validate all input with Pydantic
- ✅ Provide meaningful error messages
- ❌ NEVER expose internal errors to clients

### 5. Frontend
- ✅ Use Next.js App Router (not Pages Router)
- ✅ Server components by default, client components only for interactivity
- ✅ Use React Query for data fetching and caching
- ✅ Implement dark mode support
- ✅ Make responsive (mobile-first)
- ❌ NEVER hardcode API URLs (use env vars)

### 6. Testing
- ✅ Write tests BEFORE implementation (TDD)
- ✅ Test auth flows end-to-end
- ✅ Test user isolation (cross-user prevention)
- ✅ Test error scenarios
- ✅ Achieve 100% coverage of critical paths
- ❌ NEVER skip security tests

### 7. Development Process
- ✅ Use Claude Code agents for all implementation
- ✅ Create specs before coding
- ✅ Use agents for their specialized domains
- ✅ Validate with Integration Agent
- ❌ NEVER write code manually
- ❌ NEVER skip planning phase

---

## Success Criteria for Phase II

### Phase II is Complete When:

✅ **Authentication**
- Signup creates user with hashed password
- Signin returns JWT tokens
- Protected endpoints require valid JWT
- Token refresh works
- Logout clears authentication

✅ **API Endpoints**
- 6 CRUD endpoints fully functional
- Proper HTTP status codes
- User isolation enforced
- Input validation working
- Error handling comprehensive

✅ **Database**
- User and Task models created
- Relationships configured
- Indexes optimized
- Migrations working
- Data persists in Neon

✅ **Frontend**
- All pages and routes accessible
- Components render correctly
- API integration working
- Dark mode functional
- Mobile responsive

✅ **Security**
- No hardcoded secrets
- User isolation verified
- Cross-user access prevented
- Passwords hashed
- Tokens properly signed

✅ **Testing**
- 45+ API tests passing
- 32+ Component tests passing
- 34+ Integration tests passing
- 0 security vulnerabilities
- 100% critical path coverage

✅ **Documentation**
- PHRs created for all work
- ADRs for significant decisions
- API documented (Swagger)
- Code commented (task references)
- Security audit complete

---

## Agent Usage Examples

### Example 1: Database Setup
```
User: "Set up the database schema and connection"

→ Launch database-agent
→ Agent designs User and Task models
→ Agent configures Neon PostgreSQL
→ Agent creates indexes and constraints
→ Agent generates Alembic migrations
→ Agent creates 17 integration tests

Output: Schema created, connected to Neon, ready for data
```

### Example 2: Authentication Implementation
```
User: "Implement signup and signin"

→ Launch auth-agent
→ Agent configures Better Auth with JWT
→ Agent implements signup endpoint (POST /api/auth/signup)
→ Agent implements signin endpoint (POST /api/auth/signin)
→ Agent creates 11 auth flow tests

Output: Auth endpoints working, tokens generated, tests passing
```

### Example 3: Complete API Implementation
```
User: "Build the task CRUD API with authentication"

→ Launch api-agent
→ Agent implements 6 endpoints
→ Agent adds JWT middleware
→ Agent implements error handling
→ Agent creates 45 endpoint tests

Output: All endpoints functional, secure, well-tested
```

### Example 4: Frontend Build
```
User: "Build the task management UI"

→ Launch frontend-agent
→ Agent creates Next.js page structure
→ Agent builds React components (TaskList, TaskForm, TaskItem)
→ Agent integrates API client with JWT
→ Agent creates 32 component tests

Output: UI complete, responsive, dark mode working
```

### Example 5: End-to-End Validation
```
User: "Validate the complete implementation"

→ Launch integration-agent
→ Agent tests complete auth flows
→ Agent validates user isolation
→ Agent performs security audit
→ Agent creates comprehensive test suite

Output: 34 tests passing, 0 vulnerabilities, secure architecture
```

---

## Next Steps (Post-Phase II)

- **Phase III:** AI Chatbot with OpenAI Agents SDK + MCP
- **Phase IV:** Local Kubernetes with Minikube + Dapr
- **Phase V:** Cloud-Native Multi-Cloud with Kafka + Dapr

---

**Note:** All Phase II development MUST use the Agentic Development Stack. Manual coding is not permitted. Use agents for their specialized domains.
