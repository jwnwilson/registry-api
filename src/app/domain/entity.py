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
from app.ports.link_type import LinkDTO, LinkTypeDTO

from .entity_type import list_entity_type
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
    return entities


def get_entities_by_links(uuids: List[str], db_adapter: DbAdapter) -> List[EntityDTO]:
    db_params = ListParams(filters={"uuid": {"$in": uuids}})
    entities: List[EntityDTO] = [
        EntityDTO(**data) for data in db_adapter.list(TABLE, db_params)
    ]
    return entities


def _edit_linked_entity_backref(
    entity: EntityDTO, linked_entity: EntityDTO, link_types: List[LinkTypeDTO]
):
    # Edit links
    link_type = entity.links[linked_entity.uuid].link_type
    back_link_type = [x for x in filter(lambda x: x.name == link_type, link_types)][0]
    linked_entity.links[entity.uuid] = LinkDTO(
        entity_type=entity.entity_type, link_type=back_link_type.name
    )


def create_back_links(entity: EntityDTO, db_adapter: DbAdapter):
    # Create back links for entities this is linked to

    # Get related entities
    linked_entities = get_entities_by_links(
        [link for link in entity.links],
        db_adapter
    )

    # Get link types
    link_types: List[LinkTypeDTO] = [
        LinkTypeDTO(**data) for data in db_adapter.list("LinkType", ListParams())
    ]

    # Create new links
    for linked_entity in linked_entities:
        _edit_linked_entity_backref(entity, linked_entity, link_types)
        db_adapter.update(TABLE, linked_entity.uuid, linked_entity.dict())


def update_back_links(current_entity: EntityDTO, new_entity: EntityDTO, db_adapter: DbAdapter):
    # Update back links for entities this is linked to

    # Get link diff
    removed_links = list(filter(
        lambda uuid: uuid not in new_entity.links.keys(), current_entity.links.keys()
    ))

    # Get related entities
    linked_entities: List[EntityDTO] = get_entities_by_links(
        [link for link in (list(new_entity.links.keys()) + removed_links)],
        db_adapter
    )
    # Get link types
    link_types: List[LinkTypeDTO] = [
        LinkTypeDTO(**data) for data in db_adapter.list("linkType", ListParams())
    ]

    for linked_entity in linked_entities:
        if linked_entity.uuid in removed_links:
            # Delete remove links
            del linked_entity.links[current_entity.uuid]
        else:
            # Edit links
            _edit_linked_entity_backref(new_entity, linked_entity, link_types)
        db_adapter.update(TABLE, linked_entity.uuid, linked_entity.dict())


def _validate_fields(
    entity_data: Union[List[CreateEntityDTO], List[UpdateEntityDTO], List[EntityDTO]],
    db_adapter: DbAdapter,
):
    # Get entity type for entity
    entity_type_name = entity_data[0].entity_type
    param = ListParams(filters={"name": entity_type_name})
    entity_types = list_entity_type(param, db_adapter)
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


def list_entities(query_param: QueryParam, db_adapter: DbAdapter) -> List[EntityDTO]:
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
    _validate_fields([entity_data], db_adapter)  # type: ignore
    create_data = entity_data.dict()
    entity_uuid = str(uuid.uuid4())
    create_data["uuid"] = entity_uuid

    create_back_links(entity_data, db_adapter)
    entity_data = db_adapter.create(TABLE, record_data=create_data)
    entity = EntityDTO(**create_data)

    return entity


def create(entity_data: CreateEntityDTO, db_adapter: DbAdapter) -> EntityDTO:
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
    entity_data: UpdateEntityDTO,
    db_adapter: DbAdapter,
) -> EntityDTO:
    _validate_fields([entity_data], db_adapter)
    current_entity: EntityDTO = EntityDTO(**db_adapter.read(TABLE, uuid))
    new_entity = EntityDTO(**{**current_entity.dict(), **entity_data.dict()})

    update_back_links(current_entity, new_entity, db_adapter)

    _id = db_adapter.update(table=TABLE, record_id=uuid, record_data=new_entity.dict())
    data = db_adapter.read(TABLE, uuid)
    entity = EntityDTO(**data)

    return entity


def delete(uuid: str, db_adapter: DbAdapter) -> None:
    db_adapter.delete(table=TABLE, record_id=uuid)
    return
