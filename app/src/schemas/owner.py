"""Define owner schema file."""
from pydantic import BaseModel
from sqlalchemy import UUID
from typing import Any, Optional
from fastapi import Form

def as_form(cls):
    """Define as-form."""
    cls.__signature__ = cls.__signature__.replace(
        parameters=[arg.replace(default=Form(...)) if arg.annotation == str else arg.replace(default=Form(None))
                    for arg in cls.__signature__.parameters.values()],
    )
    return cls

@as_form
class OwnerBase(BaseModel):
    """Schema define login data."""

    name: str
    address: str
    garbageMass: int
    price: int
    neighbourhood_id: Optional[str]  
    group_id: Optional[str]
    state_id: Optional[str]
    force_id: Optional[str]

@as_form
class OwnerCreate(OwnerBase):
    """Define User input schema to create user."""


@as_form
class OwnerUpdate(OwnerBase):
    """Define User input schema to update user."""
