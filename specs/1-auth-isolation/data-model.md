# Data Model: Authentication & User Isolation

**Date**: 2026-01-09
**Feature**: Authentication & User Isolation
**Phase**: 1 Design

## Entities

### User

**Purpose**: Represents a registered user in the system with authentication credentials and identity information.

**Fields**:
- `id: UUID` - Unique user identifier (primary key)
- `email: str` - User's email address (unique, indexed)
- `password_hash: str` - Hashed password (never stored in plain text)
- `created_at: datetime` - Account creation timestamp
- `updated_at: datetime` - Last update timestamp

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Password must meet minimum strength requirements (8+ characters, mixed case, special characters)
- Password hash must be generated using secure hashing algorithm (bcrypt)

**Relationships**:
- One-to-many with Todo items (user owns multiple todos)
- One-to-many with JWT tokens (user can have multiple active sessions)

**State Transitions**:
- Created → Active (upon successful registration)
- Active → Deleted (upon account deletion - soft delete preferred)

### JWT Token

**Purpose**: Represents a temporary authentication token containing user identity and session information.

**Fields**:
- `user_id: UUID` - Reference to authenticated user
- `jti: str` - JWT ID for token tracking/revocation
- `issued_at: datetime` - Token creation time
- `expires_at: datetime` - Token expiration time
- `is_active: bool` - Token status (active/expired/revoked)

**Validation Rules**:
- User_id must reference valid user
- Expiration time must be in future
- JTI must be unique per user session
- Token must contain required claims (sub, iat, exp, jti)

**Relationships**:
- Many-to-one with User (multiple tokens per user)
- One-to-one with session context

**State Transitions**:
- Created → Active (upon successful authentication)
- Active → Expired (when expires_at time passes)
- Active → Revoked (upon logout or admin action)

### Authenticated Session Context

**Purpose**: Conceptual entity representing the current authenticated user context within a request.

**Fields**:
- `user_id: UUID` - Current user identifier
- `user_email: str` - Current user email
- `session_id: str` - Current session identifier
- `permissions: list` - User permissions/roles (future extensibility)

**Validation Rules**:
- User_id must be valid and active
- Session context must be established before accessing protected resources
- Context must be refreshed for each request

**Relationships**:
- One-to-one with current JWT token
- Many-to-one with User

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

### JWT Tokens Table

```sql
CREATE TABLE jwt_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    jti VARCHAR(255) UNIQUE NOT NULL,
    issued_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_jwt_tokens_user_id ON jwt_tokens(user_id);
CREATE INDEX idx_jwt_tokens_jti ON jwt_tokens(jti);
CREATE INDEX idx_jwt_tokens_expires_at ON jwt_tokens(expires_at);
CREATE INDEX idx_jwt_tokens_is_active ON jwt_tokens(is_active);
```

## Data Access Patterns

### User Queries
- **Registration**: Insert new user with hashed password
- **Authentication**: Find user by email for credential verification
- **Profile**: Retrieve user information by ID
- **Existence Check**: Verify email uniqueness during registration

### JWT Token Queries
- **Token Creation**: Insert new token record upon successful login
- **Token Validation**: Find active token by JTI and verify expiration
- **Token Revocation**: Update token status to inactive upon logout
- **Cleanup**: Delete expired tokens periodically

### User Isolation Queries
- **Todo Access**: All todo queries must include `WHERE user_id = :current_user_id`
- **Data Modification**: All updates/deletes must verify user ownership
- **Bulk Operations**: Must filter by authenticated user ID

## Security Constraints

### Data Protection
- Passwords must never be stored in plain text
- JWT secrets must not be logged or exposed
- User IDs must be validated before any data access
- All sensitive data must be encrypted in transit (HTTPS)

### Access Control
- All read operations must filter by authenticated user ID
- All write operations must validate user ownership
- No cross-user data access allowed under any circumstances
- Administrative operations must have additional authorization checks

### Audit Requirements
- Login/logout events must be logged
- Failed authentication attempts must be tracked
- Data access patterns must be monitorable
- Token usage must be traceable for security analysis