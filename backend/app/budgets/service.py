"""Business rules and database operations for budgets."""

from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.models import User
from app.budgets.models import Budget
from app.budgets.schemas import BudgetCreate, BudgetRead, BudgetUpdate
from app.categories.models import Category
from app.expenses.models import Expense
from app.trips.models import Trip


def list_budgets(db: Session, user: User) -> list[BudgetRead]:
    """Return the current user's budgets with live spending metrics."""
    budgets = db.scalars(
        select(Budget).where(Budget.user_id == user.id).order_by(Budget.created_at.desc(), Budget.id.desc())
    ).all()
    return [_to_read(db, budget, user) for budget in budgets]


def get_budget_or_404(db: Session, budget_id: int, user: User) -> Budget:
    """Return a user's budget without exposing another user's record."""
    budget = db.scalar(select(Budget).where(Budget.id == budget_id, Budget.user_id == user.id))
    if budget is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return budget


def get_budget_read_or_404(db: Session, budget_id: int, user: User) -> BudgetRead:
    """Return a budget and its calculated metrics."""
    return _to_read(db, get_budget_or_404(db, budget_id, user), user)


def create_budget(db: Session, budget_data: BudgetCreate, user: User) -> BudgetRead:
    """Validate target ownership and persist a new budget."""
    values = budget_data.model_dump()
    _validate_target(db, values["trip_id"], values["category_id"], user)
    _ensure_unique_target(db, user, values["trip_id"], values["category_id"])
    budget = Budget(**values, user_id=user.id)
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return _to_read(db, budget, user)


def update_budget(db: Session, budget: Budget, budget_data: BudgetUpdate, user: User) -> BudgetRead:
    """Apply supplied changes after validating the resulting budget target."""
    changes = budget_data.model_dump(exclude_unset=True)
    trip_id = changes.get("trip_id", budget.trip_id)
    category_id = changes.get("category_id", budget.category_id)
    _validate_target(db, trip_id, category_id, user)
    _ensure_unique_target(db, user, trip_id, category_id, exclude_budget_id=budget.id)

    for field_name, value in changes.items():
        setattr(budget, field_name, value)

    db.commit()
    db.refresh(budget)
    return _to_read(db, budget, user)


def delete_budget(db: Session, budget: Budget) -> None:
    """Delete a budget already confirmed to belong to the current user."""
    db.delete(budget)
    db.commit()


def _validate_target(db: Session, trip_id: int | None, category_id: int | None, user: User) -> None:
    if trip_id is None and category_id is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A budget must target a trip, a category, or both",
        )
    if trip_id is not None and db.scalar(select(Trip).where(Trip.id == trip_id, Trip.user_id == user.id)) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    if category_id is not None and db.get(Category, category_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")


def _ensure_unique_target(
    db: Session,
    user: User,
    trip_id: int | None,
    category_id: int | None,
    exclude_budget_id: int | None = None,
) -> None:
    trip_condition = Budget.trip_id.is_(None) if trip_id is None else Budget.trip_id == trip_id
    category_condition = (
        Budget.category_id.is_(None) if category_id is None else Budget.category_id == category_id
    )
    statement = select(Budget).where(Budget.user_id == user.id, trip_condition, category_condition)
    if exclude_budget_id is not None:
        statement = statement.where(Budget.id != exclude_budget_id)
    if db.scalar(statement) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A budget already exists for this target",
        )


def _to_read(db: Session, budget: Budget, user: User) -> BudgetRead:
    """Build a response with only matching-currency expenses for this budget's target."""
    statement = (
        select(func.coalesce(func.sum(Expense.amount_original), 0))
        .join(Trip, Expense.trip_id == Trip.id)
        .where(Trip.user_id == user.id, Expense.currency_original == budget.currency)
    )
    if budget.trip_id is not None:
        statement = statement.where(Expense.trip_id == budget.trip_id)
    if budget.category_id is not None:
        statement = statement.where(Expense.category_id == budget.category_id)

    actual_spending = Decimal(db.scalar(statement) or 0).quantize(Decimal("0.01"))
    remaining_amount = (budget.amount - actual_spending).quantize(Decimal("0.01"))
    usage_percentage = (actual_spending / budget.amount * 100).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    return BudgetRead(
        id=budget.id,
        trip_id=budget.trip_id,
        category_id=budget.category_id,
        amount=budget.amount,
        currency=budget.currency,
        created_at=budget.created_at,
        updated_at=budget.updated_at,
        actual_spending=actual_spending,
        remaining_amount=remaining_amount,
        usage_percentage=usage_percentage,
        is_overspent=actual_spending > budget.amount,
    )
