# Quickstart: Backend API & Persistent Data Layer

## Prerequisites

- Python 3.11+
- Poetry or pip for dependency management
- Neon PostgreSQL account and connection string
- Better Auth configured with JWT support
- Environment variables configured (see below)

## Environment Setup

Create a `.env` file in the backend directory with the following variables:

```bash
# Database
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"

# JWT Configuration
JWT_SECRET_KEY="your-super-secret-jwt-key-here"
JWT_ALGORITHM="HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Better Auth
BETTER_AUTH_SECRET="your-better-auth-secret"
```

## Project Structure

```
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── todo.py       # Todo SQLModel definition
│   │   └── user.py       # User model reference
│   ├── services/
│   │   ├── __init__.py
│   │   ├── database.py   # Database connection and session management
│   │   └── auth.py       # JWT validation utilities
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py       # Dependency injection for auth
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── todos.py  # Todo API routes
│   ├── main.py           # FastAPI app entry point
│   └── config.py         # Configuration settings
├── tests/
├── requirements.txt
└── pyproject.toml
```

## Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# OR if using Poetry
poetry install
```

3. Set up your database (Neon PostgreSQL):
   - Create a Neon project
   - Get your connection string
   - Update your `.env` file with the connection details

4. Run database migrations:
```bash
# This will be implemented as part of the setup
python -m src.services.database setup
```

## Running the Application

1. Start the development server:
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

2. The API will be available at: `http://localhost:8000`
3. API documentation will be available at: `http://localhost:8000/docs`

## API Usage

### Authentication
All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Example Requests

1. **Create a Todo**:
```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Build a todo app with FastAPI and SQLModel"
  }'
```

2. **Get User's Todos**:
```bash
curl -X GET http://localhost:8000/api/v1/todos \
  -H "Authorization: Bearer <your-jwt-token>"
```

3. **Update a Todo**:
```bash
curl -X PUT http://localhost:8000/api/v1/todos/<todo-id> \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "is_completed": true
  }'
```

4. **Delete a Todo**:
```bash
curl -X DELETE http://localhost:8000/api/v1/todos/<todo-id> \
  -H "Authorization: Bearer <your-jwt-token>"
```

## Key Components

### Database Service (`src/services/database.py`)
- Handles connection to Neon PostgreSQL
- Provides async session management
- Implements connection pooling
- Includes setup and health check functions

### Auth Service (`src/services/auth.py`)
- JWT token verification
- User ID extraction from tokens
- Token expiration checking
- Integration with Better Auth

### API Dependencies (`src/api/deps.py`)
- Dependency injection for authentication
- Current user retrieval
- Database session management

### Todo API (`src/api/v1/todos.py`)
- Implements all CRUD operations
- Enforces user isolation
- Handles validation and error responses
- Follows RESTful design principles

## Testing

Run the tests using pytest:
```bash
cd backend
pytest tests/ -v
```

For integration tests that require the database:
```bash
cd backend
pytest tests/integration/ -v
```

## Deployment

1. Ensure environment variables are set in your deployment environment
2. Run database migrations before starting the application
3. Use a production ASGI server like Gunicorn for production:
```bash
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
```