from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
from sqlmodel import Session
from ..auth.models import User, UserCreate, UserRead
from ..auth.service import create_user, get_user_by_email
from ..core.security import authenticate_user, create_access_token, get_password_hash
from ..core.config import settings
from ..core.database import get_session
from ..core.logging import log_auth_event

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/signup", response_model=UserRead)
async def signup(request: Request, user_data: UserCreate, db: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = await get_user_by_email(user_data.email, db)
    if existing_user:
        log_auth_event(
            event_type="registration_failure_duplicate",
            user_id=str(existing_user.id) if existing_user else None,
            ip_address=request.client.host if request.client else None,
            details={"email": user_data.email}
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create the user
    user = User(
        email=user_data.email,
        password_hash=hashed_password
    )

    created_user = await create_user(user, db)

    log_auth_event(
        event_type="registration_success",
        user_id=str(created_user.id),
        ip_address=request.client.host if request.client else None,
        details={"email": user_data.email}
    )

    return created_user

@router.post("/signin", response_model=Token)
async def signin(request: Request, user_credentials: UserLogin, db: Session = Depends(get_session)):
    # Get user by email
    user = await get_user_by_email(user_credentials.email, db)

    if not user or not authenticate_user(user, user_credentials.password):
        log_auth_event(
            event_type="login_failure",
            user_id=str(user.id) if user else None,
            ip_address=request.client.host if request.client else None,
            details={"email": user_credentials.email}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.jwt_expiration_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    log_auth_event(
        event_type="login_success",
        user_id=str(user.id),
        ip_address=request.client.host if request.client else None,
        details={"email": user_credentials.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}


from .auth_deps import get_current_user_from_token

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user_from_token)):
    return current_user