"""Define group schema file."""
from pydantic import BaseModel


class GroupCreate(BaseModel):
    """Define Group input schema to create organization."""

    name: str


class GroupUpdate(GroupCreate):
    """Define Group input schema to update organization."""
