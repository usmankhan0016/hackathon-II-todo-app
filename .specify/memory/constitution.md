# Evolution of Todo - Project Constitution
<!-- 5-Phase Todo Application: Console → Web → AI Chatbot → Local K8s → Cloud-Native -->

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
**All code must be generated from specifications via Claude Code. Manual coding is prohibited.**

- **Spec-First Workflow**: Every feature follows the mandatory sequence: Specify → Plan → Tasks → Implement
- **Task Traceability**: Every code file must include comments referencing Task IDs and Spec sections
- **Iterative Refinement**: Specifications must be refined until Claude Code generates correct, complete output
- **No Freestyle Coding**: Developers may not write code directly; all implementation via Claude Code from approved specs
- **Single Source of Truth**: The specification is the authoritative source for requirements, architecture, and acceptance criteria

### II. Progressive Complexity Across 5 Phases
**Each phase builds incrementally on the previous phase's foundation.**

- **Phase 1 - Console App (Python)**: In-memory CRUD with Rich CLI interface
- **Phase 2 - Full-Stack Web**: Next.js frontend + FastAPI backend + Neon PostgreSQL + Better Auth
- **Phase 3 - AI Chatbot**: OpenAI Agents SDK + MCP server for natural language task management
- **Phase 4 - Local Kubernetes**: Minikube deployment with Dapr for state management
- **Phase 5 - Cloud-Native**: Multi-cloud deployment with Kafka event streaming and Dapr orchestration

**Phase Independence**: Each phase must be fully functional and testable as a standalone system
**Backward Compatibility**: Later phases may reference but must not break earlier phase implementations

### III. Test-First Development (NON-NEGOTIABLE)
**TDD is mandatory across all phases. No implementation without passing tests.**

- **Red-Green-Refactor Cycle**: Tests written → User approved → Tests fail → Implement → Tests pass → Refactor
- **Acceptance Criteria as Tests**: Every spec requirement must have corresponding test cases in tasks.md
- **Phase-Specific Testing**:
  - **Phase 1**: Python pytest with unit tests for all CRUD operations
  - **Phase 2**: Frontend (Vitest/Jest), Backend (pytest), E2E (Playwright)
  - **Phase 3**: MCP tool tests, agent conversation tests, integration tests
  - **Phase 4**: Container tests, Kubernetes manifest validation, Dapr component tests
  - **Phase 5**: End-to-end cloud deployment tests, event streaming validation, multi-cloud compatibility tests

### IV. User Experience Excellence
**Every phase must deliver a polished, production-ready user experience.**

**Phase 1 - Terminal UI Standards**:
- Modern, attractive interface using Rich library
- Color-coded output: Green (completed), Yellow (pending), Red (overdue)
- Visual hierarchy with emojis: 📝 (tasks), ✓ (done), ⏳ (pending), 🔴 (overdue)
- Styled panels, bordered tables, and consistent formatting
- Interactive menu system with clear navigation

**Phase 2 - Web UI Standards**:
- Responsive design (mobile-first with Tailwind CSS)
- Loading states and optimistic UI updates
- Toast notifications for user actions
- Accessible (WCAG 2.1 AA compliance)
- Dark/light mode support

**Phase 3 - Conversational UI Standards**:
- Natural language understanding for task commands
- Contextual responses with task previews
- Graceful error handling with helpful suggestions
- Conversation history persistence

**Phase 4 & 5 - Operational UI**:
- Health check dashboards
- Logging and monitoring interfaces
- Deployment status visibility

### V. Security and Authentication
**Security is built-in from Phase 2 onward.**

**Phase 2+**:
- JWT-based authentication (Better Auth)
- `BETTER_AUTH_SECRET` shared between frontend/backend
- User isolation: each user sees only their tasks
- All API endpoints require valid JWT tokens
- 401 Unauthorized for missing/invalid tokens
- No secrets in code or version control (use `.env` files)

**Phase 5 Additional**:
- Secret management via cloud provider (Azure Key Vault, GCP Secret Manager, Oracle Vault)
- Encrypted event streaming
- Service mesh security policies (mTLS)

