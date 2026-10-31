"""Pydantic request and response schemas for the Expense API."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ExpenseCreate(BaseModel):
    """Request body used to create an expense."""

    trip_id: int = Field(gt=0)
    category_id: int = Field(gt=0)
    amount_original: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency_original: str = Field(min_length=3, max_length=3)
    expense_date: date
    payment_method: str = Field(min_length=1, max_length=50)

    @field_validator("currency_original")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return _normalize_three_letter_code(value, "currency_original")

    @field_validator("payment_method")
    @classmethod
    def trim_payment_method(cls, value: str) -> str:
        return _trim_required_text(value, "payment_method")


class ExpenseUpdate(BaseModel):
    """Optional fields accepted by PATCH requests."""

    trip_id: int | None = Field(default=None, gt=0)
    category_id: int | None = Field(default=None, gt=0)
    amount_original: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    currency_original: str | None = Field(default=None, min_length=3, max_length=3)
    expense_date: date | None = None
    payment_method: str | None = Field(default=None, min_length=1, max_length=50)

    @field_validator("currency_original")
    @classmethod
    def normalize_optional_currency(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return _normalize_three_letter_code(value, "currency_original")

    @field_validator("payment_method")
    @classmethod
    def trim_optional_payment_method(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return _trim_required_text(value, "payment_method")


class ExpenseRead(BaseModel):
    """Expense data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    trip_id: int
    category_id: int
    amount_original: Decimal
    currency_original: str
    expense_date: date
    payment_method: str
    created_at: datetime
    updated_at: datetime


class ExpenseListResponse(BaseModel):
    """Paginated response returned by the expense list endpoint."""

    items: list[ExpenseRead]
    total: int
    offset: int
    limit: int


def _normalize_three_letter_code(value: str, field_name: str) -> str:
    code = value.strip().upper()
    if len(code) != 3 or not code.isalpha():
        raise ValueError(f"{field_name} must be a three-letter code")
    return code


def _trim_required_text(value: str, field_name: str) -> str:
    trimmed_value = value.strip()
    if not trimmed_value:
        raise ValueError(f"{field_name} must not be blank")
    return trimmed_value
