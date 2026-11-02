"""Authorized database analytics for the dashboard API."""

from collections import defaultdict
from collections.abc import Iterable
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.models import User
from app.budgets.models import Budget
from app.categories.models import Category
from app.dashboard.schemas import (
    BudgetComparison,
    CategorySpending,
    CurrencyAmount,
    DashboardFilters,
    DashboardSummary,
    SpendingTrend,
    TripSpending,
)
from app.expenses.models import Expense
from app.trips.models import Trip


def get_summary(db: Session, user: User, filters: DashboardFilters) -> DashboardSummary:
    """Return authorized trip counts and financial totals grouped by currency."""
    expenses = _get_expenses(db, user, filters)
    comparisons = _get_budget_comparisons(db, user, filters, expenses)
    total_trips, active_trips = _trip_counts(db, user, filters, expenses)
    return DashboardSummary(
        total_trips=total_trips,
        active_trips=active_trips,
        total_expenses_by_currency=_currency_amounts(
            (expense.currency_original, expense.amount_original) for expense in expenses
        ),
        remaining_budgets_by_currency=_currency_amounts(
            (comparison.currency, comparison.remaining_amount) for comparison in comparisons
        ),
    )


def get_spending_by_category(
    db: Session, user: User, filters: DashboardFilters
) -> list[CategorySpending]:
    """Group authorized filtered expenses by category and original currency."""
    categories = {category.id: category.name for category in db.scalars(select(Category)).all()}
    totals: dict[tuple[int, str], Decimal] = defaultdict(Decimal)
    for expense in _get_expenses(db, user, filters):
        totals[(expense.category_id, expense.currency_original)] += expense.amount_original
    return [
        CategorySpending(
            category_id=category_id,
            category_name=categories.get(category_id, "Unknown category"),
            currency=currency,
            amount=_money(amount),
        )
        for (category_id, currency), amount in sorted(totals.items(), key=lambda item: (item[0][0], item[0][1]))
    ]


def get_spending_by_trip(db: Session, user: User, filters: DashboardFilters) -> list[TripSpending]:
    """Group authorized filtered expenses by trip and original currency."""
    trips = {trip.id: trip.name for trip in db.scalars(select(Trip).where(Trip.user_id == user.id)).all()}
    totals: dict[tuple[int, str], Decimal] = defaultdict(Decimal)
    for expense in _get_expenses(db, user, filters):
        totals[(expense.trip_id, expense.currency_original)] += expense.amount_original
    return [
        TripSpending(
            trip_id=trip_id,
            trip_name=trips.get(trip_id, "Unknown trip"),
            currency=currency,
            amount=_money(amount),
        )
        for (trip_id, currency), amount in sorted(totals.items(), key=lambda item: (item[0][0], item[0][1]))
    ]


def get_spending_trends(
    db: Session, user: User, filters: DashboardFilters, period: str
) -> list[SpendingTrend]:
    """Group authorized filtered expenses by day or month and original currency."""
    totals: dict[tuple[str, str], Decimal] = defaultdict(Decimal)
    for expense in _get_expenses(db, user, filters):
        label = expense.expense_date.isoformat() if period == "daily" else expense.expense_date.strftime("%Y-%m")
        totals[(label, expense.currency_original)] += expense.amount_original
    return [
        SpendingTrend(period=label, currency=currency, amount=_money(amount))
        for (label, currency), amount in sorted(totals.items())
    ]


def get_budget_comparison(
    db: Session, user: User, filters: DashboardFilters
) -> list[BudgetComparison]:
    """Return matching user budgets with their actual authorized expense amounts."""
    return _get_budget_comparisons(db, user, filters, _get_expenses(db, user, filters))


def validate_filters(db: Session, user: User, filters: DashboardFilters) -> None:
    """Validate date order and ensure selected records are accessible."""
    if filters.start_date and filters.end_date and filters.end_date < filters.start_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="end_date must not be earlier than start_date",
        )
    if filters.trip_id is not None and db.scalar(
        select(Trip).where(Trip.id == filters.trip_id, Trip.user_id == user.id)
    ) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    if filters.category_id is not None and db.get(Category, filters.category_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")


def _get_expenses(db: Session, user: User, filters: DashboardFilters) -> list[Expense]:
    statement = select(Expense).join(Trip, Expense.trip_id == Trip.id).where(Trip.user_id == user.id)
    if filters.trip_id is not None:
        statement = statement.where(Expense.trip_id == filters.trip_id)
    if filters.category_id is not None:
        statement = statement.where(Expense.category_id == filters.category_id)
    if filters.start_date is not None:
        statement = statement.where(Expense.expense_date >= filters.start_date)
    if filters.end_date is not None:
        statement = statement.where(Expense.expense_date <= filters.end_date)
    return db.scalars(statement).all()


def _trip_counts(
    db: Session, user: User, filters: DashboardFilters, expenses: list[Expense]
) -> tuple[int, int]:
    """Count all trips normally, or only trips represented by active filters."""
    has_filter = any((filters.trip_id, filters.category_id, filters.start_date, filters.end_date))
    if not has_filter:
        total = db.scalar(select(func.count()).select_from(Trip).where(Trip.user_id == user.id)) or 0
        active = (
            db.scalar(
                select(func.count()).select_from(Trip).where(Trip.user_id == user.id, Trip.status == "active")
            )
            or 0
        )
        return total, active

    trip_ids = {expense.trip_id for expense in expenses}
    if filters.trip_id is not None:
        trip_ids.add(filters.trip_id)
    if not trip_ids:
        return 0, 0
    active = (
        db.scalar(
            select(func.count()).select_from(Trip).where(
                Trip.user_id == user.id, Trip.id.in_(trip_ids), Trip.status == "active"
            )
        )
        or 0
    )
    return len(trip_ids), active


def _get_budget_comparisons(
    db: Session, user: User, filters: DashboardFilters, expenses: list[Expense]
) -> list[BudgetComparison]:
    budgets = db.scalars(select(Budget).where(Budget.user_id == user.id).order_by(Budget.id)).all()
    comparisons: list[BudgetComparison] = []
    for budget in budgets:
        if filters.trip_id is not None and budget.trip_id not in (None, filters.trip_id):
            continue
        if filters.category_id is not None and budget.category_id not in (None, filters.category_id):
            continue
        actual_spending = sum(
            (
                expense.amount_original
                for expense in expenses
                if expense.currency_original == budget.currency
                and (budget.trip_id is None or expense.trip_id == budget.trip_id)
                and (budget.category_id is None or expense.category_id == budget.category_id)
            ),
            start=Decimal("0"),
        )
        actual_spending = _money(actual_spending)
        remaining_amount = _money(budget.amount - actual_spending)
        usage_percentage = (actual_spending / budget.amount * 100).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        comparisons.append(
            BudgetComparison(
                budget_id=budget.id,
                trip_id=budget.trip_id,
                category_id=budget.category_id,
                amount=budget.amount,
                currency=budget.currency,
                actual_spending=actual_spending,
                remaining_amount=remaining_amount,
                usage_percentage=usage_percentage,
                is_overspent=actual_spending > budget.amount,
            )
        )
    return comparisons


def _currency_amounts(values: Iterable[tuple[str, Decimal]]) -> list[CurrencyAmount]:
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for currency, amount in values:
        totals[currency] += amount
    return [CurrencyAmount(currency=currency, amount=_money(amount)) for currency, amount in sorted(totals.items())]


def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"))