### VI. Code Quality and Standards

**Python (Phases 1, 2 backend, 3 backend, 4-5 services)**:
- Python 3.13+
- PEP 8 compliance
- Type hints on all functions and methods
- Comprehensive docstrings (Google style)
- Dataclasses or Pydantic models for data structures
- UV for dependency management

**TypeScript (Phases 2-3 frontend)**:
- TypeScript strict mode enabled
- Server components by default (Next.js App Router)
- Client components only for interactivity
- Type-safe API calls with Zod validation
- ESLint + Prettier enforcement

**General**:
- No commented-out code in production
- Meaningful variable/function names
- Single Responsibility Principle
- DRY (Don't Repeat Yourself) but avoid premature abstraction
- Clear error messages with actionable guidance

### VII. Architecture Standards

**Monorepo Structure**:
```
todo-app/
├── .specify/              # SpecKit Plus templates and scripts
│   ├── memory/
│   │   └── constitution.md
│   ├── templates/
│   └── scripts/
├── specs/                 # All specifications organized by phase
│   ├── phase1/
│   ├── phase2/
│   ├── phase3/
│   ├── phase4/
│   └── phase5/
├── src/
│   ├── phase1/           # Console app
│   ├── phase2/           # Full-stack web
│   │   ├── frontend/
│   │   └── backend/
│   ├── phase3/           # AI chatbot
│   ├── phase4/           # K8s local
│   └── phase5/           # Cloud-native
├── history/
│   ├── prompts/          # Prompt History Records
│   │   ├── constitution/
│   │   ├── general/
│   │   └── <feature-name>/
│   └── adr/              # Architecture Decision Records
└── tests/                # Phase-specific test suites
```

**Phase-Specific Architecture**:

**Phase 1**:
- `models.py` - Task dataclass definitions
- `task_manager.py` - In-memory CRUD operations (Python list)
- `cli.py` - User input and command routing
- `ui.py` - Rich library components (panels, tables, messages)
- `main.py` - Entry point and main loop

**Phase 2**:
- Frontend: Next.js 16+ App Router, TypeScript, Tailwind CSS, ShadCN UI
- Backend: FastAPI, SQLModel ORM, Pydantic validation
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- RESTful API: `/api/{user_id}/tasks` endpoints

**Phase 3**:
- Frontend: OpenAI ChatKit
- AI: OpenAI Agents SDK
- MCP Server: Official MCP SDK exposing task operations as tools
- Backend: Stateless FastAPI endpoints
- Database: Neon PostgreSQL for conversation history

**MCP Tools Required**:
1. `add_task` - Create new task
2. `list_tasks` - Retrieve tasks with filters
3. `update_task` - Modify existing task
4. `delete_task` - Remove task
5. `search_tasks` - Full-text search

**Phase 4**:
- Containerization: Docker multi-stage builds
- Orchestration: Kubernetes (Minikube local)
- State Management: Dapr state store
- Service Mesh: Dapr for service-to-service communication
- Deployment: Helm charts

**Phase 5**:
- Multi-cloud support: Azure/GCP/Oracle Cloud
- Event Streaming: Kafka (Redpanda or Strimzi)
- Orchestration: Dapr + Kubernetes (AKS/GKE/OKE)
- CI/CD: GitHub Actions with multi-cloud deployment
- Observability: Prometheus + Grafana + Jaeger

### VIII. Dependency Management and Approved Libraries

**Phase 1 Approved**:
- Rich (terminal UI)
- Python 3.13+ standard library only

**Phase 2 Approved**:
- Frontend: Next.js 16+, React 19+, Tailwind CSS, ShadCN UI, Zod, TanStack Query
- Backend: FastAPI, SQLModel, Pydantic, uvicorn, python-jose (JWT)
- Database: Neon serverless PostgreSQL driver

**Phase 3 Approved**:
- OpenAI Agents SDK
- Official MCP SDK
- OpenAI ChatKit

**Phase 4 Approved**:
- Docker, Minikube, Helm, kubectl
- Dapr SDK (Python/Node.js)

**Phase 5 Approved**:
- Cloud SDKs (Azure SDK, GCP SDK, Oracle Cloud SDK)
- Kafka clients (kafka-python, kafkajs)
- Dapr SDK
- Prometheus client libraries

**Prohibited**:
- Unmaintained or deprecated libraries
- Libraries with known security vulnerabilities
- Any library not explicitly approved for the phase

### IX. Documentation and Traceability

**Prompt History Records (PHR)**:
- **MANDATORY**: Create PHR after every user request involving implementation, planning, debugging, or spec work
- **Routing** (all under `history/prompts/`):
  - Constitution work → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- **Format**: Use `.specify/templates/phr-template.prompt.md`
- **Required Fields**: ID, title, stage, date, model, feature, branch, user, command, prompt text (full, not truncated), response text, files changed, tests run
- **Stage Detection**: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

**Architecture Decision Records (ADR)**:
- **When to Create**: Three-part test:
  1. **Impact**: Long-term consequences (framework choice, data model, API design, security, platform)
  2. **Alternatives**: Multiple viable options considered
  3. **Scope**: Cross-cutting influence on system design
- **ALL must be true** to warrant an ADR
- **Never Auto-Create**: Suggest with: "📋 Architectural decision detected: [brief-description]. Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`"
- **Wait for User Consent**: User must explicitly approve ADR creation
- **Group Related Decisions**: Combine related decisions (e.g., "authentication stack") into one ADR when appropriate

**Code Comments**:
- Every generated file must include header comment with:
  - Task ID reference (e.g., `# Task: T-001`)
  - Spec section reference (e.g., `# Spec: specs/phase1/spec.md#crud-operations`)
  - Brief purpose description
- Inline comments for complex logic only (prefer self-documenting code)

### X. Error Handling and Resilience

**Phase 1**:
- Graceful handling of invalid inputs
- Clear error messages with recovery suggestions
- No silent failures

**Phase 2+**:
- HTTP status codes: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), 500 (Server Error)
- Structured error responses with `{ error: string, details?: object }`
- Frontend: Toast notifications for errors
- Backend: HTTPException with meaningful messages

