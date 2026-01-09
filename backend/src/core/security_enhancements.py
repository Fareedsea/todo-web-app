from fastapi import Request, HTTPException, status, Depends
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time
from typing import Dict, Optional
from collections import defaultdict
from datetime import datetime, timedelta

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Track failed login attempts
failed_attempts: Dict[str, list] = defaultdict(list)
BLOCK_DURATION = 300  # 5 minutes
MAX_FAILED_ATTEMPTS = 5

def get_blocked_ips():
    """Clean and return currently blocked IPs"""
    global failed_attempts
    now = time.time()
    # Clean old attempts
    for ip in list(failed_attempts.keys()):
        failed_attempts[ip] = [timestamp for timestamp in failed_attempts[ip]
                              if now - timestamp < BLOCK_DURATION]
        if not failed_attempts[ip]:
            del failed_attempts[ip]
    return failed_attempts

def check_brute_force(ip: str) -> bool:
    """
    Check if an IP should be blocked due to too many failed attempts

    Args:
        ip: The IP address to check

    Returns:
        True if the IP is blocked, False otherwise
    """
    now = time.time()

    # Clean old attempts for this IP
    failed_attempts[ip] = [timestamp for timestamp in failed_attempts[ip]
                          if now - timestamp < BLOCK_DURATION]

    # Check if this IP has exceeded the maximum failed attempts
    if len(failed_attempts[ip]) >= MAX_FAILED_ATTEMPTS:
        return True

    return False

def record_failed_attempt(ip: str):
    """
    Record a failed authentication attempt for an IP

    Args:
        ip: The IP address of the request
    """
    failed_attempts[ip].append(time.time())

def reset_failed_attempts(ip: str):
    """
    Reset failed attempts counter for an IP after successful login

    Args:
        ip: The IP address of the request
    """
    if ip in failed_attempts:
        del failed_attempts[ip]

def secure_verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Securely verify a password with timing attack protection
    """
    import hmac
    from ..core.security import pwd_context

    # Use a constant time comparison to prevent timing attacks
    return pwd_context.verify(plain_password, hashed_password)

def validate_input(input_str: str, max_length: int = 255, pattern: Optional[str] = None) -> bool:
    """
    Validate user input to prevent injection attacks

    Args:
        input_str: The input string to validate
        max_length: Maximum allowed length
        pattern: Regex pattern to match against

    Returns:
        True if input is valid, raises HTTPException otherwise
    """
    if not isinstance(input_str, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input type"
        )

    if len(input_str) > max_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Input exceeds maximum length of {max_length} characters"
        )

    if pattern:
        import re
        if not re.match(pattern, input_str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Input does not match required pattern"
            )

    # Check for potential SQL injection patterns
    dangerous_patterns = ["'", "\"", "--", "/*", "*/", "xp_", "sp_", "exec", "execute", "select", "insert", "update", "delete"]
    lower_input = input_str.lower()
    for pattern in dangerous_patterns:
        if pattern in lower_input:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Input contains potentially dangerous characters"
            )

    return True

def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    """
    # Remove potentially dangerous characters
    sanitized = input_str.replace("<", "&lt;").replace(">", "&gt;")
    return sanitized

def add_security_headers(response):
    """
    Add security headers to response
    """
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response