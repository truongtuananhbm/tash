"""Define state controller."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.src.models import State
from app.src.schemas.response import ResponseObject
from app.src.schemas.state import StateCreate
from app.src.services.state_service import StateService
from app.src.utils.common import row2dict
from app.src.utils.connection.sql_connection import get_db_session

state_service = StateService()

states_routers = APIRouter()


@states_routers.patch("/states")
def get_states(db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get states."""
    data = state_service.get_states(db_session)
    return ResponseObject(data=[row2dict(state) for state in data], code="BE0000")


@states_routers.post("/states")
def create_state(state_create: StateCreate, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Define create a state."""
    data = state_service.create_state(db_session, state_create)
    return ResponseObject(data=row2dict(data), code="BE0000")


@states_routers.get("/states/{state_id}")
def read_state_by_id(state_id: str, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get state by id."""
    data = state_service.get_state_by_id(db_session, state_id)
    return ResponseObject(data=row2dict(data), code="BE0000")
