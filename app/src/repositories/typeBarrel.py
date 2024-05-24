"""doc."""
from app.src import models
from app.src.repositories.base_sql import BaseSQLRepository


class TypeBarrelRepository(BaseSQLRepository[models.TypeBarrel]):
    """Define Type Barrel repository."""
