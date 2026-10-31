"""Environment-based settings for the backend application."""

import os


DEFAULT_DATABASE_URL = "sqlite:///./smart_travel_expense.db"
DEFAULT_FRONTEND_ORIGIN = "http://localhost:5173"
DEFAULT_SECRET_KEY = "development-only-secret-change-before-production"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def get_database_url() -> str:
    """Return a configured database URL or the local SQLite fallback."""
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def get_frontend_origin() -> str:
    """Return the frontend origin allowed to call this API locally."""
    return os.getenv("FRONTEND_ORIGIN", DEFAULT_FRONTEND_ORIGIN)


def get_secret_key() -> str:
    """Return the JWT signing key from the environment."""
    return os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)
