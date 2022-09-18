from typing import List, Optional

from pydantic import BaseModel


class CreateEntityPostDTO(BaseModel):
    name: str
    fields: Optional[dict]
    links: Optional[List[str]]


class UpdateEntityPatchDTO(BaseModel):
    name: Optional[str]
    fields: Optional[dict]
    links: Optional[List[str]]



class CreateEntityDTO(BaseModel):
    name: str
    entity_type: str
    fields: Optional[dict]
    links: Optional[List[str]]


class UpdateEntityDTO(BaseModel):
    name: Optional[str]
    entity_type: str
    fields: Optional[dict]
    links: Optional[List[str]]


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
    links: List[str]
