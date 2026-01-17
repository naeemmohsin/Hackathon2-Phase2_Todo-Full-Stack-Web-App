# Tasks: Authentication & Security Integration (Better Auth + JWT)

**Input**: Design documents from `/specs/002-better-auth-jwt/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Key Finding**: Backend JWT implementation is already complete. These tasks focus on frontend Better Auth integration.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` (existing, minimal changes)
- **Frontend**: `frontend/src/` (primary focus)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install Better Auth and configure project dependencies

- [x] T001 Install Better Auth package in frontend (`cd frontend && npm install better-auth`)
- [x] T002 [P] Verify backend environment variables are set (JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_HOURS)
- [x] T003 [P] Verify frontend environment variables are set (NEXT_PUBLIC_API_URL)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core authentication infrastructure that MUST be complete before user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Better Auth client configuration in `frontend/src/lib/auth-client.ts`
- [x] T005 Configure Better Auth to use custom backend endpoints (`/auth/register`, `/auth/login`)
- [x] T006 [P] Verify existing backend auth endpoints work (`POST /auth/register`, `POST /auth/login`)
- [x] T007 [P] Verify existing JWT middleware in `backend/app/api/deps.py` extracts user correctly

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Sign Up (Priority: P1) 🎯 MVP

**Goal**: New users can create accounts using Better Auth sign-up form and receive JWT tokens

**Independent Test**: Navigate to /register, enter email and password, verify redirect to dashboard with valid JWT

### Implementation for User Story 1

- [x] T008 [US1] Update `frontend/src/app/register/page.tsx` to use Better Auth sign-up component
- [x] T009 [US1] Configure sign-up form to POST to backend `/auth/register` endpoint
- [x] T010 [US1] Handle registration response - extract and store JWT token in localStorage
- [x] T011 [US1] Add validation error display for duplicate email, weak password, invalid format
- [x] T012 [US1] Implement redirect to dashboard on successful registration
- [x] T013 [US1] Update or replace `frontend/src/components/auth/RegisterForm.tsx` if needed

**Acceptance Criteria**:
- FR-002: Better Auth provides sign-up with email/password
- FR-004: JWT token issued and stored on success
- Users can register and are redirected to dashboard

**Checkpoint**: User Story 1 fully functional - new users can sign up

---

## Phase 4: User Story 2 - User Sign In (Priority: P2)

**Goal**: Registered users can sign in using Better Auth and receive JWT tokens

**Independent Test**: Navigate to /login, enter valid credentials, verify redirect to dashboard with JWT

### Implementation for User Story 2

- [x] T014 [US2] Update `frontend/src/app/login/page.tsx` to use Better Auth sign-in component
- [x] T015 [US2] Configure sign-in form to POST to backend `/auth/login` endpoint
- [x] T016 [US2] Handle login response - extract and store JWT token in localStorage
- [x] T017 [US2] Add authentication error display for invalid credentials
- [x] T018 [US2] Implement redirect to dashboard on successful sign-in
- [x] T019 [US2] Update or replace `frontend/src/components/auth/LoginForm.tsx` if needed

**Acceptance Criteria**:
- FR-003: Better Auth provides sign-in with email/password
- FR-004: JWT token issued and stored on success
- Users can sign in and access their tasks

**Checkpoint**: User Story 2 fully functional - returning users can sign in

---

## Phase 5: User Story 3 - Protected API Routes (Priority: P3)

**Goal**: All task endpoints require valid JWT - backend already implemented, verify integration

**Independent Test**: Make API requests with valid JWT (success), invalid JWT (401), no JWT (401)

**Note**: Backend implementation is already complete. This phase verifies integration.

### Verification for User Story 3

- [x] T020 [US3] Verify `backend/app/api/deps.py` CurrentUser dependency rejects missing tokens
- [x] T021 [US3] Verify `backend/app/api/deps.py` CurrentUser dependency rejects invalid tokens
- [x] T022 [US3] Verify `backend/app/api/deps.py` CurrentUser dependency rejects expired tokens
- [x] T023 [US3] Verify all task endpoints in `backend/app/api/tasks.py` use CurrentUser dependency

**Acceptance Criteria**:
- FR-010, FR-011, FR-012: JWT verified on every protected route
- FR-013: 401 Unauthorized for missing/invalid/expired tokens
- SC-002: 100% of requests without valid JWT return 401

