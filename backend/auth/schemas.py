# Importing the BaseModel class from the Pydantic library, which is used to define data models with validation
from pydantic import BaseModel

# Defining a Pydantic model for creating a new user, with required fields for username, email, and password
class UserCreate(BaseModel):
    # The username field, which is a required string
    username: str
    # The email field, which is a required string and will be validated as an email by Pydantic if specified in constraints
    email: str
    # The password field, which is a required string
    password: str

# Defining a Pydantic model for user login, with required fields for username and password
class UserLogin(BaseModel):
    # The username field for login, which is a required string
    username: str
    # The password field for login, which is a required string
    password: str
