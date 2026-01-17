# Implementation Plan: Authentication & Security Integration (Better Auth + JWT)

**Branch**: `002-better-auth-jwt` | **Date**: 2026-01-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-better-auth-jwt/spec.md`

## Summary

Integrate Better Auth on the frontend for authentication UI (sign-up/sign-in) while maintaining the existing FastAPI JWT backend. The backend already has complete JWT authentication infrastructure - this feature focuses on:
1. Installing and configuring Better Auth on the frontend
2. Connecting Better Auth to existing backend auth endpoints
3. Ensuring JWT tokens flow correctly between frontend and backend
4. Verifying per-user data isolation works end-to-end

**Key Finding**: The backend authentication is already fully implemented. This is primarily a frontend integration task.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript/Node 18+ (frontend)
**Primary Dependencies**: FastAPI, python-jose, Next.js 14, Better Auth
**Storage**: PostgreSQL (Neon) - via existing SQLModel
**Testing**: pytest (backend), manual testing (frontend)
**Target Platform**: Web browser (desktop and mobile viewports)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <2s page load, <200ms API response
**Constraints**: Stateless backend, JWT-only auth, no sessions
**Scale/Scope**: Single-tenant, 50+ concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The constitution template is not fully configured. Applying default principles:

| Principle | Status | Notes |
|-----------|--------|-------|
| Security First | PASS | JWT with bcrypt hashing, no secrets in code |
| Stateless Backend | PASS | No session storage, JWT-only validation |
| Per-User Isolation | PASS | All queries filter by owner_id |
| Minimal Changes | PASS | Backend unchanged, frontend-only additions |

## Project Structure

### Documentation (this feature)

```text
specs/002-better-auth-jwt/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0: Better Auth research
├── data-model.md        # Phase 1: Data model documentation
├── quickstart.md        # Phase 1: Setup instructions
├── contracts/           # Phase 1: API contracts
│   └── auth-api.yaml    # OpenAPI specification
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── api/
│   │   ├── auth.py          # Auth endpoints (existing, no changes)
│   │   ├── deps.py          # JWT middleware (existing, no changes)
│   │   └── tasks.py         # Task endpoints (existing, no changes)
│   ├── models/
│   │   ├── user.py          # User model (existing)
│   │   └── task.py          # Task model (existing)
│   ├── services/
│   │   └── auth.py          # JWT creation/verification (existing)
│   └── config.py            # Settings (existing)
├── tests/
└── requirements.txt         # Dependencies (no changes)

frontend/
├── src/
│   ├── app/
│   │   ├── login/
│   │   │   └── page.tsx     # MODIFY: Integrate Better Auth sign-in
│   │   ├── register/
│   │   │   └── page.tsx     # MODIFY: Integrate Better Auth sign-up
│   │   └── dashboard/
│   │       └── page.tsx     # Existing (no changes)
│   ├── components/
│   │   └── auth/
│   │       ├── LoginForm.tsx    # May be replaced by Better Auth
│   │       └── RegisterForm.tsx # May be replaced by Better Auth
│   └── lib/
│       ├── api.ts           # Existing API client (no changes)
│       ├── auth.ts          # MODIFY: Integrate with Better Auth
│       ├── auth-client.ts   # NEW: Better Auth client configuration
│       └── types.ts         # Existing types
├── package.json             # MODIFY: Add better-auth dependency
└── .env.local               # Environment variables
```

**Structure Decision**: Web application with separate frontend/backend. Backend remains unchanged; all modifications in frontend.

## Implementation Phases

### Phase 1: Better Auth Installation and Configuration

**Objective**: Install Better Auth and create client configuration

**Tasks**:
1. Install Better Auth package: npm install better-auth
2. Create frontend/src/lib/auth-client.ts with Better Auth configuration
3. Configure Better Auth to use existing backend auth endpoints

**Acceptance Criteria**:
- Better Auth installed and importable
- Auth client configured with backend URL
- No breaking changes to existing code

### Phase 2: Sign-Up Integration

**Objective**: Replace custom registration with Better Auth sign-up

**Tasks**:
1. Update /register page to use Better Auth sign-up component
2. Configure sign-up to POST to /auth/register
3. Handle registration response (store JWT token)
4. Add validation error display

**Acceptance Criteria**:
- FR-002: Better Auth provides sign-up with email/password
- FR-004: JWT token issued and stored on success
- Users can register and are redirected to dashboard

### Phase 3: Sign-In Integration

**Objective**: Replace custom login with Better Auth sign-in

**Tasks**:
1. Update /login page to use Better Auth sign-in component
2. Configure sign-in to POST to /auth/login
3. Handle login response (store JWT token)
4. Add authentication error display

**Acceptance Criteria**:
- FR-003: Better Auth provides sign-in with email/password
- FR-004: JWT token issued and stored on success
- Users can sign in and access their tasks

### Phase 4: JWT Token Handling

**Objective**: Ensure JWT flows correctly through the system

**Tasks**:
1. Verify token is stored in localStorage on auth success
2. Confirm API client attaches Bearer token to all requests
3. Handle 401 responses by redirecting to sign-in
4. Clear token on logout

**Acceptance Criteria**:
- FR-009: JWT attached to every API request
- FR-022: 401 responses redirect to sign-in
- Token cleared on logout

### Phase 5: End-to-End Verification

**Objective**: Verify complete auth flow and user isolation

**Tasks**:
1. Test sign-up to dashboard to create task flow
2. Test sign-in to view tasks to logout flow
3. Test cross-user isolation (User A cannot see User B tasks)
4. Test expired token handling

**Acceptance Criteria**:
- SC-001: Sign-up and sign-in in under 30 seconds
- SC-002: 100% of requests without JWT return 401
- SC-003: 100% of cross-user access blocked
- SC-005: 0% data leakage between users

## Security Considerations

### Token Storage
- JWT stored in localStorage (client-side only)
- Token not httpOnly (required for JavaScript access)
- Risk: XSS could steal token
- Mitigation: Content Security Policy, input sanitization

### Secrets Management
- JWT_SECRET in environment variables only
- Never committed to version control
- Same secret across backend instances

### Password Security
- Passwords hashed with bcrypt (backend)
- Password validation by Better Auth (frontend)
- Minimum 8 characters enforced

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Better Auth incompatible with backend | Low | High | Research complete, hybrid approach planned |
| Token format mismatch | Low | Medium | Backend issues tokens, format unchanged |
| Breaking existing users | Low | High | No database changes, backward compatible |
| Performance degradation | Low | Low | No additional API calls |

## Dependencies

### External Dependencies
- better-auth npm package (frontend)
- Existing backend JWT implementation (python-jose)

### Internal Dependencies
- Spec 001 implementation complete
- Database schema with User and Task tables
- Environment variables configured

## Artifacts Generated

| Artifact | Path | Status |
|----------|------|--------|
| Research | specs/002-better-auth-jwt/research.md | Complete |
| Data Model | specs/002-better-auth-jwt/data-model.md | Complete |
| API Contract | specs/002-better-auth-jwt/contracts/auth-api.yaml | Complete |
| Quickstart | specs/002-better-auth-jwt/quickstart.md | Complete |
| Tasks | specs/002-better-auth-jwt/tasks.md | Pending (/sp.tasks) |

## Next Steps

1. Run /sp.tasks to generate detailed implementation tasks
2. Execute tasks in priority order (P1-P5)
3. Verify against success criteria
4. Create PR for review
