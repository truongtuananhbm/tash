"""Define position service file."""
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.src import models
from app.src.exceptions.error_code import BEErrorCode
from app.src.models import Position
from app.src.repositories.position import PositionRepository
from app.src.schemas.position import PositionCreate

class PositionService(object):
    """Define Position Service object."""

    def __init__(self) -> None:
        """Define constructor for Position service object."""
        self.position_repository = PositionRepository(models.Position)
    
    def get_position_by_id(self, db_session: Session, state_id: uuid.UUID) -> models.Position:
        """Define get position by id method."""
        position = self.position_repository.get(db_session, obj_id=state_id)
        if not position:
           raise BEErrorCode.POSITION_NOT_FOUND.value
        return position
    
    def get_positions(self, db_session: Session) -> List[models.Position]:
        """Define get positions method."""
        positions = self.position_repository.get_all(db_session)
        if not positions:
           raise BEErrorCode.POSITION_NOT_FOUND.value
        return positions

    def create_position(self, db_session: Session, position_creat: PositionCreate) -> models.Position:
        """Define create position method."""
        position = self.position_repository.create(db_session, obj_in=position_creat)
        return position
