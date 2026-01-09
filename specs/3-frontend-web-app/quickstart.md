# Quickstart: Frontend Web Application

## Prerequisites

- Node.js 18+ with npm or yarn
- Access to the backend API (running on localhost:8000 or deployed endpoint)
- Git for version control
- Environment variables configured (see below)

## Environment Setup

Create a `.env.local` file in the frontend directory with the following variables:

```bash
# Backend API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_JWT_SECRET_KEY=your-jwt-secret-key-here

# Additional configuration
NEXT_PUBLIC_APP_NAME="Todo Application"
NEXT_PUBLIC_SENTRY_DSN=""  # Optional: for error tracking
```

## Project Structure

```
frontend/
├── public/
│   ├── favicon.ico
│   ├── robots.txt
│   └── sitemap.xml
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── layout.tsx          # Root layout with global styles
│   │   ├── page.tsx            # Home/Landing page
│   │   ├── auth/
│   │   │   ├── page.tsx        # Login page
│   │   │   ├── signup/page.tsx # Signup page
│   │   │   └── components/
│   │   │       ├── LoginForm.tsx
│   │       └── SignupForm.tsx
│   │   ├── dashboard/
│   │   │   ├── page.tsx        # Todo dashboard
│   │   │   └── components/
│   │   │       ├── TodoList.tsx
│   │   │       ├── TodoItem.tsx
│   │   │       └── TodoForm.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/                 # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Card.tsx
│   │   │   └── ...
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Sidebar.tsx
│   │   └── auth/
│   │       ├── ProtectedRoute.tsx
│   │       └── AuthProvider.tsx
│   ├── lib/
│   │   ├── auth.ts             # Authentication utilities
│   │   ├── api.ts              # API client with JWT handling
│   │   ├── types.ts            # Type definitions
│   │   └── utils.ts            # Helper functions
│   ├── hooks/
│   │   ├── useAuth.ts          # Authentication hook
│   │   └── useTodos.ts         # Todo management hook
│   └── styles/
│       └── globals.css
├── tests/
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── next.config.js
```

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# OR if using yarn
yarn install
```

3. Set up your environment variables (see above)

## Running the Application

1. Start the development server:
```bash
npm run dev
# OR if using yarn
yarn dev
```

2. The application will be available at: `http://localhost:3000`
3. The API will be accessible at: `http://localhost:3000/api/*`

## Key Components

### Authentication Provider (`src/components/auth/AuthProvider.tsx`)
- Manages authentication state globally
- Handles JWT token storage and retrieval
- Provides authentication context to child components
- Handles token expiration and automatic logout

### API Client (`src/lib/api.ts`)
- Centralized API client with automatic JWT token attachment
- Handles common error scenarios (401, network errors)
- Provides loading and error state management
- Implements retry logic for failed requests

### Authentication Hook (`src/hooks/useAuth.ts`)
- Provides authentication state and functions to components
- Handles login, signup, and logout operations
- Manages user session state
- Redirects after authentication operations

### Todo Hook (`src/hooks/useTodos.ts`)
- Manages todo state and operations
- Handles CRUD operations with the backend
- Provides loading and error states for each operation
- Updates UI immediately with optimistic updates

### Protected Route Component (`src/components/auth/ProtectedRoute.tsx`)
- Ensures only authenticated users can access certain pages
- Redirects unauthenticated users to login
- Handles loading states during authentication checks

## UI Components

### Layout Components
- **Header**: Navigation and user profile menu
- **Footer**: Site-wide information and links
- **Sidebar**: Secondary navigation for dashboard views

### Authentication Components
- **LoginForm**: Handles user login with validation
- **SignupForm**: Handles user registration with validation
- **ProtectedRoute**: Wrapper for authenticated routes

### Todo Components
- **TodoList**: Displays user's todo items
- **TodoItem**: Individual todo display with action buttons
- **TodoForm**: Form for creating and editing todos

## API Usage

### Authentication
The frontend automatically handles authentication by:

1. Storing JWT tokens securely in browser storage
2. Attaching tokens to all authenticated API requests
3. Redirecting users after authentication events
4. Handling token expiration gracefully

### Todo Operations
All todo operations are performed through the `useTodos` hook:

```typescript
const { todos, isLoading, error, createTodo, updateTodo, deleteTodo } = useTodos();

// Create a new todo
await createTodo({ title: "New task", description: "Task description" });

// Update an existing todo
await updateTodo(todoId, { title: "Updated title", isCompleted: true });

// Delete a todo
await deleteTodo(todoId);
```

## Testing

Run the tests using:
```bash
# Unit tests
npm run test:unit

# Integration tests
npm run test:integration

# End-to-end tests
npm run test:e2e

# All tests
npm run test
```

For development, you can run tests in watch mode:
```bash
npm run test:watch
```

## Building for Production

1. Create a production build:
```bash
npm run build
# OR if using yarn
yarn build
```

2. The build output will be in the `out/` directory

3. Serve the application:
```bash
npm run start
# OR if using yarn
yarn start
```

## Deployment

### Environment Variables for Production
```bash
NEXT_PUBLIC_API_BASE_URL=https://your-backend-domain.com/api/v1
```

### Deployment Platforms
The application is ready for deployment on platforms like:
- Vercel (recommended for Next.js)
- Netlify
- AWS Amplify
- Azure Static Web Apps
- Any Node.js hosting platform