**Phase 3+**:
- Retry logic for transient failures (AI API, database)
- Fallback responses for AI unavailability
- Circuit breaker patterns for external dependencies

**Phase 4-5**:
- Health checks (`/health`, `/ready`)
- Graceful degradation when services unavailable
- Dead letter queues for failed events
- Distributed tracing for error diagnosis

## Development Workflow

### Mandatory Workflow Sequence
1. **Specify**: Create/update spec in `specs/phase<N>/<feature>/spec.md`
2. **Plan**: Generate architectural plan in `specs/phase<N>/<feature>/plan.md`
3. **Tasks**: Break down into testable tasks in `specs/phase<N>/<feature>/tasks.md`
4. **Implement**: Generate code via Claude Code referencing task IDs
5. **Validate**: Run tests, verify acceptance criteria
6. **Record**: Create PHR documenting the work

### Slash Commands
- `/sp.constitution` - Create/update project constitution
- `/sp.specify` - Create feature specification
- `/sp.plan` - Generate architectural plan
- `/sp.tasks` - Generate task breakdown
- `/sp.implement` - Execute implementation
- `/sp.adr` - Create Architecture Decision Record
- `/sp.phr` - Create Prompt History Record
- `/sp.analyze` - Cross-artifact consistency check

### Human-in-the-Loop Strategy
**Treat the user as a specialized tool for clarification and decision-making.**

**Invoke User When**:
1. **Ambiguous Requirements**: Ask 2-3 targeted clarifying questions before proceeding
2. **Unforeseen Dependencies**: Surface discovered dependencies and ask for prioritization
3. **Architectural Uncertainty**: Present options with tradeoffs and get user preference
4. **Completion Checkpoint**: After major milestones, summarize what was done and confirm next steps

**Never Assume**: If data, APIs, or contracts are missing, ask targeted questions instead of inventing

