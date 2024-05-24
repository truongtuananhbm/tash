"""Define state service file."""
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.src import models
from app.src.exceptions.error_code import BEErrorCode
from app.src.models import TypeBarrel
from app.src.repositories.typeBarrel import TypeBarrelRepository
from app.src.schemas.typeBarrel import TypeBarrelCreate

class TypeBarrelService(object):
    """Define Type Barrel Service object."""

    def __init__(self) -> None:
        """Define constructor for Type Barrel service object."""
        self.type_barrel_repository = TypeBarrelRepository(models.TypeBarrel)
    
    def get_type_barrel_by_id(self, db_session: Session, type_barrel_id: uuid.UUID) -> models.TypeBarrel:
        """Define get type barrel by id method."""
        type_barrel = self.type_barrel_repository.get(db_session, obj_id=type_barrel_id)
        if not type_barrel:
           raise BEErrorCode.TYPE_BARREL_NOT_FOUND.value
        return type_barrel
    
    def get_type_barrels(self, db_session: Session) -> List[models.TypeBarrel]:
        """Define get type barrels method."""
        type_barrels = self.type_barrel_repository.get_all(db_session)
        if not type_barrels:
           raise BEErrorCode.TYPE_BARREL_NOT_FOUND.value
        return type_barrels

    def create_type_barrel(self, db_session: Session, type_barrel_create: TypeBarrelCreate) -> models.TypeBarrel:
        """Define create type barrel method."""
        type_barrel = self.type_barrel_repository.create(db_session, obj_in=type_barrel_create)
        return type_barrel
