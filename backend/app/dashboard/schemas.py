"""Response schemas for authenticated dashboard analytics."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class CurrencyAmount(BaseModel):
    """One exact monetary total in its original currency."""

    currency: str
    amount: Decimal


class DashboardSummary(BaseModel):
    """Top-level counts and currency-separated financial totals."""

    total_trips: int
    active_trips: int
    total_expenses_by_currency: list[CurrencyAmount]
    remaining_budgets_by_currency: list[CurrencyAmount]


class CategorySpending(BaseModel):
    """Expense total for one seeded category and currency."""

    category_id: int
    category_name: str
    currency: str
    amount: Decimal


class TripSpending(BaseModel):
    """Expense total for one trip and currency."""

    trip_id: int
    trip_name: str
    currency: str
    amount: Decimal


class SpendingTrend(BaseModel):
    """Expense total for one date or month and currency."""

    period: str
    currency: str
    amount: Decimal


class BudgetComparison(BaseModel):
    """Planned and actual spending for one selected budget target."""

    budget_id: int
    trip_id: int | None
    category_id: int | None
    amount: Decimal
    currency: str
    actual_spending: Decimal
    remaining_amount: Decimal
    usage_percentage: Decimal
    is_overspent: bool


class DashboardFilters(BaseModel):
    """Optional filters shared by dashboard endpoints."""

    trip_id: int | None = None
    category_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
