import logging
from typing import List

from adapter.into.fastapi.dependencies import (
    get_db_adapater,
    get_current_user
)
from fastapi import APIRouter, Depends, HTTPException
from ports.entity_type import EntityType
from use_case import entity_type

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/entity-type",
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def list_entity_type(
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user)
) -> List[dict]:
    # call create use case
    data: List[dict] = entity_type.list(
        db_adapter,
        user
    )
    return data


@router.get("/{uuid}")
async def get_entity_type(
    uuid,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user)
) -> List[dict]:
    # call create use case
    data: List[dict] = entity_type.get(
        uuid,
        db_adapter,
        user
    )
    return data



@router.post("/")
async def create_entity_type(
    entity_type: EntityType,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user)
) -> dict:
    # call create use case
    data: dict = entity_type.create(
        entity_type,
        db_adapter,
        user
    )
    return data


@router.patch("/{uuid}")
async def create_entity_type(
    uuid: str,
    entity_type: EntityType,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user)
) -> dict:
    entity_type.uuid = uuid
    # call create use case
    data: dict = entity_type.patch(
        entity_type,
        db_adapter,
        user
    )
    return data


@router.delete("/{uuid}")
async def delete_entity(
    uuid: str,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user)
) -> None:
    # call create use case
    entity_type.delete(
        uuid,
        db_adapter,
        user
    )
    return None, 201
