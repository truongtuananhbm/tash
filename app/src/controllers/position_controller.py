"""Define position controller."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.src.models import Position
from app.src.schemas.response import ResponseObject
from app.src.schemas.position import PositionCreate
from app.src.services.position_service import PositionService
from app.src.utils.common import row2dict
from app.src.utils.connection.sql_connection import get_db_session

position_service = PositionService()

positions_routers = APIRouter()


@positions_routers.patch("/positions")
def get_positions(db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get positions."""
    data = position_service.get_positions(db_session)
    return ResponseObject(data=[row2dict(position) for position in data], code="BE0000")


@positions_routers.post("/positions")
def create_position(position_create: PositionCreate, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Define create a position."""
    data = position_service.create_position(db_session, position_create)
    return ResponseObject(data=row2dict(data), code="BE0000")


@positions_routers.get("/positions/{position_id}")
def read_position_by_id(position_id: str, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get position by id."""
    data = position_service.get_position_by_id(db_session, position_id)
    return ResponseObject(data=row2dict(data), code="BE0000")
