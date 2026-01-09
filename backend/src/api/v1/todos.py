from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from ..auth_deps import get_current_user_from_token as get_current_user
from ..deps import get_db_session
from fastapi import Depends
from ...auth.models import User
from ...models.todo import Todo, TodoCreate, TodoUpdate, TodoPublic
from ...services.todo import TodoService
from ...auth.models import User
from sqlmodel import Session

router = APIRouter()

@router.post("/", response_model=TodoPublic, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_create: TodoCreate,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
) -> TodoPublic:
    """
    Create a new todo item for the authenticated user.
    """
    try:
        todo_service = TodoService(db_session)
        todo = todo_service.create_todo(todo_create, current_user.id)
        return todo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating todo: {str(e)}"
        )

@router.get("/", response_model=List[TodoPublic])
def get_todos(
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100
) -> List[TodoPublic]:
    """
    Get all todos for the authenticated user.
    """
    try:
        todo_service = TodoService(db_session)
        todos = todo_service.get_todos_by_user(current_user.id, skip=skip, limit=limit)
        return todos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving todos: {str(e)}"
        )

@router.get("/{todo_id}", response_model=TodoPublic)
def get_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
) -> TodoPublic:
    """
    Get a specific todo by ID for the authenticated user.
    """
    try:
        todo_service = TodoService(db_session)
        todo = todo_service.get_todo_by_id_and_user(todo_id, current_user.id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or does not belong to you"
            )
        return todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving todo: {str(e)}"
        )

@router.put("/{todo_id}", response_model=TodoPublic)
def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
) -> TodoPublic:
    """
    Update a specific todo for the authenticated user.
    """
    try:
        todo_service = TodoService(db_session)
        todo = todo_service.update_todo(todo_id, current_user.id, todo_update)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or does not belong to you"
            )
        return todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating todo: {str(e)}"
        )

@router.patch("/{todo_id}", response_model=TodoPublic)
def partial_update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
) -> TodoPublic:
    """
    Partially update a specific todo for the authenticated user.
    """
    try:
        todo_service = TodoService(db_session)
        todo = todo_service.update_todo(todo_id, current_user.id, todo_update)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or does not belong to you"
            )
        return todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating todo: {str(e)}"
        )

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_db_session)
):
    """
    Delete a specific todo for the authenticated user.
    """
    try:
        todo_service = TodoService(db_session)
        success = todo_service.delete_todo(todo_id, current_user.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or does not belong to you"
            )
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting todo: {str(e)}"
        )