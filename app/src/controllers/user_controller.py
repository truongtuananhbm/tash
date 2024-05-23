"""Define user controller."""
from typing import List, Tuple, Union

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.src.models import User
from app.src.schemas.response import ResponseObject
from app.src.schemas.user_organization import UserOrganizationCreate, UserOrganizationUpdate
from app.src.schemas.user_system import UserSystemCreate, UserSystemUpdate
from app.src.services.user_service import UserService
from app.src.utils.common import row2dict
from app.src.utils.connection.sql_connection import get_db_session

reusable_oauth2 = HTTPBearer(scheme_name="Authorization")

user_service = UserService()

users_routers = APIRouter()


@users_routers.put("/user_systems/{user_system_id}")
def update_user_system(user_system_id: str, user_system_update: UserSystemUpdate, db_session: Session = Depends(get_db_session), # noqa
                       user_system: Tuple[User, str] = Depends(user_service.get_current_user_system)) -> ResponseObject: # noqa
    """Update an existing user system."""
    data = user_service.update_user_system(db_session, user_system_id, user_system_update, user_system[0])
    return ResponseObject(data=data.to_dict(), code="BE0000")



@users_routers.get("/user-systems")
def read_user_systems(db_session: Session = Depends(get_db_session), # noqa
                      user_system: Tuple[User, str] = Depends(user_service.get_current_user_system)) -> ResponseObject: # noqa
    """Get all user."""
    data = user_service.get_all_user_system(db_session, user_system[0])
    return ResponseObject(data=data, code="BE0000")


@users_routers.get("/user-systems/{user_system_id}")
def read_user_system_by_id(user_system_id: str, db_session: Session = Depends(get_db_session),
                           user_system: Tuple[User, str] = Depends(user_service.get_current_user_system)) -> ResponseObject: # noqa
    """Get user by id."""
    data = user_service.get_user_system_by_id(db_session, user_system_id, user_system[0])
    return ResponseObject(data=data, code="BE0000")



@users_routers.post("/user-systems")
def create_user_system(user_create: UserSystemCreate, db_session: Session = Depends(get_db_session),
                       user_system: Tuple[User, str] = Depends(user_service.get_current_user_system)) -> ResponseObject: # noqa
    """Define create a user system."""
    data = user_service.create_user_system(db_session, user_create, user_system[0])
    return ResponseObject(data=row2dict(data), code="BE0000")
