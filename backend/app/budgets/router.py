"""FastAPI routes for authenticated budget management."""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.auth.dependencies import CurrentUser
from app.budgets import service
from app.budgets.schemas import BudgetCreate, BudgetRead, BudgetUpdate
from app.database import get_db


router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.get("", response_model=list[BudgetRead])
def read_budgets(current_user: CurrentUser, db: Session = Depends(get_db)) -> list[BudgetRead]:
    return service.list_budgets(db, current_user)


@router.post("", response_model=BudgetRead, status_code=status.HTTP_201_CREATED)
def create_budget(
    budget_data: BudgetCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> BudgetRead:
    return service.create_budget(db, budget_data, current_user)


@router.get("/{budget_id}", response_model=BudgetRead)
def read_budget(budget_id: int, current_user: CurrentUser, db: Session = Depends(get_db)) -> BudgetRead:
    return service.get_budget_read_or_404(db, budget_id, current_user)


@router.patch("/{budget_id}", response_model=BudgetRead)
def patch_budget(
    budget_id: int,
    budget_data: BudgetUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
) -> BudgetRead:
    budget = service.get_budget_or_404(db, budget_id, current_user)
    return service.update_budget(db, budget, budget_data, current_user)


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_budget(budget_id: int, current_user: CurrentUser, db: Session = Depends(get_db)) -> Response:
    budget = service.get_budget_or_404(db, budget_id, current_user)
    service.delete_budget(db, budget)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
