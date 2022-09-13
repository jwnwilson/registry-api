from sqlite3 import dbapi2
from typing import List
import uuid

from hex_lib.ports.db import DbAdapter, ListParams
from hex_lib.ports.user import UserData
from ports.entity_type import EntityTypeDTO, QueryParam, CreateEntityTypeDTO

TABLE = "entityType"


def list(
    query_param: QueryParam, user: UserData, db_adapter: DbAdapter
) -> List[EntityTypeDTO]:
    params = ListParams(
        limit=query_param.limit,
        filters=query_param.filters,
        organisation=user.organisation_id
    )
    data = db_adapter.list(TABLE, params)
    return [EntityTypeDTO(**x) for x in data]


def create(
    entity_data: CreateEntityTypeDTO, user: UserData, db_adapter: DbAdapter
) -> EntityTypeDTO:
    create_data = entity_data.dict()
    entity_uuid = str(uuid.uuid4())
    create_data["uuid"] = entity_uuid
    create_data["owner"] = user.user_id
    create_data["organisation"] = user.organisation_id
    _id = db_adapter.create(TABLE, create_data)
    data = db_adapter.read(TABLE, entity_uuid)
    return EntityTypeDTO(**data)