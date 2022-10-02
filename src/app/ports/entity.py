from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class LinkType(Enum):
    bi_directional = 'bi_directional'
    related_to = 'related_to'
    related_fom = 'related_fom'


class Link(BaseModel):
    uuid: str
    direction : LinkType = LinkType.bi_directional

    class Config:  
        use_enum_values = True


class CreateEntityPostDTO(BaseModel):
    name: str
    fields: Optional[dict]
    links: Optional[List[Link]]


class UpdateEntityPatchDTO(BaseModel):
    name: Optional[str]
    fields: Optional[dict]
    links: Optional[List[Link]]


class CreateEntityDTO(BaseModel):
    name: str
    entity_type: str
    fields: Optional[dict]
    links: Optional[List[Link]]


class UpdateEntityDTO(BaseModel):
    name: Optional[str]
    entity_type: str
    fields: Optional[dict]
    links: Optional[List[Link]]


class QueryParam(BaseModel):
    name: Optional[str]
    entity_type: Optional[str]
    uuid: Optional[str]
    limit: Optional[int]
    filters: Optional[dict]


class EntityDTO(BaseModel):
    name: str
    entity_type: str
    uuid: str
    owner: str
    organisation: Optional[str]
    fields: dict
    links: List[Link]
