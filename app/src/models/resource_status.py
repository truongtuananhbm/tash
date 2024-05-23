"""Define resource status model."""
import uuid

from sqlalchemy import BOOLEAN, TIMESTAMP, UUID, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.src.utils.common import generate_uuid

from .base_model import Base


class ResourceStatus(Base):
    """Define resource status model."""

    __tablename__ = "resource_statuss"  # type: ignore
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid) # noqa
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(BOOLEAN, default=False, nullable=False)
    resource_status = relationship('Resource', back_populates='resource_status')
