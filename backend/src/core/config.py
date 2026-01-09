from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # JWT Configuration
    jwt_secret: str = os.getenv("JWT_SECRET", "fallback-jwt-secret-key-change-in-production")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration_minutes: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))

    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "")
    neon_database_url: str = os.getenv("NEON_DATABASE_URL", "")

    # Better Auth Configuration
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")

    # Server Configuration
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        env_file = ".env"

settings = Settings()