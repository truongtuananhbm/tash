"""Define user organization schema file."""
from typing import Optional

from pydantic import BaseModel


class UserOrganizationLogin(BaseModel):
    """Schema define login data."""

    email: str
    password: str


class UserOrganizationCreate(UserOrganizationLogin):
    """Define User input schema to create user."""

    group_id: Optional[str] = None
    organization_id: str


class UserOrganizationUpdate(BaseModel):
    """Define User input schema to update user."""

    password: str
    group_id: Optional[str] = None
