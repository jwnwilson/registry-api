import logging
from typing import List
from pydantic import ValidationError
import uuid

from hex_lib.ports.db import DbAdapter, ListParams
from hex_lib.ports.user import UserData

from app.ports.entity_type import EntityTypeDTO, CreateEntityTypeDTO, UpdateEntityTypeDTO

TABLE = "entityType"

logger = logging.getLogger(__name__)


def list(
    query_param: ListParams, user: UserData, db_adapter: DbAdapter
) -> List[EntityTypeDTO]:
    params = ListParams(
        limit=query_param.limit,
        filters=query_param.filters,
        organisation=user.organisation_id
    )
    data = db_adapter.list(TABLE, params)
    entity_types = []
    for entity in data:
        try:
            entity_types.append(EntityTypeDTO(**entity))
        except ValidationError as err:
            uuid = entity.get("uuid")
            logger.warn(f"Invalid record uuid: '{uuid}', error: {err}\n skipping...")

    return entity_types


def read(
    uuid:str, user: UserData, db_adapter: DbAdapter
) -> EntityTypeDTO:
    data = db_adapter.read(TABLE, uuid)
    return EntityTypeDTO(**data)


def update(
    uuid:str, entity_data: UpdateEntityTypeDTO, user: UserData, db_adapter: DbAdapter
) -> EntityTypeDTO:
    update_data = entity_data.dict()
    _id = db_adapter.update(table=TABLE, record_id=uuid, record_data=update_data)
    data = db_adapter.read(TABLE, uuid)
    return EntityTypeDTO(**data)


def delete(
    uuid: str, user: UserData, db_adapter: DbAdapter
) -> None:
    db_adapter.delete(table=TABLE, record_id=uuid)
    return


def create(
    entity_data: CreateEntityTypeDTO, user: UserData, db_adapter: DbAdapter
) -> EntityTypeDTO:
    create_data = entity_data.dict()
    entity_uuid = str(uuid.uuid4())
    create_data["uuid"] = entity_uuid
    create_data["owner"] = user.user_id
    create_data["organisation"] = user.organisation_id
    _id = db_adapter.create(TABLE, record_data=create_data)
    data = db_adapter.read(TABLE, entity_uuid)
    return EntityTypeDTO(**data)