"""Define force service file."""
import uuid
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app.src import models
from app.src.exceptions.error_code import BEErrorCode
from app.src.models import Force
from app.src.repositories.force import ForceRepository
from app.src.schemas.force import ForceCreate, ForceUpdate

class ForceService(object):
    """Define Force service object."""

    def __init__(self) -> None:
        """Define constructor for Force service object."""
        self.force_repository = ForceRepository(models.Force)

    def get_force_by_id(self, db_session: Session, force_id: uuid.UUID) -> models.Force:
        """Define get force by id method."""
        force = self.force_repository.get(db_session, obj_id=force_id)
        owners_data = []
        for owner in force.force:
           owner_data = {'name': owner.name}
           owners_data.append(owner_data)
        force_data = {key: value for key, value in force.__dict__.items() if key != '_sa_instance_state'}
        force_data['owner'] = owners_data
        if not force:
           raise BEErrorCode.FORCE_NOT_FOUND.value
        return force_data

    def create_force(self, db_session: Session, force_create:ForceCreate) -> models.Force:
        """Define create force method."""
        if force_create.unit == 'string':
            force_create.unit = None
        if force_create.numberBarrel == 0:
            force_create.numberBarrel = 0
        if force_create.typeBarrel_id == 'string':
            force_create.typeBarrel_id = None
        if force_create.position_id == 'string':
             force_create.position_id = None
        if force_create.worker == 0:
             force_create.worker = 0
        force = self.force_repository.create(db_session, obj_in=force_create)
        return force

    def delete_force(self, db_session: Session, force_id: uuid.UUID) -> None:
        """Define remove force method."""
        force = self.force_repository.get(db_session, obj_id=force_id)
        if not force:
            raise BEErrorCode.FORCE_NOT_FOUND.value
        self.force_repository.delete(db_session, obj_id=force.id)

    def update_force(self, db_session: Session, force_id: uuid.UUID, force_update: ForceCreate) -> models.Force:
        """Update an existing force."""
        force = self.force_repository.get(db_session, obj_id=force_id)
        if self.force_repository.get(db_session, obj_id=force_id) is None:
            raise BEErrorCode.FORCE_NOT_FOUND.value
        if force_update.name == 'string':
            force_update.name = force.name
        if force_update.unit == 'string':
            force_update.unit = force.unit
        if force_update.numberBarrel==0:
            force_update.numberBarrel =  force.numberBarrel
        if force_update.typeBarrel_id == 'string':
            force_update.typeBarrel_id = force.typeBarrel_id
        if force_update.position_id == 'string':
            force_update.position_id = force.position_id
        if force_update.worker == 0:
            force_update.worker = force.worker
        force = self.force_repository.update(db_session, obj_id=force_id, obj_in=force_update)
        force = self.force_repository.get(db_session, force_id)
        if not force:
            raise BEErrorCode.FORCE_NOT_FOUND.value
        return force
    
    def search_forces(self, db_session: Session, filters: ForceUpdate) -> List[models.Force]:
        """Define method to search force based on filters."""
        forces = self.force_repository.search_forces(db_session, filters)
        if not forces:
            raise BEErrorCode.FORCE_NOT_FOUND.value
        forces_data = []
        for force in forces:
            owners_data = []
            for owner in force.force:
                owner_data = {'name': owner.name}
                owners_data.append(owner_data)
            force_data = {key: value for key, value in force.__dict__.items() if key != '_sa_instance_state'}
            force_data['owner'] = owners_data
            forces_data.append(force_data)
        return forces_data
    