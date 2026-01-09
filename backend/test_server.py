from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.core.config import settings
from src.core.database import engine
from src.models.todo import Todo
from src.auth.models import User
from sqlmodel import SQLModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    SQLModel.metadata.create_all(engine)
    yield
    # Cleanup on shutdown if needed

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)