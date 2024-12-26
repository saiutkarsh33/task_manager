from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Task
from .schemas import TaskCreate, TaskResponse
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pika
import json

# Define the task router
router = APIRouter()
RABBITMQ_HOST = "localhost"
RABBITMQ_QUEUE = "task_notifications"

# RabbitMQ connection setup
POOL_SIZE = 5
connection_pool = Queue(maxsize=POOL_SIZE)

# Create connections and add them to the pool
for _ in range(POOL_SIZE):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    connection_pool.put(connection)

# Function to send a message to RabbitMQ using connection pooling
def send_to_rabbitmq(message: dict):
    """Send a message to RabbitMQ using a connection from the pool."""
    try:
        # Get a connection from the pool
        connection = connection_pool.get()

        # Create a channel for publishing
        channel = connection.channel()

        # Ensure the queue exists
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

        # Publish the message to the queue
        channel.basic_publish(
            exchange="",
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )

        # Return the connection to the pool
        connection_pool.put(connection)

    except Exception as e:
        print(f"Error sending message to RabbitMQ: {e}")

# Clean up the pool when the application shuts down
@app.on_event("shutdown")
def shutdown_event():
    """Close all RabbitMQ connections in the pool."""
    while not connection_pool.empty():
        connection = connection_pool.get()
        connection.close()

# Background task to check deadlines
def check_deadlines():
    """Check for tasks with deadlines coming up in one day and notify via RabbitMQ."""
    with next(get_db()) as db:
        upcoming_tasks = db.query(Task).filter(
            Task.deadline <= datetime.utcnow() + timedelta(days=1),
            Task.deadline > datetime.utcnow(),
            Task.status == "Pending"
        ).all()
        
        for task in upcoming_tasks:
            message = {
                "task_id": task.task_id,
                "title": task.title,
                "deadline": task.deadline.isoformat(),
                "assigned_user_id": task.assigned_user_id
            }
            send_to_rabbitmq(message)

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(check_deadlines, "interval", minutes=1)  # Run every minute
scheduler.start()


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
