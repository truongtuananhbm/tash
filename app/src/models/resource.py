"""Define resource tag model."""
import uuid

from sqlalchemy import TIMESTAMP, UUID, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.src.utils.common import generate_uuid

from .base_model import Base
from .resource_resource_tag import resource_resource_tag


class Resource(Base):
    """Define resource tag model."""

    __tablename__ = "resources"  # type: ignore
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)  # noqa
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    version: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    stage_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('resource_stages.id'), nullable=False)
    status_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('resource_statuss.id'), nullable=False)
    resource_status = relationship('ResourceStatus', back_populates='resource_status')
    platform_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('resource_platforms.id'),
                                                   nullable=False)
    product_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('product_types.id'),
                                                       nullable=False)
    repo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('package_repos.id'), nullable=False)
    user_organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_organizations.id'),
                                                            nullable=False)
    group_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('groups.id'), nullable=False)
    resource_tags = relationship("ResourceTag", secondary=resource_resource_tag, back_populates="resources")
