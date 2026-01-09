# Research: Backend API & Persistent Data Layer

## Decision: SQLModel for Data Modeling
**Rationale**: SQLModel is chosen as it combines the power of SQLAlchemy with the benefits of Pydantic, providing type hints, validation, and compatibility with FastAPI. It's specifically designed for FastAPI applications and supports async operations needed for Neon PostgreSQL.

**Alternatives considered**:
- Pure SQLAlchemy: More complex setup, less type safety
- Tortoise ORM: Good async support but less mature than SQLModel
- Peewee: Simpler but lacks async support and Pydantic integration

## Decision: Neon Serverless PostgreSQL
**Rationale**: Neon provides serverless PostgreSQL with auto-scaling, branching, and built-in connection pooling. It integrates well with modern applications and provides the persistent storage required by the spec. The serverless nature aligns with the stateless architecture requirement.

**Alternatives considered**:
- Traditional PostgreSQL: Requires manual scaling and connection management
- SQLite: Not suitable for production web applications with multiple users
- MongoDB: Doesn't align with relational data model requirements
- Supabase: Built on PostgreSQL but adds complexity layer

## Decision: JWT Authentication with Better Auth
**Rationale**: Better Auth provides a complete authentication solution with JWT support. It integrates well with FastAPI and provides the user isolation required by the constitution. The shared secret approach aligns with the security-first principle.

**Alternatives considered**:
- Custom JWT implementation: More control but more security considerations
- Auth0/Firebase: External dependencies, less control
- Session-based auth: Violates stateless requirement

## Decision: FastAPI Framework
**Rationale**: FastAPI provides automatic API documentation, type validation, async support, and excellent integration with Pydantic and SQLModel. It's perfect for building secure, RESTful APIs with minimal boilerplate.

**Alternatives considered**:
- Flask: More manual work for validation and documentation
- Django: Overkill for this API-only requirement
- Starlette: Lower-level, requires more manual implementation

## Decision: RESTful API Design
**Rationale**: RESTful design provides standard HTTP methods and status codes that are familiar to developers. It aligns with the "RESTful Todo endpoints" requirement in the spec and supports the stateless architecture.

**API Structure**:
- `POST /todos` - Create new todo
- `GET /todos` - List user's todos
- `GET /todos/{id}` - Get specific todo
- `PUT/PATCH /todos/{id}` - Update todo
- `DELETE /todos/{id}` - Delete todo

## Decision: User Isolation Strategy
**Rationale**: All database queries will be filtered by the authenticated user's ID extracted from the JWT token. This ensures that users can only access their own data, meeting the security-first requirement.

**Implementation approach**:
- Dependency injection to extract user ID from JWT
- Query filtering in all data access methods
- 404 responses for attempts to access other users' data (not 403 to avoid leaking information)

## Decision: Error Handling Strategy
**Rationale**: Consistent error responses with appropriate HTTP status codes ensure predictable API behavior. This meets the "Standardize error responses" requirement from the spec.

**Standard error format**:
```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE"
}
```

**Common status codes**:
- 401: Unauthorized (missing/invalid JWT)
- 404: Not Found (todo doesn't exist or belongs to another user)
- 422: Unprocessable Entity (validation errors)
- 500: Internal Server Error (unexpected errors)