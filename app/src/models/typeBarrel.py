"""Define Type Barrel model."""
import uuid

from sqlalchemy import BOOLEAN, TIMESTAMP, UUID, Column, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.src.utils.common import generate_uuid

from .base_model import Base


class TypeBarrel(Base):
    """Define type barrel model."""

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)  # noqa
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp(), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(BOOLEAN, default=False, nullable=False)
    typeBarrel:  Mapped[list["Force"]] = relationship('Force',back_populates="typeBarrel")
