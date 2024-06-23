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
user_table = table(
    "users",
    column("id", UUID),
    column("email", String),
    column("password", String),
    column("is_deleted", BOOLEAN),
)
neighbourhood_table = table(
    'neighbourhoods',
    column("id", UUID),
    column("name", String),
    column("is_deleted", BOOLEAN),
)
group_table = table(
    'groups',
    column("id", UUID),
    column("name", String),
    column("is_deleted", BOOLEAN),
)
type_barrel_table = table(
    'type_barrels',
    column("id", UUID),
    column("name", String),
    column("is_deleted", BOOLEAN),
)
position_table = table(
    'positions',
    column("id", UUID),
    column("name", String),
    column("is_deleted", BOOLEAN),
)
state_table = table(
    'states',
    column("id", UUID),
    column("name", String),
    column("is_deleted", BOOLEAN),
)
user_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, datetime.now().isoformat())
neighbourhood_data = ["01", "02", "03", "04", "05", "06"]
neighbourhood_ids = [uuid.uuid5(uuid.NAMESPACE_DNS, datetime.now().isoformat()) for _ in range(len(neighbourhood_data))]
group_data = ["Hộ gia đình", "Nhóm 1", "Nhóm 2", "Nhóm 3", "Nhóm 4"]
group_ids = [uuid.uuid5(uuid.NAMESPACE_DNS, datetime.now().isoformat()) for _ in range(len(group_data))]
type_barrel_data = ["Thùng tự chế", "Thùng nhựa Composite"]
type_barrel_ids = [uuid.uuid5(uuid.NAMESPACE_DNS, datetime.now().isoformat()) for _ in range(len(type_barrel_data))]
position_data = ["Quận 10", "Nơi khác"]
position_ids = [uuid.uuid5(uuid.NAMESPACE_DNS, datetime.now().isoformat()) for _ in range(len(position_data))]
state_data = ["Chưa nộp", "đã nộp", "đã nộp 1 phần"]
state_ids = [uuid.uuid5(uuid.NAMESPACE_DNS, datetime.now().isoformat()) for _ in range(len(state_data))]
def upgrade() -> None:
    op.bulk_insert(
        user_table,
        [
            {
                "id": user_uuid,
                "email": "admin@truongtuananh.com",
                "password": get_password_hash('123456').decode('utf-8'),
                "is_deleted": False,
            }
        ],
    )
    op.bulk_insert(
        neighbourhood_table,
        [
            {
                "id": neighbourhood_ids[index],
                "name": neighbourhood,
                "is_deleted": False,
            } for index, neighbourhood in enumerate(neighbourhood_data)
        ],
    )
    op.bulk_insert(
        group_table,
        [
            {
                "id": group_ids[index],
                "name": group,
                "is_deleted": False,
            } for index, group in enumerate(group_data)
        ],
    )
    op.bulk_insert(
        type_barrel_table,
        [
            {
                "id": type_barrel_ids[index],
                "name": type_barrel,
                "is_deleted": False,
            } for index, type_barrel in enumerate(type_barrel_data)
        ],
    )
    op.bulk_insert(
        position_table,
        [
            {
                "id": position_ids[index],
                "name": position,
                "is_deleted": False,
            } for index, position in enumerate(position_data)
        ],
    )
    op.bulk_insert(
        state_table,
        [
            {
                "id": state_ids[index],
                "name": state,
                "is_deleted": False,
            } for index, state in enumerate(state_data)
        ],
    )
def downgrade() -> None:
    pass