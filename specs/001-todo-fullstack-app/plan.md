# Implementation Plan: Todo Full-Stack Web Application

**Branch**: `001-todo-fullstack-app` | **Date**: 2026-01-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-fullstack-app/spec.md`

## Summary

Build a secure, multi-user Todo web application with JWT-based authentication. The system consists of a FastAPI backend providing REST APIs for task CRUD operations, a Next.js frontend for user interaction, and Neon PostgreSQL for data persistence. All user data is strictly isolated - users can only access their own tasks.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, SQLModel, python-jose (backend); Next.js 16+, Better Auth (frontend)
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (backend), Playwright or manual testing (frontend)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
**Project Type**: Web application (separate frontend + backend)
**Performance Goals**: Task list loads within 2 seconds, 50 concurrent users supported
**Constraints**: JWT tokens required for all protected endpoints, stateless backend auth
**Scale/Scope**: Single-user to 50 concurrent users, 5 core features

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Verification |
|-----------|--------|--------------|
| I. Spec-Driven Development | ✅ PASS | Specification completed before planning |
| II. Agentic Development | ✅ PASS | All code will be generated via Claude Code |
| III. Security-First Design | ✅ PASS | JWT auth on all protected routes, ownership enforcement |
| IV. Fixed Technology Stack | ✅ PASS | Using Next.js, FastAPI, SQLModel, Neon, Better Auth |
| V. Strict Data Isolation | ✅ PASS | User ID filtering at database query level |
| VI. Quality Standards | ✅ PASS | Responsive UI, proper error handling, documented APIs |

**Gate Result**: PASS - All principles satisfied. Proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-fullstack-app/
├── plan.md              # This file
├── research.md          # Phase 0: Technology decisions
├── data-model.md        # Phase 1: Entity definitions
├── quickstart.md        # Phase 1: Setup instructions
├── contracts/           # Phase 1: API specifications
│   ├── auth.yaml        # Authentication endpoints
│   └── tasks.yaml       # Task CRUD endpoints
└── tasks.md             # Phase 2: Implementation tasks (via /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Environment configuration
│   ├── database.py          # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User SQLModel
│   │   └── task.py          # Task SQLModel
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # Pydantic request/response schemas
│   │   └── task.py          # Task schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependency injection (auth, db)
│   │   ├── auth.py          # Auth endpoints
│   │   └── tasks.py         # Task CRUD endpoints
│   └── services/
│       ├── __init__.py
│       ├── auth.py          # JWT creation/validation
│       └── task.py          # Task business logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures
│   ├── test_auth.py         # Auth endpoint tests
│   └── test_tasks.py        # Task endpoint tests
├── requirements.txt
├── .env.example
└── README.md

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home/redirect
│   │   ├── login/
│   │   │   └── page.tsx     # Login page
│   │   ├── register/
│   │   │   └── page.tsx     # Registration page
│   │   └── dashboard/
│   │       └── page.tsx     # Task dashboard (protected)
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── CreateTaskForm.tsx
│   │   │   └── EditTaskModal.tsx
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       └── ErrorMessage.tsx
│   ├── lib/
│   │   ├── auth.ts          # Better Auth client config
│   │   ├── api.ts           # API client with JWT headers
│   │   └── types.ts         # TypeScript types
│   └── middleware.ts        # Route protection
├── public/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── .env.example
└── README.md
```

**Structure Decision**: Web application structure selected (Option 2) as this is a full-stack app with separate frontend and backend. Backend uses FastAPI with modular organization (models, schemas, api, services). Frontend uses Next.js App Router with component-based architecture.

## Complexity Tracking

> No violations requiring justification. Architecture follows constitution principles directly.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Separate frontend/backend | Required | Constitution mandates REST API communication |
| SQLModel over raw SQLAlchemy | Simpler | Combines Pydantic + SQLAlchemy, reduces boilerplate |
| Better Auth for frontend | Required | Constitution specifies Better Auth + JWT |
| No ORM on frontend | Required | Constitution prohibits direct DB access from frontend |

## Architecture Overview

