# Tasks: Todo Full-Stack Web Application

**Input**: Design documents from `/specs/001-todo-fullstack-app/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the specification. Tasks focus on implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` for source, `backend/tests/` for tests
- **Frontend**: `frontend/src/` for source

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both backend and frontend

- [x] T001 Create backend directory structure per plan.md at `backend/`
- [x] T002 Create `backend/requirements.txt` with FastAPI, SQLModel, python-jose, passlib, python-dotenv, uvicorn, psycopg2-binary
- [x] T003 [P] Create `backend/.env.example` with DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_HOURS, CORS_ORIGINS
- [x] T004 [P] Create `backend/app/__init__.py` as empty package marker
- [x] T005 Create frontend directory with Next.js App Router at `frontend/` using `npx create-next-app@latest`
- [x] T006 [P] Configure Tailwind CSS in `frontend/tailwind.config.ts`
- [x] T007 [P] Create `frontend/.env.example` with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET

**Checkpoint**: Project skeleton ready - can proceed with foundational phase

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Core

- [x] T008 Create environment config loader in `backend/app/config.py` with Settings class using pydantic-settings
- [x] T009 Create database connection module in `backend/app/database.py` with SQLModel engine and session factory
- [x] T010 [P] Create User SQLModel in `backend/app/models/user.py` with id, email, password_hash, created_at, updated_at
- [x] T011 [P] Create Task SQLModel in `backend/app/models/task.py` with id, title, is_completed, owner_id, created_at, updated_at
- [x] T012 Create `backend/app/models/__init__.py` exporting User and Task models
- [x] T013 Create auth service in `backend/app/services/auth.py` with password hashing (bcrypt) and JWT create/verify functions
- [x] T014 Create dependency injection module in `backend/app/api/deps.py` with get_db session and get_current_user from JWT
- [x] T015 Create FastAPI app entry point in `backend/app/main.py` with CORS middleware and router includes
- [x] T016 Create `backend/app/api/__init__.py` with router aggregation

### Frontend Core

- [x] T017 Create TypeScript types in `frontend/src/lib/types.ts` with User, Task, AuthResponse, ApiError interfaces
- [x] T018 Create API client in `frontend/src/lib/api.ts` with fetch wrapper that includes JWT from localStorage
- [x] T019 Create auth client in `frontend/src/lib/auth.ts` with login, register, logout, getCurrentUser functions
- [x] T020 Create root layout in `frontend/src/app/layout.tsx` with HTML structure and global styles
- [x] T021 Create middleware for route protection in `frontend/src/middleware.ts` redirecting unauthenticated users

### Shared UI Components

- [x] T022 [P] Create Button component in `frontend/src/components/ui/Button.tsx` with variants (primary, secondary, danger)
- [x] T023 [P] Create Input component in `frontend/src/components/ui/Input.tsx` with label, error state, validation
- [x] T024 [P] Create ErrorMessage component in `frontend/src/components/ui/ErrorMessage.tsx` for displaying errors

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Registration and Login (Priority: P1) 🎯 MVP

**Goal**: Enable users to register, login, and logout from the application

**Independent Test**: Register a new account, logout, login again. Verify JWT is issued and stored.

### Backend Implementation for US1

- [x] T025 [P] [US1] Create user schemas in `backend/app/schemas/user.py` with RegisterRequest, LoginRequest, UserResponse, AuthResponse
- [x] T026 [US1] Create auth router in `backend/app/api/auth.py` with POST /auth/register endpoint
- [x] T027 [US1] Add POST /auth/login endpoint to `backend/app/api/auth.py`
- [x] T028 [US1] Add POST /auth/logout endpoint to `backend/app/api/auth.py`
- [x] T029 [US1] Add GET /auth/me endpoint to `backend/app/api/auth.py` for current user info
- [x] T030 [US1] Register auth router in `backend/app/main.py`

### Frontend Implementation for US1

- [x] T031 [P] [US1] Create LoginForm component in `frontend/src/components/auth/LoginForm.tsx` with email, password fields
- [x] T032 [P] [US1] Create RegisterForm component in `frontend/src/components/auth/RegisterForm.tsx` with email, password fields
- [x] T033 [US1] Create login page in `frontend/src/app/login/page.tsx` using LoginForm component
- [x] T034 [US1] Create register page in `frontend/src/app/register/page.tsx` using RegisterForm component
- [x] T035 [US1] Create home page in `frontend/src/app/page.tsx` that redirects to dashboard if logged in, else to login
- [x] T036 [US1] Add logout button functionality to dashboard layout (prepare for Phase 4)

