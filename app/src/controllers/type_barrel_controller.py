"""Define type barrel controller."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.src.models import TypeBarrel
from app.src.schemas.response import ResponseObject
from app.src.schemas.typeBarrel import TypeBarrelCreate
from app.src.services.type_barrel_service import TypeBarrelService
from app.src.utils.common import row2dict
from app.src.utils.connection.sql_connection import get_db_session

type_barrel_service = TypeBarrelService()

type_barrels_routers = APIRouter()


@type_barrels_routers.patch("/type_barrels")
def get_type_barrels(db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get type barrels."""
    data = type_barrel_service.get_type_barrels(db_session)
    return ResponseObject(data=[row2dict(state) for state in data], code="BE0000")


@type_barrels_routers.post("/type_barrels")
def create_type_barrel(type_barrel_create: TypeBarrelCreate, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Define create a type barrel."""
    data = type_barrel_service.create_type_barrel(db_session, type_barrel_create)
    return ResponseObject(data=row2dict(data), code="BE0000")


@type_barrels_routers.get("/type_barrels/{type_barrel_id}")
def read_type_barrel_by_id(type_barrel_id: str, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get type barrel by id."""
    data = type_barrel_service.get_type_barrel_by_id(db_session, type_barrel_id)
    return ResponseObject(data=row2dict(data), code="BE0000")
