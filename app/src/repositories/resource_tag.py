"""doc."""


from app.src import models
from app.src.repositories.base_sql import BaseSQLRepository


class ResourceTagRepository(BaseSQLRepository[models.ResourceTag]):
    """Define Resource Tag repository."""
