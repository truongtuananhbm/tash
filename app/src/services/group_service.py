"""Define group service file."""
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.src import models
from app.src.exceptions.error_code import BEErrorCode
from app.src.models import Group
from app.src.repositories.group import GroupRepository
from app.src.schemas.group import GroupCreate

class GroupService(object):
    """Define Group Service object."""

    def __init__(self) -> None:
        """Define constructor for Group service object."""
        self.group_repository = GroupRepository(models.Group)

    def get_group_by_id(self, db_session: Session, group_id: uuid.UUID) -> models.Group:
        """Define get group by id method."""
        group = self.group_repository.get(db_session, obj_id=group_id)
        if not group:
           raise BEErrorCode.GROUP_NOT_FOUND.value
        return group

    def get_groups(self, db_session: Session) -> List[models.Group]:
        """Define get groups method."""
        groups = self.group_repository.get_all(db_session)
        if not groups:
           raise BEErrorCode.GROUP_NOT_FOUND.value
        return groups

    def create_group(self, db_session: Session, group_create: GroupCreate) -> models.Group:
        """Define create group method."""
        group = self.group_repository.create(db_session, obj_in=group_create)
        return group
