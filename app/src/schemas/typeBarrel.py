"""Define type barrel schema file."""
from pydantic import BaseModel


class TypeBarrelCreate(BaseModel):
    """Define Type Barrel input schema to create State."""

    name: str


class TypeBarrelUpdate(TypeBarrelCreate):
    """Define Type Barrel input schema to update state."""
