from typing import Any, Dict, Optional

from pydantic import BaseModel

from .link import LinkFields

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
