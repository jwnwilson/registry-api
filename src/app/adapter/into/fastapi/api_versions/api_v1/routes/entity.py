import logging
from json import JSONDecodeError
from typing import List

from fastapi import Depends, HTTPException, UploadFile

from app.adapter.into.fastapi.dependencies import get_current_user, get_repo, get_db
from app.domain import entity
from app.port.domain.entity import (
    CreateEntityDTO,
    EntityDTO,
    UpdateEntityDTO,
)
from app.port.domain.file import FileDTO
from ....crud import CrudRouter

logger = logging.getLogger(__name__)

router_v1 = CrudRouter(
    repo_dependency=get_repo,
    respository="entity_type",
    methods=["CREATE", "READ", "UPDATE", "DELETE"],
    response_schema=EntityDTO,
    create_schema=CreateEntityDTO,
    update_schema=UpdateEntityDTO,
).router


@router_v1.post("/{entity_type}/import/", tags=["Import / Export"])
def import_entities(
    entity_type: str,
    file: UploadFile,
    db_adapter=Depends(get_db),
    user=Depends(get_current_user),
) -> List[EntityDTO]:
    valid_file_types = ["application/json"]
    if file.content_type not in valid_file_types:
        raise HTTPException(
            400,
            detail="Invalid file type, valid types: {}".format(str(valid_file_types)),
        )

    # call create use case
    fileDTO = FileDTO(
        file=file.file, filename=file.filename, content_type=file.content_type
    )
    try:
        entities = entity.create_entities_from_file(entity_type, fileDTO, db_adapter)
    except JSONDecodeError as err:
        raise HTTPException(400, str(err))

    return entities


# router = APIRouter(
#     prefix="/entity",
#     dependencies=[],
#     responses={404: {"description": "Not found"}},
#     redirect_slashes=True,
# )


# @router.get("/{entity_type}/", tags=["Entity"], response_model=Page[EntityDTO])
# def list_entity(
#     entity_type: str,
#     db_adapter=Depends(get_db),
#     user=Depends(get_current_user),
# ) -> AbstractPage[EntityDTO]:
#     query_param: QueryParam = QueryParam(entity_type=entity_type)
#     data: List[EntityDTO] = entity.list_entities(query_param, db_adapter=db_adapter)
#     return paginate(data)


# @router.get("/{entity_type}/{uuid}/", tags=["Entity"])
# def get_entity(
#     entity_type: str,
#     uuid: str,
#     db_adapter=Depends(get_db),
#     user=Depends(get_current_user),
# ) -> EntityDTO:
#     data: EntityDTO = entity.read(
#         uuid=uuid, entity_type=entity_type, db_adapter=db_adapter
#     )
#     return data


# @router.post("/{entity_type}/", tags=["Entity"])
# def create_entity(
#     entity_type: str,
#     entity_data: CreateEntityPostDTO,
#     db_adapter=Depends(get_db),
#     user=Depends(get_current_user),
# ) -> EntityDTO:
#     try:
#         create_data: CreateEntityDTO = CreateEntityDTO(
#             entity_type=entity_type, **entity_data.dict()
#         )
#     except EntityValidationError as err:
#         raise HTTPException(400, str(err))
#     try:
#         data: EntityDTO = entity.create(entity_data=create_data, db_adapter=db_adapter)
#     except (DuplicateRecord, EntityValidationError) as err:
#         raise HTTPException(400, str(err))
#     return data


# @router.patch("/{entity_type}/{uuid}/", tags=["Entity"])
# def update_entity(
#     entity_type: str,
#     uuid: str,
#     entity_data: UpdateEntityPatchDTO,
#     db_adapter=Depends(get_db),
#     user=Depends(get_current_user),
# ) -> EntityDTO:
#     try:
#         update_entity_data: UpdateEntityDTO = UpdateEntityDTO(
#             entity_type=entity_type, **entity_data.dict()
#         )
#         data: EntityDTO = entity.update(
#             uuid=uuid,
#             entity_data=update_entity_data,
#             db_adapter=db_adapter,
#         )
#     except (DuplicateRecord, EntityValidationError) as err:
#         raise HTTPException(400, str(err))
#     return data


# @router.delete("/{entity_type}/{uuid}/", tags=["Entity"], status_code=201)
# def delete_entity(
#     entity_type: str,
#     uuid: str,
#     db_adapter=Depends(get_db),
#     user=Depends(get_current_user),
# ) -> None:
#     # call create use case
#     entity.delete(uuid=uuid, db_adapter=db_adapter)
#     return
