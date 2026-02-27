"""Database configuration and connection management.

This module provides database initialization and session management
for the SQLModel ORM.
"""

from sqlmodel import Session, create_engine, SQLModel
from models import EventType, Event, Participant, User
from config.app_config import settings
from typing import Generator

DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def init_db() -> None:
    """Initialize the database by creating all tables.

    Creates all tables defined in SQLModel metadata if they don't exist.
    Should be called once at application startup.
    """
    SQLModel.metadata.create_all(engine)


def get_db_conn() -> Generator[Session, None, None]:
    """Provide a database session for dependency injection.

    This is a FastAPI dependency that yields a database session
    and ensures it is properly closed after the request.

    Yields:
        A SQLModel Session instance.
    """
    with Session(engine) as session:
        yield session
