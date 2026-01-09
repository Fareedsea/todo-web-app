from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from typing import Generator
from ..core.database import get_session
from ..auth.service import get_current_user
from ..auth.models import User

def get_db_session() -> Generator[Session, None, None]:
    """Dependency to get database session."""
    session = next(get_session())
    try:
        yield session
    finally:
        session.close()

