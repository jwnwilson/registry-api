from typing import List

from domain import entity_type
from hex_lib.ports.db import DbAdapter
from hex_lib.ports.user import UserData
from ports.entity_type import EntityTypeDTO, QueryParam, CreateEntityTypeDTO, UpdateEntityTypeDTO


def list(
    query_param: QueryParam, db_adapter: DbAdapter, user: UserData
) -> List[EntityTypeDTO]:
    return entity_type.list(query_param, user=user, db_adapter=db_adapter)


def read(
    uuid:str, db_adapter: DbAdapter, user: UserData
) -> List[EntityTypeDTO]:
    return entity_type.read(uuid, user=user, db_adapter=db_adapter)


def update(
    uuid:str, entity_data: UpdateEntityTypeDTO, db_adapter: DbAdapter, user: UserData
) -> List[EntityTypeDTO]:
    return entity_type.update(uuid, entity_data=entity_data, user=user, db_adapter=db_adapter)


def delete(
    uuid:str, db_adapter: DbAdapter, user: UserData
) -> None:
    return entity_type.delete(uuid, user=user, db_adapter=db_adapter)



def create(
    entity_data: CreateEntityTypeDTO, user: UserData, db_adapter: DbAdapter
) -> List[EntityTypeDTO]:
    return entity_type.create(entity_data, user=user, db_adapter=db_adapter)
