"""Define group model."""
import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import BOOLEAN, TIMESTAMP, UUID, Column, ForeignKey, String, func, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.src.utils.common import generate_uuid

from .base_model import Base



class Owner(Base):
    """Define owmer model."""

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)  # noqa
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    garbageMass: Mapped[int] =  mapped_column(Integer, unique=True, nullable=False)
    neighbourhood_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('neighbourhoods.id'),
                                                       nullable=True)
    neighbourhood: Mapped["Neighbourhood"] = relationship('Neighbourhood',back_populates="neighbourhood")
    group_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('groups.id'), nullable=True)
    group: Mapped["Group"] = relationship('Group', back_populates="group")
    price: Mapped[float] =  mapped_column(Float, unique=True, nullable=True)
    state_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('states.id'),
                                                       nullable=True)
    state: Mapped["State"] = relationship('State',back_populates="state")
    force_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('forces.id'),
                                                       nullable=True)
    force: Mapped["Force"] = relationship('Force',back_populates="force")
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at : Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(BOOLEAN, default=False, nullable=False)