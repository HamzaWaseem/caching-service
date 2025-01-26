from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./cache_service.db"  # Change to PostgreSQL URL for production
engine = create_engine(DATABASE_URL, echo=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


def init_db():
    from .models import TransformedString, Payload
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
