from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .core.config import settings
from .core.logging import setup_logging
from .core.exceptions import register_exception_handlers
from .core.security_headers import add_security_headers
from .auth.middleware import JWTMiddleware
from .api.auth import router as auth_router
from .api.v1.todos import router as todos_router

# Set up logging
setup_logging()

app = FastAPI(
    title="Todo Application API",
    version="1.0.0",
    description="API for todo application with authentication and user isolation"
)

# Register custom exception handlers
register_exception_handlers(app)

# Add security headers
add_security_headers(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add JWT Middleware for authentication
app.add_middleware(JWTMiddleware)

# Include auth routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Include todos routes
app.include_router(todos_router, prefix="/api/v1", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Application API"}

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)