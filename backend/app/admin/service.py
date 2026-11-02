"""Database operations and safety rules for administrator user management."""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.admin.schemas import AdminUserCreate, AdminUserUpdate
from app.auth.models import User
from app.auth.security import hash_password


def list_users(db: Session) -> list[User]:
    """Return safe user records in a stable order for administrator review."""
    return db.scalars(select(User).order_by(User.created_at.desc(), User.id.desc())).all()


def create_user(db: Session, user_data: AdminUserCreate) -> User:
    """Create a user with an administrator-selected role."""
    _ensure_email_is_available(db, user_data.email)
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=user_data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_or_404(db: Session, user_id: int) -> User:
    """Return a user for administration or report that it does not exist."""
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def update_user(db: Session, target: User, user_data: AdminUserUpdate, admin: User) -> User:
    """Update another user without allowing an admin to remove their own access."""
    _reject_self_management(target, admin)
    changes = user_data.model_dump(exclude_unset=True, exclude_none=True)
    if "email" in changes:
        _ensure_email_is_available(db, changes["email"], excluded_user_id=target.id)
        target.email = changes["email"]
    if "role" in changes:
        target.role = changes["role"]
    if "password" in changes:
        target.password_hash = hash_password(changes["password"])
    db.commit()
    db.refresh(target)
    return target


def delete_user(db: Session, target: User, admin: User) -> None:
    """Delete another user but never the current administrator."""
    _reject_self_management(target, admin)
    db.delete(target)
    db.commit()


def _ensure_email_is_available(db: Session, email: str, excluded_user_id: int | None = None) -> None:
    existing = db.scalar(select(User).where(User.email == email))
    if existing is not None and existing.id != excluded_user_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")


def _reject_self_management(target: User, admin: User) -> None:
    if target.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Administrators cannot manage their own account from this endpoint",
        )
