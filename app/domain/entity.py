from typing import List
import logging
from pydantic import ValidationError
import uuid

from hex_lib.ports.db import DbAdapter, ListParams
from hex_lib.ports.user import UserData
from ports.entity import CreateEntityDTO, EntityDTO, QueryParam


TABLE = "entity"

logger = logging.getLogger(__name__)


def list(
    query_param: QueryParam, user: UserData, db_adapter: DbAdapter
) -> List[EntityDTO]:

    filters = query_param.filters or {}
    filters.update({
        "entity_type": query_param.entity_type
    })
    params = ListParams(
        limit=query_param.limit,
        filters=filters,
        organisation=user.organisation_id
    )
    data = db_adapter.list(TABLE, params)
    entity_types = []
    for entity in data:
        try:
            entity_types.append(EntityDTO(**entity))
        except ValidationError:
            uuid = entity.get("uuid")
            logger.warn(f"Invalid record uuid: '{uuid}', skipping...")

    return entity_types


def create(
    entity_data: CreateEntityDTO, user: UserData, db_adapter: DbAdapter
) -> List[EntityDTO]:
    create_data = entity_data.dict()
    entity_uuid = str(uuid.uuid4())
    create_data["uuid"] = entity_uuid
    create_data["owner"] = user.user_id
    create_data["organisation"] = user.organisation_id
    print(create_data)
    _id = db_adapter.create(TABLE, record_data=create_data)
    data = db_adapter.read(TABLE, entity_uuid)
    return EntityDTO(**data)
