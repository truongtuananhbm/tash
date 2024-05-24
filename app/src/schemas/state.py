"""Define state schema file."""
from pydantic import BaseModel


class StateCreate(BaseModel):
    """Define State input schema to create State."""

    name: str


class StateUpdate(StateCreate):
    """Define State input schema to update state."""
