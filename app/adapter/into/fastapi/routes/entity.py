import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate

from .....adapter.into.fastapi.dependencies import get_current_user, get_db_adapater
from .....ports.entity import EntityDTO
from .....use_case import entity

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/entity",
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", tags=["Entity"], response_model=Page[EntityDTO])
def list_entity(
    db_adapter=Depends(get_db_adapater), user=Depends(get_current_user)
) -> EntityDTO:
    # call create use case
    data: List[EntityDTO] = entity.list(db_adapter, user)
    return paginate(data)


@router.get("/{uuid}", tags=["Entity"])
def get_entity(
    uuid, db_adapter=Depends(get_db_adapater), user=Depends(get_current_user)
) -> EntityDTO:
    # call create use case
    data: EntityDTO = entity.get(uuid, db_adapter, user)
    return data


@router.post("/", tags=["Entity"])
def create_entity(
    entity: EntityDTO,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user),
) -> EntityDTO:
    # call create use case
    data: EntityDTO = entity.create(entity, db_adapter, user)
    return data


@router.patch("/{uuid}", tags=["Entity"])
def create_entity(
    uuid: str,
    entity: EntityDTO,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user),
) -> EntityDTO:
    entity.uuid = uuid
    # call create use case
    data: EntityDTO = entity.patch(entity, db_adapter, user)
    return data


@router.delete("/{uuid}", tags=["Entity"])
def delete_entity(
    uuid: str, db_adapter=Depends(get_db_adapater), user=Depends(get_current_user)
) -> None:
    # call create use case
    entity.delete(uuid, db_adapter, user)
    return None, 201