### Execution Contract (Every Request)
1. **Confirm**: Surface and success criteria (one sentence)
2. **List**: Constraints, invariants, non-goals
3. **Produce**: Artifact with acceptance checks (checkboxes/tests)
4. **Follow-ups**: Risks and next steps (max 3 bullets)
5. **Record**: Create PHR in appropriate subdirectory
6. **Suggest ADR**: If significant decisions identified

### Minimum Acceptance Criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change (no unrelated edits)
- Code references to modified/inspected files
- All tests passing before marking task complete

## Environment Setup Requirements

### Phase 1 Environment
- Python 3.13+
- UV package manager
- Rich library installed
- Git for version control

### Phase 2 Environment
- Node.js 20+ (for Next.js)
- Python 3.13+ (for FastAPI backend)
- Neon PostgreSQL account (serverless)
- Environment variables: `DATABASE_URL`, `BETTER_AUTH_SECRET`

### Phase 3 Environment
- OpenAI API key (`OPENAI_API_KEY`)
- MCP SDK installed
- ChatKit setup

### Phase 4 Environment
- Docker Desktop
- Minikube
- kubectl
- Helm 3+
- Dapr CLI

### Phase 5 Environment
- Cloud account (Azure/GCP/Oracle Cloud)
- Cloud CLI tools (az/gcloud/oci)
- Kafka service (Redpanda Cloud or Strimzi self-hosted)
- Dapr production setup
- GitHub repository with Actions enabled

**WSL 2**: Required for Windows users across all phases

## Technology Stack Summary

| Phase | Frontend | Backend | Database | Infrastructure | AI/Tools |
|-------|----------|---------|----------|----------------|----------|
| 1     | Rich (CLI) | Python | In-memory | - | - |
| 2     | Next.js 16+ | FastAPI | Neon PostgreSQL | - | - |
| 3     | ChatKit | FastAPI | Neon PostgreSQL | - | OpenAI Agents + MCP |
| 4     | Next.js | FastAPI | PostgreSQL | Minikube + Dapr | - |
| 5     | Next.js | FastAPI | PostgreSQL | K8s + Dapr + Kafka | Cloud-native |

## Quality Gates

### Code Merge Requirements
- All tests passing (unit, integration, E2E)
- Linting and formatting checks pass
- Task IDs referenced in code comments
- PHR created for the work
- Spec updated if requirements changed
- Peer review (for collaborative projects)

### Phase Completion Criteria
Each phase is considered complete when:
1. All features from phase spec implemented
2. All acceptance criteria met
3. All tests passing (100% of defined test cases)
4. Documentation complete (PHRs, ADRs, README)
5. User can successfully run the phase end-to-end
6. Phase demo recorded (video walkthrough)

## Governance

### Constitution Authority
- This constitution supersedes all other development practices
- All agents, subagents, and developers must adhere to these principles
- Deviations require explicit documented justification and approval

### Amendment Process
- Amendments must be documented in ADR
- Requires user approval
- Must include migration plan if affecting existing code
- Version and date must be updated

### Compliance Verification
- All PRs must verify constitution compliance
- Complexity must be justified against "smallest viable change" principle
- Use `CLAUDE.md` for runtime development guidance

### Conflict Resolution
- Specification is the single source of truth
- If code conflicts with spec, spec wins (update code)
- If requirements conflict, escalate to user for clarification
- If constitution conflicts with external standards, document ADR and get user approval

## Prohibited Practices

### Strictly Forbidden
- Manual code writing without spec-driven process
- Skipping test-first development
- Using unapproved libraries or dependencies
- Hardcoding secrets or credentials
- Ignoring acceptance criteria
- Creating code without task ID references
- Skipping PHR creation for implementation work
- Auto-creating ADRs without user consent
- Refactoring unrelated code during feature implementation

### Discouraged (Require Justification)
- Premature optimization
- Over-engineering solutions
- Creating abstractions for single use cases
- Copying code between phases (prefer shared libraries)
- Large, multi-purpose commits (keep changes focused)

---

**Version**: 1.0.0
**Ratified**: 2026-01-02
**Last Amended**: 2026-01-02
**Scope**: All 5 phases of Evolution of Todo project
**Authority**: Project-wide, binding on all development activities
