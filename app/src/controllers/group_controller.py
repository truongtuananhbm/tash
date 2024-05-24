"""Define group controller."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.src.models import Group
from app.src.schemas.response import ResponseObject
from app.src.schemas.group import GroupCreate
from app.src.services.group_service import GroupService
from app.src.utils.common import row2dict
from app.src.utils.connection.sql_connection import get_db_session

group_service = GroupService()

groups_routers = APIRouter()


@groups_routers.patch("/groups")
def get_groups(db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get groups."""
    data = group_service.get_groups(db_session)
    return ResponseObject(data=[row2dict(group) for group in data], code="BE0000")


@groups_routers.post("/groups")
def create_group(group_create: GroupCreate, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Define create a neighbourhood."""
    data = group_service.create_group(db_session, group_create)
    return ResponseObject(data=row2dict(data), code="BE0000")


@groups_routers.get("/groups/{group_id}")
def read_group_by_id(group_id: str, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get group by id."""
    data = group_service.get_group_by_id(db_session, group_id)
    return ResponseObject(data=row2dict(data), code="BE0000")
