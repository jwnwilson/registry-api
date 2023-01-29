from fastapi import APIRouter

from .routes.healthcheck import router_v1 as healthcheck_router
from .routes.entity_type import router_v1 as entity_type_router
from .routes.entity import router_v1 as entity_router
from .routes.link_type import router_v1 as link_type_router

api_router_v1 = APIRouter()

api_router_v1.include_router(
    healthcheck_router,
    tags=["Healthcheck"],
    prefix="/heathcheck",
)
api_router_v1.include_router(
    entity_type_router,
    tags=["Entity Type"],
    prefix="/entity-type",
)
api_router_v1.include_router(
    entity_router,
    tags=["Entity"],
    prefix="/entity",
)
api_router_v1.include_router(
    link_type_router,
    tags=["Link Type"],
    prefix="/link-type",
)



