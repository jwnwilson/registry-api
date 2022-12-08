from typing import List

from hex_lib.ports.db import DbAdapter, ListParams
from hex_lib.ports.user import UserData

from app.domain import entity_type
from app.ports.entity_type import (
    CreateEntityTypeDTO,
    EntityTypeDTO,
    UpdateEntityTypeDTO,
)


def list(query_param: ListParams, db_adapter: DbAdapter) -> List[EntityTypeDTO]:
    return entity_type.list(query_param, db_adapter=db_adapter)


def read(uuid: str, db_adapter: DbAdapter) -> EntityTypeDTO:
    return entity_type.read(uuid, db_adapter=db_adapter)


def update(
    uuid: str, entity_data: UpdateEntityTypeDTO, db_adapter: DbAdapter
) -> EntityTypeDTO:
    return entity_type.update(uuid, entity_data=entity_data, db_adapter=db_adapter)


def delete(uuid: str, db_adapter: DbAdapter) -> None:
    return entity_type.delete(uuid, db_adapter=db_adapter)


def create(entity_data: CreateEntityTypeDTO, db_adapter: DbAdapter) -> EntityTypeDTO:
    return entity_type.create(entity_data, db_adapter=db_adapter)
