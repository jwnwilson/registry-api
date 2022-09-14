from typing import List

from hex_lib.ports.db import DbAdapter
from hex_lib.ports.user import UserData

from ..domain import entity
from ..ports.entity import EntityDTO, QueryParam, UpdateEntityDTO, CreateEntityDTO


def list(
    query_param: QueryParam, db_adapter: DbAdapter, user: UserData
) -> List[EntityDTO]:
    return entity.list(query_param, user=user, db_adapter=db_adapter)


def read(
    uuid:str, entity_type: str, db_adapter: DbAdapter, user: UserData
) -> List[EntityDTO]:
    return entity.read(uuid, entity_type, user=user, db_adapter=db_adapter)


def update(
    uuid:str, entity_type: str, entity_data: UpdateEntityDTO, db_adapter: DbAdapter, user: UserData
) -> List[EntityDTO]:
    return entity.update(uuid, entity_type, entity_data=entity_data, user=user, db_adapter=db_adapter)


def delete(
    uuid:str, entity_type: str, db_adapter: DbAdapter, user: UserData
) -> None:
    return entity.delete(uuid, entity_type, user=user, db_adapter=db_adapter)


def create(
    entity_data: CreateEntityDTO, user: UserData, db_adapter: DbAdapter
) -> List[EntityDTO]:
    return entity.create(entity_data, user=user, db_adapter=db_adapter)
