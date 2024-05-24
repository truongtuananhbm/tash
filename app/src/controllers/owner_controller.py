"""Define user controller."""
from typing import List, Tuple, Union

from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.src.models import Owner
from app.src.schemas.response import ResponseObject
from app.src.schemas.owner import OwnerCreate, OwnerUpdate
from app.src.services.owner_service import OwnerService
from app.src.utils.common import row2dict
from app.src.utils.connection.sql_connection import get_db_session


owner_service = OwnerService()

owners_routers = APIRouter()


@owners_routers.put("/owners/{owner_id}")
def update_owner(owner_id: str, owner_update: OwnerUpdate, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Update an existing owner system."""
    data = owner_service.update_owner(db_session, owner_id, owner_update)
    return ResponseObject(data=row2dict(data), code="BE0000")


@owners_routers.patch("/owners")
def search_owners(owner_filters:OwnerUpdate, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get owners."""
    data = owner_service.search_owners(db_session, filters=owner_filters)
    return ResponseObject(data=[row2dict(owner) for owner in data], code="BE0000")


@owners_routers.get("/owners/{owner_id}")
def read_owner_by_id(owner_id: str, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get owner by id."""
    data = owner_service.get_owner_by_id(db_session, owner_id)
    return ResponseObject(data=row2dict(data), code="BE0000")


@owners_routers.post("/owners")
def create_owner(owner_create: OwnerCreate, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Define create a owner."""
    data = owner_service.create_owner(db_session, owner_create)
    return ResponseObject(data=row2dict(data), code="BE0000")



@owners_routers.delete('/owners/{owner_id}}')
def delete_owner(owner_id: str, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Delete a owner."""
    owner_service.delete_owner(db_session, owner_id)
    return ResponseObject(code="BE0000")

@owners_routers.patch("/download/owners")
def generate_excel(filters: OwnerUpdate , db_session: Session = Depends(get_db_session)):
    """doc,"""
    excel_data, filename = owner_service.generate_excel(db_session, filters)  
    return Response(content=excel_data, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename={filename}"})