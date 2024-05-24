"""Define postion schema file."""
from pydantic import BaseModel


class PositionCreate(BaseModel):
    """Define Position input schema to create State."""

    name: str


class PositionUpdate(PositionCreate):
    """Define Position input schema to update state."""
