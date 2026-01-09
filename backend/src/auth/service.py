from sqlmodel import Session, select
from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi import status
from ..core.security import get_password_hash
from ..core.database import get_session
from ..auth.models import User, UserCreate, JWTToken, JWTTokenCreate
from uuid import UUID

def create_user_sync(user: User, db_session: Session) -> User:
    """
    Create a new user in the database
    """
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

async def create_user(user: User, db_session: Session) -> User:
    """
    Create a new user in the database
    """
    return create_user_sync(user, db_session)

def get_user_by_email_sync(email: str, db_session: Session) -> Optional[User]:
    """
    Get a user by email
    """
    statement = select(User).where(User.email == email)
    result = db_session.exec(statement)
    return result.first()

async def get_user_by_email(email: str, db_session: Session) -> Optional[User]:
    """
    Get a user by email
    """
    return get_user_by_email_sync(email, db_session)

def get_user_by_id_sync(user_id: UUID, db_session: Session) -> Optional[User]:
    """
    Get a user by ID
    """
    statement = select(User).where(User.id == user_id)
    result = db_session.exec(statement)
    return result.first()

async def get_user_by_id(user_id: UUID, db_session: Session) -> Optional[User]:
    """
    Get a user by ID
    """
    return get_user_by_id_sync(user_id, db_session)

def create_jwt_token_sync(token_data: JWTTokenCreate, db_session: Session) -> JWTToken:
    """
    Create a new JWT token record in the database
    """
    token = JWTToken(
        user_id=token_data.user_id,
        jti=token_data.jti,
        issued_at=token_data.issued_at,
        expires_at=token_data.expires_at,
        is_active=token_data.is_active
    )
    db_session.add(token)
    db_session.commit()
    db_session.refresh(token)
    return token

async def create_jwt_token(token_data: JWTTokenCreate, db_session: Session) -> JWTToken:
    """
    Create a new JWT token record in the database
    """
    return create_jwt_token_sync(token_data, db_session)

def get_active_token_by_jti_sync(jti: str, db_session: Session) -> Optional[JWTToken]:
    """
    Get an active token by JTI
    """
    statement = select(JWTToken).where(
        JWTToken.jti == jti,
        JWTToken.is_active == True,
        JWTToken.expires_at > datetime.utcnow()
    )
    result = db_session.exec(statement)
    return result.first()

async def get_active_token_by_jti(jti: str, db_session: Session) -> Optional[JWTToken]:
    """
    Get an active token by JTI
    """
    return get_active_token_by_jti_sync(jti, db_session)

def deactivate_token_sync(jti: str, db_session: Session) -> bool:
    """
    Deactivate a token by JTI
    """
    statement = select(JWTToken).where(JWTToken.jti == jti)
    result = db_session.exec(statement)
    token = result.first()

    if token:
        token.is_active = False
        db_session.add(token)
        db_session.commit()
        return True

    return False

async def deactivate_token(jti: str, db_session: Session) -> bool:
    """
    Deactivate a token by JTI
    """
    return deactivate_token_sync(jti, db_session)


def get_current_user_sync(db_session: Session, user_id: UUID) -> Optional[User]:
    """
    Get the current user by ID
    """
    return get_user_by_id_sync(user_id, db_session)


async def get_current_user(db_session: Session, user_id: UUID) -> Optional[User]:
    """
    Get the current user by ID
    """
    return get_current_user_sync(db_session, user_id)


def get_current_user_dependency(user_id: UUID = None, db_session: Session = Depends(get_session)) -> Optional[User]:
    """
    Dependency function to get the current user by ID for FastAPI
    """
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not provided",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return get_user_by_id_sync(user_id, db_session)