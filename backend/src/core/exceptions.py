from fastapi import HTTPException, status
from typing import Optional

class BaseCustomException(HTTPException):
    """
    Base exception class for custom application exceptions
    """
    def __init__(self, detail: str, status_code: int, headers: Optional[dict] = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class AuthenticationException(BaseCustomException):
    """
    Exception raised for authentication-related errors
    """
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"}
        )

class AuthorizationException(BaseCustomException):
    """
    Exception raised for authorization-related errors
    """
    def __init__(self, detail: str = "Access denied"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_403_FORBIDDEN
        )

class UserNotFoundException(BaseCustomException):
    """
    Exception raised when a user is not found
    """
    def __init__(self, detail: str = "User not found"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_404_NOT_FOUND
        )

class UserAlreadyExistsException(BaseCustomException):
    """
    Exception raised when attempting to create a user that already exists
    """
    def __init__(self, detail: str = "User already exists"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_409_CONFLICT
        )

class ValidationErrorException(BaseCustomException):
    """
    Exception raised for validation errors
    """
    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

def register_exception_handlers(app):
    """
    Register custom exception handlers with the FastAPI application
    """
    @app.exception_handler(AuthenticationException)
    async def handle_auth_exception(request, exc):
        return exc

    @app.exception_handler(AuthorizationException)
    async def handle_authz_exception(request, exc):
        return exc

    @app.exception_handler(UserNotFoundException)
    async def handle_user_not_found_exception(request, exc):
        return exc

    @app.exception_handler(UserAlreadyExistsException)
    async def handle_user_already_exists_exception(request, exc):
        return exc

    @app.exception_handler(ValidationErrorException)
    async def handle_validation_error_exception(request, exc):
        return exc