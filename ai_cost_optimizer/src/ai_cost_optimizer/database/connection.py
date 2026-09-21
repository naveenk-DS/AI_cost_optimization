import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Build the connection URL securely from environment variables.
# We DO NOT hardcode passwords or IPs.
# We also use `quote_plus` to safely encode passwords in case yours contains special symbols like '#' or '@'.
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT", "5433")
DB_NAME = os.getenv("DATABASE_NAME")

# Because your Brother's PostgreSQL Desktop goes to sleep/offline,
# we are temporarily failing over to a localized SQLite file!
DATABASE_URL = "sqlite:///./cost_analytics.db"

# ENGINE: The core interface resolving how we speak to the database.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}, # Required for FastAPI SQLite
    echo=False            
)

# SESSION FACTORY: Generates temporary database "Sessions".
# Autocommit is False so we have explicit control over transactions (we can rollback on failure).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# BASE MODEL: Every SQLAlchemy database table we define later will inherit from this class.
Base = declarative_base()

# FASTAPI DEPENDENCY: FastAPI uses this `yield` generator to safely inject a database session 
# straight into our API routes. It mathematically guarantees that it will close the connection 
# when the network request finishes, even if the python code crashes!
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
