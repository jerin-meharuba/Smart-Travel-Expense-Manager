"""FastAPI routes for the Expense CRUD feature."""

from datetime import date

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.expenses import service
from app.expenses.schemas import ExpenseCreate, ExpenseListResponse, ExpenseRead, ExpenseUpdate


router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(expense_data: ExpenseCreate, db: Session = Depends(get_db)) -> ExpenseRead:
    return service.create_expense(db, expense_data)


@router.get("", response_model=ExpenseListResponse)
def read_expenses(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    trip_id: int | None = Query(default=None, gt=0),
    category_id: int | None = Query(default=None, gt=0),
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
) -> ExpenseListResponse:
    expenses, total = service.list_expenses(
        db, offset, limit, trip_id, category_id, start_date, end_date
    )
    return ExpenseListResponse(items=expenses, total=total, offset=offset, limit=limit)


@router.get("/{expense_id}", response_model=ExpenseRead)
def read_expense(expense_id: int, db: Session = Depends(get_db)) -> ExpenseRead:
    return service.get_expense_or_404(db, expense_id)


@router.patch("/{expense_id}", response_model=ExpenseRead)
def patch_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
) -> ExpenseRead:
    expense = service.get_expense_or_404(db, expense_id)
    return service.update_expense(db, expense, expense_data)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_expense(expense_id: int, db: Session = Depends(get_db)) -> Response:
    expense = service.get_expense_or_404(db, expense_id)
    service.delete_expense(db, expense)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
