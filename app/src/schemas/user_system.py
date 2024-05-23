"""Define user system schema file."""
from pydantic import BaseModel


class UserSystemLogin(BaseModel):
    """Schema define login data."""

    email: str
    password: str


class UserSystemCreate(UserSystemLogin):
    """Define User input schema to create user."""


class UserSystemUpdate(BaseModel):
    """Define User input schema to update user."""

    password: str
