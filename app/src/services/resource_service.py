"""Define Resource service."""
import logging
import os
import tempfile
import uuid
from typing import List, Union

from fastapi import UploadFile
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.src import models
from app.src.exceptions.error_code import BEErrorCode
from app.src.models import UserOrganization
from app.src.repositories.resource import FileRepository
from app.src.repositories.user_system import UserSystemRepository
from app.src.schemas import ResourceCreate, ResourceInfoCreate, ResourceUpdate
from app.src.schemas.resource import ResourceGet
from app.src.services.base_service import BaseService
from app.src.services.user_service import UserService

reusable_oauth2 = HTTPBearer(scheme_name="Authorization")
user_service = UserService()


class ResourceService:
    """Define resource service."""

    def __init__(self):
        """Define init service."""
        self.base_service = BaseService()
        self.resource_info_mapping = {"ResourceStage": "stage_id", "ResourceStatus": "status_id",
                                      "ResourcePlatform": "platform_id", "ProductType": "product_type_id",
                                      "PackageRepository": "repo_id", "ResourceTag": "tag_id"}
        self.file_repository = FileRepository(models.Resource)
        self.user_repository = UserSystemRepository(models.UserOrganization)

    async def upload_resource(self, file_upload: UploadFile, resource_create: ResourceCreate, user):
        """Define upload resource service."""
        try:
            if user.role.name in ["Editer", "Admin"]:
                content = await file_upload.read()
                key = f"/images/{resource_create.version}_{file_upload.filename}"
                user_id = user.id
                resource_create_dict = resource_create.dict(exclude={'user_id', 'key'})
                resource_create_dict['user_id'] = user_id
                resource_create_dict['key'] = key
                self.base_service.engine_s3.put_object(key, content)
                self.check_info(resource_create)
                uploaded_file_metadata = self.base_service.engine_postgresql.create(models.Resource,
                                                                                    resource_create_dict)
                return uploaded_file_metadata
            else:
                raise BEErrorCode.USER_NOT_PERMISSION.value
        except Exception as e:
            logging.error(f"Lỗi khi tải lên tài nguyên: {str(e)}")
            raise

    def download_resource(self, db_session: Session, resource_id: str, user):
        """Define download_resource service."""
        resource = self.file_repository.get(db_session, resource_id)
        if resource.user_id == user.id:
            s3_key = self.base_service.engine_postgresql.get_single_data(models.Resource, resource_id).key
            content = self.base_service.engine_s3.get_object(s3_key)
            file_path = os.path.join(tempfile.gettempdir(), os.path.basename(s3_key))
            with open(file_path, "wb") as file:
                file.write(content)
            return file_path
        else:
            raise BEErrorCode.USER_NOT_PERMISSION.value

    def check_info(self, schema: Union[ResourceCreate, ResourceUpdate]) -> None:
        """Define check infor service."""
        for k, v in self.resource_info_mapping.items():
            info_obj = getattr(schema, v)
            if info_obj:  # noqa
                info_obj = self.base_service.engine_postgresql.get_by_attribute(getattr(models, k), "id", info_obj)
                if not info_obj:
                    _ = self.base_service.engine_postgresql.create(getattr(models, k),
                                                                   ResourceInfoCreate(name=info_obj))

    def get(self, db_session: Session, resource_id: uuid.UUID) -> models.Resource:
        """Define read Resource method."""
        resource = self.file_repository.get(db_session, resource_id)
        if not resource:
            raise BEErrorCode.RESOURCE_NOT_FOUND.value
        return resource

    def search_resources(self, db_session: Session, filters: ResourceGet,
                         user: UserOrganization) -> List[models.Resource]:
        """Define method to search resources based on filters."""
        if user.role.name == "Admin":
            resources = self.file_repository.search_resources(db_session, filters)
        elif user.role.name == "Editer":
            resources = self.file_repository.search_resources(db_session, filters, user_id=user.id)
        sorted_resource = sorted(resources, key=lambda x: x.created_at)
        if not resources:
            raise BEErrorCode.RESOURCE_NOT_FOUND.value
        return sorted_resource

    def update(self, db_session: Session, resource_id: int, resource_update: ResourceUpdate, user) -> models.Resource:
        """Update an existing resource."""
        resource = self.file_repository.get(db_session, resource_id)
        user_id = str(user.id)
        if resource.user_id == user_id:
            if self.file_repository.get(db_session, resource_id) is None:
                raise BEErrorCode.RESOURCE_NOT_FOUND.value
            update_data = {}
            for key, value in resource_update.dict().items():
                if value != 'string':
                    update_data[key] = value
            if update_data:
                _ = self.file_repository.update(db_session, obj_id=resource_id, obj_in=update_data)
        resource = self.file_repository.get(db_session, resource_id)
        if not resource:
            raise BEErrorCode.RESOURCE_NOT_FOUND.value
        return resource

    def delete(self, db_session: Session, resource_id: uuid.UUID) -> None:
        """Define remove resource method."""
        resource = self.file_repository.get(db_session, obj_id=resource_id)
        if not resource:
            raise BEErrorCode.RESOURCE_NOT_FOUND.value
        self.file_repository.delete(db_session, obj_id=resource.id)

    def back_up(self, db_session: Session, resource_id: uuid.UUID) -> None:
        """Define back up resource method."""
        resource = self.file_repository.get_back_up(db_session, obj_id=resource_id)
        if not resource:
            raise BEErrorCode.RESOURCE_NOT_FOUND.value
        self.file_repository.back_up(db_session, obj_id=resource.id)
