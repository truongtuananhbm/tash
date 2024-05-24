"""doc."""
from typing import Any, Optional, Union

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.src import models
from app.src.exceptions.error_code import ServerErrorCode
from app.src.repositories.base_sql import BaseSQLRepository


class UserSystemRepository(BaseSQLRepository[models.User]):
    """Define User System repository."""

    def get_user_system_by_email(self, session: Session, value: Any) -> Union[Optional[models.User]]:
        """Define method get user by email."""
        try:
            obj = session.query(self.model).filter(self.model.email == value,
                                                   self.model.is_deleted.is_(False)).first()
        except SQLAlchemyError as ex:
            raise ServerErrorCode.DATABASE_ERROR.value(ex)
        return obj
