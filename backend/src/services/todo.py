from typing import List, Optional
from sqlmodel import select, Session, func
from uuid import UUID
import logging
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..auth.models import User

logger = logging.getLogger(__name__)

class TodoService:
    def __init__(self, session: Session):
        self.session = session

    def create_todo(self, todo_data: TodoCreate, user_id: UUID) -> Todo:
        """Create a new todo for the specified user."""
        logger.info(f"Creating todo for user_id: {user_id}")
        todo = Todo(
            **todo_data.model_dump(),
            user_id=user_id
        )
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        logger.info(f"Created todo with id: {todo.id} for user_id: {user_id}")
        return todo

    def get_todos_by_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Todo]:
        """Get all todos for a specific user."""
        logger.info(f"Getting todos for user_id: {user_id}, skip: {skip}, limit: {limit}")
        statement = (
            select(Todo)
            .where(Todo.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        todos = self.session.exec(statement).all()
        logger.info(f"Retrieved {len(todos)} todos for user_id: {user_id}")
        return todos

    def get_todo_by_id_and_user(self, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        """Get a specific todo by ID for a specific user."""
        logger.debug(f"Getting todo by id: {todo_id} for user_id: {user_id}")
        statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        todo = self.session.exec(statement).first()
        if todo:
            logger.debug(f"Found todo with id: {todo.id} for user_id: {user_id}")
        else:
            logger.debug(f"No todo found with id: {todo_id} for user_id: {user_id}")
        return todo

    def update_todo(self, todo_id: UUID, user_id: UUID, todo_data: TodoUpdate) -> Optional[Todo]:
        """Update a specific todo for a specific user."""
        logger.info(f"Updating todo with id: {todo_id} for user_id: {user_id}")
        todo = self.get_todo_by_id_and_user(todo_id, user_id)
        if not todo:
            logger.warning(f"Attempt to update non-existent todo with id: {todo_id} for user_id: {user_id}")
            return None

        update_data = todo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)

        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        logger.info(f"Updated todo with id: {todo.id} for user_id: {user_id}")
        return todo

    def delete_todo(self, todo_id: UUID, user_id: UUID) -> bool:
        """Delete a specific todo for a specific user."""
        logger.info(f"Deleting todo with id: {todo_id} for user_id: {user_id}")
        todo = self.get_todo_by_id_and_user(todo_id, user_id)
        if not todo:
            logger.warning(f"Attempt to delete non-existent todo with id: {todo_id} for user_id: {user_id}")
            return False

        self.session.delete(todo)
        self.session.commit()
        logger.info(f"Deleted todo with id: {todo.id} for user_id: {user_id}")
        return True

    def get_todos_count_by_user(self, user_id: UUID) -> int:
        """Get the count of todos for a specific user."""
        logger.debug(f"Getting todos count for user_id: {user_id}")
        statement = select(func.count(Todo.id)).where(Todo.user_id == user_id)
        count = self.session.exec(statement).one()
        logger.debug(f"User {user_id} has {count} todos")
        return count