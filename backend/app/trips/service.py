"""Business rules and database operations for trips."""

from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.trips.models import Trip
from app.trips.schemas import TripCreate, TripUpdate


def get_trip_or_404(db: Session, trip_id: int) -> Trip:
    """Return a trip or the standard not-found API response."""
    trip = db.get(Trip, trip_id)
    if trip is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return trip


def create_trip(db: Session, trip_data: TripCreate) -> Trip:
    """Persist a newly validated trip."""
    trip = Trip(**trip_data.model_dump())
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


def list_trips(db: Session, offset: int, limit: int) -> tuple[list[Trip], int]:
    """Return newest trips first together with their total count."""
    total = db.scalar(select(func.count()).select_from(Trip)) or 0
    trips = db.scalars(
        select(Trip).order_by(Trip.created_at.desc(), Trip.id.desc()).offset(offset).limit(limit)
    ).all()
    return trips, total


def update_trip(db: Session, trip: Trip, trip_data: TripUpdate) -> Trip:
    """Apply only supplied fields and validate the resulting date range."""
    changes = trip_data.model_dump(exclude_unset=True)
    proposed_start_date = changes.get("start_date", trip.start_date)
    proposed_end_date = changes.get("end_date", trip.end_date)
    _validate_date_range(proposed_start_date, proposed_end_date)

    if "budget_amount" in changes and changes["budget_amount"] is not None:
        currency = changes.get("budget_currency", trip.budget_currency)
        if currency is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="budget_currency is required when budget_amount is set",
            )

    for field_name, value in changes.items():
        setattr(trip, field_name, value)

    db.commit()
    db.refresh(trip)
    return trip


def delete_trip(db: Session, trip: Trip) -> None:
    """Remove a trip that was already confirmed to exist."""
    db.delete(trip)
    db.commit()


def _validate_date_range(start_date: date, end_date: date) -> None:
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="end_date must not be earlier than start_date",
        )
