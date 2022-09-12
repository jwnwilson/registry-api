import logging
from typing import List

from adapter.into.fastapi.dependencies import (
    get_db_adapater,
    get_current_user
)
from fastapi import APIRouter, Depends, HTTPException
from ports.entity import Entity
from use_case import entity

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/entity",
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def list_entity(
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user)
) -> List[dict]:
    # call create use case
    data: List[dict] = entity.list(
        db_adapter,
        user
    )
    return data


@router.get("/{uuid}")
async def get_entity(
    uuid,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user)
) -> List[dict]:
    # call create use case
    data: List[dict] = entity.get(
        uuid,
        db_adapter,
        user
    )
    return data



@router.post("/")
async def create_entity(
    entity: Entity,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user)
) -> dict:
    # call create use case
    data: dict = entity.create(
        entity,
        db_adapter,
        user
    )
    return data


@router.patch("/{uuid}")
async def create_entity(
    uuid: str,
    entity: Entity,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user)
) -> dict:
    entity.uuid = uuid
    # call create use case
    data: dict = entity.patch(
        entity,
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
    entity.delete(
        uuid,
        db_adapter,
        user
    )
    return None, 201
