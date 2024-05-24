"""doc."""
from app.src import models
from app.src.repositories.base_sql import BaseSQLRepository


class GroupRepository(BaseSQLRepository[models.Group]):
    """Define Group repository."""
