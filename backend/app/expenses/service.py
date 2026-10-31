"""Business rules and database operations for expenses."""

from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.categories.models import Category
from app.expenses.models import Expense
from app.expenses.schemas import ExpenseCreate, ExpenseUpdate
from app.trips.models import Trip


def get_expense_or_404(db: Session, expense_id: int) -> Expense:
    """Return an expense or the standard not-found API response."""
    expense = db.get(Expense, expense_id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


def create_expense(db: Session, expense_data: ExpenseCreate) -> Expense:
    """Validate relations and persist a new expense."""
    _validate_relationships(db, expense_data.trip_id, expense_data.category_id)
    expense = Expense(**expense_data.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def list_expenses(
    db: Session,
    offset: int,
    limit: int,
    trip_id: int | None,
    category_id: int | None,
    start_date: date | None,
    end_date: date | None,
) -> tuple[list[Expense], int]:
    """Return newest expenses first, with optional filters and a total."""
    statement = select(Expense)
    count_statement = select(func.count()).select_from(Expense)

    if trip_id is not None:
        statement = statement.where(Expense.trip_id == trip_id)
        count_statement = count_statement.where(Expense.trip_id == trip_id)
    if category_id is not None:
        statement = statement.where(Expense.category_id == category_id)
        count_statement = count_statement.where(Expense.category_id == category_id)
    if start_date is not None:
        statement = statement.where(Expense.expense_date >= start_date)
        count_statement = count_statement.where(Expense.expense_date >= start_date)
    if end_date is not None:
        statement = statement.where(Expense.expense_date <= end_date)
        count_statement = count_statement.where(Expense.expense_date <= end_date)

    total = db.scalar(count_statement) or 0
    expenses = db.scalars(
        statement.order_by(Expense.expense_date.desc(), Expense.id.desc()).offset(offset).limit(limit)
    ).all()
    return expenses, total


def update_expense(db: Session, expense: Expense, expense_data: ExpenseUpdate) -> Expense:
    """Apply only supplied fields after validating updated relationships."""
    changes = expense_data.model_dump(exclude_unset=True)
    trip_id = changes.get("trip_id", expense.trip_id)
    category_id = changes.get("category_id", expense.category_id)
    _validate_relationships(db, trip_id, category_id)

    for field_name, value in changes.items():
        setattr(expense, field_name, value)

    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense: Expense) -> None:
    """Remove an expense that was already confirmed to exist."""
    db.delete(expense)
    db.commit()


def _validate_relationships(db: Session, trip_id: int, category_id: int) -> None:
    if db.get(Trip, trip_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    if db.get(Category, category_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
