"""Define neighbourhood service file."""
from typing import List
import uuid
from fastapi import Depends
from sqlalchemy.orm import Session
from app.src import models
from app.src.exceptions.error_code import BEErrorCode
from app.src.repositories.neighbourhood import NeighbourhoodRepository
from app.src.schemas.neighbourhood import NeighbourhoodCreate


class NeighbourhoodService(object):
    """Define Neighbourhood service object."""
 
    def __init__(self) -> None:
        """Define constructor for Neighbourhood service object."""
        self.neighbourhood_repository = NeighbourhoodRepository(models.Neighbourhood)

    def get_neighbourhood_by_id(self, db_session: Session, neighbourhood_id: uuid.UUID) -> models.Neighbourhood:
        """Define get neighbourhood by id method."""
        neighbourhood = self.neighbourhood_repository.get(db_session, obj_id=neighbourhood_id)
        if not neighbourhood:
           raise BEErrorCode.NEIGHBOURHOOD_NOT_FOUND.value
        return neighbourhood

    def get_neighbourhoods(self, db_session: Session) -> List[models.Owner]:
        """Define get owners method."""
        neighbourhoods = self.neighbourhood_repository.get_all(db_session)
        if not neighbourhoods:
           raise BEErrorCode.NEIGHBOURHOOD_NOT_FOUND.value
        return neighbourhoods

    def create_neighbourhood(self, db_session: Session, neighobourhood_create: NeighbourhoodCreate) -> models.Neighbourhood:
        """Define create neighbourhood method."""
        neighbourhood = self.neighbourhood_repository.create(db_session, obj_in=neighobourhood_create)
        return neighbourhood
