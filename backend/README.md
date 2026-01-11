# Todo API Backend

A FastAPI-based REST API backend for the Todo application with JWT authentication and PostgreSQL storage.

## Prerequisites

- Python 3.11+
- PostgreSQL database (Neon serverless recommended)

## Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your settings:
   - `DATABASE_URL`: PostgreSQL connection string
   - `JWT_SECRET`: Secret key for JWT tokens (min 32 characters)
   - `JWT_ALGORITHM`: Algorithm for JWT (default: HS256)
   - `JWT_EXPIRATION_HOURS`: Token expiration time (default: 24)
   - `CORS_ORIGINS`: Comma-separated list of allowed origins

## Running the Server

**Development**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout (client-side token removal)
- `GET /auth/me` - Get current user info

### Tasks
- `GET /tasks` - List all tasks for current user
- `POST /tasks` - Create a new task
- `PUT /tasks/{task_id}` - Update a task's title
- `DELETE /tasks/{task_id}` - Delete a task
- `PATCH /tasks/{task_id}/toggle` - Toggle task completion

### Health
- `GET /health` - Health check endpoint

## API Documentation

When running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── api/           # API routes
│   │   ├── auth.py    # Authentication endpoints
│   │   ├── tasks.py   # Task management endpoints
│   │   └── deps.py    # Dependency injection
│   ├── models/        # SQLModel database models
│   │   ├── user.py    # User model
│   │   └── task.py    # Task model
│   ├── schemas/       # Pydantic request/response schemas
│   │   ├── user.py    # User schemas
│   │   └── task.py    # Task schemas
│   ├── services/      # Business logic
│   │   ├── auth.py    # Auth service (JWT, password hashing)
│   │   └── task.py    # Task service (CRUD operations)
│   ├── config.py      # Environment configuration
│   ├── database.py    # Database connection
│   └── main.py        # FastAPI application entry point
├── requirements.txt   # Python dependencies
└── .env.example       # Environment variables template
```

## Security Features

- Bcrypt password hashing
- JWT token authentication
- User-based data isolation (users can only access their own tasks)
- CORS protection
- Input validation with Pydantic
