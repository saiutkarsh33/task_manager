from pydantic import BaseModel
from datetime import datetime

# Pydantic model for task creation request
class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_user_id: int

class TaskResponse(BaseModel):
    task_id: int
    title: str
    description: str
    status: str
    assigned_user_id: int
    created_at: datetime
    updated_at: datetime