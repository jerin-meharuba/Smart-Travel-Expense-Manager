"""Pydantic schemas for authentication and user profile endpoints."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserRegister(BaseModel):
    """Registration request with a normalized email and password."""

    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        email = value.strip().lower()
        if "@" not in email or email.startswith("@") or email.endswith("@"):
            raise ValueError("email must be valid")
        return email


class UserLogin(UserRegister):
    """Login uses the same email and password validation as registration."""


class UserRead(BaseModel):
    """Safe user details returned to clients without password data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: str
    created_at: datetime


class TokenResponse(BaseModel):
    """JWT returned after a successful login."""

    access_token: str
    token_type: str = "bearer"
    user: UserRead
