import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate

from .....adapter.into.fastapi.dependencies import get_current_user, get_db_adapater
from .....ports.entity import EntityDTO, CreateEntityTypeDTO, UpdateEntityTypeDTO
from .....use_case import entity as entity_uc

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/entity",
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/{entity_type}", tags=["Entity"], response_model=Page[EntityDTO])
def list_entity(
    entity_type:str, db_adapter=Depends(get_db_adapater), user=Depends(get_current_user)
) -> EntityDTO:
    data: List[EntityDTO] = entity_uc.list(db_adapter=db_adapter, user=user)
    return paginate(data)


@router.get("/{entity_type}/{uuid}", tags=["Entity"])
def get_entity(
    entity_type:str, uuid:str, db_adapter=Depends(get_db_adapater), user=Depends(get_current_user)
) -> EntityDTO:
    data: EntityDTO = entity_uc.read(uuid=uuid, entity_type=entity_type, db_adapter=db_adapter, user=user)
    return data


@router.post("/{entity_type}", tags=["Entity"])
def create_entity(
    entity_type:str,
    entity_data: EntityDTO,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user),
) -> EntityDTO:
    data: EntityDTO = entity_uc.create(entity_type=entity_type, entity_data=entity_data, db_adapter=db_adapter, user=user)
    return data


@router.patch("/{entity_type}/{uuid}", tags=["Entity"])
def create_entity(
    entity_type:str,
    uuid: str,
    entity_data: EntityDTO,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user),
) -> EntityDTO:
    data: EntityDTO = entity_uc.update(uuid=uuid, entity_type=entity_type, entity_data=entity_data, db_adapter=db_adapter, user=user)
    return data


@router.delete("/{entity_type}/{uuid}", tags=["Entity"])
def delete_entity(
    entity_type:str, uuid: str, db_adapter=Depends(get_db_adapater), user=Depends(get_current_user)
) -> None:
    # call create use case
    entity_uc.delete(uuid=uuid, entity_type=entity_type, db_adapter=db_adapter, user=user)
    return None, 201
