# Importing the os module to access environment variables
import os

# Setting the database URL from an environment variable
# If the environment variable "DATABASE_URL" is not set, it defaults to a local PostgreSQL database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://saiutkarsh33:12345@localhost/task_manager_db")

# Defining a secret key used for signing and verifying JWTs
# This should be a secure, randomly generated key, especially in production to prevent unauthorized access
SECRET_KEY = "supersecretkey"  # Use a more secure key in production

# Defining the hashing algorithm used for encoding JWTs
# "HS256" is HMAC with SHA-256, a secure and widely used algorithm
ALGORITHM = "HS256"

# Setting the expiration time for access tokens in minutes
# Tokens will be valid for 30 minutes by default, after which they will expire
ACCESS_TOKEN_EXPIRE_MINUTES = 30
