"""Pydantic request and response schemas for budgets."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class BudgetTarget(BaseModel):
    """Optional target fields shared by budget writes."""

    trip_id: int | None = Field(default=None, gt=0)
    category_id: int | None = Field(default=None, gt=0)


class BudgetCreate(BudgetTarget):
    """Request body used to create a budget."""

    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return _normalize_currency(value)

    @model_validator(mode="after")
    def require_target(self) -> "BudgetCreate":
        if self.trip_id is None and self.category_id is None:
            raise ValueError("a budget must target a trip, a category, or both")
        return self


class BudgetUpdate(BudgetTarget):
    """Optional fields accepted by PATCH requests."""

    amount: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    currency: str | None = Field(default=None, min_length=3, max_length=3)

    @field_validator("currency")
    @classmethod
    def normalize_optional_currency(cls, value: str | None) -> str | None:
        return _normalize_currency(value) if value is not None else None


class BudgetRead(BaseModel):
    """Budget data together with spending calculated from matching expenses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    trip_id: int | None
    category_id: int | None
    amount: Decimal
    currency: str
    created_at: datetime
    updated_at: datetime
    actual_spending: Decimal
    remaining_amount: Decimal
    usage_percentage: Decimal
    is_overspent: bool


def _normalize_currency(value: str) -> str:
    code = value.strip().upper()
    if len(code) != 3 or not code.isalpha():
        raise ValueError("currency must be a three-letter code")
    return code
