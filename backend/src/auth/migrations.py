"""
Database migration module for authentication models
"""

from sqlmodel import SQLModel
from .models import User, JWTToken
from .database import engine

def create_db_and_tables():
    """
    Creates database tables based on SQLModel definitions
    """
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()