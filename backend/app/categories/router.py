"""Read-only API routes for seeded expense categories."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.categories.schemas import CategoryRead
from app.categories import service
from app.database import get_db


router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryRead])
def read_categories(db: Session = Depends(get_db)) -> list[CategoryRead]:
    return service.list_categories(db)
