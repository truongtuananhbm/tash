"""Define Resource Tag service file."""
import uuid
from typing import Any, Dict

import decouple
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.src import models
from app.src.exceptions.error_code import BEErrorCode
from app.src.repositories.resource_tag import ResourceTagRepository
from app.src.schemas.resource_tag import ResourceTagCreate, ResourceTagUpdate  # noqa

ACCESS_TOKEN_EXPIRE_MINUTES = decouple.config("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = decouple.config("REFRESH_TOKEN_EXPIRE_MINUTES")

reusable_oauth2 = HTTPBearer(scheme_name='Authorization')


class ResourceTagService(object):
    """Define Resource Tag service object."""

    def __init__(self) -> None:
        """Define constructor for Resource Tag service object."""
        self.resource_tag_repository = ResourceTagRepository(models.ResourceTag)

    def get(self, db_session: Session, resource_tag_id: uuid.UUID) -> models.ResourceTag:
        """Define remove Resource Tag method."""
        resource_tag = self.resource_tag_repository.get(db_session, resource_tag_id)
        if not resource_tag:
            raise BEErrorCode.RESOURCE_TAG_NOT_FOUND.value
        return resource_tag

    def delete(self, db_session: Session, resource_tag_id: uuid.UUID) -> None:
        """Define remove resource tag method."""
        resource_tag = self.resource_tag_repository.get(db_session, resource_tag_id)
        if not resource_tag:
            raise BEErrorCode.RESOURCE_TAG_NOT_FOUND.value
        self.resource_tag_repository.delete(db_session, obj_id=resource_tag.id)

    def get_all(self, db_session: Session) -> Dict[str, Any]:
        """Retrieve all resource tags."""
        resource_tags = self.resource_tag_repository.get_all(db_session)
        if not resource_tags:
            raise BEErrorCode.RESOURCE_TAG_NOT_FOUND.value
        data = {}
        for resource_tag in resource_tags:
            data[str(resource_tag.id)] = resource_tag.__dict__
        return data

    def update(self, db_session: Session, resource_tag_id: int, resource_tag_update: ResourceTagUpdate) \
            -> models.ResourceTag:
        """Update an existing resource tag."""
        if self.resource_tag_repository.get(db_session, resource_tag_id) is None:
            raise BEErrorCode.RESOURCE_TAG_NOT_FOUND.value
        _ = self.resource_tag_repository.update(db_session, obj_id=resource_tag_id, obj_in=resource_tag_update)
        resource_tag = self.resource_tag_repository.get(db_session, resource_tag_id)
        if not resource_tag:
            raise BEErrorCode.RESOURCE_TAG_NOT_FOUND.value
        return resource_tag

    def create(self, db_session: Session, resource_tag_create: ResourceTagCreate) -> models.resource_tag:
        """Create a new resource tag."""
        resource_tag = self.resource_tag_repository.create(db_session, obj_in=resource_tag_create)
        return resource_tag
