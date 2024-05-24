"""Define user service file."""
import uuid
from typing import Any, Dict, List, Union

import decouple
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.src import models
from app.src.exceptions.error_code import AuthErrorCode, BEErrorCode
from app.src.models import User
from app.src.repositories.blacklist_token import BlackListTokenRepository
from app.src.repositories.user import UserSystemRepository
from app.src.schemas.session import TokenPayload
from app.src.schemas.user_organization import UserOrganizationCreate, UserOrganizationUpdate
from app.src.schemas.user_system import UserSystemCreate, UserSystemUpdate
from app.src.utils.connection.sql_connection import get_db_session
from app.src.utils.security import get_password_hash, jwt_decode_token, verify_password

ACCESS_TOKEN_EXPIRE_MINUTES = decouple.config("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = decouple.config("REFRESH_TOKEN_EXPIRE_MINUTES")

reusable_oauth2 = HTTPBearer(scheme_name="Authorization")


class UserService(object):
    """Define User service object."""

    def __init__(self) -> None:
        """Define constructor for User service object."""
        self.user_system_repository = UserSystemRepository(models.User)
        self.blacklist_token_repository = BlackListTokenRepository(
            models.BlacklistToken,
        )

    def get_user_system_by_access_token(self, db_session: Session, token: str) -> Union[models.User]:
        """Define get user system by access token."""
        if self.blacklist_token_repository.is_black_token(db_session, token):
            raise AuthErrorCode.BLACKLIST_TOKEN.value

        payload = jwt_decode_token(token)
        token_data = TokenPayload(**payload)

        user_system = self.user_system_repository.get_user_system_by_email(db_session, token_data.sub)
        if user_system:
            return user_system

        user_organization = self.user_organization_repository.get_user_organization_by_email(db_session, token_data.sub)
        if user_organization:
            return user_organization

    def get_current_user_system(
            self,
            db_session: Session = Depends(get_db_session),
            credentials: HTTPAuthorizationCredentials = Depends(reusable_oauth2),
    ) -> Union[tuple[User, str]]:
        """Define get current user system method."""
        user = self.get_user_system_by_access_token(db_session, credentials.credentials)
        return user, credentials.credentials

    def authenticate_system(
            self,
            db_session: Session,
            email: str,
            password: str,
    ) -> models.User:
        """Define authenticate method."""
        user = self.user_system_repository.get_user_system_by_email(db_session, email)
        if not user:
            raise AuthErrorCode.USERNAME_NOT_FOUND.value
        if not verify_password(password, str(user.password)):
            raise AuthErrorCode.INCORRECT_PASSWORD.value
        return user


    def get_user_system_by_id(self, db_session: Session, user_system_id: uuid.UUID, user_system) -> models.User:
        """Define get user system method."""
        permissions = user_system.permissions
        kt = 0
        for permission in permissions:
            if permission.name in ["AllAccess", "UserSystem:Read", "UserSystem:AllAccess"]:
                kt = 1
                user_system = self.user_system_repository.get(db_session, obj_id=user_system_id)
                data = {}
                if not user_system:
                    raise AuthErrorCode.USERNAME_NOT_FOUND.value
                permissions_data = [p.__dict__ for p in user_system.permissions]
                user_data = {key: value for key, value in user_system.__dict__.items()
                             if (key != 'password') and (key != 'is_deleted')}
                user_data['permissions'] = permissions_data
                data[str(user_system.id)] = user_data
                return data
        if kt == 0:
            raise BEErrorCode.USER_NOT_PERMISSION.value

    def create_user_system(self, db_session: Session, user_system_create: UserSystemCreate,
                           user_system) -> models.User:
        """Define create user system method."""
        permissions = user_system.permissions
        kt = 0
        for permission in permissions:
            if permission.name in ["AllAccess", "UserSystem:Create", "UserSystem:AllAccess"]:
                kt = 1
                if self.user_system_repository.get_user_system_by_email(db_session, user_system_create.email):
                    raise AuthErrorCode.USER_EXISTED.value
                user_system_create.password = get_password_hash(user_system_create.password).decode("utf-8")
                user = self.user_system_repository.create(db_session, obj_in=user_system_create)
                return user
        if kt == 0:
            raise BEErrorCode.USER_NOT_PERMISSION.value


    def delete_user_system(self, db_session: Session, user_system_id: uuid.UUID, user_system) -> None:
        """Define remove user system method."""
        permissions = user_system.permissions
        kt = 0
        for permission in permissions:
            if permission.name in ["AllAccess", "UserSystem:Delete", "UserSystem:AllAccess"]:
                kt = 1
                user = self.get_user_system_by_id(db_session, user_system_id, user_system)
                if not user:
                    raise AuthErrorCode.USERNAME_NOT_FOUND.value
                self.user_system_repository.delete(db_session, obj_id=user.id)
        if kt == 0:
            raise BEErrorCode.USER_NOT_PERMISSION.value

    def delete_user_organization(self, db_session: Session, user_organization_id: uuid.UUID, user_organization) -> None:
        """Define remove user organization method."""
        permissions = user_organization.permissions
        kt = 0
        for permission in permissions:
            if permission.name in ["AllAccess", "UserOrganization:Delete", "UserOrganization:AllAccess"]:
                kt = 1
                user = self.get_user_organization_by_id(db_session, user_organization_id, user_organization)
                if not user:
                    raise AuthErrorCode.USERNAME_NOT_FOUND.value
                self.user_organization_repository.delete(db_session, obj_id=user_organization_id)
        if kt == 0:
            raise BEErrorCode.USER_NOT_PERMISSION.value

    def update_user_system(self, db_session: Session, user_system_id: uuid.UUID, user_system_update: UserSystemUpdate,
                           user_system) -> models.User:
        """Update an existing user system."""
        permissions = user_system.permissions
        kt = 0
        for permission in permissions:
            if permission.name in ["AllAccess", "UserSystem:Update", "UserSystem:AllAccess"]:
                kt = 1
                if self.get_user_system_by_id(db_session, user_system_id, user_system) is None:
                    raise BEErrorCode.USER_NOT_FOUND.value
                user_system_update.password = get_password_hash(user_system_update.password).decode("utf-8")
                user = self.user_system_repository.update(db_session, obj_id=user_system_id, obj_in=user_system_update)
                user = self.user_system_repository.get(db_session, user_system_id)
                if not user:
                    raise BEErrorCode.USER_NOT_FOUND.value
                return user
        if kt == 0:
            raise BEErrorCode.USER_NOT_PERMISSION.value

    def get_all_user_system(self, db_session: Session, user_system) -> Dict[str, Any]:
        """Retrieve all user systems."""
        permissions = user_system.permissions
        kt = 0
        for permission in permissions:
            if permission.name in ["AllAccess", "UserSystem:Read", "UserSystem:AllAccess"]:
                kt = 1
                users = self.user_system_repository.get_all(db_session)
                if not users:
                    raise BEErrorCode.USER_NOT_FOUND.value
                data = {}
                for user in users:
                    permissions_data = [p.__dict__ for p in user.permissions]
                    user_data = {key: value for key, value in user.__dict__.items()
                                 if (key != 'password') and (key != 'is_deleted')}
                    user_data['permissions'] = permissions_data
                    data[str(user.id)] = user_data
                return data
        if kt == 0:
            raise BEErrorCode.USER_NOT_PERMISSION.value

    def get_all_user_organization(self, db_session: Session, user_organization) -> Dict[str, Any]:
        """Retrieve all user organizations."""
        permissions = user_organization.permissions
        kt = 0
        for permission in permissions:
            if permission.name in ["AllAccess", "UserOrganization:Read", "UserOrganization:AllAccess"]:
                kt = 1
                users = self.user_organization_repository.get_all(db_session)
                if not users:
                    raise BEErrorCode.USER_NOT_FOUND.value
                data = {}
                for user in users:
                    permissions_data = [p.__dict__ for p in user.permissions]
                    user_data = {key: value for key, value in user.__dict__.items()
                                 if (key != 'password') and (key != 'is_deleted')}
                    user_data['permissions'] = permissions_data
                    data[str(user.id)] = user_data
                return data
        if kt == 0:
            raise BEErrorCode.USER_NOT_PERMISSION.value
