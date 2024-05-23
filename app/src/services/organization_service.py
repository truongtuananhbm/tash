"""Define permission file."""
import uuid
from typing import Any, Dict

from sqlalchemy.orm import Session

from app.src import models
from app.src.exceptions.error_code import AuthErrorCode, BEErrorCode
from app.src.repositories.blacklist_token import BlackListTokenRepository
from app.src.schemas.organization import OrganizationCreate, OrganizationUpdate


class OrganizationService(object):
    """Define Organization service object."""

    def __init__(self) -> None:
        """Define constructor for Organization service object."""
        self.blacklist_token_repository = BlackListTokenRepository(
            models.BlacklistToken,
        )

    def delete_organization(self, db_session: Session, organization_id: uuid.UUID, user_system) -> None:
        """Define remove organization method."""
        permissions = user_system.permissions
        kt = 0
        for permission in permissions:
            if permission.name in ["AllAccess", "Organization:Delete", "Organization:AllAccess"]:
                kt = 1
                organization = self.get_organization_by_id(db_session, organization_id, user_system)
                if not organization:
                    raise AuthErrorCode.ORGANIZATION_NOT_FOUND.value
                self.organization_repository.delete(db_session, obj_id=organization.id)
        if kt == 0:
            raise BEErrorCode.USER_NOT_PERMISSION.value


    def get_all_organization(self, db_session: Session, user_system) -> Dict[str, Any]:
        """Retrieve all organizations."""
        permissions = user_system.permissions
        kt = 0
        for permission in permissions:
            if permission.name in ["AllAccess", "Organization:Read", "Organization:AllAccess"]:
                kt = 1
                organizations = self.organization_repository.get_all(db_session)
                if not organizations:
                    raise AuthErrorCode.ORGANIZATION_NOT_FOUND.value
                data = {}
                for organization in organizations:
                    data[str(organization.id)] = organization.__dict__
                return data
        if kt == 0:
            raise BEErrorCode.USER_NOT_PERMISSION.value
