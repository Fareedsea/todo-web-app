from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from typing import Optional, Union
from fastapi import HTTPException, status
from sqlmodel import Session
from ..auth.models import User
from .config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create a secret key for JWT if not provided in settings
SECRET_KEY = settings.jwt_secret
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_expiration_minutes

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plaintext password
    """
    return pwd_context.hash(password)

def authenticate_user(user: User, password: str) -> bool:
    """
    Authenticate a user by verifying their password
    """
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return True

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with the provided data and expiration
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Cache for decoded tokens to improve performance
# In a production environment, you might want to use Redis or another cache
import functools
from typing import Dict, Any

TOKEN_CACHE: Dict[str, Dict[str, Any]] = {}

def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the payload if valid
    With caching to improve performance for repeated validations
    """
    # Check cache first
    cached_result = TOKEN_CACHE.get(token)
    if cached_result:
        # Verify it hasn't expired since caching
        import time
        if cached_result.get("exp", 0) > time.time():
            return cached_result

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Add to cache with TTL slightly less than token expiration
        import time
        TOKEN_CACHE[token] = payload

        return payload
    except jwt.ExpiredSignatureError:
        # Remove expired token from cache if present
        TOKEN_CACHE.pop(token, None)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def clear_token_cache():
    """Clear the token cache - useful for testing or security reasons"""
    TOKEN_CACHE.clear()

def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from JWT token
    """
    payload = verify_token(token)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id