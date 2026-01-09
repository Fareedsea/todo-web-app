from fastapi import Request, HTTPException, status
from sqlmodel import Session, select
from typing import TypeVar, Type
from ..auth.models import User

T = TypeVar('T')

def ensure_user_owns_resource(
    db_session: Session,
    resource_model: Type[T],
    resource_id: str,
    user_id: str,
    user_id_field: str = "user_id"
) -> T:
    """
    Ensure that the authenticated user owns the specified resource.

    Args:
        db_session: Database session
        resource_model: The model class of the resource
        resource_id: ID of the resource to check
        user_id: ID of the authenticated user
        user_id_field: Name of the field that stores the user ID in the resource model

    Returns:
        The resource if the user owns it

    Raises:
        HTTPException: If the user doesn't own the resource or if the resource doesn't exist
    """
    # Construct a query to get the resource that belongs to the user
    statement = select(resource_model).where(
        getattr(resource_model, 'id') == resource_id,
        getattr(resource_model, user_id_field) == user_id
    )

    result = db_session.exec(statement)
    resource = result.first()

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found or you don't have permission to access it"
        )

    return resource

def apply_user_filter(
    model: Type[T],
    user_id: str,
    user_id_field: str = "user_id"
):
    """
    Create a select statement that automatically filters by user.

    Args:
        model: The model class to query
        user_id: ID of the authenticated user
        user_id_field: Name of the field that stores the user ID in the model

    Returns:
        A select statement with the user filter applied
    """
    return select(model).where(getattr(model, user_id_field) == user_id)

def verify_user_access(
    request: Request,
    resource_user_id: str
) -> bool:
    """
    Verify that the authenticated user has access to a resource based on user ID.

    Args:
        request: FastAPI request object containing user information
        resource_user_id: User ID associated with the resource

    Returns:
        True if the user has access, raises HTTPException otherwise
    """
    if not hasattr(request.state, 'user_id') or not request.state.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if str(request.state.user_id) != str(resource_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You don't have permission to access this resource"
        )

    return True