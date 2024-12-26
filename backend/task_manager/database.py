# Importing the create_engine function from SQLAlchemy, which is used to establish a connection to the database
from sqlalchemy import create_engine

# Importing the declarative_base function from SQLAlchemy, which is a factory function that returns a new base class from which all mapped classes should inherit
from sqlalchemy.ext.declarative import declarative_base

# Importing the sessionmaker function from SQLAlchemy, which creates a new session factory to interact with the database
from sqlalchemy.orm import sessionmaker

# Importing the DATABASE_URL variable from the config file, which contains the URL of the database
from .config import DATABASE_URL

# Creating a new SQLAlchemy Engine instance, which establishes a connection to the database using the provided URL
engine = create_engine(DATABASE_URL)

# Creating a new session factory using sessionmaker, which will create individual sessions for each request
# autocommit=False: disables automatic committing, so transactions are committed explicitly
# bind=engine: binds this session factory to the database engine created above
SessionLocal = sessionmaker(autocommit=False, bind=engine)

# Creating a new base class for declarative class definitions; all models will inherit from this base
Base = declarative_base()

# Defining a function get_db() to create a new database session for each request and manage its lifecycle
def get_db():
    # Creating a new session from the session factory
    db = SessionLocal()
    try:
        # Yielding the session object to be used in request handling functions
        yield db
    finally:
        # Ensuring the session is closed after the request is completed to release database resources
        db.close()
