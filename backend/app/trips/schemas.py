"""Pydantic request and response schemas for the Trip API."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class TripFields(BaseModel):
    """Fields shared by trip creation and responses."""

    name: str = Field(min_length=1, max_length=120)
    destination: str = Field(min_length=1, max_length=160)
    start_date: date
    end_date: date
    status: str = Field(default="planned", min_length=1, max_length=30)
    budget_amount: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    budget_currency: str | None = Field(default=None, min_length=3, max_length=3)

    @field_validator("name", "destination", "status")
    @classmethod
    def trim_required_text(cls, value: str) -> str:
        """Reject values that contain only whitespace."""
        trimmed_value = value.strip()
        if not trimmed_value:
            raise ValueError("must not be blank")
        return trimmed_value

    @field_validator("budget_currency")
    @classmethod
    def normalize_currency(cls, value: str | None) -> str | None:
        return value.upper() if value else value

    @model_validator(mode="after")
    def validate_date_range(self) -> "TripFields":
        if self.end_date < self.start_date:
            raise ValueError("end_date must not be earlier than start_date")
        return self

    @model_validator(mode="after")
    def validate_budget_currency(self) -> "TripFields":
        if self.budget_amount is not None and self.budget_currency is None:
            raise ValueError("budget_currency is required when budget_amount is set")
        return self


class TripCreate(TripFields):
    """Request body used to create a trip."""


class TripUpdate(BaseModel):
    """Optional fields accepted by PATCH requests."""

    name: str | None = Field(default=None, min_length=1, max_length=120)
    destination: str | None = Field(default=None, min_length=1, max_length=160)
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = Field(default=None, min_length=1, max_length=30)
    budget_amount: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    budget_currency: str | None = Field(default=None, min_length=3, max_length=3)

    @field_validator("name", "destination", "status")
    @classmethod
    def trim_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        trimmed_value = value.strip()
        if not trimmed_value:
            raise ValueError("must not be blank")
        return trimmed_value

    @field_validator("budget_currency")
    @classmethod
    def normalize_optional_currency(cls, value: str | None) -> str | None:
        return value.upper() if value else value


class TripRead(TripFields):
    """Trip data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class TripListResponse(BaseModel):
    """Paginated response returned by the trip list endpoint."""

    items: list[TripRead]
    total: int
    offset: int
    limit: int
