from fastapi import Depends, HTTPException, status, Request
from typing import Optional
from ..auth.models import User
from ..auth.service import get_user_by_id
from sqlmodel import Session
from ..core.database import get_session

async def get_current_user(
    request: Request,
    db: Session = Depends(get_session)
) -> User:
    """
    Get the current authenticated user from the request state
    """
    if not hasattr(request.state, 'user_id') or not request.state.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = request.state.user_id
    user = await get_user_by_id(user_id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user