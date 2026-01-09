from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
import re
from pydantic import validator, EmailStr

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, nullable=False, max_length=255)

class User(UserBase, table=True):
    """
    User model representing a registered user in the system.
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"

    # Relationship to Todo
    todos: list["Todo"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "select"})

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str

    @validator('password')
    def validate_password(cls, v):
        """
        Validate password strength requirements:
        - At least 8 characters
        - Contains uppercase letter
        - Contains lowercase letter
        - Contains digit
        - Contains special character
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')

        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')

        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')

        return v

class UserRead(UserBase):
    """
    Schema for returning user data without sensitive information.
    """
    id: uuid.UUID
    created_at: datetime

class JWTTokenBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    jti: str = Field(unique=True, nullable=False, max_length=255)
    issued_at: datetime = Field(default=datetime.utcnow())
    expires_at: datetime
    is_active: bool = Field(default=True)

class JWTToken(JWTTokenBase, table=True):
    """
    JWT Token model for tracking active tokens and enabling token revocation.
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)

    def __repr__(self):
        return f"<JWTToken(id={self.id}, user_id={self.user_id}, jti={self.jti})>"

class JWTTokenCreate(JWTTokenBase):
    """
    Schema for creating a new JWT token record.
    """
    pass

class JWTTokenRead(JWTTokenBase):
    """
    Schema for returning JWT token information.
    """
    id: uuid.UUID