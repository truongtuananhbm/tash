"""seed_init_admin_user

Revision ID: 7e66bbf6d64c
Revises: c3e514f72ae5
Create Date: 2023-03-22 16:06:20.205023

"""
import uuid
from datetime import datetime
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy import table, column, String, UUID, BOOLEAN

from app.src.utils.security import get_password_hash

revision = '7e66bbf6d64c'
down_revision = 'c3e514f72ae5'
branch_labels = None
depends_on = None
user_system_table = table(
    "users",
    column("id", UUID),
    column("email", String),
    column("password", String),
    column("is_deleted", BOOLEAN),
)
user_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, datetime.now().isoformat())
def upgrade() -> None:
    op.bulk_insert(
        user_system_table,
        [
            {
                "id": user_uuid,
                "email": "admin@truongtuananh.com",
                "password": get_password_hash('123456').decode('utf-8'),
                "is_deleted": False,
            }
        ],
    )
def downgrade() -> None:
    pass