import logging

from app.adapter.into.fastapi.dependencies import get_db
from app.domain import entity_type
from app.port.domain.entity_type import (
    CreateEntityTypeDTO,
    EntityTypeDTO,
    UpdateEntityTypeDTO,
)

from ....crud import CrudRouter


logger = logging.getLogger(__name__)

router_v1 = CrudRouter(
    db_dependency=get_db,
    respository="entity_type",
    methods=["CREATE", "READ", "UPDATE", "DELETE"],
    response_schema=EntityTypeDTO,
    create_schema=CreateEntityTypeDTO,
    update_schema=UpdateEntityTypeDTO,
).router


# router = APIRouter(
#     prefix="/entity-type",
#     dependencies=[],
#     responses={404: {"description": "Not found"}},
#     redirect_slashes=True,
# )


# @router.get("/", tags=["Entity Type"], response_model=Page[EntityTypeDTO])
# def list_entity_type(
#     filters: Optional[str] = None,
#     limit: Optional[int] = None,
#     db_adapter=Depends(get_db),
#     user=Depends(get_current_user),
# ) -> AbstractPage[EntityTypeDTO]:
#     # call create use case
#     query_param = ListParams(filters=filters, limit=limit)
#     data: List[EntityTypeDTO] = entity_type.list_entity_type(
#         query_param=query_param, db_adapter=db_adapter
#     )
#     return paginate(data)


# @router.get("/{uuid}/", tags=["Entity Type"])
# def get_entity_type(
#     uuid, db_adapter=Depends(get_db), user=Depends(get_current_user)
# ) -> EntityTypeDTO:
#     # call create use case
#     data: EntityTypeDTO = entity_type.read(uuid, db_adapter=db_adapter)
#     return data


# @router.post("/", tags=["Entity Type"])
# def create_entity_type(
#     entity_type_data: CreateEntityTypeDTO,
#     db_adapter=Depends(get_db),
#     user=Depends(get_current_user),
# ) -> EntityTypeDTO:
#     # call create use case
#     try:
#         data: EntityTypeDTO = entity_type.create(
#             entity_type_data, db_adapter=db_adapter
#         )
#     except DuplicateRecord as err:
#         raise HTTPException(400, str(err))
#     return data


# @router.patch("/{uuid}/", tags=["Entity Type"])
# def update_entity_type(
#     uuid: str,
#     entity_type_data: UpdateEntityTypeDTO,
#     db_adapter=Depends(get_db),
#     user=Depends(get_current_user),
# ) -> EntityTypeDTO:
#     # call create use case
#     data: EntityTypeDTO = entity_type.update(
#         uuid=uuid, entity_data=entity_type_data, db_adapter=db_adapter
#     )
#     return data


# @router.delete("/{uuid}/", tags=["Entity Type"], status_code=201)
# def delete_entity(
#     uuid: str, db_adapter=Depends(get_db), user=Depends(get_current_user)
# ) -> None:
#     # call create use case
#     entity_type.delete(uuid, db_adapter)
#     return