**Checkpoint**: Backend protection verified - all task routes require valid JWT

---

## Phase 6: User Story 4 - Per-User Data Isolation (Priority: P4)

**Goal**: Users can only access their own tasks - backend already implemented, verify integration

**Independent Test**: Create tasks as User A, attempt access as User B, verify 404/403 response

**Note**: Backend implementation is already complete. This phase verifies isolation works.

### Verification for User Story 4

- [x] T024 [US4] Verify `backend/app/api/tasks.py` GET /tasks filters by authenticated user's owner_id
- [x] T025 [US4] Verify `backend/app/api/tasks.py` GET /tasks/{id} returns 404 for other users' tasks
- [x] T026 [US4] Verify `backend/app/api/tasks.py` PUT /tasks/{id} rejects updates to other users' tasks
- [x] T027 [US4] Verify `backend/app/api/tasks.py` DELETE /tasks/{id} rejects deletion of other users' tasks
- [x] T028 [US4] Verify task creation automatically sets owner_id from authenticated user

**Acceptance Criteria**:
- FR-015, FR-016, FR-017, FR-018, FR-019: Per-user isolation enforced
- SC-003: 100% of cross-user access attempts blocked
- SC-005: 0% data leakage between users

**Checkpoint**: Data isolation verified - users see only their own tasks

---

## Phase 7: User Story 5 - Frontend JWT Handling (Priority: P5)

**Goal**: Frontend automatically attaches JWT to API requests and handles 401 redirects

**Independent Test**: Monitor network requests for Authorization header, trigger 401, verify redirect

### Implementation for User Story 5

- [x] T029 [US5] Update `frontend/src/lib/api.ts` to attach JWT Bearer token to all requests
- [x] T030 [US5] Implement 401 response interceptor to redirect to /login
- [x] T031 [US5] Update `frontend/src/lib/auth.ts` to integrate with Better Auth client
- [x] T032 [US5] Implement logout function that clears JWT from localStorage
- [x] T033 [US5] Add logout button/link to dashboard navigation

**Acceptance Criteria**:
- FR-009: JWT attached to every API request
- FR-022: 401 responses redirect to sign-in
- SC-006: Frontend automatically attaches JWT without manual intervention
- SC-007: Users redirected to sign-in on authentication failure

**Checkpoint**: JWT handling complete - seamless authentication across all API calls

---

## Phase 8: Polish & End-to-End Verification

**Purpose**: Verify complete auth flow and cross-cutting concerns

- [x] T034 [P] Test complete sign-up flow: register → dashboard → create task
- [x] T035 [P] Test complete sign-in flow: login → view tasks → logout
- [x] T036 Test cross-user isolation: User A tasks not visible to User B
- [x] T037 Test expired token handling: verify redirect to login
- [x] T038 [P] Run quickstart.md verification steps
- [x] T039 Security review: verify JWT_SECRET not in code, tokens not logged

**Success Criteria Verification**:
- SC-001: Sign-up and sign-in complete in under 30 seconds
- SC-008: Backend remains stateless (no session storage)
- SC-009: JWT expiration enforced
- SC-010: Same JWT secret validates tokens across frontend and backend

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (Sign Up) and US2 (Sign In) can proceed in parallel
  - US3 and US4 are verification-only (backend complete)
  - US5 (JWT Handling) can proceed in parallel with US1/US2
- **Polish (Phase 8)**: Depends on all user stories being complete

### Parallel Opportunities

- T002, T003 can run in parallel (different env files)
- T006, T007 can run in parallel (different verification targets)
- US1 (T008-T013) and US2 (T014-T019) can run in parallel (different pages)
- US3 and US4 verification tasks can run in parallel
- T034, T035, T038, T039 can run in parallel (different test scenarios)

### Critical Path

1. T001 (install Better Auth)
2. T004, T005 (configure auth client)
3. T008-T012 (US1: Sign Up - MVP)
4. T014-T018 (US2: Sign In)
5. T029-T032 (US5: JWT Handling)
6. T034-T039 (End-to-End Verification)

---

## Notes

- Backend JWT implementation is already complete - minimal backend changes required
- Focus is on frontend Better Auth integration
- Verification tasks (US3, US4) confirm existing backend functionality
- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
