"""Read and seed operations for fixed expense categories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.categories.models import Category


DEFAULT_CATEGORY_NAMES = (
    "Accommodation",
    "Activities",
    "Food",
    "Other",
    "Transport",
)


def seed_default_categories(db: Session) -> None:
    """Insert the initial categories once without modifying existing data."""
    existing_names = set(db.scalars(select(Category.name)).all())
    missing_categories = [
        Category(name=name) for name in DEFAULT_CATEGORY_NAMES if name not in existing_names
    ]
    if missing_categories:
        db.add_all(missing_categories)
        db.commit()


def list_categories(db: Session) -> list[Category]:
    """Return seeded categories in a predictable alphabetical order."""
    return db.scalars(select(Category).order_by(Category.name)).all()
