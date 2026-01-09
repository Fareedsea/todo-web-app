from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..auth.models import User
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Index

class TodoPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)
    priority: TodoPriority = Field(default=TodoPriority.medium)
    due_date: Optional[datetime] = Field(default=None)

class Todo(TodoBase, table=True):
    __table_args__ = (
        Index("idx_todo_user_id", "user_id"),
        Index("idx_todo_created_at", "created_at"),
        Index("idx_todo_updated_at", "updated_at"),
        Index("idx_todo_is_completed", "is_completed"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to User
    user: Optional["User"] = Relationship(back_populates="todos", sa_relationship_kwargs={"lazy": "select"})

class TodoCreate(TodoBase):
    pass

class TodoUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: Optional[bool] = Field(default=None)
    priority: Optional[TodoPriority] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)

class TodoPublic(TodoBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime