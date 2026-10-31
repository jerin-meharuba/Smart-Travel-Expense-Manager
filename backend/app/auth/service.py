"""Database operations for user registration and login."""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.schemas import UserRegister
from app.auth.security import hash_password, verify_password


def create_user(db: Session, registration: UserRegister) -> User:
    """Create a user unless the normalized email is already registered."""
    existing_user = db.scalar(select(User).where(User.email == registration.email))
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

    user = User(email=registration.email, password_hash=hash_password(registration.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    """Return the user only when the submitted credentials are valid."""
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return user
