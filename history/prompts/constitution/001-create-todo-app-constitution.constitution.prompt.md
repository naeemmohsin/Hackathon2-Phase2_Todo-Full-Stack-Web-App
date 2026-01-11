---
id: 001
title: Create Todo App Constitution
stage: constitution
date: 2026-01-11
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: master
user: ACER
command: /sp.constitution
labels: ["constitution", "todo-app", "hackathon", "full-stack", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

/sp.constitution

Project: Todo Full-Stack Web Application (Agentic Dev Stack, Hackathon Phase-2)

Core principles:
- Spec-driven development (spec → plan → tasks → implementation)
- Zero manual coding (all code generated via Claude Code)
- Deterministic, reviewable agent behavior
- Security-first design (authentication, authorization, data isolation)
- Production-grade full-stack architecture

Key standards:
- All functionality must be explicitly defined in specs before implementation
- Each API endpoint must have:
  - Clear purpose
  - Defined request/response schema
  - Proper HTTP status codes
- Authentication is mandatory for all protected routes
- User data isolation must be enforced at every layer
- Frontend, backend, and auth responsibilities must be clearly separated
- Environment configuration must be explicit and reproducible

Constraints:
- Technology stack is fixed and non-negotiable:
  - Frontend: Next.js 16+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth with JWT
- No manual code edits outside Claude Code execution
- All API access requires a valid JWT token
- Shared JWT secret must be used consistently across services
- Backend must remain stateless with respect to authentication

Development rules:
- Follow the Agentic Dev Stack workflow strictly:
  1. Write specification (sp.specify)
  2. Generate implementation plan
  3. Break into executable tasks
  4. Implement via Claude Code
- No step may skip or override a previous phase
- Specs must be precise enough to prevent ambiguous implementations
- Frontend and backend must communicate exclusively via REST APIs

Security requirements:
- JWT tokens must be verified on every backend request
- Unauthorized requests must return HTTP 401
- Authenticated users may only access their own tasks
- Task ownership must be enforced on:
  - Read
  - Create
  - Update
  - Delete
  - Complete toggle operations
- Token expiry must be respected

Quality standards:
- Code must be readable, modular, and maintainable
- API behavior must be predictable and consistent
- Frontend must be responsive and usable on mobile and desktop
- Error states must be handled gracefully on both frontend and backend

Success criteria:
- All 5 basic-level Todo features work end-to-end
- Multi-user support with strict data isolation
- Authenticated users can only see and modify their own tasks
- Backend rejects all unauthenticated or invalid requests
- Frontend successfully integrates authentication and API access
- Entire project is reproducible from specs without manual intervention

## Response snapshot

Created the project constitution at `.specify/memory/constitution.md` with version 1.0.0.

The constitution establishes 6 core principles:
1. **Spec-Driven Development**: All functionality must be defined in specs before implementation
2. **Agentic Development**: Zero manual coding, all code generated via Claude Code
3. **Security-First Design**: JWT auth on all protected routes, task ownership enforcement
4. **Fixed Technology Stack**: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth
5. **Strict Data Isolation**: Users can only access their own tasks at every layer
6. **Quality Standards**: Readable, modular code with proper error handling

Added sections for Technology Stack table, Development Rules (workflow enforcement, API contract requirements, environment configuration), and Governance procedures.

## Outcome

- ✅ Impact: Established foundational project governance for Todo Full-Stack Web Application
- 🧪 Tests: N/A (constitution document, no tests)
- 📁 Files: 1 file created/updated (.specify/memory/constitution.md)
- 🔁 Next prompts: /sp.specify to define Todo feature specification
- 🧠 Reflection: Constitution captures all user requirements comprehensively with clear MUST/SHOULD language

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review - PASS (all placeholders filled, version/dates correct)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
