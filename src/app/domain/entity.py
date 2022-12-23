import json
import logging
import uuid
from typing import List, Union

from hex_lib.ports.db import DbAdapter, ListParams
from hex_lib.ports.user import UserData
from jsonschema import validate  # type: ignore
from jsonschema.exceptions import ValidationError as JsonValidationError  # type: ignore
from pydantic import ValidationError

from app.ports.entity import CreateEntityDTO, EntityDTO, QueryParam, UpdateEntityDTO
from app.ports.entity_type import EntityTypeDTO
from app.ports.file import FileDTO

from .entity_type import list as list_entity_types
from .entity_type import read as read_entity_type
from .exceptions import EntityValidationError

TABLE = "entity"

logger = logging.getLogger(__name__)


def parse_json(entity_type: str, parse_json: FileDTO, db_adapter: DbAdapter):
    json_data = json.load(parse_json.file)
    entities = []
    for entity in json_data:
        entities.append(
            CreateEntityDTO(
                name=entity["name"],
                entity_type=entity_type,
                fields=entity.get("fields", []),
                links=entity.get("links", []),
            )
        )
    _validate_fields(entities, db_adapter)
    return entities


def _validate_fields(
    entity_data: Union[List[CreateEntityDTO], List[UpdateEntityDTO], List[EntityDTO]],
    db_adapter: DbAdapter,
):
    # Get entity type for entity
    entity_type_name = entity_data[0].entity_type
    param = ListParams(filters={"name": entity_type_name})
    entity_types = list_entity_types(param, db_adapter)
    entity_types_len = len(entity_types)

    try:
        assertion_error_msg = f"Unknown Entity Type: {entity_type_name}"
        assert entity_types_len == 1, assertion_error_msg
    except AssertionError as err:
        raise EntityValidationError(str(err))

    entity_type: EntityTypeDTO = entity_types[0]
    entity_type_data = entity_type.dict()
    required = []

    # build properties from entity field data
    for key in entity_type_data["fields"]:
        field_dict = entity_type_data["fields"][key]
        required += [key] if field_dict["required"] else []
        entity_type_data["fields"][key] = {
            k: v for k, v in field_dict.items() if k not in ["required", "choices"]
        }

    # Validate Fields
    schema = {
        "type": "object",
        "properties": entity_type_data["fields"],
        "required": required,
    }
    try:
        for entity in entity_data:
            validate(instance=entity.fields, schema=schema)
    except JsonValidationError as err:
        raise EntityValidationError(str(err))


def list(query_param: QueryParam, db_adapter: DbAdapter) -> List[EntityDTO]:

    filters = query_param.filters or {}
    filters.update({"entity_type": query_param.entity_type})
    params = ListParams(limit=query_param.limit, filters=filters)
    data = db_adapter.list(TABLE, params)
    entity_types = []
    for entity in data:
        try:
            entity_types.append(EntityDTO(**entity))
        except ValidationError:
            uuid = entity.get("uuid")
            logger.warn(f"Invalid record uuid: '{uuid}', skipping...")

    return entity_types


def _create_entity(
    entity_data: Union[CreateEntityDTO, EntityDTO],
    db_adapter: DbAdapter,
) -> EntityDTO:
    create_data = entity_data.dict()
    entity_uuid = str(uuid.uuid4())
    create_data["uuid"] = entity_uuid

    entity_data = db_adapter.create(TABLE, record_data=create_data)
    return EntityDTO(**create_data)


def create(entity_data: CreateEntityDTO, db_adapter: DbAdapter) -> EntityDTO:
    _validate_fields([entity_data], db_adapter)

    entity_dto = _create_entity(entity_data, db_adapter)
    return entity_dto


def create_entities(
    entity_data: Union[List[CreateEntityDTO], List[EntityDTO]],
    db_adapter: DbAdapter,
) -> List[EntityDTO]:
    entity_dtos = []

    for entity in entity_data:
        entity_dtos.append(_create_entity(entity, db_adapter))
    return entity_dtos


def create_entities_from_file(
    entity_type: str,
    fileDTO: FileDTO,
    db_adapter: DbAdapter,
) -> List[EntityDTO]:
    
    entities_dto: List[EntityDTO] = parse_json(entity_type, fileDTO, db_adapter)
    entities: List[EntityDTO] = create_entities(entities_dto, db_adapter=db_adapter)
    return entities



def read(uuid: str, entity_type: str, db_adapter: DbAdapter) -> EntityDTO:
    data = db_adapter.read(TABLE, uuid)
    return EntityDTO(**data)


def update(
    uuid: str,
    entity_type: str,
    entity_data: UpdateEntityDTO,
    db_adapter: DbAdapter,
) -> EntityDTO:
    _validate_fields([entity_data], db_adapter)
    update_data = entity_data.dict()
    _id = db_adapter.update(table=TABLE, record_id=uuid, record_data=update_data)
    data = db_adapter.read(TABLE, uuid)
    return EntityDTO(**data)


def delete(uuid: str, entity_type: str, db_adapter: DbAdapter) -> None:
    db_adapter.delete(table=TABLE, record_id=uuid)
    return
