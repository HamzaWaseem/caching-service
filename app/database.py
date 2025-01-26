"""
This module contains database-related utilities, including session management
and model definitions for interacting with the database.
"""
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./cache_service.db"  # Change to PostgreSQL URL for production
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


def init_db():
    """Initializes the database."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Returns a session object to interact with the database."""
    with Session(engine) as session:
        yield session
