"""doc."""
from app.src import models
from app.src.repositories.base_sql import BaseSQLRepository


class StateRepository(BaseSQLRepository[models.State]):
    """Define State repository."""
