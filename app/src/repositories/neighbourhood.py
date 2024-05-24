"""doc."""
from typing import Any, Optional, Union, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.src import models
from app.src.exceptions.error_code import ServerErrorCode
from app.src.repositories.base_sql import BaseSQLRepository


class NeighbourhoodRepository(BaseSQLRepository[models.Neighbourhood]):
    """Define Neigbourhood repository."""
