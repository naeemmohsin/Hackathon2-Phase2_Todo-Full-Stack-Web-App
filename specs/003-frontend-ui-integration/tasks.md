# Tasks: Frontend Application (UI, UX & Integration)

**Input**: Design documents from `/specs/003-frontend-ui-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Key Finding**: Frontend is already ~90% implemented from Spec 1 & 2. Tasks focus on verification and gap closure.

**Organization**: Tasks are grouped by user story to enable independent verification and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/src/` (all frontend code)
- **Components**: `frontend/src/components/` (React components)
- **Lib**: `frontend/src/lib/` (utilities and services)
- **App**: `frontend/src/app/` (Next.js pages)

---

## Phase 1: Setup (Verification Environment)

**Purpose**: Ensure development environment is ready for verification

- [x] T001 Verify frontend dependencies are installed (`cd frontend && npm install`)
- [x] T002 [P] Verify backend is running and accessible at http://localhost:8000
- [x] T003 [P] Verify frontend dev server starts (`npm run dev`)
- [x] T004 Verify frontend builds without errors (`npm run build`)

---

## Phase 2: Foundational (Cross-Cutting Verification)

**Purpose**: Verify foundational elements work across all user stories

**⚠️ CRITICAL**: These must pass before user story verification

- [x] T005 Verify JWT token is stored in localStorage after authentication in `frontend/src/lib/api.ts`
- [x] T006 [P] Verify Authorization header is attached to all API requests in `frontend/src/lib/api.ts`
- [x] T007 [P] Verify 401 responses redirect to login in `frontend/src/lib/api.ts`
- [x] T008 Verify responsive breakpoints are configured in `frontend/tailwind.config.ts`
- [x] T009 [P] Verify loading state component exists in `frontend/src/app/dashboard/page.tsx`

**Checkpoint**: Foundation verified - user story verification can begin

---

## Phase 3: User Story 1 - User Registration Flow (Priority: P1) 🎯 MVP

**Goal**: Verify new users can create accounts and are redirected to dashboard

**Independent Test**: Visit /register, complete form, verify redirect to dashboard

### Verification for User Story 1

- [x] T010 [US1] Verify RegisterForm exists and renders in `frontend/src/components/auth/RegisterForm.tsx`
- [x] T011 [US1] Verify email validation displays error for invalid format in `frontend/src/components/auth/RegisterForm.tsx`
- [x] T012 [US1] Verify password validation displays error for < 8 characters in `frontend/src/components/auth/RegisterForm.tsx`
- [x] T013 [US1] Verify form submission calls `/auth/register` endpoint
- [x] T014 [US1] Verify successful registration redirects to /dashboard
- [x] T015 [US1] Verify duplicate email error is displayed clearly
- [x] T016 [US1] Verify loading state is shown during form submission

**Acceptance Criteria**:
- FR-001: Sign-up page with email/password ✓
- FR-003: Email validation ✓
- FR-004: Password validation ✓
- FR-005: Field-level errors ✓
- FR-006: Server-side errors ✓

**Checkpoint**: User Story 1 verified - new users can register

---

## Phase 4: User Story 2 - User Sign In Flow (Priority: P2)

**Goal**: Verify returning users can sign in and access dashboard

**Independent Test**: Visit /login with valid credentials, verify redirect to dashboard

### Verification for User Story 2

- [x] T017 [US2] Verify LoginForm exists and renders in `frontend/src/components/auth/LoginForm.tsx`
- [x] T018 [US2] Verify email validation displays error for invalid format
- [x] T019 [US2] Verify form submission calls `/auth/login` endpoint
- [x] T020 [US2] Verify successful login redirects to /dashboard
- [x] T021 [US2] Verify invalid credentials error is displayed without revealing which field was wrong
- [x] T022 [US2] Verify authenticated users accessing /login are redirected to /dashboard

**Acceptance Criteria**:
- FR-002: Sign-in page with email/password ✓
- FR-007: Redirect authenticated users from auth pages ✓

**Checkpoint**: User Story 2 verified - returning users can sign in

---

## Phase 5: User Story 3 - Task Creation (Priority: P3)

**Goal**: Verify authenticated users can create new tasks

**Independent Test**: Login, enter task title, submit, verify task appears in list

### Verification for User Story 3

- [x] T023 [US3] Verify CreateTaskForm exists and renders in `frontend/src/components/tasks/CreateTaskForm.tsx`
- [x] T024 [US3] Verify empty title validation prevents submission
- [x] T025 [US3] Verify form submission calls `/tasks` POST endpoint
- [x] T026 [US3] Verify new task appears in list after creation
- [x] T027 [US3] Verify loading state is shown during submission
- [x] T028 [US3] Verify error message displays on network failure

