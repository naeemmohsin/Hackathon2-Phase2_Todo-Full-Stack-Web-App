# Data Model: Todo Full-Stack Web Application

**Feature Branch**: `001-todo-fullstack-app`
**Date**: 2026-01-11
**Status**: Complete

## Overview

This document defines the data entities for the Todo application. The model is designed for multi-user task management with strict data isolation.

## Entity Relationship Diagram

```
┌─────────────────────────────────────┐
│              User                   │
├─────────────────────────────────────┤
│ id: UUID (PK)                       │
│ email: String (unique, not null)    │
│ password_hash: String (not null)    │
│ created_at: DateTime (not null)     │
│ updated_at: DateTime (not null)     │
└─────────────────────────────────────┘
                 │
                 │ 1:N (one user has many tasks)
                 ▼
┌─────────────────────────────────────┐
│              Task                   │
├─────────────────────────────────────┤
│ id: UUID (PK)                       │
│ title: String (not null)            │
│ is_completed: Boolean (default: F)  │
│ owner_id: UUID (FK → User.id)       │
│ created_at: DateTime (not null)     │
│ updated_at: DateTime (not null)     │
└─────────────────────────────────────┘
```

## Entities

### User

Represents a registered account in the system.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key | Unique identifier |
| email | String(255) | Unique, Not Null, Index | User's email address (login identifier) |
| password_hash | String(255) | Not Null | bcrypt hash of password |
| created_at | DateTime | Not Null, Default: NOW | Account creation timestamp |
| updated_at | DateTime | Not Null, Default: NOW | Last modification timestamp |

**Validation Rules**:
- Email must be valid format (contains @ and domain)
- Email must be unique across all users
- Password must be at least 8 characters before hashing

**SQLModel Definition**:
```python
class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: list["Task"] = Relationship(back_populates="owner")
```

### Task

Represents a todo item owned by a specific user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key | Unique identifier |
| title | String(500) | Not Null | Task description |
| is_completed | Boolean | Not Null, Default: False | Completion status |
| owner_id | UUID | Foreign Key (User.id), Not Null, Index | Task owner reference |
| created_at | DateTime | Not Null, Default: NOW | Task creation timestamp |
| updated_at | DateTime | Not Null, Default: NOW | Last modification timestamp |

**Validation Rules**:
- Title must not be empty or whitespace-only
- Title maximum length: 500 characters
- owner_id must reference a valid User

**SQLModel Definition**:
```python
class Task(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=500)
    is_completed: bool = Field(default=False)
    owner_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    owner: User = Relationship(back_populates="tasks")
```

## Indexes

| Table | Index Name | Columns | Purpose |
|-------|------------|---------|---------|
| user | ix_user_email | email | Fast lookup by email (login) |
| task | ix_task_owner_id | owner_id | Fast filtering by owner |

## Database Schema (SQL)

```sql
-- Users table
CREATE TABLE "user" (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_user_email ON "user" (email);

-- Tasks table
CREATE TABLE task (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    owner_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_task_owner_id ON task (owner_id);
```

## State Transitions

### Task Completion Status

```
┌───────────────┐         toggle          ┌───────────────┐
│               │ ──────────────────────→ │               │
│  Incomplete   │                         │   Completed   │
│ is_completed  │ ←────────────────────── │ is_completed  │
│   = false     │         toggle          │   = true      │
└───────────────┘                         └───────────────┘
```

### User Lifecycle

```
New User → Registration → Active User → (Logout/Login cycles) → Active User
```

## Data Isolation Rules

1. **Task Creation**: `owner_id` is automatically set to authenticated user's ID
2. **Task Listing**: Query includes `WHERE owner_id = :current_user_id`
3. **Task Update**: Verify `owner_id = :current_user_id` before update
4. **Task Delete**: Verify `owner_id = :current_user_id` before delete
5. **Task Toggle**: Verify `owner_id = :current_user_id` before toggle

## Cascade Behavior

| Parent | Child | On Delete |
|--------|-------|-----------|
| User | Task | CASCADE (delete all user's tasks) |

## Timestamps

All entities use UTC timestamps:
- `created_at`: Set once at creation, never modified
- `updated_at`: Updated on every modification

## Migration Strategy

1. Create `user` table first (no dependencies)
2. Create `task` table with foreign key to `user`
3. Create indexes after table creation

SQLModel handles migrations via Alembic or table creation:
```python
SQLModel.metadata.create_all(engine)
```
