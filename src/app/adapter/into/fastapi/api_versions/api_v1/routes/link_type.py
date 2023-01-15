import logging

from app.adapter.into.fastapi.dependencies import get_db
from app.port.domain.link_type import CreateLinkTypeDTO, LinkTypeDTO, UpdateLinkTypeDTO
from ....crud import CrudRouter

logger = logging.getLogger(__name__)

router_v1 = CrudRouter(
    db_dependency=get_db,
    respository="link_type",
    methods=["CREATE", "READ", "UPDATE", "DELETE"],
    response_schema=LinkTypeDTO,
    create_schema=CreateLinkTypeDTO,
    update_schema=UpdateLinkTypeDTO,
).router

# router = APIRouter(
#     prefix="/link-type",
#     dependencies=[],
#     responses={404: {"description": "Not found"}},
#     redirect_slashes=True,
# )


# @router.get("/", tags=["Link Type"], response_model=Page[LinkTypeDTO])
# def list_links(
#     filters: Optional[str] = None,
#     limit: Optional[int] = None,
#     db_adapter=Depends(get_db),
#     user=Depends(get_current_user),
# ) -> AbstractPage[LinkTypeDTO]:
#     query_param = ListParams(filters=filters, limit=limit)
#     data: List[LinkTypeDTO] = link_type.list_link_type(
#         query_param=query_param, db_adapter=db_adapter
#     )
#     return paginate(data)


# @router.get("/{uuid}/", tags=["Link Type"])
# def get_link(
#     uuid: str,
#     db_adapter=Depends(get_db),
#     user=Depends(get_current_user),
# ) -> LinkTypeDTO:
#     data: LinkTypeDTO = link_type.read(uuid=uuid, db_adapter=db_adapter)
#     return data


# @router.post("/", tags=["Link Type"])
# def create_entity(
#     link_data: CreateLinkTypeDTO,
#     db_adapter=Depends(get_db),
#     user=Depends(get_current_user),
# ) -> LinkTypeDTO:
#     try:
#         data: LinkTypeDTO = link_type.create(
#             entity_data=link_data, db_adapter=db_adapter
#         )
#     except (DuplicateRecord, EntityValidationError) as err:
#         raise HTTPException(400, str(err))
#     return data


# @router.patch("/{uuid}/", tags=["Link Type"])
# def update_entity(
#     uuid: str,
#     entity_data: UpdateLinkTypeDTO,
#     db_adapter=Depends(get_db),
#     user=Depends(get_current_user),
# ) -> LinkTypeDTO:
#     try:
#         data: LinkTypeDTO = link_type.update(
#             uuid=uuid,
#             entity_data=entity_data,
#             db_adapter=db_adapter,
#         )
#     except (DuplicateRecord, EntityValidationError) as err:
#         raise HTTPException(400, str(err))
#     return data


# @router.delete("/{uuid}/", tags=["Link Type"], status_code=201)
# def delete_entity(
#     entity_type: str,
#     uuid: str,
#     db_adapter=Depends(get_db),
#     user=Depends(get_current_user),
# ) -> None:
#     link_type.delete(uuid=uuid, db_adapter=db_adapter)
#     return
