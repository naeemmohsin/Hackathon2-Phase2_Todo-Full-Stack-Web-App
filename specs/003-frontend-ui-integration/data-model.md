# Data Model: Frontend Application (UI, UX & Integration)

**Feature**: 003-frontend-ui-integration
**Date**: 2026-01-12

## Overview

This document describes the frontend data model - the TypeScript types and interfaces used to represent data in the UI layer. No database schema changes are required for this feature.

## Existing Types (from `frontend/src/lib/types.ts`)

### User

Represents an authenticated user in the system.

```typescript
interface User {
  id: string;        // UUID from backend
  email: string;     // User's email address
  created_at: string; // ISO timestamp
}
```

**Used in**: Auth forms, dashboard header, session state

### Task

Represents a todo item owned by a user.

```typescript
interface Task {
  id: string;           // UUID from backend
  title: string;        // Task description (max 500 chars)
  is_completed: boolean; // Completion status
  created_at: string;   // ISO timestamp
  updated_at: string;   // ISO timestamp
}
```

**Used in**: TaskList, TaskItem, CreateTaskForm, EditTaskModal

### AuthResponse

Response from login/register endpoints.

```typescript
interface AuthResponse {
  user: User;    // The authenticated user
  token: string; // JWT access token
}
```

**Used in**: login(), register() functions

### Request Types

```typescript
interface LoginRequest {
  email: string;
  password: string;
}

interface RegisterRequest {
  email: string;
  password: string;
}

interface CreateTaskRequest {
  title: string;
}

interface UpdateTaskRequest {
  title: string;
}
```

### Error Types

```typescript
interface ApiError {
  detail: string; // Error message from backend
}

interface SuccessResponse {
  success: boolean;
  message?: string;
}
```

## UI State Types (from `frontend/src/lib/auth-client.ts`)

### AuthState

Client-side authentication state managed by Better Auth integration.

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

**State Transitions**:
- Initial: `{ user: null, token: null, isAuthenticated: false, isLoading: true }`
- Authenticated: `{ user: {...}, token: "...", isAuthenticated: true, isLoading: false }`
- Logged out: `{ user: null, token: null, isAuthenticated: false, isLoading: false }`

## Component State Patterns

### Form State Pattern

Used consistently across LoginForm, RegisterForm, CreateTaskForm, EditTaskModal:

```typescript
// Common form state
const [value, setValue] = useState('');
const [error, setError] = useState('');
const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
const [isLoading, setIsLoading] = useState(false);
```

### Task List State Pattern

Used in dashboard page:

```typescript
const [tasks, setTasks] = useState<Task[]>([]);
const [isLoadingTasks, setIsLoadingTasks] = useState(true);
const [editingTask, setEditingTask] = useState<Task | null>(null);
const [isEditModalOpen, setIsEditModalOpen] = useState(false);
```

## Data Flow

### Authentication Flow

```
User Input → Form Validation → API Call → Token Storage → Redirect
     ↓              ↓              ↓            ↓           ↓
  useState    fieldErrors    apiFetch()   localStorage  router.push()
```

### Task CRUD Flow

```
User Action → Optimistic Update → API Call → Confirm/Revert
     ↓              ↓               ↓            ↓
  onClick    setTasks(...)    apiFetch()   Update state
```

## Storage

### localStorage Keys

| Key | Value | Purpose |
|-----|-------|---------|
| `auth_token` | JWT string | Authentication token for API requests |

### No Session Storage

The application uses localStorage only. No sessionStorage is used per spec requirement for stateless backend.

## Validation Rules

### Email Validation

```typescript
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
```

### Password Validation

```typescript
const minLength = 8;
```

### Task Title Validation

- Required (non-empty after trim)
- Max 500 characters (enforced by backend)

## Type Safety Notes

1. All API responses are typed with TypeScript interfaces
2. Component props are explicitly typed
3. State variables have type annotations
4. No `any` types in production code

## Migration Notes

No data migration required - this feature uses existing types from Spec 1.
