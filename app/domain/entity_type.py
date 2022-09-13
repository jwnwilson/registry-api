from sqlite3 import dbapi2
from typing import List

from hex_lib.ports.db import DbAdapter, ListParams
from hex_lib.ports.user import UserData
from ports.entity_type import EntityTypeDTO, QueryParam

TABLE = "entityType"


def list(
    query_param: QueryParam, user: UserData, db_adapter: DbAdapter
) -> List[EntityTypeDTO]:
    params = ListParams(limit=query_param.limit, filters=query_param.filters)
    data = db_adapter.list(TABLE, params)
    return [EntityTypeDTO(**x) for x in data]


def create(
    entity_data: EntityTypeDTO, user: UserData, db_adapter: DbAdapter
) -> EntityTypeDTO:
    _id = db_adapter.create(TABLE, entity_data.dict())
    data = db_adapter.read(TABLE, entity_data.uuid)
    return EntityTypeDTO(**data)