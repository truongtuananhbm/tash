"""doc."""
from typing import List
from sqlalchemy.orm import Session
from app.src import models
from app.src.repositories.base_sql import BaseSQLRepository
from app.src.schemas.force import ForceUpdate


class ForceRepository(BaseSQLRepository[models.Force]):
    """Define Force repository."""

    def search_forces(self, session: Session, filters: ForceUpdate) -> List[models.Force]:
        """Define method to search forces based on filters."""
        query = session.query(self.model).filter(
            self.model.is_deleted.is_(False),
        )
        if filters.name != 'string' and filters.name:
            query = query.filter(self.model.name.like(f"%{filters.name}%"))
        if filters.unit != 'string' and filters.unit:
            query = query.filter(self.model.unit == filters.unit)
        if filters.numberBarrel !=0 and filters.numberBarrel:
            query = query.filter(self.model.numberBarrel == filters.numberBarrel)
        if filters.typeBarrel_id != 'string' and filters.typeBarrel_id:
            query = query.filter(self.model.typeBarrel_id == filters.typeBarrel_id)
        if filters.position_id != 'string' and filters.position_id:
            query = query.filter(self.model.position_id == filters.position_id)
        if filters.worker != 0 and filters.worker:
            query = query.filter(self.model.worker == filters.worker)
        owners = query.all()
        return owners

