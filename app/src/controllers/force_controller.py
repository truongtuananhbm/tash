"""Define force controller."""
from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session
from app.src.models import Force
from app.src.schemas.response import ResponseObject
from app.src.schemas.force import ForceCreate, ForceUpdate
from app.src.services.force_service import ForceService
from app.src.utils.common import row2dict
from app.src.utils.connection.sql_connection import get_db_session


force_service = ForceService()
forces_routers = APIRouter()


@forces_routers.put("/forces/{force_id}")
def update_owner(force_id: str, force_update: ForceUpdate, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Update an existing force."""
    data = force_service.update_force(db_session, force_id, force_update)
    return ResponseObject(data=row2dict(data), code="BE0000")


@forces_routers.patch("/force")
def search_forces(force_filters: ForceUpdate, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get forces."""
    data = force_service.search_forces(db_session, filters=force_filters)
    return ResponseObject(data=data, code="BE0000")


@forces_routers.get("/forces/{force_id}")
def read_force_by_id(force_id: str, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get force by id."""
    data = force_service.get_force_by_id(db_session, force_id)
    return ResponseObject(data=data, code="BE0000")


@forces_routers.post("/forces")
def create_force(force_create: ForceCreate, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Define create a force."""
    data = force_service.create_force(db_session, force_create)
    return ResponseObject(data=row2dict(data), code="BE0000")



@forces_routers.delete('/forces/{force_id}}')
def delete_force(force_id: str, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Delete a force."""
    force_service.delete_force(db_session, force_id)
    return ResponseObject(code="BE0000")


@forces_routers.patch("/forces")
def get_forces(db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get forces."""
    data = force_service.get_forces(db_session)
    return ResponseObject(data=[row2dict(force) for force in data], code="BE0000")