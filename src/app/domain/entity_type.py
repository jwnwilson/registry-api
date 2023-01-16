import logging
import uuid
from typing import List

from pydantic import ValidationError

from app.port.adapter.db import DbAdapter
from app.port.adapter.db.repository import ListParams
from app.port.domain.user import UserData
from app.port.domain.entity_type import (
    CreateEntityTypeDTO,
    EntityTypeDTO,
    UpdateEntityTypeDTO,
)

# TABLE = "entityType"

# logger = logging.getLogger(__name__)


# def list_entity_type(
#     query_param: ListParams, db_adapter: DbAdapter
# ) -> List[EntityTypeDTO]:
#     params = ListParams(limit=query_param.limit, filters=query_param.filters)
#     entity_types = db_adapter.list(TABLE, params)
    
#     return entity_types


# def read(uuid: str, db_adapter: DbAdapter) -> EntityTypeDTO:
#     data = db_adapter.read(TABLE, uuid)
#     return EntityTypeDTO(**data)


# def update(
#     uuid: str, entity_data: UpdateEntityTypeDTO, db_adapter: DbAdapter
# ) -> EntityTypeDTO:
#     update_data = entity_data.dict()
#     _id = db_adapter.update(table=TABLE, record_id=uuid, record_data=update_data)
#     data = db_adapter.read(TABLE, uuid)
#     return EntityTypeDTO(**data)


# def delete(uuid: str, db_adapter: DbAdapter) -> None:
#     db_adapter.delete(table=TABLE, record_id=uuid)
#     return


# def create(entity_data: CreateEntityTypeDTO, db_adapter: DbAdapter) -> EntityTypeDTO:
#     create_data = entity_data.dict()
#     entity_uuid = str(uuid.uuid4())
#     create_data["uuid"] = entity_uuid
#     _id = db_adapter.create(TABLE, record_data=create_data)
#     data = db_adapter.read(TABLE, entity_uuid)
#     return EntityTypeDTO(**data)