**Checkpoint**: User Story 1 complete - users can register, login, and logout

---

## Phase 4: User Story 2 - Create New Task (Priority: P2)

**Goal**: Allow authenticated users to create new tasks

**Independent Test**: Login, enter a task title, submit. Verify task appears in list.

### Backend Implementation for US2

- [x] T037 [P] [US2] Create task schemas in `backend/app/schemas/task.py` with CreateTaskRequest, TaskResponse
- [x] T038 [US2] Create task service in `backend/app/services/task.py` with create_task function setting owner_id
- [x] T039 [US2] Create tasks router in `backend/app/api/tasks.py` with POST /tasks endpoint
- [x] T040 [US2] Register tasks router in `backend/app/main.py`

### Frontend Implementation for US2

- [x] T041 [US2] Create CreateTaskForm component in `frontend/src/components/tasks/CreateTaskForm.tsx` with title input
- [x] T042 [US2] Create dashboard page in `frontend/src/app/dashboard/page.tsx` with CreateTaskForm and placeholder for task list

**Checkpoint**: User Story 2 complete - users can create tasks

---

## Phase 5: User Story 3 - View My Tasks (Priority: P3)

**Goal**: Display all tasks belonging to the authenticated user

**Independent Test**: Login with user that has tasks, verify only that user's tasks are shown.

### Backend Implementation for US3

- [x] T043 [US3] Add list_tasks function to `backend/app/services/task.py` filtering by owner_id
- [x] T044 [US3] Add GET /tasks endpoint to `backend/app/api/tasks.py` returning user's tasks only

### Frontend Implementation for US3

- [x] T045 [P] [US3] Create TaskItem component in `frontend/src/components/tasks/TaskItem.tsx` displaying title and completion status
- [x] T046 [US3] Create TaskList component in `frontend/src/components/tasks/TaskList.tsx` mapping tasks to TaskItem
- [x] T047 [US3] Update dashboard page `frontend/src/app/dashboard/page.tsx` to fetch and display TaskList
- [x] T048 [US3] Add empty state message to TaskList when no tasks exist

**Checkpoint**: User Story 3 complete - users can view their tasks

---

## Phase 6: User Story 4 - Update Task Title (Priority: P4)

**Goal**: Allow users to edit the title of their existing tasks

**Independent Test**: Login, select a task, edit title, save. Verify change persists.

### Backend Implementation for US4

- [x] T049 [P] [US4] Add UpdateTaskRequest schema to `backend/app/schemas/task.py` with title field
- [x] T050 [US4] Add update_task function to `backend/app/services/task.py` with ownership verification
- [x] T051 [US4] Add PUT /tasks/{task_id} endpoint to `backend/app/api/tasks.py`

### Frontend Implementation for US4

- [x] T052 [US4] Create EditTaskModal component in `frontend/src/components/tasks/EditTaskModal.tsx` with title input
- [x] T053 [US4] Add edit button to TaskItem component in `frontend/src/components/tasks/TaskItem.tsx`
- [x] T054 [US4] Integrate EditTaskModal into dashboard page `frontend/src/app/dashboard/page.tsx`

**Checkpoint**: User Story 4 complete - users can edit task titles

---

## Phase 7: User Story 5 - Delete Task (Priority: P5)

**Goal**: Allow users to permanently delete their tasks

**Independent Test**: Login, delete a task, verify it's removed from list.

### Backend Implementation for US5

- [x] T055 [US5] Add delete_task function to `backend/app/services/task.py` with ownership verification
- [x] T056 [US5] Add DELETE /tasks/{task_id} endpoint to `backend/app/api/tasks.py`

### Frontend Implementation for US5

- [x] T057 [US5] Add delete button to TaskItem component in `frontend/src/components/tasks/TaskItem.tsx`
- [x] T058 [US5] Add delete confirmation and handler to dashboard page `frontend/src/app/dashboard/page.tsx`

**Checkpoint**: User Story 5 complete - users can delete tasks

---

## Phase 8: User Story 6 - Toggle Task Completion (Priority: P6)

**Goal**: Allow users to mark tasks as complete or incomplete

**Independent Test**: Login, toggle a task's completion, verify visual change and persistence.

### Backend Implementation for US6

