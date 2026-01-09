import logging
import sys
from datetime import datetime
from enum import Enum

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

def setup_logging(level: LogLevel = LogLevel.INFO):
    """
    Set up logging configuration for the application
    """
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.value))
    root_logger.addHandler(console_handler)

    # Suppress overly verbose logs from third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

    return root_logger

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name
    """
    return logging.getLogger(name)

def log_auth_event(event_type: str, user_id: str = None, ip_address: str = None, details: dict = None):
    """
    Log authentication-related events for monitoring and security

    Args:
        event_type: Type of authentication event (login, logout, registration, etc.)
        user_id: ID of the user involved in the event
        ip_address: IP address of the request
        details: Additional details about the event
    """
    logger = get_logger(__name__)

    event_details = {
        "event_type": event_type,
        "user_id": user_id,
        "ip_address": ip_address,
        "timestamp": datetime.now().isoformat(),
        "details": details or {}
    }

    logger.info(f"AUTH_EVENT: {event_details}")

# Global logger instance
logger = get_logger(__name__)