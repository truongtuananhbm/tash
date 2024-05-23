"""Define owner service file."""
import uuid
from typing import Any, Dict, List, Union
from fastapi import FastAPI, Response
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from io import BytesIO
import decouple
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.src import models
from app.src.exceptions.error_code import AuthErrorCode, BEErrorCode
from app.src.models import Owner
from app.src.repositories.owner import OwnerRepository
from app.src.schemas.owner import OwnerCreate, OwnerUpdate
from app.src.utils.connection.sql_connection import get_db_session

class OwnerService(object):
    """Define Owner service object."""

    def __init__(self) -> None:
        """Define constructor for Owner service object."""
        self.owner_repository = OwnerRepository(models.Owner)

    def get_owner_by_id(self, db_session: Session, owner_id: uuid.UUID) -> models.Owner:
        """Define get owner by id method."""
        owner = self.owner_repository.get(db_session, obj_id=owner_id)
        if not user_system:
           raise BEErrorCode.OWNER_NOT_FOUND.value
        return data

    def create_owner(self, db_session: Session, owner_create: OwnerCreate,) -> models.Owner:
        """Define create owner method."""
        owner = self.owner_repository.create(db_session, obj_in=owner_create)
        return owner

    def delete_user_owner(self, db_session: Session, owner_id: uuid.UUID) -> None:
        """Define remove owner method."""
        owner = self.owner_repository.get(db_session, obj_id=owner_id)
        if not owner:
            raise BEErrorCode.OWNER_NOT_FOUND.value
        self.owner_repository.delete(db_session, obj_id=owner.id)

    def update_owner(self, db_session: Session, onwer_id: uuid.UUID, owner_update: OwnerUpdate) -> models.Owner:
        """Update an existing owner."""
        if self.owner_repository.get(db_session, obj_id=onwer_id) is None:
            raise BEErrorCode.OWNER_NOT_FOUND.value
        if owner_update.name=='string':
            del owner_update['name']
        if owner_update.address=='string':
            del owner_update['address']
        if owner_update.garbageMass==0:
            del owner_update['garbageMass']
        if owner_update.group_id=='string':
            del owner_update['group_id']
        if owner_update.state_id=='string':
            del owner_update['state_id']
        if owner_update.force_id=='string':
            del owner_update['force_id']
        owner = self.owner_repository.update(db_session, obj_id=onwer_id, obj_in=owner_update)
        owner = self.owner_repository.get(db_session, onwer_id)
        if not owner:
            raise BEErrorCode.OWNER_NOT_FOUND.value
        return owner
    
    def search_owners(self, db_session: Session, filters: OwnerUpdate) -> List[models.Owner]:
        """Define method to search owner based on filters."""
        owers = self.owner_repository.search_owners(db_session, filters)
        sorted_owner = sorted(owers, key=lambda x: x.created_at)
        if not owers:
            raise BEErrorCode.OWNER_NOT_FOUND.value
        return sorted_owner
    
    def generate_excel(self, db_session: Session, filters: OwnerUpdate):
        sorted_owner = self.search_owners(db_session, filters)
        wb = Workbook()
        ws = wb.active
        ws.append(["Owner ID", "Name", "Address", "Khoi Luong Rac", "Gia Tien", "Khu Pho", "Nhom", "Tinh Trang", "Luc Luong"])
        for owner in sorted_owner:
           ws.append([owner.id, owner.name, owner.address, owner.garbageMass, owner.price, owner.neighbouhood_id, owner.group_id, owner.state_id, owner.force_id])
        for col in ws.iter_cols(min_row=1, max_row=1, min_col=1, max_col=3):
           for cell in col:
             cell.font = Font(bold=True)
        excel_file = BytesIO()
        wb.save(excel_file)
        excel_file.seek(0) 
        return excel_file.getvalue()
    