"""Define neighbourhood controller."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.src.models import Neighbourhood
from app.src.schemas.response import ResponseObject
from app.src.schemas.neighbourhood import NeighbourhoodCreate
from app.src.services.neighbourhood_service import NeighbourhoodService
from app.src.utils.common import row2dict
from app.src.utils.connection.sql_connection import get_db_session


neighbourhood_service = NeighbourhoodService()

neighbourhoods_routers = APIRouter()


@neighbourhoods_routers.patch("/neighbourhoods")
def get_neighbourhoods(db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get neighbourhoods."""
    data = neighbourhood_service.get_neighbourhoods(db_session)
    return ResponseObject(data=[row2dict(neighbourhood) for neighbourhood in data], code="BE0000")


@neighbourhoods_routers.post("/neighbourhoods")
def create_neighbourhood(neighbourhood_create: NeighbourhoodCreate, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Define create a neighbourhood."""
    data = neighbourhood_service.create_neighbourhood(db_session, neighbourhood_create)
    return ResponseObject(data=row2dict(data), code="BE0000")


@neighbourhoods_routers.get("/neighbourhoods/{neighbourhood_id}")
def read_neighbourhood_by_id(neighbourhood_id: str, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Get neighbourhood by id."""
    data = neighbourhood_service.get_neighbourhood_by_id(db_session, neighbourhood_id)
    return ResponseObject(data=row2dict(data), code="BE0000")
