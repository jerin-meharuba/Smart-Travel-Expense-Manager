"""Registration, login, logout, and profile API routes."""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.auth.dependencies import CurrentUser
from app.auth.schemas import TokenResponse, UserLogin, UserRead, UserRegister
from app.auth import service
from app.auth.security import create_access_token
from app.database import get_db


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(registration: UserRegister, db: Session = Depends(get_db)) -> UserRead:
    return service.create_user(db, registration)


@router.post("/login", response_model=TokenResponse)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    user = service.authenticate_user(db, credentials.email, credentials.password)
    return TokenResponse(access_token=create_access_token(user.id), user=user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(_: CurrentUser) -> Response:
    """JWT logout is completed client-side by discarding the stored token."""
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: CurrentUser) -> UserRead:
    return current_user
