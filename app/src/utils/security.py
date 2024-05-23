"""Security file."""
import base64
from datetime import datetime, timedelta
from typing import Any, Dict

import bcrypt
import decouple
from jose import jwt
from pydantic import ValidationError

from app.src.exceptions.error_code import AuthErrorCode

SECRET_KEY = decouple.config("SECRET_KEY")
ALGORITHM = decouple.config("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = decouple.config("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = decouple.config("REFRESH_TOKEN_EXPIRE_MINUTES")


def jwt_create_token(subject: str, public_key: str = "", expires_minutes: int = 0) -> str:
    """Create token when login with user."""
    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes if expires_minutes else int(ACCESS_TOKEN_EXPIRE_MINUTES))

    if public_key:
        to_encode = {"sub": subject, "exp": expire, "key": public_key}
    else:
        to_encode = {"sub": subject, "exp": expire}
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY)
    return encoded_jwt


def jwt_decode_token(access_token: str) -> Dict[str, Any]:
    """Decode jwt token."""
    try:
        payload: Dict[str, Any] = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise AuthErrorCode.EXPIRED_ACCESS_TOKEN.value
    except (jwt.JWTError, ValidationError):
        raise AuthErrorCode.INVALID_ACCESS_TOKEN.value
    return payload


def verify_password(plain_password: str, hashed_password: str) -> Any:
    """Verify 2 password when hash password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> Any:
    """Get password hash."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def password_encode(password: str) -> Any:
    """Encode password with base64."""
    password = password + '!@#$%^&*()'
    password_encode_64 = base64.b64encode(password.encode('utf8')).decode('utf-8')
    return password_encode_64


# def password_decode(password: str) -> Any:
#     """Decode password with base64."""
#     password_decode_64 = base64.b64decode(password).decode('utf-8')
#     password_decode_64 = password_decode_64[:-10]
#     return password_decode_64
