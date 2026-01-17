# Quickstart: Authentication & Security Integration

**Feature**: 002-better-auth-jwt
**Date**: 2026-01-11

## Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (Neon or local)
- Existing spec-001 implementation complete

## Environment Setup

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://user:password@host/database

# JWT Configuration (REQUIRED)
JWT_SECRET=your-secure-random-secret-at-least-32-characters
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth (optional - for future expansion)
# BETTER_AUTH_SECRET=same-as-jwt-secret-if-needed
```

## Installation Steps

### 1. Install Better Auth (Frontend)

```bash
cd frontend
npm install better-auth
```

### 2. Backend Dependencies (Already Installed)

The backend already has all required dependencies:
- `python-jose[cryptography]` - JWT handling
- `passlib[bcrypt]` - Password hashing
- `fastapi` - API framework

No additional backend packages required.

### 3. Start Services

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Quick Verification

### 1. Test Backend Auth Endpoints

```bash
# Register a user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"securepass123"}'

# Expected: {"token":"eyJ...", "user":{...}}

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"securepass123"}'

# Expected: {"token":"eyJ...", "user":{...}}
```

### 2. Test Protected Endpoints

```bash
# Save token from login response
TOKEN="eyJ..."

# Access tasks (should work)
curl http://localhost:8000/tasks \
  -H "Authorization: Bearer $TOKEN"

# Expected: []

# Access without token (should fail)
curl http://localhost:8000/tasks

# Expected: {"detail":"Not authenticated"}
```

### 3. Test Frontend Auth Flow

1. Navigate to http://localhost:3000
2. Click "Register" or navigate to /register
3. Enter email and password
4. Verify redirect to dashboard
5. Create a task
6. Logout and login again
7. Verify tasks persist

## Security Checklist

- [ ] JWT_SECRET is set and at least 32 characters
- [ ] JWT_SECRET is NOT committed to version control
- [ ] HTTPS in production (CORS origins updated)
- [ ] Password minimum length enforced (8 characters)
- [ ] Token expiration is reasonable (24 hours default)

## Troubleshooting

### "Could not validate credentials"
- Check JWT_SECRET matches between restarts
- Verify token hasn't expired
- Check token format: `Bearer <token>` (with space)

### "CORS error"
- Verify `CORS_ORIGINS` includes frontend URL
- Restart backend after .env changes

### "Module not found" (Frontend)
- Run `npm install` in frontend directory
- Delete `node_modules` and reinstall if needed

### Token not persisted after refresh
- Check browser localStorage: `auth_token` key
- Verify no JavaScript errors in console

## Architecture Summary

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Better Auth   │  │   API Client    │  │   Pages/    │ │
│  │   Components    │──│   (with JWT)    │──│   Components│ │
│  └────────┬────────┘  └────────┬────────┘  └─────────────┘ │
│           │                    │                            │
│           │    localStorage    │                            │
│           └───── [JWT Token] ──┘                            │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP + Bearer Token
┌───────────────────────▼─────────────────────────────────────┐
│                        Backend (FastAPI)                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Auth Routes    │  │  JWT Middleware │  │   Task      │ │
│  │  /auth/*        │──│  (deps.py)      │──│   Routes    │ │
│  └────────┬────────┘  └────────┬────────┘  └──────┬──────┘ │
│           │                    │                   │        │
│           └─────── JWT Secret ─┴───────────────────┘        │
│                        (.env)                               │
└───────────────────────┬─────────────────────────────────────┘
                        │ SQL
┌───────────────────────▼─────────────────────────────────────┐
│                    PostgreSQL (Neon)                        │
│           ┌──────────────┐  ┌──────────────┐               │
│           │     User     │──│     Task     │               │
│           │    Table     │  │    Table     │               │
│           └──────────────┘  └──────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement Better Auth components
3. Test auth flow end-to-end
4. Verify user isolation (create tasks as different users)
