import logging

from app.adapter.into.fastapi.dependencies import get_repo
from app.port.domain.entity_type import (
    CreateEntityTypeDTO,
    EntityTypeDTO,
    UpdateEntityTypeDTO,
)

from ....crud import CrudRouter


logger = logging.getLogger(__name__)

router_v1 = CrudRouter(
    repo_dependency=get_repo,
    respository="entity_type",
    methods=["CREATE", "READ", "UPDATE", "DELETE"],
    response_schema=EntityTypeDTO,
    create_schema=CreateEntityTypeDTO,
    update_schema=UpdateEntityTypeDTO,
)