```
┌─────────────────┐     HTTPS/REST      ┌─────────────────┐     SQL      ┌─────────────────┐
│                 │ ←─────────────────→ │                 │ ←──────────→ │                 │
│  Next.js App    │   JWT in headers    │  FastAPI API    │              │  Neon Postgres  │
│  (Browser)      │                     │  (Backend)      │              │  (Database)     │
│                 │                     │                 │              │                 │
└─────────────────┘                     └─────────────────┘              └─────────────────┘
        │                                       │
        │ Better Auth                           │ python-jose
        │ (JWT handling)                        │ (JWT validation)
        ▼                                       ▼
   ┌─────────┐                            ┌─────────────┐
   │ Session │                            │ Middleware  │
   │ Storage │                            │ (Auth Gate) │
   └─────────┘                            └─────────────┘
```

### Authentication Flow

1. **Registration**: User submits email/password → Backend hashes password → Stores in DB → Returns JWT
2. **Login**: User submits credentials → Backend validates → Returns JWT
3. **Protected Requests**: Frontend includes JWT in Authorization header → Backend validates → Processes request
4. **Logout**: Frontend clears JWT from storage

### Data Flow

1. **Create Task**: Authenticated request → Extract user_id from JWT → Create task with owner_id → Return task
2. **Read Tasks**: Authenticated request → Query tasks WHERE owner_id = user_id → Return list
3. **Update Task**: Authenticated request → Verify owner_id matches → Update → Return updated task
4. **Delete Task**: Authenticated request → Verify owner_id matches → Delete → Return success
5. **Toggle Complete**: Authenticated request → Verify owner_id matches → Toggle status → Return updated task

## Security Design

### JWT Token Structure

```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

### Endpoint Protection

| Endpoint | Auth Required | Owner Check |
|----------|---------------|-------------|
| POST /auth/register | No | N/A |
| POST /auth/login | No | N/A |
| POST /auth/logout | Yes | N/A |
| GET /tasks | Yes | Filter by owner |
| POST /tasks | Yes | Set owner |
| PUT /tasks/{id} | Yes | Verify owner |
| DELETE /tasks/{id} | Yes | Verify owner |
| PATCH /tasks/{id}/toggle | Yes | Verify owner |

### Error Responses

| Status | Meaning |
|--------|---------|
| 400 | Validation error (invalid input) |
| 401 | Unauthorized (missing/invalid JWT) |
| 403 | Forbidden (valid JWT but not owner) |
| 404 | Not found |
| 500 | Server error |

## Environment Configuration

### Backend (.env)

```
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
JWT_SECRET=shared-secret-between-frontend-and-backend
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)

```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=shared-secret-between-frontend-and-backend
```

## API Endpoints Summary

### Authentication

| Method | Path | Request | Response | Description |
|--------|------|---------|----------|-------------|
| POST | /auth/register | `{email, password}` | `{user, token}` | Create account |
| POST | /auth/login | `{email, password}` | `{user, token}` | Authenticate |
| POST | /auth/logout | - | `{success}` | Invalidate session |

### Tasks

| Method | Path | Request | Response | Description |
|--------|------|---------|----------|-------------|
| GET | /tasks | - | `[{task}]` | List user's tasks |
| POST | /tasks | `{title}` | `{task}` | Create task |
| PUT | /tasks/{id} | `{title}` | `{task}` | Update title |
| DELETE | /tasks/{id} | - | `{success}` | Delete task |
| PATCH | /tasks/{id}/toggle | - | `{task}` | Toggle completion |

## Implementation Phases

### Phase 1: Backend Foundation
- Initialize FastAPI project structure
- Configure Neon PostgreSQL connection
- Define SQLModel entities (User, Task)
- Implement database migrations

### Phase 2: Authentication & Security
- Implement password hashing (bcrypt)
- Implement JWT token generation/validation
- Create auth endpoints (register, login, logout)
- Add auth middleware for protected routes

### Phase 3: Task CRUD API
- Implement task creation with owner assignment
- Implement task listing with owner filtering
- Implement task update with ownership verification
- Implement task deletion with ownership verification
- Implement completion toggle with ownership verification

### Phase 4: Frontend Setup
- Initialize Next.js project with App Router
- Configure Tailwind CSS for styling
- Set up Better Auth client
- Create API client with JWT handling

### Phase 5: Auth UI
- Build login page and form
- Build registration page and form
- Implement auth state management
- Add protected route middleware

### Phase 6: Task UI
- Build dashboard layout
- Create task list component
- Create task creation form
- Create task edit modal
- Create task delete confirmation
- Add completion toggle button
- Implement empty state

### Phase 7: Polish & Validation
- Add loading states
- Add error handling UI
- Responsive design adjustments
- End-to-end testing
