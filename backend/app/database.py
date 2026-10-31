"""SQLAlchemy engine and session helpers."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_database_url


DATABASE_URL = get_database_url()

engine_options: dict[str, object] = {}
if DATABASE_URL.startswith("sqlite"):
    # SQLite needs this option because FastAPI handles requests in threads.
    engine_options["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_options)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Base class shared by database models."""


def get_db() -> Generator[Session, None, None]:
    """Provide one database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """Create local tables for a first-run development database."""
    # Importing the model registers it with Base.metadata before create_all.
    from app.trips import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
