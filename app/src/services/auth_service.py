"""Define auth service file."""
from typing import Dict

import decouple
from sqlalchemy.orm import Session

from app.src.exceptions.error_code import AuthErrorCode
from app.src.models import BlacklistToken, User
from app.src.repositories.blacklist_token import BlackListTokenRepository
from app.src.repositories.user import UserSystemRepository
from app.src.schemas.blacklist_token import BlackListTokenCreate
from app.src.schemas.session import TokenPayload
from app.src.utils.security import jwt_create_token, jwt_decode_token

REFRESH_TOKEN_EXPIRE_MINUTES = decouple.config("REFRESH_TOKEN_EXPIRE_MINUTES", 300)


class AuthService(object):
    """Define auth service object."""

    def __init__(self) -> None:
        """Define constructor for Auth service object."""
        self.user_repository = UserSystemRepository(User)
        self.blacklist_token_repository = BlackListTokenRepository(BlacklistToken)

    @staticmethod
    def login(val_input: str) -> Dict[str, str]:
        """Define login with username and password method."""
        access_token = jwt_create_token(val_input)
        refresh_token = jwt_create_token(val_input, expires_minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "refresh_token": refresh_token}

    def refresh_access_token(self, val_input: str, refresh_token: str) -> Dict[str, str]:
        """Define refresh access token method."""
        token_data = jwt_decode_token(refresh_token)
        token_payload = TokenPayload(**token_data)
        if token_payload.sub != val_input:
            raise AuthErrorCode.INVALID_ACCESS_TOKEN.value
        return self.login(val_input)

    def logout(self, db_session: Session, token: str) -> None:
        """Define logout method."""
        token_data = jwt_decode_token(token)
        token_payload = TokenPayload(**token_data)
        if not self.user_repository.get_user_system_by_email(db_session, token_payload.sub):
            raise AuthErrorCode.INVALID_ACCESS_TOKEN.value
        self.blacklist_token_repository.create(db_session, obj_in=BlackListTokenCreate(token=token))
