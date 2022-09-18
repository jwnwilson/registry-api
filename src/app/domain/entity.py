from typing import List, Union
import logging
from pydantic import ValidationError
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import uuid

from hex_lib.ports.db import DbAdapter, ListParams
from hex_lib.ports.user import UserData

from app.ports.entity import CreateEntityDTO, UpdateEntityDTO, EntityDTO, QueryParam
from app.ports.entity_type import EntityTypeDTO
from .entity_type import TABLE as ENTITY_TYPE_TABLE
from .exceptions import EntityValidationError

TABLE = "entity"

logger = logging.getLogger(__name__)


def _validate_fields(entity_data: Union[CreateEntityDTO, UpdateEntityDTO], db_adapter: DbAdapter):
    # Get entity type for entity
    param = ListParams(
        filters={"name": entity_data.entity_type}
    )
    entity_types = db_adapter.list(ENTITY_TYPE_TABLE, param)
    entity_types_len = len(entity_types)
    assertion_error_msg = f"Entity Type: {entity_data.entity_type} has {entity_types_len} records, 1 expected"
    assert entity_types_len == 1, assertion_error_msg

    entity_type: EntityTypeDTO = EntityTypeDTO(
        **entity_types[0]
    )

    entity_type_data = entity_type.dict()
    required = []

    # build properties from entity field data
    for key in entity_type_data["fields"]:
        field_dict = entity_type_data["fields"][key]
        required += [key] if field_dict["required"] else []
        entity_type_data["fields"][key] = {k: v for k,v in field_dict.items() if k not in ["required", "choices"]}

    # Validate Fields
    schema = {
        "type" : "object",
        "properties" : entity_type_data["fields"],
        "required": required
    }
    try:
        validate(instance=entity_data.fields, schema=schema)
    except ValidationError as err:
        raise EntityValidationError(str(err))
        

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
    _validate_fields(entity_data, db_adapter)

    create_data = entity_data.dict()
    entity_uuid = str(uuid.uuid4())
    create_data["uuid"] = entity_uuid
    create_data["owner"] = user.user_id
    create_data["organisation"] = user.organisation_id

    _id = db_adapter.create(TABLE, record_data=create_data)
    data = db_adapter.read(TABLE, entity_uuid)
    return EntityDTO(**data)


def read(
    uuid:str, entity_type:str, user: UserData, db_adapter: DbAdapter
) -> List[EntityDTO]:
    data = db_adapter.read(TABLE, uuid)
    return EntityDTO(**data)


def update(
    uuid:str, entity_type: str, entity_data: UpdateEntityDTO, user: UserData, db_adapter: DbAdapter
) -> EntityDTO:
    _validate_fields(entity_data, db_adapter)
    update_data = entity_data.dict()
    _id = db_adapter.update(table=TABLE, record_id=uuid, record_data=update_data)
    data = db_adapter.read(TABLE, uuid)
    return EntityDTO(**data)


def delete(
    uuid: str, entity_type: str, user: UserData, db_adapter: DbAdapter
) -> None:
    db_adapter.delete(table=TABLE, record_id=uuid)
    return
