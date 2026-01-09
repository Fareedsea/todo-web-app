from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlmodel import Session
from typing import Optional
from ..auth.models import User
from ..auth.service import get_user_by_id
from ..core.database import get_session
from ..core.config import settings
from uuid import UUID

oauth2_scheme = HTTPBearer()

async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session)
) -> User:
    """
    Get the current authenticated user from the JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = UUID(user_id_str)
    except JWTError:
        raise credentials_exception
    except ValueError:
        raise credentials_exception

    user = await get_user_by_id(user_id, db)
    if user is None:
        raise credentials_exception

    return user