import json
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
from app.ports.file import FileDTO
from .entity_type import list as list_entity_types, read as read_entity_type
from .exceptions import EntityValidationError

TABLE = "entity"

logger = logging.getLogger(__name__)


def _validate_fields(
        entity_data: List[Union[CreateEntityDTO, UpdateEntityDTO]],
        user: UserData,
        db_adapter: DbAdapter):
    # Get entity type for entity
    param = ListParams(
        filters={"name": entity_data.entity_type}
    )
    entity_types = list_entity_types(param, user, db_adapter)
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
        for entity in entity_data:
            validate(instance=entity.fields, schema=schema)
    except ValidationError as err:
        raise EntityValidationError(str(err))
        

def list(
    query_param: ListParams, user: UserData, db_adapter: DbAdapter
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


def _create_entity(entity_data: CreateEntityDTO, user: UserData, db_adapter: DbAdapter) -> int:
    create_data = entity_data.dict()
    entity_uuid = str(uuid.uuid4())
    create_data["uuid"] = entity_uuid
    create_data["owner"] = user.user_id
    create_data["organisation"] = user.organisation_id

    _id = db_adapter.create(TABLE, record_data=create_data)
    return _id


def create(
    entity_data: CreateEntityDTO, user: UserData, db_adapter: DbAdapter
) -> List[EntityDTO]:
    _validate_fields([entity_data], user, db_adapter)

    entity_uuid = _create_entity(entity_data, user, db_adapter)
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
    _validate_fields([entity_data], user, db_adapter)
    update_data = entity_data.dict()
    _id = db_adapter.update(table=TABLE, record_id=uuid, record_data=update_data)
    data = db_adapter.read(TABLE, uuid)
    return EntityDTO(**data)


def delete(
    uuid: str, entity_type: str, user: UserData, db_adapter: DbAdapter
) -> None:
    db_adapter.delete(table=TABLE, record_id=uuid)
    return


def parse_json(entity_type:str, parse_json: FileDTO, user:UserData, db_adapter: DbAdapter):
    reader = json.load(parse_json.file)
    entities = []
    for row in reader:
        entities.append(CreateEntityDTO(
            name=row["name"],
            entity_type=entity_type,
            fields=row["fields"],
            links=row["links"],
        ))
    _validate_fields(entities, user, db_adapter)
    return entities


def create_entities(entity_data: List[CreateEntityDTO], user:UserData, db_adapter: DbAdapter) -> List[EntityDTO]:
    entity_uuids = []

    for entity in entity_data:
        entity_uuids.append(
            _create_entity(entity, user, db_adapter)
        )
    
    params = ListParams(
        filters={
            '_id':{"$in":entity_uuids}
        },
        organisation=user.organisation_id
    )
    entity_records: List[EntityDTO] = list(params, user, db_adapter)
    return entity_records
