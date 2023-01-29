import logging
from json import JSONDecodeError
from typing import List

from fastapi import Depends, HTTPException, UploadFile

from app.adapter.into.fastapi.dependencies import get_current_user, get_repo, get_db
from app.domain import entity
from app.domain.entity import (
    CreateEntityDTO,
    EntityDTO,
    UpdateEntityDTO,
)
from app.domain.file import FileDTO
from ....crud import CrudRouter

logger = logging.getLogger(__name__)

router_v1 = CrudRouter(
    repo_dependency=get_repo,
    respository="entity_type",
    methods=["CREATE", "READ", "UPDATE", "DELETE"],
    response_schema=EntityDTO,
    create_schema=CreateEntityDTO,
    update_schema=UpdateEntityDTO,
)


@router_v1.post("/{entity_type}/import/")
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
