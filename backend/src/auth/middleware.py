from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from typing import Optional
from ..core.security import verify_token
import logging

logger = logging.getLogger(__name__)

class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.security = HTTPBearer(auto_error=False)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Extract token from Authorization header
        authorization: str = request.headers.get("Authorization")

        if authorization:
            try:
                # Extract the token from "Bearer <token>" format
                scheme, credentials = authorization.split(" ")
                if scheme.lower() == "bearer":
                    # Verify the token
                    payload = verify_token(credentials)

                    # Store user info in request state for later use
                    request.state.user_id = payload.get("sub")
                    request.state.user_email = payload.get("email")
                    request.state.token_payload = payload
                    request.state.is_authenticated = True
                else:
                    request.state.is_authenticated = False
            except HTTPException:
                # Re-raise HTTP exceptions (like expired token, invalid credentials)
                raise
            except Exception as e:
                logger.warning(f"Invalid token: {str(e)}")
                request.state.is_authenticated = False
        else:
            request.state.is_authenticated = False

        response = await call_next(request)
        return response