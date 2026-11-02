"""Request and response schemas for administrator user management."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.auth.schemas import UserRead


class AdminUserCreate(BaseModel):
    """User details an administrator may create."""

    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    role: Literal["user", "admin"] = "user"

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return _normalize_email(value)


class AdminUserUpdate(BaseModel):
    """Optional user details an administrator may change for another user."""

    email: str | None = Field(default=None, min_length=5, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    role: Literal["user", "admin"] | None = None

    @field_validator("email")
    @classmethod
    def normalize_optional_email(cls, value: str | None) -> str | None:
        return _normalize_email(value) if value is not None else None


AdminUserRead = UserRead


def _normalize_email(value: str) -> str:
    email = value.strip().lower()
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        raise ValueError("email must be valid")
    return email
