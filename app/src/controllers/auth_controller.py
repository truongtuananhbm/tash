"""Define process for authentication."""
from typing import Tuple

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.src.schemas.response import ResponseObject
from app.src.schemas.session import RefreshToken
from app.src.models.user import User
from app.src.schemas.user_organization import UserOrganizationLogin
from app.src.schemas.user_system import UserSystemLogin
from app.src.services.auth_service import AuthService
from app.src.services.user_service import UserService
from app.src.utils.connection.sql_connection import get_db_session
from app.src.utils.const.document import generate_doc_response, get_response

user_service = UserService()
auth_service = AuthService()

auth_routers = APIRouter()


@auth_routers.post("/user-system/login/access-token",
                   responses={status.HTTP_200_OK: generate_doc_response(example=get_response("API_LOGIN_USER"),
                                                                        model=ResponseObject)})
def login_email_password_system(login_data: UserSystemLogin, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Define function login with email and password."""
    user_service.authenticate_system(db_session, login_data.email, login_data.password)
    data = auth_service.login(login_data.email)
    return ResponseObject(data=data, code="AUTH0000")


@auth_routers.post("/user-organization/login/access-token",
                   responses={status.HTTP_200_OK: generate_doc_response(example=get_response("API_LOGIN_USER"),
                                                                        model=ResponseObject)})
def login_email_password_organization(login_data: UserOrganizationLogin, db_session: Session = Depends(get_db_session)) -> ResponseObject: # noqa
    """Define function login with email and password."""
    user_service.authenticate_organization(db_session, login_data.email, login_data.password)
    data = auth_service.login(login_data.email)
    return ResponseObject(data=data, code="AUTH0000")


@auth_routers.post("/user-system/refresh-token")
def refresh_access_token_system(
        refresh_token: RefreshToken,
        user_data: Tuple[User, str] = Depends(user_service.get_current_user_system),
) -> ResponseObject:
    """Define function get access token from refresh token."""
    if isinstance(user_data[0], UserSystem):

        user_object = user_data[0]
        email = user_object.email
    else:
        user_object, email = user_data

    data = auth_service.refresh_access_token(email, refresh_token.refresh_token)
    return ResponseObject(data=data, code="AUTH0000")


@auth_routers.post("/user-system/logout")
def logout_system(
        db_session: Session = Depends(get_db_session),
        user_token: Tuple[User, str] = Depends(user_service.get_current_user_system),
) -> ResponseObject:
    """Define logout function."""
    auth_service.logout(db_session, user_token[1])
    return ResponseObject(message="Logout Success", code="AUTH0000")
