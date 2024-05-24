"""doc."""
from typing import Any, Optional, Union, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.src import models
from app.src.exceptions.error_code import ServerErrorCode
from app.src.repositories.base_sql import BaseSQLRepository
from app.src.schemas.owner import OwnerUpdate


class OwnerRepository(BaseSQLRepository[models.Owner]):
    """Define Owner repository."""

    def search_owners(self, session: Session, filters: OwnerUpdate) -> List[models.Owner]:
        """Define method to search owners based on filters."""
        query = session.query(self.model).filter(
            self.model.is_deleted.is_(False),
        )
        if filters.name != 'string' and filters.name:
            query = query.filter(self.model.name.like(f"%{filters.name}%"))
        if filters.address != 'string' and filters.address:
            query = query.filter(self.model.address == filters.address)
        if filters.garbageMass!=0 and filters.garbageMass:
            query = query.filter(self.model.garbageMass == filters.garbageMass)
        if filters.group_id != 'string' and filters.group_id:
            query = query.filter(self.model.group_id == filters.group_id)
        if filters.state_id != 'string' and filters.state_id:
            query = query.filter(self.model.state_id == filters.state_id)
        if filters.force_id != 'string' and filters.force_id:
            query = query.filter(self.model.force_id == filters.force_id)
        owners = query.all()
        return owners

