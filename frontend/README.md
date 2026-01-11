# Todo App Frontend

A Next.js 16+ frontend application for the Todo application with App Router and Tailwind CSS.

## Prerequisites

- Node.js 18+
- npm or yarn

## Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env.local
   ```

   Edit `.env.local` with your settings:
   - `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)
   - `BETTER_AUTH_SECRET`: Secret for auth operations

## Running the Application

**Development**:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`.

**Production Build**:
```bash
npm run build
npm start
```

## Features

- User registration and login
- JWT-based authentication
- Create, read, update, delete tasks
- Toggle task completion status
- Responsive design (320px - 1920px)
- Loading states and error handling

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── dashboard/          # Protected dashboard page
│   │   ├── login/              # Login page
│   │   ├── register/           # Registration page
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   └── globals.css         # Global styles
│   ├── components/             # React components
│   │   ├── auth/               # Authentication components
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── tasks/              # Task management components
│   │   │   ├── CreateTaskForm.tsx
│   │   │   ├── EditTaskModal.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   └── TaskList.tsx
│   │   └── ui/                 # Shared UI components
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       └── ErrorMessage.tsx
│   ├── lib/                    # Utilities and API
│   │   ├── api.ts              # API client with JWT handling
│   │   ├── auth.ts             # Auth helper functions
│   │   └── types.ts            # TypeScript interfaces
│   └── middleware.ts           # Route protection middleware
├── public/                     # Static assets
├── package.json
├── tailwind.config.ts          # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
└── .env.example                # Environment variables template
```

## Pages

| Route | Description | Protection |
|-------|-------------|------------|
| `/` | Home page - redirects to dashboard or login | Public |
| `/login` | User login page | Public |
| `/register` | User registration page | Public |
| `/dashboard` | Main task management page | Protected |

## Components

### UI Components
- **Button**: Primary, secondary, and danger variants with loading state
- **Input**: Form input with label and error state support
- **ErrorMessage**: Error display component

### Auth Components
- **LoginForm**: Email/password login form
- **RegisterForm**: User registration form

### Task Components
- **CreateTaskForm**: Form to create new tasks
- **TaskList**: Displays list of tasks with empty state
- **TaskItem**: Individual task with toggle, edit, and delete actions
- **EditTaskModal**: Modal for editing task titles

## Tech Stack

- **Framework**: Next.js 16+ with App Router
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **State Management**: React useState/useEffect
- **HTTP Client**: Native fetch API
