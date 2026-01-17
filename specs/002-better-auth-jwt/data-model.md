# Data Model: Authentication & Security Integration

**Feature**: 002-better-auth-jwt
**Date**: 2026-01-11

## Entity Overview

This feature introduces no new database entities. It leverages the existing User and Task models from spec-001, with focus on JWT token flow rather than data storage.

## Existing Entities (No Changes Required)

### User (Existing)

**Source**: `backend/app/models/user.py`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique user identifier (used in JWT `sub` claim) |
| email | string | unique, indexed | User email address |
| hashed_password | string | required | bcrypt-hashed password |
| created_at | datetime | auto-generated | Account creation timestamp |

**Relationships**:
- One-to-many with Task (owner)

### Task (Existing)

**Source**: `backend/app/models/task.py`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique task identifier |
| title | string | max 500 chars | Task description |
| is_completed | boolean | default false | Completion status |
| owner_id | UUID | FK → User.id, indexed | Task owner reference |
| created_at | datetime | auto-generated | Task creation timestamp |
| updated_at | datetime | auto-generated | Last modification timestamp |

**Relationships**:
- Many-to-one with User (owner)

## JWT Token Structure (Stateless - No Storage)

JWT tokens are not stored in the database. They are:
- Generated on authentication by FastAPI backend
- Validated on each request using signature verification
- Contain user identity without database lookup for validation

### Token Payload Schema

```json
{
  "sub": "uuid-string",     // User ID
  "email": "user@example.com",
  "exp": 1736625600,        // Expiration timestamp
  "iat": 1736539200         // Issued at timestamp
}
```

### Token Configuration

| Setting | Value | Source |
|---------|-------|--------|
| Algorithm | HS256 | `backend/app/config.py` |
| Expiration | 24 hours | `JWT_EXPIRATION_HOURS` env var |
| Secret | From env | `JWT_SECRET` env var |

## Better Auth Client State (Frontend Only)

Better Auth manages client-side authentication state. No additional database tables required.

### Client State Shape

```typescript
interface AuthState {
  user: {
    id: string;
    email: string;
  } | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
```

### Storage Location

| Data | Storage | Persistence |
|------|---------|-------------|
| JWT Token | localStorage | Survives page refresh |
| User Info | Memory (React state) | Cleared on page refresh, rehydrated from token |

## Data Flow Diagrams

### Authentication Flow

```
┌──────────┐      ┌─────────────┐      ┌─────────────┐
│  Better  │      │   FastAPI   │      │  PostgreSQL │
│   Auth   │      │   Backend   │      │   Database  │
│   (UI)   │      │             │      │             │
└────┬─────┘      └──────┬──────┘      └──────┬──────┘
     │                   │                    │
     │ POST /auth/login  │                    │
     │ {email, password} │                    │
     │──────────────────>│                    │
     │                   │ SELECT user        │
     │                   │ WHERE email = ?    │
     │                   │───────────────────>│
     │                   │                    │
     │                   │ User record        │
     │                   │<───────────────────│
     │                   │                    │
     │                   │ Verify bcrypt      │
     │                   │ Generate JWT       │
     │                   │                    │
     │ {token, user}     │                    │
     │<──────────────────│                    │
     │                   │                    │
     │ Store in          │                    │
     │ localStorage      │                    │
     └───────────────────┴────────────────────┘
```

### Protected Request Flow

```
┌──────────┐      ┌─────────────┐      ┌─────────────┐
│ Frontend │      │   FastAPI   │      │  PostgreSQL │
│   API    │      │   Backend   │      │   Database  │
│  Client  │      │             │      │             │
└────┬─────┘      └──────┬──────┘      └──────┬──────┘
     │                   │                    │
     │ GET /tasks        │                    │
     │ Authorization:    │                    │
     │ Bearer <JWT>      │                    │
     │──────────────────>│                    │
     │                   │                    │
     │                   │ Verify JWT         │
     │                   │ signature + exp    │
     │                   │ (no DB call)       │
     │                   │                    │
     │                   │ Extract user_id    │
     │                   │ from JWT.sub       │
     │                   │                    │
     │                   │ SELECT tasks       │
     │                   │ WHERE owner_id = ? │
     │                   │───────────────────>│
     │                   │                    │
     │                   │ Task records       │
     │                   │<───────────────────│
     │                   │                    │
     │ [tasks]           │                    │
     │<──────────────────│                    │
     └───────────────────┴────────────────────┘
```

## Validation Rules

### User Registration
- Email must be valid format
- Email must be unique (database constraint)
- Password minimum 8 characters (enforced by Better Auth + backend)

### JWT Validation
- Signature must match using JWT_SECRET
- Expiration time must be in the future
- `sub` claim must contain valid UUID

### Task Ownership
- `owner_id` must match authenticated user's ID
- Enforced at query level: `WHERE owner_id = current_user.id`

## Migration Notes

**No database migrations required for this feature.**

The existing schema fully supports the authentication requirements:
- User table has all necessary fields
- Task table already has `owner_id` foreign key
- All ownership filtering is implemented in service layer
