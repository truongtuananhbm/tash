"""Define neighbourhood schema file."""
from pydantic import BaseModel


class NeighbourhoodCreate(BaseModel):
    """Define Neighbourhood input schema to create organization."""

    name: str


class NeighbourhoodUpdate(NeighbourhoodCreate):
    """Define Neighbourhood input schema to update organization."""
