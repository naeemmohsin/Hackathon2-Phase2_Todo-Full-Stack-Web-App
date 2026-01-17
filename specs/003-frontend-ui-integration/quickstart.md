# Quickstart: Frontend Application (UI, UX & Integration)

**Feature**: 003-frontend-ui-integration
**Date**: 2026-01-12

## Prerequisites

- Node.js 20+
- npm 10+
- Backend server running (from Spec 1)
- Database configured with migrations applied

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

Frontend will be available at http://localhost:3000

## Verification Checklist

### Authentication Flow

- [ ] Navigate to http://localhost:3000/register
- [ ] Create new account with email/password
- [ ] Verify redirect to /dashboard
- [ ] Click "Logout" button
- [ ] Verify redirect to /login
- [ ] Sign in with created account
- [ ] Verify redirect to /dashboard

### Task Management

- [ ] Create a new task via form
- [ ] Verify task appears in list
- [ ] Click checkbox to toggle completion
- [ ] Verify visual state changes
- [ ] Click edit on a task
- [ ] Modify title and save
- [ ] Verify title updated
- [ ] Click delete on a task
- [ ] Confirm deletion
- [ ] Verify task removed from list

### Protected Routes

- [ ] Clear localStorage in browser dev tools
- [ ] Navigate to http://localhost:3000/dashboard
- [ ] Verify redirect to /login
- [ ] Sign in again
- [ ] Verify access to dashboard

### Responsive Design

- [ ] Open browser dev tools
- [ ] Toggle device toolbar (mobile view)
- [ ] Verify layout adapts properly
- [ ] Test all interactions in mobile view
- [ ] Switch to desktop view
- [ ] Verify full-width layout

### Error Handling

- [ ] Stop backend server
- [ ] Try to create a task
- [ ] Verify error message displays
- [ ] Start backend server
- [ ] Retry task creation
- [ ] Verify success

### Edge Cases

- [ ] Try to register with existing email
- [ ] Verify error message shows
- [ ] Try to login with wrong password
- [ ] Verify error message shows
- [ ] Try to create task with empty title
- [ ] Verify validation prevents submission

## Running Tests (Future)

```bash
# Unit tests (if implemented)
npm test

# Build for production
npm run build

# Run production build
npm start
```

## Troubleshooting

### API Connection Issues

1. Verify backend is running on port 8000
2. Check `NEXT_PUBLIC_API_URL` in `.env.local`
3. Check browser console for CORS errors
4. Verify backend has CORS configured for localhost:3000

### Authentication Issues

1. Check localStorage for `auth_token` key
2. Verify token format is valid JWT
3. Check network tab for 401 responses
4. Clear localStorage and re-authenticate

### Build Issues

1. Run `npm install` to ensure dependencies
2. Check for TypeScript errors: `npm run lint`
3. Clear `.next` folder and rebuild

## Component Reference

| Component | Location | Purpose |
|-----------|----------|---------|
| RegisterForm | `src/components/auth/RegisterForm.tsx` | User registration |
| LoginForm | `src/components/auth/LoginForm.tsx` | User sign-in |
| TaskList | `src/components/tasks/TaskList.tsx` | Display task list |
| TaskItem | `src/components/tasks/TaskItem.tsx` | Individual task row |
| CreateTaskForm | `src/components/tasks/CreateTaskForm.tsx` | New task input |
| EditTaskModal | `src/components/tasks/EditTaskModal.tsx` | Task editing dialog |
| Button | `src/components/ui/Button.tsx` | Reusable button |
| Input | `src/components/ui/Input.tsx` | Form input field |
| ErrorMessage | `src/components/ui/ErrorMessage.tsx` | Error display |

## API Client Reference

| Function | Location | Purpose |
|----------|----------|---------|
| `login()` | `src/lib/auth.ts` | Authenticate user |
| `register()` | `src/lib/auth.ts` | Create new user |
| `logout()` | `src/lib/auth.ts` | End user session |
| `getTasks()` | `src/lib/api.ts` | Fetch user tasks |
| `createTask()` | `src/lib/api.ts` | Create new task |
| `updateTask()` | `src/lib/api.ts` | Update task title |
| `deleteTask()` | `src/lib/api.ts` | Remove task |
| `toggleTask()` | `src/lib/api.ts` | Toggle completion |
