"""doc."""
from app.src import models
from app.src.repositories.base_sql import BaseSQLRepository


class PositionRepository(BaseSQLRepository[models.Position]):
    """Define Posoition repository."""
