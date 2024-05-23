"""Define permission file."""
import uuid
from typing import Any, Dict

from sqlalchemy.orm import Session

from app.src import models
from app.src.exceptions.error_code import BEErrorCode
from app.src.schemas.permission import PermissionCreate, PermissionUpdate


class PermissionService(object):
    """Define Permission service object."""

    def __init__(self) -> None:
        """Define constructor for Permission service object."""


    def delete_permission(self, db_session: Session, permission_id: uuid.UUID, user_organization) -> None:
        """Define remove permission method."""
        permissions = user_organization.permissions
        kt = 0
        for permission in permissions:
            if permission.name in ["AllAccess", "Permission:Delete", "Permission:AllAccess"]:
                kt = 1
                permission = self.get_permission_by_id(db_session, permission_id, user_organization)
                if not permission:
                    raise BEErrorCode.PERMISSION_EXITED.value
                self.permission_repository.delete(db_session, obj_id=permission_id)
        if kt == 0:
            raise BEErrorCode.USER_NOT_PERMISSION.value
