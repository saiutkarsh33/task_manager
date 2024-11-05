# Importing CryptContext from passlib to handle password hashing and verification
from passlib.context import CryptContext

# Importing jwt from jose to create and verify JSON Web Tokens (JWTs) for authentication
from jose import jwt

# Importing datetime and timedelta from the datetime module to handle time-related operations
from datetime import datetime, timedelta

# Importing configuration values for the secret key, algorithm, and token expiration time
from ..core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Initializing CryptContext with bcrypt as the hashing scheme
# "bcrypt" is a secure, adaptive hashing algorithm that makes it computationally expensive for attackers to guess passwords
# "deprecated='auto'" allows bcrypt to automatically handle deprecated hashing schemes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def hash_password(password: str):
    # Hashes the input password using bcrypt and returns the hashed version
    return pwd_context.hash(password)

# Function to verify a password
def verify_password(plain_password, hashed_password):
    # Compares a plain password with a hashed password to verify if they match
    # Returns True if the passwords match, False otherwise
    return pwd_context.verify(plain_password, hashed_password)

# Function to create an access token, which will be used for user authentication
def create_access_token(data: dict):
    # Creates a copy of the input data to avoid modifying the original dictionary
    to_encode = data.copy()
    
    # Sets an expiration time for the token by adding a timedelta (in minutes) to the current UTC time
    # ACCESS_TOKEN_EXPIRE_MINUTES defines how long the token will be valid
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Adds the expiration time to the data dictionary under the key "exp" (used by JWT to define expiration)
    to_encode.update({"exp": expire})
    
    # Encodes the data as a JWT using the secret key and specified algorithm, then returns the encoded token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