**Acceptance Criteria**:
- FR-013: Create task form with title input ✓
- FR-020: Loading indicators ✓
- FR-021: Error messages ✓

**Checkpoint**: User Story 3 verified - users can create tasks

---

## Phase 6: User Story 4 - Task List Viewing (Priority: P4)

**Goal**: Verify authenticated users can view their task list

**Independent Test**: Login with user that has tasks, verify all tasks displayed

### Verification for User Story 4

- [x] T029 [US4] Verify TaskList component exists in `frontend/src/components/tasks/TaskList.tsx`
- [x] T030 [US4] Verify tasks are fetched on dashboard mount in `frontend/src/app/dashboard/page.tsx`
- [x] T031 [US4] Verify tasks display in chronological order (newest first)
- [x] T032 [US4] Verify loading indicator shows while tasks are loading
- [x] T033 [US4] Verify empty state message when user has no tasks (Gap: may need to add)
- [x] T034 [US4] Verify task completion status is visually indicated

**Gap Closure Task**:
- [x] T035 [US4] Add empty state message to TaskList if missing in `frontend/src/components/tasks/TaskList.tsx`

**Acceptance Criteria**:
- FR-014: Display all tasks in list format ✓
- FR-015: Show completion status visually ✓
- FR-019: Chronological order ✓
- FR-022: Empty state message ✓

**Checkpoint**: User Story 4 verified - users can view tasks

---

## Phase 7: User Story 5 - Task Completion Toggle (Priority: P5)

**Goal**: Verify users can toggle task completion status

**Independent Test**: Click completion toggle on task, verify visual state changes

### Verification for User Story 5

- [x] T036 [US5] Verify TaskItem has completion toggle in `frontend/src/components/tasks/TaskItem.tsx`
- [x] T037 [US5] Verify clicking toggle calls `/tasks/{id}/toggle` PATCH endpoint
- [x] T038 [US5] Verify visual state updates on successful toggle
- [x] T039 [US5] Verify error handling when toggle fails
- [x] T040 [US5] Verify toggle target is at least 44x44px for touch (Gap: verify)

**Gap Closure Task**:
- [x] T041 [US5] Ensure toggle button meets 44x44px minimum touch target in `frontend/src/components/tasks/TaskItem.tsx`

**Acceptance Criteria**:
- FR-016: Toggle completion with single click/tap ✓
- FR-026: Touch-friendly tap targets (44x44px minimum) ✓

**Checkpoint**: User Story 5 verified - users can toggle task completion

---

## Phase 8: User Story 6 - Task Editing (Priority: P6)

**Goal**: Verify users can edit task titles

**Independent Test**: Click edit, change title, save, verify updated title

### Verification for User Story 6

- [x] T042 [US6] Verify edit button exists on TaskItem in `frontend/src/components/tasks/TaskItem.tsx`
- [x] T043 [US6] Verify EditTaskModal opens on edit click in `frontend/src/components/tasks/EditTaskModal.tsx`
- [x] T044 [US6] Verify modal pre-fills with current task title
- [x] T045 [US6] Verify empty title validation prevents save
- [x] T046 [US6] Verify save calls `/tasks/{id}` PUT endpoint
- [x] T047 [US6] Verify updated title displays after save
- [x] T048 [US6] Verify cancel preserves original title

**Acceptance Criteria**:
- FR-017: Edit functionality for task titles ✓

**Checkpoint**: User Story 6 verified - users can edit tasks

---

## Phase 9: User Story 7 - Task Deletion (Priority: P7)

**Goal**: Verify users can delete tasks with confirmation

**Independent Test**: Click delete, confirm, verify task removed from list

### Verification for User Story 7

- [x] T049 [US7] Verify delete button exists on TaskItem in `frontend/src/components/tasks/TaskItem.tsx`
- [x] T050 [US7] Verify confirmation dialog appears before deletion
- [x] T051 [US7] Verify confirming calls `/tasks/{id}` DELETE endpoint
- [x] T052 [US7] Verify task is removed from list after deletion
- [x] T053 [US7] Verify canceling preserves the task
- [x] T054 [US7] Verify error handling when deletion fails

**Acceptance Criteria**:
- FR-018: Delete functionality with confirmation ✓

**Checkpoint**: User Story 7 verified - users can delete tasks

---

