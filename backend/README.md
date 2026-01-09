# Todo Application Backend

This is the backend service for the Todo application, built with FastAPI and SQLModel.

## Features

- **User Authentication**: JWT-based authentication with secure token handling
- **Todo Management**: Full CRUD operations for todo items
- **User Isolation**: Each user can only access their own todos
- **RESTful API**: Standard HTTP methods and status codes
- **Database**: PostgreSQL with SQLModel ORM

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL (with Neon support)
- **Authentication**: JWT with secure token handling
- **Validation**: Pydantic models
- **Security**: CORS, security headers, input validation

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout and invalidate token
- `GET /auth/me` - Get current user info

### Todos

- `GET /api/v1/todos` - Get all todos for authenticated user
- `POST /api/v1/todos` - Create a new todo
- `GET /api/v1/todos/{id}` - Get a specific todo
- `PUT /api/v1/todos/{id}` - Update a specific todo
- `PATCH /api/v1/todos/{id}` - Partially update a specific todo
- `DELETE /api/v1/todos/{id}` - Delete a specific todo

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Run the application:
   ```bash
   python -m src.main
   ```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT signing
- `JWT_ALGORITHM`: Algorithm for JWT (default: HS256)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

## Running Tests

```bash
pytest tests/
```

## API Documentation

Interactive API documentation is available at:
- `/docs` - Swagger UI
- `/redoc` - ReDoc

## Security

- All endpoints (except auth) require a valid JWT token
- User data is isolated - users can only access their own todos
- Input validation is performed on all requests
- SQL injection is prevented through ORM usage
- Rate limiting can be implemented as needed