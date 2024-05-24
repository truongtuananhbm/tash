"""Define state service file."""
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.src import models
from app.src.exceptions.error_code import BEErrorCode
from app.src.models import State
from app.src.repositories.state import StateRepository
from app.src.schemas.state import StateCreate

class StateService(object):
    """Define State Service object."""

    def __init__(self) -> None:
        """Define constructor for State service object."""
        self.state_repository = StateRepository(models.State)
    
    def get_state_by_id(self, db_session: Session, state_id: uuid.UUID) -> models.State:
        """Define get state by id method."""
        state = self.state_repository.get(db_session, obj_id=state_id)
        if not state:
           raise BEErrorCode.STATE_NOT_FOUND.value
        return state
    
    def get_states(self, db_session: Session) -> List[models.State]:
        """Define get states method."""
        states = self.state_repository.get_all(db_session)
        if not states:
           raise BEErrorCode.STATE_NOT_FOUND.value
        return states

    def create_state(self, db_session: Session, state_create: StateCreate) -> models.State:
        """Define create state method."""
        state = self.state_repository.create(db_session, obj_in=state_create)
        return state
