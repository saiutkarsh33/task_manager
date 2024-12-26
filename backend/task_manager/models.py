from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="Pending")
    assigned_user_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deadline = Column(DateTime)
    # 
    user = relationship("User", back_populates="tasks")

    __table_args__ = (
        Index('idx_assigned_user_status', 'assigned_user_id', 'status'),
        Index('idx_assigned_user_deadline', 'assigned_user_id', 'deadline'),
    )
