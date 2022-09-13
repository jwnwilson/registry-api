from typing import List, Optional

from pydantic import BaseModel


class CreateEntityTypeDTO(BaseModel):
    name: str
    entity_type: str
    fields: dict
    links: Optional[List[str]]


class UpdateEntityTypeDTO(BaseModel):
    name: Optional[str]
    fields: Optional[dict]
    links: Optional[List[str]]
    owner: Optional[str]
    organisation: Optional[str]


class QueryParam(BaseModel):
    name: Optional[str]
    entity_type: Optional[str]
    uuid: Optional[str]


class EntityDTO(BaseModel):
    name: str
    entity_type: str
    uuid: str
    owner: str
    organisation: str
    fields: dict
    links: List[str]
