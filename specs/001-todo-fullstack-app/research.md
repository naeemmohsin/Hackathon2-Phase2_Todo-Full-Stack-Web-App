# Research: Todo Full-Stack Web Application

**Feature Branch**: `001-todo-fullstack-app`
**Date**: 2026-01-11
**Status**: Complete

## Overview

This document captures technology decisions and research findings for the Todo Full-Stack Web Application. All decisions align with the fixed technology stack defined in the constitution.

## Technology Decisions

### 1. Backend Framework: FastAPI

**Decision**: Use FastAPI as the Python backend framework

**Rationale**:
- Constitution mandates FastAPI (Principle IV)
- Native async support for efficient concurrent connections
- Automatic OpenAPI documentation generation
- Built-in request validation via Pydantic
- Excellent performance for REST APIs

**Alternatives Considered**:
- Django REST Framework: More opinionated, heavier weight
- Flask: Less structured, manual validation needed
- Tornado: Lower-level, more boilerplate

**Best Practices**:
- Use dependency injection for database sessions and auth
- Organize routes in separate modules (api/auth.py, api/tasks.py)
- Use Pydantic models for request/response validation
- Implement proper CORS configuration for frontend

### 2. ORM: SQLModel

**Decision**: Use SQLModel for database models and queries

**Rationale**:
- Constitution mandates SQLModel (Principle IV)
- Combines SQLAlchemy ORM with Pydantic validation
- Single model definition serves as both DB schema and API schema
- Type hints provide IDE support and documentation

**Alternatives Considered**:
- Pure SQLAlchemy: More boilerplate, separate Pydantic models needed
- Tortoise ORM: Less mature, different async model
- Raw SQL: Too error-prone, no type safety

**Best Practices**:
- Define models in separate files (models/user.py, models/task.py)
- Use `SQLModel` base class for database tables
- Define relationships using `Relationship` field
- Use `Optional` for nullable fields

### 3. Database: Neon Serverless PostgreSQL

**Decision**: Use Neon as the PostgreSQL provider

**Rationale**:
- Constitution mandates Neon PostgreSQL (Principle IV)
- Serverless architecture scales automatically
- PostgreSQL compatibility ensures standard SQL support
- Built-in connection pooling for concurrent access

**Alternatives Considered**:
- AWS RDS: Requires server management
- Supabase: Different authentication model
- Local PostgreSQL: Not cloud-ready

**Best Practices**:
- Use connection pooling (Neon provides this)
- Set `sslmode=require` for secure connections
- Store connection string in environment variables
- Use SQLModel's async session for non-blocking queries

### 4. Authentication: JWT with Better Auth

**Decision**: Use JWT tokens with Better Auth on frontend, python-jose on backend

**Rationale**:
- Constitution mandates Better Auth + JWT (Principle IV)
- Stateless authentication fits backend requirement
- Shared JWT secret enables cross-service validation
- Better Auth provides React hooks for auth state

**Alternatives Considered**:
- Session-based auth: Requires server-side state
- OAuth2 only: Overkill for simple email/password
- Firebase Auth: Different ecosystem

**Best Practices**:
- Use HS256 algorithm with shared secret
- Set reasonable token expiry (24 hours)
- Include user ID in token subject claim
- Validate token on every protected request
- Store token in httpOnly cookie or secure localStorage

### 5. Frontend Framework: Next.js App Router

**Decision**: Use Next.js 16+ with App Router

**Rationale**:
- Constitution mandates Next.js 16+ (Principle IV)
- App Router provides modern React Server Components
- Built-in routing and middleware support
- Excellent TypeScript support

**Alternatives Considered**:
- Pages Router: Legacy pattern, less optimal
- Create React App: No SSR, manual routing
- Remix: Different data loading pattern

**Best Practices**:
- Use App Router directory structure (app/)
- Implement middleware for route protection
- Use Server Components where possible
- Client Components only for interactivity
- Fetch API client for backend communication

### 6. Styling: Tailwind CSS

**Decision**: Use Tailwind CSS for styling

**Rationale**:
- Rapid development with utility classes
- Responsive design built-in
- Minimal CSS bundle with purging
- Consistent design system

**Alternatives Considered**:
- CSS Modules: More boilerplate
- Styled Components: Runtime overhead
- Plain CSS: Harder to maintain

**Best Practices**:
- Configure custom colors if needed
- Use responsive prefixes (sm:, md:, lg:)
- Extract common patterns to components
- Use cn() utility for conditional classes

### 7. Password Hashing: bcrypt

**Decision**: Use bcrypt for password hashing

**Rationale**:
- Industry standard for password security
- Adaptive cost factor for future-proofing
- Built-in salt generation
- Available via `passlib` library

**Alternatives Considered**:
- Argon2: Newer but less widely adopted
- SHA-256: Not designed for passwords
- PBKDF2: Less secure than bcrypt

**Best Practices**:
- Use cost factor of 12 (default)
- Never store plain text passwords
- Hash on registration, verify on login
- Use constant-time comparison

## Integration Patterns

### Frontend-Backend Communication

```
Frontend (Next.js) → API Client → HTTP Request → FastAPI → Database
                   ↑                            ↓
                JWT Token              JWT Validation
```

### JWT Flow

1. User submits credentials
2. Backend validates credentials
3. Backend generates JWT with user ID
4. Frontend stores JWT
5. Frontend includes JWT in Authorization header
6. Backend validates JWT on each request
7. Backend extracts user ID from token

### Error Handling Pattern

| Layer | Responsibility |
|-------|----------------|
| Database | SQLAlchemy exceptions |
| Service | Business logic validation |
| API | HTTP status codes, JSON errors |
| Frontend | User-friendly messages |

## Security Considerations

1. **Password Storage**: bcrypt with cost factor 12
2. **Token Security**: JWT with HS256, 24h expiry
3. **CORS**: Restrict to frontend origin only
4. **Input Validation**: Pydantic models validate all input
5. **SQL Injection**: SQLModel/SQLAlchemy parameterized queries
6. **XSS**: React's automatic escaping
7. **CSRF**: Not applicable for JWT-based auth

## Performance Considerations

1. **Database Connections**: Use connection pooling (Neon built-in)
2. **JWT Validation**: Stateless, no database lookup needed
3. **Task Queries**: Index on owner_id for efficient filtering
4. **Frontend Rendering**: Server Components for initial load
5. **API Response Size**: Return only necessary fields

## Unresolved Items

None - all technology choices are defined by the constitution.

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- Neon Documentation: https://neon.tech/docs
- Better Auth Documentation: https://www.better-auth.com/
- Next.js App Router: https://nextjs.org/docs/app
