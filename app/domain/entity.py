from typing import List

from hex_lib.ports.db import DbAdapter, ListParams
from hex_lib.ports.user import UserData
from ports.entity import EntityDTO, QueryParam


def list(
    query_param: QueryParam, user: UserData, db_adapter: DbAdapter
) -> List[EntityDTO]:
    params = ListParams(limit=query_param.limit, filters=query_param.filters)
    data = db_adapter.list(params)
    return [EntityDTO(**x) for x in data]


def create(
    create_dto: EntityDTO, user: UserData, db_adapter: DbAdapter
) -> List[EntityDTO]:
    params = ListParams(limit=query_param.limit, filters=query_param.filters)
    data = db_adapter.create(params)
    return [EntityDTO(**x) for x in data]
