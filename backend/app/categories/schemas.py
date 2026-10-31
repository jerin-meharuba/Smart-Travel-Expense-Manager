"""Response schema for fixed expense categories."""

from pydantic import BaseModel, ConfigDict


class CategoryRead(BaseModel):
    """Category data exposed to the frontend."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
