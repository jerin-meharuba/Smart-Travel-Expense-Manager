"""FastAPI routes for authenticated dashboard analytics."""

from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import CurrentUser
from app.dashboard import service
from app.dashboard.schemas import (
    BudgetComparison,
    CategorySpending,
    DashboardFilters,
    DashboardSummary,
    SpendingTrend,
    TripSpending,
)
from app.database import get_db


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _filters(
    trip_id: int | None = Query(default=None, gt=0),
    category_id: int | None = Query(default=None, gt=0),
    start_date: date | None = None,
    end_date: date | None = None,
) -> DashboardFilters:
    return DashboardFilters(
        trip_id=trip_id,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/summary", response_model=DashboardSummary)
def read_summary(
    current_user: CurrentUser,
    filters: DashboardFilters = Depends(_filters),
    db: Session = Depends(get_db),
) -> DashboardSummary:
    service.validate_filters(db, current_user, filters)
    return service.get_summary(db, current_user, filters)


@router.get("/spending-by-category", response_model=list[CategorySpending])
def read_spending_by_category(
    current_user: CurrentUser,
    filters: DashboardFilters = Depends(_filters),
    db: Session = Depends(get_db),
) -> list[CategorySpending]:
    service.validate_filters(db, current_user, filters)
    return service.get_spending_by_category(db, current_user, filters)


@router.get("/spending-by-trip", response_model=list[TripSpending])
def read_spending_by_trip(
    current_user: CurrentUser,
    filters: DashboardFilters = Depends(_filters),
    db: Session = Depends(get_db),
) -> list[TripSpending]:
    service.validate_filters(db, current_user, filters)
    return service.get_spending_by_trip(db, current_user, filters)


@router.get("/spending-trends", response_model=list[SpendingTrend])
def read_spending_trends(
    current_user: CurrentUser,
    filters: DashboardFilters = Depends(_filters),
    period: Literal["daily", "monthly"] = Query(default="monthly"),
    db: Session = Depends(get_db),
) -> list[SpendingTrend]:
    service.validate_filters(db, current_user, filters)
    return service.get_spending_trends(db, current_user, filters, period)


@router.get("/budget-comparison", response_model=list[BudgetComparison])
def read_budget_comparison(
    current_user: CurrentUser,
    filters: DashboardFilters = Depends(_filters),
    db: Session = Depends(get_db),
) -> list[BudgetComparison]:
    service.validate_filters(db, current_user, filters)
    return service.get_budget_comparison(db, current_user, filters)