- [x] T059 [US6] Add toggle_task function to `backend/app/services/task.py` with ownership verification
- [x] T060 [US6] Add PATCH /tasks/{task_id}/toggle endpoint to `backend/app/api/tasks.py`

### Frontend Implementation for US6

- [x] T061 [US6] Add checkbox/toggle to TaskItem component in `frontend/src/components/tasks/TaskItem.tsx`
- [x] T062 [US6] Style completed tasks with strikethrough and muted colors in TaskItem
- [x] T063 [US6] Add toggle handler to dashboard page `frontend/src/app/dashboard/page.tsx`

**Checkpoint**: User Story 6 complete - users can toggle task completion

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T064 [P] Add loading states to all forms in `frontend/src/components/`
- [x] T065 [P] Add error handling to API calls in `frontend/src/lib/api.ts` with user-friendly messages
- [x] T066 [P] Ensure responsive design works 320px-1920px width in all pages
- [x] T067 [P] Create `backend/README.md` with setup and run instructions
- [x] T068 [P] Create `frontend/README.md` with setup and run instructions
- [x] T069 Add database table creation on startup in `backend/app/main.py` using SQLModel.metadata.create_all
- [x] T070 Validate all form inputs (email format, password length, non-empty title) across frontend

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 - BLOCKS all user stories
- **Phase 3-8 (User Stories)**: All depend on Phase 2 completion
  - US1 (Auth) MUST complete before US2-6 (they require authentication)
  - US2-6 can be done in parallel AFTER US1, but P2→P3 is recommended for best flow
- **Phase 9 (Polish)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1 - Auth)**: Can start after Phase 2 - BLOCKS all other stories
- **US2 (P2 - Create)**: Depends on US1 for authentication
- **US3 (P3 - View)**: Depends on US1; benefits from US2 for test data
- **US4 (P4 - Update)**: Depends on US1 and US3 (need tasks to update)
- **US5 (P5 - Delete)**: Depends on US1 and US3 (need tasks to delete)
- **US6 (P6 - Toggle)**: Depends on US1 and US3 (need tasks to toggle)

### Within Each User Story

1. Backend schemas first
2. Backend service/business logic
3. Backend API endpoints
4. Frontend components (can be parallel)
5. Frontend page integration

### Parallel Opportunities

**Phase 1 (Setup)**:
```
T003, T004 can run in parallel
T006, T007 can run in parallel
```

**Phase 2 (Foundational)**:
```
T010, T011 can run in parallel (different model files)
T022, T023, T024 can run in parallel (different UI components)
```

**User Story Phases**:
```
Backend schema tasks marked [P] can run in parallel
Frontend component tasks marked [P] can run in parallel
```

---

## Implementation Strategy

### MVP First (User Stories 1-3)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: User Story 1 (Auth)
4. **VALIDATE**: Can register, login, logout
5. Complete Phase 4: User Story 2 (Create)
6. Complete Phase 5: User Story 3 (View)
7. **MVP DEMO**: Users can register, login, create, and view tasks

### Incremental Delivery

1. Setup + Foundational → Infrastructure ready
2. Add US1 (Auth) → Users can log in
3. Add US2 (Create) → Users can add tasks
4. Add US3 (View) → Users can see tasks
5. Add US4 (Update) → Users can edit tasks
6. Add US5 (Delete) → Users can remove tasks
7. Add US6 (Toggle) → Users can complete tasks
8. Polish → Production-ready

### Single Developer Strategy

Execute in order: T001 → T070, following the phase order.
Each task builds on the previous, minimal context switching.

---

## Summary

| Phase | Story | Task Count | Parallel Tasks |
|-------|-------|------------|----------------|
| 1 - Setup | - | 7 | 4 |
| 2 - Foundational | - | 17 | 5 |
| 3 - US1 Auth | P1 | 12 | 4 |
| 4 - US2 Create | P2 | 6 | 1 |
| 5 - US3 View | P3 | 6 | 1 |
| 6 - US4 Update | P4 | 6 | 1 |
| 7 - US5 Delete | P5 | 4 | 0 |
| 8 - US6 Toggle | P6 | 5 | 0 |
| 9 - Polish | - | 7 | 5 |
| **TOTAL** | | **70** | **21** |

---

## Notes

- All tasks include exact file paths for clarity
- [P] tasks can be executed in parallel (different files, no dependencies)
- [Story] label traces each task to its user story
- Commit after each task or logical group
- Test each user story independently at checkpoints
- Backend must be running before frontend integration testing
