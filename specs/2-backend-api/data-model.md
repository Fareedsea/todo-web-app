# Data Model: Backend API & Persistent Data Layer

## Entity: Todo

### Fields
- `id`: UUID (Primary Key, auto-generated)
- `title`: String (Required, max length 255)
- `description`: Text (Optional)
- `is_completed`: Boolean (Default: False)
- `user_id`: UUID (Foreign Key, references User.id, Required)
- `created_at`: DateTime (Auto-generated, timezone-aware)
- `updated_at`: DateTime (Auto-generated, timezone-aware, updates on change)

### Relationships
- Belongs to one `User` (many-to-one)

### Validation Rules
- `title` must be 1-255 characters
- `user_id` must reference an existing user
- `is_completed` default value is `False`

### SQLModel Definition
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .user import User

class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)

class Todo(TodoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to User
    user: "User" = Relationship(back_populates="todos")

class TodoCreate(TodoBase):
    pass

class TodoUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    is_completed: Optional[bool] = Field(default=None)

class TodoPublic(TodoBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
```

## Entity: User (Reference)

### Fields
- `id`: UUID (Primary Key, auto-generated)
- `email`: String (Unique, Required)
- `name`: String (Optional)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated, updates on change)

### Relationships
- Has many `Todo` items (one-to-many)

### Note
The User model will be primarily managed by Better Auth, but we'll reference it for foreign key relationships in our Todo model.

## Database Constraints
- Primary key constraints on all ID fields
- Foreign key constraint on `user_id` in Todo table
- Unique constraint on user email (handled by Better Auth)
- Index on `user_id` in Todo table for efficient filtering
- Index on `created_at` for sorting queries

## State Transitions
- `is_completed` can transition from `False` to `True` (completed) or `True` to `False` (reopened)
- `updated_at` automatically updates on any record modification
- `created_at` is immutable after creation

## Access Patterns
- Query by `user_id` (primary access pattern for user isolation)
- Query by `id` with `user_id` verification (individual todo access)
- Sort by `created_at` (chronological listing)
- Filter by `is_completed` (completed/incomplete items)