"""Define force schema file."""
from pydantic import BaseModel
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
class ForceBase(BaseModel):
    """Schema define force base."""

    name: str
    unit: str
    numberBarrel: int
    typeBarrel_id: Optional[str]  
    position_id: Optional[str]
    worker: Optional[int]

@as_form
class ForceCreate(ForceBase):
    """Define input schema to create force."""


@as_form
class ForceUpdate(ForceBase):
    """Definei nput schema to update force."""
