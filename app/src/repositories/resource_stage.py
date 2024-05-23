"""doc."""


from app.src import models
from app.src.repositories.base_sql import BaseSQLRepository


class ResourceStageRepository(BaseSQLRepository[models.ResourceStage]):
    """Define User repository."""
