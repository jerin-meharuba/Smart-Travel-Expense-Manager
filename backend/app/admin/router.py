"""FastAPI routes for administrator-only user management."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.admin import service
from app.admin.schemas import AdminUserCreate, AdminUserRead, AdminUserUpdate
from app.auth.dependencies import require_admin
from app.auth.models import User
from app.database import get_db


router = APIRouter(prefix="/admin/users", tags=["administrator"])
AdminUser = Annotated[User, Depends(require_admin)]


@router.get("", response_model=list[AdminUserRead])
def read_users(_: AdminUser, db: Session = Depends(get_db)) -> list[AdminUserRead]:
    return service.list_users(db)


@router.post("", response_model=AdminUserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: AdminUserCreate,
    _: AdminUser,
    db: Session = Depends(get_db),
) -> AdminUserRead:
    return service.create_user(db, user_data)


@router.patch("/{user_id}", response_model=AdminUserRead)
def patch_user(
    user_id: int,
    user_data: AdminUserUpdate,
    admin: AdminUser,
    db: Session = Depends(get_db),
) -> AdminUserRead:
    target = service.get_user_or_404(db, user_id)
    return service.update_user(db, target, user_data, admin)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int, admin: AdminUser, db: Session = Depends(get_db)) -> Response:
    target = service.get_user_or_404(db, user_id)
    service.delete_user(db, target, admin)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
