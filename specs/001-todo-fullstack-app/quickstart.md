# Quickstart Guide: Todo Full-Stack Web Application

**Feature Branch**: `001-todo-fullstack-app`
**Date**: 2026-01-11

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or pnpm
- Neon PostgreSQL account (https://neon.tech)

## Environment Setup

### 1. Clone and Navigate

```bash
cd phase2_Todo-Full-Stack-Web-App
git checkout 001-todo-fullstack-app
```

### 2. Create Neon Database

1. Go to https://console.neon.tech
2. Create a new project
3. Copy the connection string (will look like `postgresql://user:pass@host/db?sslmode=require`)

### 3. Generate JWT Secret

Generate a secure random string for JWT signing:

```bash
# Linux/Mac
openssl rand -hex 32

# Or use Python
python -c "import secrets; print(secrets.token_hex(32))"
```

Save this secret - you'll use it in both backend and frontend.

## Backend Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create `backend/.env`:

```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
JWT_SECRET=your-generated-secret-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:3000
```

### 4. Initialize Database

```bash
# This creates all tables
python -c "from app.database import init_db; init_db()"
```

### 5. Run Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

Backend will be available at http://localhost:8000

### 6. Verify Backend

Open http://localhost:8000/docs to see the Swagger UI.

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
# or
pnpm install
```

### 2. Configure Environment

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-generated-secret-here
```

**Important**: Use the same JWT secret as the backend!

### 3. Run Frontend Server

```bash
npm run dev
# or
pnpm dev
```

Frontend will be available at http://localhost:3000

## Verification Checklist

### Backend Health Check

```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

### Registration Test

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpassword123"}'
```

Expected response:
```json
{
  "user": {
    "id": "uuid-here",
    "email": "test@example.com",
    "created_at": "2026-01-11T..."
  },
  "token": "eyJhbGciOiJIUzI1..."
}
```

### Login Test

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpassword123"}'
```

### Create Task Test

```bash
# Replace TOKEN with the token from login response
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"title": "My first task"}'
```

### Frontend Test

1. Open http://localhost:3000
2. Click "Register" and create an account
3. Log in with your credentials
4. Create a task from the dashboard
5. Verify the task appears in the list
6. Toggle completion and verify visual change
7. Edit the task title
8. Delete the task
9. Log out and verify redirect to login

## Common Issues

### CORS Errors

Make sure `CORS_ORIGINS` in backend `.env` includes your frontend URL:
```env
CORS_ORIGINS=http://localhost:3000
```

### Database Connection Failed

1. Verify your Neon connection string is correct
2. Check that `sslmode=require` is included
3. Ensure your IP is allowed in Neon settings

### JWT Token Invalid

1. Ensure the same `JWT_SECRET` is used in both frontend and backend
2. Check that the token hasn't expired (24h default)
3. Verify the Authorization header format: `Bearer <token>`

### Frontend Can't Connect to Backend

1. Verify `NEXT_PUBLIC_API_URL` is correct
2. Ensure backend is running on port 8000
3. Check browser console for network errors

## Development Workflow

1. Start backend: `cd backend && uvicorn app.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Make changes
4. Backend auto-reloads on Python file changes
5. Frontend auto-reloads on TypeScript/React changes

## Project URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | User interface |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| ReDoc | http://localhost:8000/redoc | Alternative API docs |
