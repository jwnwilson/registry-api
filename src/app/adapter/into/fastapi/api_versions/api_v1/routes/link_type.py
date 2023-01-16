import logging

from app.adapter.into.fastapi.dependencies import get_repo
from app.port.domain.link_type import CreateLinkTypeDTO, LinkTypeDTO, UpdateLinkTypeDTO
from ....crud import CrudRouter

logger = logging.getLogger(__name__)

router_v1 = CrudRouter(
    repo_dependency=get_repo,
    respository="link_type",
    methods=["CREATE", "READ", "UPDATE", "DELETE"],
    response_schema=LinkTypeDTO,
    create_schema=CreateLinkTypeDTO,
    update_schema=UpdateLinkTypeDTO,
).router
