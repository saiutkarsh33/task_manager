from fastapi import APIRouter
from .routes import router as task_router
from .database import engine, Base
from .models import *

# Create database tables for the task manager service
Base.metadata.create_all(bind=engine)

def create_task_service():
    # Initialize the router for the task manager service
    router = APIRouter()
    router.include_router(task_router, prefix="/tasks")
    return router


