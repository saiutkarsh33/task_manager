from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from .models import Task
from .schemas import TaskCreate, TaskResponse


# Define the task router
router = APIRouter()



# Endpoint to create a task
@router.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        assigned_user_id=task.assigned_user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Endpoint to get all tasks for a user
@router.get("/tasks/", response_model=list[TaskResponse])
def get_tasks(assigned_user_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.assigned_user_id == assigned_user_id).all()
    return tasks

# Endpoint to delete a task by ID
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
