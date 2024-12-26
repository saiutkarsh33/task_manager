from fastapi import FastAPI
from backend.auth import routes as auth_routes  # Triggers backend/auth/__init__.py
from backend.task_manager import routes as task_routes  # Triggers backend/task_manager/__init__.py

app = FastAPI()

# Include routers for each service
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(task_routes.router, prefix="/tasks")

