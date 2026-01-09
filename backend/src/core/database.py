from sqlmodel import create_engine, Session
from sqlalchemy import event
from sqlalchemy.pool import QueuePool
from .config import settings
import os

# Use Neon database URL if available, otherwise fall back to standard database URL
database_url = settings.neon_database_url or settings.database_url

# Create the database engine with connection pooling optimized for serverless
engine = create_engine(
    database_url,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    echo=False           # Set to True for SQL query logging
)

def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session

# Add a listener to handle disconnections gracefully for serverless environments
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Configure connection for better serverless compatibility"""
    if 'sqlite' in str(dbapi_connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()