"""Define app."""
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.src.controllers.auth_controller import auth_routers
from app.src.controllers.user_controller import users_routers
from app.src.exceptions.exception import BusinessException
from app.src.exceptions.exception_handler import business_exception_handler
from app.src.controllers.owner_controller import owners_routers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    """Define custon openapi."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Resource-Management",
        version=app.version,
        openapi_version=app.openapi_version,
        terms_of_service=app.terms_of_service,
        contact=app.contact,
        license_info=app.license_info,
        routes=app.routes,
        tags=app.openapi_tags,
        servers=app.servers,
    )
    for _, method_item in openapi_schema.get('paths').items():
        for _, param in method_item.items():
            responses = param.get('responses')
            if '422' in responses:
                del responses['422']
    openapi_schema["info"]["x-logo"] = {
        "url": "https://rabiloo.weekly.vn/images/hrm_logo.png",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.exception_handler(BusinessException)(business_exception_handler)
PREFIX = "/Resource-Management"
app.include_router(auth_routers, tags=["Authentication"], prefix=PREFIX)
app.include_router(users_routers, tags=["User"], prefix=PREFIX)
app.include_router(owners_routers, tags=["Owner"], prefix=PREFIX)