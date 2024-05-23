"""Define group model."""
import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import BOOLEAN, TIMESTAMP, UUID, Column, ForeignKey, String, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.src.utils.common import generate_uuid

from .base_model import Base


class Force(Base):
    """Define force model."""

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)  # noqa
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    force: Mapped[List["Owner"]] = relationship('Owner', back_populates="force")
    unit: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    numberBarrel: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    typeBarrel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('typeBarrel.id'),
                                                       nullable=False)
    typeBarrel: Mapped["TypeBarrel"] = relationship('TypeBarrel',back_populates="typeBarrel")
    position_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('positions.id'),
                                                       nullable=False)
    position: Mapped["Position"] = relationship(back_populates="force")
    worker: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp(), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(BOOLEAN, default=False, nullable=False)
