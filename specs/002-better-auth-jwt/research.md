# Research: Authentication & Security Integration (Better Auth + JWT)

**Feature**: 002-better-auth-jwt
**Date**: 2026-01-11
**Status**: Complete

## Executive Summary

This research document addresses the integration of Better Auth with the existing Todo application. The key finding is that Better Auth uses **cookie-based session management by default**, but provides a **bearer token plugin** that enables token-based API authentication suitable for our FastAPI backend.

## Research Questions & Findings

### RQ-001: Better Auth Token Strategy

**Question**: How does Better Auth handle JWT tokens and can it share secrets with FastAPI?

**Findings**:
- Better Auth uses cookie-based sessions by default, NOT JWTs
- The **bearer token plugin** enables token-based authentication
- Bearer tokens from Better Auth are NOT standard JWTs - they are session tokens
- Better Auth does NOT support sharing JWT secrets with external backends

**Decision**: Use Better Auth's bearer token plugin, and configure FastAPI to validate Better Auth session tokens OR implement a hybrid approach where Better Auth issues tokens and FastAPI independently verifies them.

**Rationale**: The spec requires JWT tokens validated by FastAPI. Since Better Auth's bearer tokens are session-based (not JWTs), we have two options:
1. **Option A**: Keep existing backend JWT implementation, use Better Auth only for UI, sync users between systems
2. **Option B**: Use Better Auth as the sole auth provider, have FastAPI call Better Auth to validate tokens

**Selected**: **Option A** - Hybrid approach with shared JWT secret

**Alternatives Rejected**:
- Option B requires network calls from FastAPI to Better Auth on every request, adding latency
- Pure Better Auth would require deploying Better Auth as a separate service

### RQ-002: Better Auth Bearer Plugin Configuration

**Question**: How to configure Better Auth to issue bearer tokens?

**Findings**:
```typescript
// Server configuration
import { bearer } from "better-auth/plugins";

export const auth = betterAuth({
    plugins: [bearer()]
});

// Client retrieval after sign-in
const authToken = ctx.response.headers.get("set-auth-token");
localStorage.setItem("bearer_token", authToken);
```

**Decision**: Install bearer plugin and configure token retrieval on successful authentication.

### RQ-003: Existing Codebase Analysis

**Question**: What authentication infrastructure already exists?

**Findings**:
The existing codebase has a **complete JWT implementation**:

**Backend (FastAPI)**:
- `backend/app/services/auth.py`: JWT creation/verification using python-jose
- `backend/app/api/deps.py`: `CurrentUser` dependency extracts user from JWT
- `backend/app/config.py`: JWT secret, algorithm (HS256), expiration (24h) from env vars
- All task routes already require authentication via `CurrentUser` dependency

**Frontend (Next.js)**:
- `frontend/src/lib/api.ts`: API client with Bearer token attachment
- `frontend/src/lib/auth.ts`: Login/register functions storing tokens in localStorage
- `frontend/src/middleware.ts`: Route protection

**Decision**: The backend JWT infrastructure is complete and well-implemented. Focus Better Auth integration on the frontend only, replacing the custom auth UI with Better Auth's components while maintaining the existing JWT token flow.

### RQ-004: Integration Strategy

**Question**: How to integrate Better Auth without breaking existing backend?

**Findings**:
Two viable approaches:

1. **Replace Frontend Auth Only**:
   - Use Better Auth for sign-up/sign-in UI
   - Backend continues issuing JWTs via `/auth/register` and `/auth/login` endpoints
   - Better Auth calls existing backend auth endpoints
   - Store returned JWT in localStorage (current behavior)

2. **Full Better Auth Integration**:
   - Deploy Better Auth with its own database tables
   - Configure Better Auth to issue JWTs (not default behavior)
   - Share JWT secret between Better Auth and FastAPI
   - Requires significant backend changes

**Decision**: **Approach 1** - Frontend-only Better Auth integration
- Minimal backend changes required
- Maintains existing security model
- Better Auth handles UI/UX, backend handles token issuance

**Rationale**: The existing backend JWT implementation satisfies all spec requirements. Better Auth adds value as a UI library, not as a replacement auth system.

### RQ-005: JWT Secret Sharing

**Question**: How to ensure same JWT secret is used by frontend and backend?

**Findings**:
- Backend reads `JWT_SECRET` from `.env` file
- Better Auth (in our hybrid approach) doesn't need the JWT secret - it calls backend APIs
- Only the FastAPI backend creates and validates JWTs

**Decision**: No secret sharing required with hybrid approach. Backend remains the sole JWT issuer and validator.

## Technical Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth strategy | Hybrid (Better Auth UI + Backend JWT) | Maintains existing security, minimal changes |
| Token type | JWT (unchanged) | Already implemented, spec requirement |
| Token storage | localStorage | Already implemented, Better Auth compatible |
| User management | Backend database | Single source of truth |
| Session validation | FastAPI JWT verification | Stateless, already implemented |

## Implementation Impact

### Files to Modify (Frontend)
- `frontend/package.json` - Add Better Auth dependencies
- `frontend/src/lib/auth-client.ts` - New: Better Auth client configuration
- `frontend/src/app/login/page.tsx` - Replace with Better Auth sign-in
- `frontend/src/app/register/page.tsx` - Replace with Better Auth sign-up
- `frontend/src/components/auth/*` - May be removed or simplified

### Files to Preserve (Backend)
- All backend files remain unchanged
- JWT implementation already complete and correct
- Task routes already enforce user isolation

### New Environment Variables
- `BETTER_AUTH_URL` - Better Auth endpoint (if needed)
- No JWT secret changes required

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Better Auth API changes | Medium | Pin exact version in package.json |
| Token format mismatch | Low | Backend issues tokens, format unchanged |
| Session sync issues | Low | Both systems use same user ID |

## References

- [Better Auth Documentation](https://www.better-auth.com/)
- [Better Auth Next.js Integration](https://www.better-auth.com/docs/integrations/next)
- [Better Auth Bearer Plugin](https://www.better-auth.com/docs/plugins/bearer)
- Existing codebase: `backend/app/services/auth.py`, `frontend/src/lib/auth.ts`
