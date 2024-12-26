# backend/auth/models.py
from sqlalchemy import Column, Integer, String, UniqueConstraint, relationship
from .database import Base

class User(Base): 
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # Lazy Loading: By default, SQLAlchemy uses lazy loading for relationships, meaning the related objects are not loaded from the database until they are accessed. This is efficient and allows you to work with the related objects as if they were a lis
    tasks = relationship("Task", back_populates="user")
    
    __table_args__ = (
        UniqueConstraint("username", name="uq_user_username"),
        UniqueConstraint("email", name="uq_user_email"),
    )
