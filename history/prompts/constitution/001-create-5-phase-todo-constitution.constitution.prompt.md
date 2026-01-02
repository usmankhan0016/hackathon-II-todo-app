---
id: 001
title: Create 5-Phase Todo Constitution
stage: constitution
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: usmankhan
command: /sp.constitution
labels: ["constitution", "spec-driven-development", "5-phase-project", "python", "nextjs", "ai-chatbot", "kubernetes", "cloud-native"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/001-create-5-phase-todo-constitution.constitution.prompt.md
tests:
  - N/A (documentation artifact)
---

## Prompt

/sp.constitution

Create a comprehensive constitution for a 5-phase Todo application project following Spec-Driven Development principles.

## Project Overview
- **Name:** Evolution of Todo - From CLI to Cloud-Native AI System
- **Phases:** 5 progressive phases (Console → Web → AI Chatbot → Local K8s → Cloud Deployment)
- **Methodology:** Strict Spec-Driven Development - No manual coding allowed
- **Tools:** Claude Code + Spec-Kit Plus for all implementation

## Core Principles

### 1. Development Methodology
- **Spec-First:** All features must follow: Specify → Plan → Tasks → Implement
- **No Manual Coding:** All code generated via Claude Code from specifications
- **Task Traceability:** Every code file must reference Task IDs and Spec sections
- **Iterative Refinement:** Refine specs until Claude Code generates correct output

### 2. Project Structure
- Monorepo organization for all 5 phases
- Phase-specific folders under `/src/phase[1-5]/`
- Centralized `/specs/` directory with phase-based organization
- Constitution applies across all phases

## Phase-Specific Technical Standards

### Phase 1: Console App (Python)
**Tech Stack:**
- Python 3.13+
- UV for dependency management
- Rich library for CLI interface
- In-memory storage (Python list)

**Code Standards:**
- PEP 8 compliance
- Type hints on all functions
- Comprehensive docstrings
- Dataclasses for models

**UI/UX Requirements:**
- Modern, attractive terminal interface using Rich library
- Color-coded output: Green (completed), Yellow (pending), Red (overdue)
- Styled panels and bordered tables
- Visual hierarchy with emojis (📝, ✓, ⏳, 🔴)
- Interactive menu system
- Consistent formatting across all commands
- Task display: ID | Title | Status | Priority | Tags

**Architecture:**
- Module: `models.py` - Dataclass definitions
- Module: `task_manager.py` - In-memory CRUD operations
- Module: `cli.py` - User input and display
- Module: `ui.py` - Rich library components (headers, tables, messages)
- Module: `main.py` - Entry point and main loop

**Approved Libraries:**
- Rich (primary UI library)
- No external dependencies beyond Python 3.13+ standard library

### Phase 2: Full-Stack Web App
**Tech Stack:**
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI, SQLModel ORM
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT tokens

**Architecture:**
- Monorepo: `/frontend` and `/backend` folders
- RESTful API: `/api/{user_id}/tasks` endpoints
- JWT-based authentication with shared secret
- User isolation: each user sees only their tasks

**Security:**
- JWT tokens required for all API requests
- BETTER_AUTH_SECRET shared between frontend/backend
- User ID validation on every request
- 401 Unauthorized for missing/invalid tokens

**Code Standards:**
- Frontend: Server components by default, client only for interactivity
- Backend: Pydantic models for request/response validation
- Type safety: TypeScript (frontend), Python type hints (backend)
- Error handling: HTTPException with meaningful messages

### Phase 3: AI Chatbot
**Tech Stack:**
- Frontend: OpenAI ChatKit
- AI: OpenAI Agents SDK
- MCP: Official MCP SDK (Model Context Protocol)
- Backend: FastAPI (stateless)
- Database: Neon PostgreSQL (state persistence)

**Architecture:**
- Stateless chat endpoint: `/api/{user_id}/chat`
- MCP server exposes task operations as tools
- Conversation history stored in database
- Agent invokes MCP tools for task management

**MCP Tools Required:**
1. `add_task` - Create new task
2. `list_tasks` - Retrieve tasks with filters
3. `update_task` - Modify existing task
4. `delete_task` - Remove task
5. `search_tasks` - Full-text search

### Phase 4: Local Kubernetes
**Tech Stack:**
- Docker for containerization
- Minikube for local K8s cluster
- Helm for package management
- Dapr for state management and service communication

**Architecture:**
- Frontend and backend as separate containers
- PostgreSQL StatefulSet
- Dapr state store component
- Service mesh via Dapr
- Helm chart for deployment

### Phase 5: Cloud-Native Deployment
**Tech Stack:**
- Multi-cloud: Azure/GCP/Oracle Cloud
- Kafka for event streaming (Redpanda or Strimzi)
- Dapr for distributed orchestration
- GitHub Actions for CI/CD

**Architecture:**
- Managed Kubernetes (AKS/GKE/OKE)
- Event-driven architecture with Kafka
- Dapr pub/sub for async communication
- Observability: Prometheus + Grafana + Jaeger
- Multi-region deployment capability

## Quality Standards

### Testing Requirements
- **Phase 1**: Pytest for all CRUD operations, 90%+ coverage
- **Phase 2**: Frontend (Vitest), Backend (pytest), E2E (Playwright)
- **Phase 3**: MCP tool tests, agent conversation tests
- **Phase 4**: Container tests, K8s manifest validation
- **Phase 5**: Cloud deployment tests, event streaming validation

### Documentation
- PHR (Prompt History Record) for every significant interaction
- ADR (Architecture Decision Record) for major architectural choices
- Code comments with Task ID and Spec section references
- README for each phase with setup instructions

## Constraints

### Mandatory
- Spec-driven development workflow (no manual coding)
- TDD (Test-Driven Development) for all phases
- Task ID references in all generated code
- PHR creation for implementation work
- No code generation without task reference
- Constitution adherence across all phases
- WSL 2 for Windows users

### Prohibited
- Manual code writing (must use Claude Code)
- Skipping specification phase
- Using unapproved libraries
- Ignoring acceptance criteria
- Freestyle implementation without specs

## Environment Setup

### Phase 1
- Python 3.13+, UV, Rich library

### Phase 2
- Node.js, Next.js 16+, FastAPI, Neon DB account

### Phase 3
- OpenAI API key, ChatKit setup, MCP SDK

### Phase 4
- Docker Desktop, Minikube, Helm, kubectl

### Phase 5
- Cloud account (Azure/GCP/Oracle)
- Kafka service (Redpanda/Strimzi)
- Dapr CLI, GitHub Actions

---

**This constitution governs all development across all 5 phases. All agents, subagents, and developers must adhere to these principles. The spec is the single source of truth.**

## Response snapshot

I've created a comprehensive constitution for your 5-phase Todo application project at `.specify/memory/constitution.md`. The constitution establishes the following framework:

**Core Principles (10 sections)**:
1. **Spec-Driven Development (NON-NEGOTIABLE)** - All code must be generated from specifications via Claude Code
2. **Progressive Complexity Across 5 Phases** - Each phase builds incrementally
3. **Test-First Development (NON-NEGOTIABLE)** - TDD mandatory across all phases
4. **User Experience Excellence** - Polished, production-ready UX for each phase
5. **Security and Authentication** - Built-in from Phase 2 onward
6. **Code Quality and Standards** - Python PEP 8, TypeScript strict mode
7. **Architecture Standards** - Monorepo structure with phase-specific organization
8. **Dependency Management** - Approved libraries for each phase
9. **Documentation and Traceability** - PHR and ADR requirements
10. **Error Handling and Resilience** - Phase-appropriate error strategies

**Technology Stack Summary**:
- Phase 1: Python + Rich (CLI)
- Phase 2: Next.js + FastAPI + Neon PostgreSQL
- Phase 3: OpenAI Agents + MCP + ChatKit
- Phase 4: Docker + Kubernetes (Minikube) + Dapr
- Phase 5: Multi-cloud + Kafka + Dapr + Observability

**Project Structure Created**:
- `.specify/memory/constitution.md` (4,000+ words)
- Directory structure: `specs/`, `src/`, `history/prompts/`, `history/adr/`, `tests/`
- Phase-specific subdirectories for all 5 phases

The constitution provides:
- Mandatory workflow sequences
- Quality gates and completion criteria
- Governance and compliance rules
- Prohibited practices
- Environment setup requirements for each phase

## Outcome

- ✅ Impact: Project constitution created establishing spec-driven development framework for all 5 phases
- 🧪 Tests: N/A (documentation artifact, no code generated)
- 📁 Files: Created constitution.md (429 lines) and directory structure for specs/, src/, history/, tests/
- 🔁 Next prompts: User can now run `/sp.specify` to create Phase 1 specification for console Todo app
- 🧠 Reflection: Constitution provides comprehensive governance for the entire 5-phase project lifecycle, ensuring consistency and quality across all development stages

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution successfully created with complete coverage
- Graders run and results (PASS/FAIL): N/A (documentation artifact)
- Prompt variant (if applicable): N/A (initial constitution creation)
- Next experiment (smallest change to try): Begin Phase 1 specification using `/sp.specify` for console Todo app with Rich UI