## Phase 10: User Story 8 - User Logout (Priority: P8)

**Goal**: Verify users can log out and session is cleared

**Independent Test**: Click logout, verify redirect to login with cleared session

### Verification for User Story 8

- [x] T055 [US8] Verify logout button exists on dashboard in `frontend/src/app/dashboard/page.tsx`
- [x] T056 [US8] Verify clicking logout calls logout function in `frontend/src/lib/auth.ts`
- [x] T057 [US8] Verify JWT token is cleared from localStorage
- [x] T058 [US8] Verify redirect to /login after logout
- [x] T059 [US8] Verify accessing /dashboard after logout redirects to /login

**Acceptance Criteria**:
- FR-008: Logout button on authenticated pages ✓
- FR-009: Redirect unauthenticated users to login ✓

**Checkpoint**: User Story 8 verified - users can log out

---

## Phase 11: Accessibility & Polish

**Purpose**: Close accessibility gaps and verify cross-cutting concerns

### Accessibility Verification

- [x] T060 [P] Verify keyboard navigation works on all interactive elements
- [x] T061 [P] Audit ARIA labels on form inputs in `frontend/src/components/ui/Input.tsx`
- [x] T062 [P] Audit ARIA labels on buttons in `frontend/src/components/ui/Button.tsx`
- [x] T063 [P] Verify color contrast meets WCAG AA standards

### Gap Closure Tasks

- [x] T064 Add missing ARIA labels to interactive elements if needed
- [x] T065 Add `aria-label` to icon buttons (edit, delete, toggle) in `frontend/src/components/tasks/TaskItem.tsx`

### Enhancement Tasks (Optional)

- [ ] T066 [P] Add optimistic UI updates to task toggle in `frontend/src/app/dashboard/page.tsx`
- [ ] T067 [P] Add optimistic UI updates to task creation in `frontend/src/app/dashboard/page.tsx`

### Final Verification

- [x] T068 Run complete build verification (`npm run build`)
- [x] T069 [P] Run responsive design verification (320px to 1920px)
- [x] T070 Execute quickstart.md verification checklist

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3-10)**: All depend on Foundational phase
  - US1-US2 (Auth): Can run in parallel
  - US3-US7 (Tasks): Can run in parallel after auth verification
  - US8 (Logout): Can run after auth verification
- **Polish (Phase 11)**: Depends on all user stories being verified

### User Story Dependencies

- **US1 (Registration)**: No dependencies - entry point
- **US2 (Sign In)**: Requires registered user (depends on US1 for test data)
- **US3 (Task Creation)**: Requires authenticated user (depends on US1 or US2)
- **US4 (Task Viewing)**: Requires authenticated user with tasks (depends on US3)
- **US5 (Task Toggle)**: Requires existing tasks (depends on US4)
- **US6 (Task Edit)**: Requires existing tasks (depends on US4)
- **US7 (Task Delete)**: Requires existing tasks (depends on US4)
- **US8 (Logout)**: Requires authenticated user (depends on US1 or US2)

### Parallel Opportunities

- T002, T003 can run in parallel (different verification targets)
- T005, T006, T007, T008, T009 - some can run in parallel
- US1 and US2 verification can run in parallel
- US3-US7 can run in parallel after prerequisite tasks
- T060-T063, T066-T067, T069 can run in parallel (different concerns)

---

## Implementation Strategy

### Verification-First Approach

Since ~90% of functionality is already implemented:

1. Complete Phase 1: Setup verification
2. Complete Phase 2: Foundational verification
3. Verify US1 (Registration) → MVP checkpoint
4. Verify US2 (Sign In) → Auth complete
5. Verify US3-US7 (Task CRUD) → Core features verified
6. Verify US8 (Logout) → Full flow verified
7. Complete Phase 11: Gap closure and polish

### Gap Closure Priority

If gaps are found during verification:
1. **Critical**: FR-022 empty state, FR-023 optimistic updates
2. **Important**: FR-026 touch targets, FR-028/029 accessibility
3. **Nice-to-have**: Color contrast verification

### MVP Scope

User Story 1 (Registration) alone provides:
- Working sign-up flow
- JWT authentication
- Redirect to dashboard

This is a viable demonstration even without other stories.

---

## Notes

- Most tasks are VERIFICATION tasks, not implementation tasks
- Implementation is only needed for identified gaps (T035, T041, T064-T067)
- [P] tasks = different files/concerns, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently verifiable
- Stop at any checkpoint to validate story independently
- Total estimated effort: 10-20% of greenfield implementation
