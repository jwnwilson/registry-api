from typing import List, Optional

from pydantic import BaseModel


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
