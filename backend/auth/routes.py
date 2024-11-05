# Import necessary modules from FastAPI and SQLAlchemy
from fastapi import APIRouter, Depends, HTTPException  # APIRouter organizes routes, Depends handles dependencies, HTTPException manages errors
from sqlalchemy.orm import Session  # Session manages database transactions

# Import necessary modules and functions from the current package
from . import models, schemas, auth  # Import models for database tables, schemas for request validation, and auth for authentication functions
from ..core.database import get_db  # Import get_db to provide a database session to each request

# Create an APIRouter instance to group and manage authentication-related routes
router = APIRouter()

# Define the route for user registration
@router.post("/register")  # This decorator registers the function as a POST route for "/register"
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user in the database.
    """

    # Check if a user with the same username already exists in the database
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        # If a user is found, raise an HTTP 400 error to indicate that the username is already taken
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password provided by the user for secure storage
    hashed_password = auth.hash_password(user.password)

    # Create a new User object with the provided username, email, and hashed password
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)

    # Add the new user object to the database session
    db.add(new_user)

    # Commit the transaction to save the new user to the database
    db.commit()

    # Return a success message as a JSON response
    return {"message": "User registered successfully"}

# Define the route for user login
@router.post("/login")  # This decorator registers the function as a POST route for "/login"
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and provide an access token upon successful login.
    """

    # Query the database for a user with the provided username
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    # Check if the user exists and if the password provided matches the stored hashed password
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        # If either the user does not exist or the password is incorrect, raise an HTTP 400 error
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create a JSON Web Token (JWT) for the user with their username as part of the payload
    token = auth.create_access_token(data={"sub": user.username})

    # Return the JWT in a JSON response, allowing the user to use it for authenticated requests
    return {"access_token": token, "token_type": "bearer"}

