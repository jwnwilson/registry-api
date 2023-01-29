import json
import logging
import uuid
from typing import List, Union, Any, Dict, Optional

from jsonschema import validate  # type: ignore
from jsonschema.exceptions import ValidationError as JsonValidationError  # type: ignore
from pydantic import ValidationError, BaseModel

from app.port.adapter.db import DbAdapter, Repositories
from .entity_type import EntityTypeDTO
from .file import FileDTO
from .link_type import LinkDTO, LinkTypeDTO, LinkFields
from .exceptions import EntityValidationError

TABLE = "entity"

logger = logging.getLogger(__name__)


Fields = Dict[str, Any]


class EntityDTO(BaseModel):
    name: str
    description: str
    entity_type: str
    uuid: str
    fields: Fields
    links: LinkFields
    metadata: Dict


class CreateEntityPostDTO(BaseModel):
    name: str
    description: Optional[str] = ""
    fields: Optional[Fields] = {}
    links: Optional[LinkFields] = {}
    metadata: Optional[Dict] = {}


class UpdateEntityPatchDTO(BaseModel):
    name: str
    description: str
    fields: Fields
    links: LinkFields
    metadata: Dict


class CreateEntityDTO(BaseModel):
    name: str
    description: Optional[str] = ""
    entity_type: str
    fields: Optional[Fields]
    links: Optional[LinkFields] = {}
    metadata: Optional[Dict] = {}


class UpdateEntityDTO(BaseModel):
    name: str
    description: str
    entity_type: str
    fields: Fields
    links: LinkFields
    metadata: Dict


class QueryParam(BaseModel):
    name: Optional[str]
    entity_type: Optional[str]
    uuid: Optional[str]
    limit: Optional[int]
    filters: Optional[dict]



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


def get_entities_by_links(uuids: List[str], repos: Repositories) -> List[EntityDTO]:
    db_params = dict(filters={"uuid": {"$in": uuids}})
    entities: List[EntityDTO] = repos.entity.read_multi(db_params)
    return entities


def _edit_linked_entity_backref(
    entity: EntityDTO, linked_entity: EntityDTO, link_types: List[LinkTypeDTO]
) -> bool:
    # Edit links
    link_type = entity.links[linked_entity.uuid].link_type
    back_link_type = [x for x in filter(lambda x: x.name == link_type, link_types)][0]
    new_link = LinkDTO(
        entity_type=entity.entity_type, link_type=back_link_type.name
    )
    if linked_entity.links[entity.uuid] != new_link:
        linked_entity.links[entity.uuid] = new_link
        return True
    else:
        return False


def create_back_links(entity: EntityDTO, repos: Repositories):
    # Create back links for entities this is linked to

    # Get related entities
    linked_entities = get_entities_by_links([link for link in entity.links], db_adapter)

    # Get link types
    link_types: List[LinkTypeDTO] = repos.link_type.read_multi()

    # Create new links
    for linked_entity in linked_entities:
        _edit_linked_entity_backref(entity, linked_entity, link_types)
        repos.entity.update(linked_entity.uuid, linked_entity)


def update_back_links(
    current_entity: EntityDTO, updated_entity: EntityDTO, repos: Repositories
):
    # Update back links for entities this is linked to

    # Get link diff
    removed_links = list(
        filter(
            lambda uuid: uuid not in updated_entity.links.keys(),
            current_entity.links.keys(),
        )
    )

    # Get related entities
    linked_entities: List[EntityDTO] = get_entities_by_links(
        [link for link in (list(updated_entity.links.keys()) + removed_links)], repos
    )
    # Get link types
    link_types: List[LinkTypeDTO] = repos.link_type.read_multi()

    for linked_entity in linked_entities:
        modified = False
        if linked_entity.uuid in removed_links:
            # Delete remove links
            del linked_entity.links[current_entity.uuid]
            modified = True
        else:
            # Edit links
            modified = _edit_linked_entity_backref(updated_entity, linked_entity, link_types)
        if modified:
            repos.entity.update(linked_entity.uuid, linked_entity)


def validate_fields(
    entity_data: Union[List[CreateEntityDTO], List[UpdateEntityDTO], List[EntityDTO]],
    repos: Repositories,
):
    # Get entity type for entity
    entity_type_name = entity_data[0].entity_type
    filters = {"name": entity_type_name}
    entity_types = repos.entity_type.read_multi(filters=filters)
    entity_types_len = len(entity_types)

    try:
        assert entity_types_len == 1, f"Unknown Entity Type: {entity_type_name}"
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


def create_entities_from_file(
    entity_type: str,
    fileDTO: FileDTO,
    repositories: Repositories,
) -> List[EntityDTO]:
    entities_dto: List[EntityDTO] = parse_json(entity_type, fileDTO, repositories)
    entities: List[EntityDTO] = repositories.entity.create_multi(entities_dto)
    return entities

