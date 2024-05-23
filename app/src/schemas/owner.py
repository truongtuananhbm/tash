"""Define owner schema file."""
from pydantic import BaseModel



class OwnerBase(BaseModel):
    """Schema define login data."""

    name: str
    address: str
    garbageMass: int
    neighbourhood_id: str
    group_id: str
    state_id: str
    force_id: str


class OwnerCreate(OwnerBase):
    """Define User input schema to create user."""


class OwnerUpdate(OwnerBase):
    """Define User input schema to update user."""

    password: str
