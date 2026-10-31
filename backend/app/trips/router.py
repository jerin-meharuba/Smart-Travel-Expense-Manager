"""FastAPI routes for the Trip CRUD feature."""

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.trips.schemas import TripCreate, TripListResponse, TripRead, TripUpdate
from app.trips import service


router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("", response_model=TripRead, status_code=status.HTTP_201_CREATED)
def create_trip(trip_data: TripCreate, db: Session = Depends(get_db)) -> TripRead:
    return service.create_trip(db, trip_data)


@router.get("", response_model=TripListResponse)
def read_trips(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> TripListResponse:
    trips, total = service.list_trips(db, offset, limit)
    return TripListResponse(items=trips, total=total, offset=offset, limit=limit)


@router.get("/{trip_id}", response_model=TripRead)
def read_trip(trip_id: int, db: Session = Depends(get_db)) -> TripRead:
    return service.get_trip_or_404(db, trip_id)


@router.patch("/{trip_id}", response_model=TripRead)
def patch_trip(trip_id: int, trip_data: TripUpdate, db: Session = Depends(get_db)) -> TripRead:
    trip = service.get_trip_or_404(db, trip_id)
    return service.update_trip(db, trip, trip_data)


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_trip(trip_id: int, db: Session = Depends(get_db)) -> Response:
    trip = service.get_trip_or_404(db, trip_id)
    service.delete_trip(db, trip)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
