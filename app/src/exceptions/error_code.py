"""doc."""
from enum import Enum

from starlette import status

from app.src.schemas.response import ExceptionDetail

from .exception import BusinessException


class BEErrorCode(Enum):
    """doc."""

    WRONG_TIME_FORMAT = BusinessException(ExceptionDetail(message="Invalid Time Format", code="BE0001"))
    APP_NOT_FOUND = BusinessException(ExceptionDetail(message="App Not Found", code="BE0002"))
    BUDGET_NOT_FOUND = BusinessException(ExceptionDetail(message="Budget Not Found", code="BE0003"))
    CONTENT_NOT_FOUND = BusinessException(ExceptionDetail(message="Content Not Found", code="BE0004"))
    RESULT_NOT_FOUND = BusinessException(ExceptionDetail(message="Result Not Found", code="BE0005"))
    TOKEN_NOT_FOUND = BusinessException(ExceptionDetail(message="Token Not Found", code="BE0006"))
    CONFIG_NOT_FOUND = BusinessException(ExceptionDetail(message="Config Not Found", code="BE0009"))
    CONFIG_EXISTED = BusinessException(ExceptionDetail(message="Config Existed", code="BE0010"))
    FORCE_NOT_FOUND = BusinessException(ExceptionDetail(message="Force Not Found", code="BE0011"))
    TYPE_BARREL_NOT_FOUND = BusinessException(ExceptionDetail(message="Type Barrel Not Found", code="BE0012"))
    POSITION_NOT_FOUND = BusinessException(ExceptionDetail(message="Position Not Found", code="BE0013"))
    JOB_EXISTED = BusinessException(ExceptionDetail(message="Job Existed", code="BE0014"))
    # JOB_CREATING_ERROR = BusinessException(ExceptionDetail(message="Can't Creat Job", code="BE0015"))
    ROLE_NOT_FOUND = BusinessException(ExceptionDetail(message="Role Not Found", code="BE0018"))
    ROLE_EXISTED = BusinessException(ExceptionDetail(message="Role Existed", code="BE0019"))
    RESOURCE_STAGE_NOT_FOUND = BusinessException(ExceptionDetail(message="Resource Stage Not Found", code="BE0020"))
    RESOURCE_NOT_FOUND = BusinessException(ExceptionDetail(message="Resource Not Found", code="BE0021"))
    RESOURCE_TAG_NOT_FOUND = BusinessException(ExceptionDetail(message="Resource Tag Not Found", code="BE0022"))
    USER_NOT_FOUND = BusinessException(ExceptionDetail(message="User Not Found", code="BE0022"))
    INVALID_ROLE = BusinessException(ExceptionDetail(message="Invalid Role", code="BE0023"))
    USER_NOT_PERMISSION = BusinessException(ExceptionDetail(message="User Not Permission", code="BE0024"))
    GROUP_NOT_FOUND = BusinessException(ExceptionDetail(message="Group Not Found", code="BE0025"))
    GROUP_EXITED = BusinessException(ExceptionDetail(message="Group Exited", code="BE0026"))
    PERMISSION_EXITED = BusinessException(ExceptionDetail(message="Permission Exited", code="BE0027"))
    PERMISSION_NOT_FOUND = BusinessException(ExceptionDetail(message="Permission Not Found", code="BE0028"))
    OWNER_NOT_FOUND = BusinessException(ExceptionDetail(message="Owner Not Found", code="BE0029"))
    NEIGHBOURHOOD_NOT_FOUND = BusinessException(ExceptionDetail(message="Neighbourhood Not Found", code="BE0030"))
    STATE_NOT_FOUND = BusinessException(ExceptionDetail(message="State Not Found", code="BE0031"))


class ServerErrorCode(Enum):
    """doc."""

    SERVER_ERROR = BusinessException(ExceptionDetail(message="INTERNAL SERVER ERROR", code="SERVER0100"),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    DATABASE_ERROR = BusinessException(ExceptionDetail(message="Database Error", code="SERVER0101"),
                                       status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    FILE_STORAGE_ERROR = BusinessException(ExceptionDetail(message="FILE STORAGE ERROR", code="SERVER0102"),
                                           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuthErrorCode(Enum):
    """doc."""

    USERNAME_NOT_FOUND = BusinessException(ExceptionDetail(message="User Not Found", code="AUTH0001"))
    INCORRECT_PASSWORD = BusinessException(ExceptionDetail(message="Incorrect Password", code="AUTH0002"))
    EMAIL_NOT_CONFIRM = BusinessException(ExceptionDetail(message="User Not Confirmed", code="AUTH0003"))
    INVALID_ACCESS_TOKEN = BusinessException(ExceptionDetail(message="Invalid Access Token", code="AUTH0004"))
    BLACKLIST_TOKEN = BusinessException(ExceptionDetail(message="Blacklisted Token", code="AUTH0005"))
    EXPIRED_ACCESS_TOKEN = BusinessException(ExceptionDetail(message="Expired Access Token", code="AUTH0006"))
    PERMISSION_DENIED = BusinessException(ExceptionDetail(message="Permission Denied", code="AUTH0007"))
    USER_EXISTED = BusinessException(ExceptionDetail(message="Username Existed", code="AUTH0008"))
    INVALID_ENCRYPTION_KEY = BusinessException(ExceptionDetail(message="Invalid Public Key", code="AUTH0009"))
    INVALID_SIGNATURE = BusinessException(ExceptionDetail(message="Invalid Signature", code="AUTH0010"))
    TOKEN_NOT_FOUND = BusinessException(ExceptionDetail(message="Token Not Found", code="AUTH0011"))
    INCORRECT_SECRET_KEY = BusinessException(ExceptionDetail(message="Incorrect Key", code="AUTH0012"))
    INVALID_REFRESH_TOKEN = BusinessException(ExceptionDetail(message="Invalid Refresh Access Token", code="AUTH0013"))
    EXPIRED_REFRESH_TOKEN = BusinessException(ExceptionDetail(message="Expired Refresh Token", code="AUTH0014"))
    INVALID_TOKEN = BusinessException(ExceptionDetail(message="Invalid Token", code="AUTH0015"))
    EMAIL_EXISTED = BusinessException(ExceptionDetail(message="Email Has Been Used", code="AUTH0016"))

