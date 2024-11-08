# backend/main.py
from fastapi import FastAPI
#from auth.models import models
from .auth.routes import router as auth_router
from .task_manager.routes import router as task_router
from .core.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include  routes prefixes
app.include_router(auth_router, prefix="/auth")

app.include_router(task_router, prefix="/tasks")

