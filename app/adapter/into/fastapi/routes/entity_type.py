import logging
from typing import List, Optional

from adapter.into.fastapi.dependencies import get_current_user, get_db_adapater
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from ports.entity_type import EntityTypeDTO, QueryParam
from use_case import entity_type

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/entity-type",
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", tags=["Entity Type"], response_model=Page[EntityTypeDTO])
def list_entity_type(
    filters: Optional[str] = None,
    limit: Optional[int] = None,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user),
) -> List[EntityTypeDTO]:
    # call create use case
    query_param = QueryParam(filters=filters, limit=limit)
    data: List[EntityTypeDTO] = entity_type.list(
        query_param=query_param, db_adapter=db_adapter, user=user
    )
    return paginate(data)


@router.get("/{uuid}", tags=["Entity Type"])
def get_entity_type(
    uuid, db_adapter=Depends(get_db_adapater), user=Depends(get_current_user)
) -> EntityTypeDTO:
    # call create use case
    data: List[EntityTypeDTO] = entity_type.get(uuid, db_adapter=db_adapter, user=user)
    return data


@router.post("/", tags=["Entity Type"])
def create_entity_type(
    entity_type_data: EntityTypeDTO,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user),
) -> dict:
    # call create use case
    data: dict = entity_type.create(entity_type_data, db_adapter=db_adapter, user=user)
    return data


@router.patch("/{uuid}", tags=["Entity Type"])
def create_entity_type(
    uuid: str,
    entity_type_data: EntityTypeDTO,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user),
) -> dict:
    entity_type.uuid = uuid
    # call create use case
    data: dict = entity_type.patch(entity_type_data, db_adapter, user)
    return data


@router.delete("/{uuid}", tags=["Entity Type"])
def delete_entity(
    uuid: str, db_adapter=Depends(get_db_adapater), user=Depends(get_current_user)
) -> None:
    # call create use case
    entity_type.delete(uuid, db_adapter, user)
    return None, 201
