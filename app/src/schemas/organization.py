"""Define organization schema file."""
from pydantic import BaseModel


class OrganizationCreate(BaseModel):
    """Define Organization input schema to create organization."""

    name: str


class OrganizationUpdate(OrganizationCreate):
    """Define Organization input schema to update organization."""
