from typing import Dict, List, Optional

from pydantic import BaseModel

from .link import Link


class CreateEntityPostDTO(BaseModel):
    name: str
    description: Optional[str] = ""
    fields: Optional[dict]
    links: Dict[str, Link] = {}


class UpdateEntityPatchDTO(BaseModel):
    name: Optional[str]
    description: str
    fields: Optional[dict]
    links: Dict[str, Link] = {}


class CreateEntityDTO(BaseModel):
    name: str
    description: Optional[str] = ""
    entity_type: str
    fields: Optional[dict]
    links: Dict[str, Link] = {}


class UpdateEntityDTO(BaseModel):
    name: Optional[str]
    description: str
    entity_type: str
    fields: Optional[dict]
    links: Dict[str, Link] = {}


class QueryParam(BaseModel):
    name: Optional[str]
    entity_type: Optional[str]
    uuid: Optional[str]
    limit: Optional[int]
    filters: Optional[dict]


class EntityDTO(BaseModel):
    name: str
    description: str
    entity_type: str
    uuid: str
    fields: dict
    links: Dict[str, Link] = {}
