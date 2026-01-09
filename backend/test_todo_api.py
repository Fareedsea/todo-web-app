"""
Basic tests for the Todo API functionality
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from src.main import app
from src.models.todo import Todo, TodoCreate, TodoUpdate
from src.auth.models import User
from uuid import uuid4

client = TestClient(app)

def test_todo_endpoints_exist():
    """Test that todo endpoints are accessible"""

    # Test that we get a 401 for protected endpoints without auth
    response = client.get("/api/v1/")
    assert response.status_code in [200, 404]  # May be a root endpoint or 404

    # Test that protected endpoints require authentication
    response = client.get("/api/v1/todos")
    assert response.status_code == 401  # Unauthorized without JWT

    response = client.post("/api/v1/todos", json={"title": "Test"})
    assert response.status_code == 401  # Unauthorized without JWT

def test_todo_model_structure():
    """Test that Todo model has required fields"""

    # Create a sample todo
    user_id = uuid4()
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "is_completed": False
    }

    todo = Todo(user_id=user_id, **todo_data)

    assert todo.title == "Test Todo"
    assert todo.description == "Test Description"
    assert todo.is_completed == False
    assert todo.user_id == user_id
    assert todo.id is not None  # Auto-generated

def test_todo_create_model():
    """Test TodoCreate model validation"""

    # Valid data
    valid_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "is_completed": False
    }

    todo_create = TodoCreate(**valid_data)
    assert todo_create.title == "Test Todo"

    # Test validation - title required
    with pytest.raises(ValueError):
        TodoCreate(title="")  # Empty title should fail validation

if __name__ == "__main__":
    pytest.main([__file__])