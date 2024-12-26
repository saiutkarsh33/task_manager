from fastapi import APIRouter
from .routes import router as auth_router
from .database import engine, Base
from .models import *

# Create database tables for the task manager service
Base.metadata.create_all(bind=engine)

def create_auth_service():
    # Initialize the router for the auth service
    router = APIRouter()
    router.include_router(auth_router, prefix="/auth")
    return router
