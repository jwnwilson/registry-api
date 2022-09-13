from lib2to3.pgen2.token import OP
from typing import Optional

from pydantic import BaseModel


class QueryParam(BaseModel):
    limit: Optional[int]
    filters: Optional[dict]


class EntityTypeDTO(BaseModel):
    name: str
    uuid: str
    owner: str
    organisation: str
    fields: dict


class CreateEntityTypeDTO(BaseModel):
    name: str
    owner: str
    organisation: str
    fields: dict


class UpdateEntityTypeDTO(BaseModel):
    name: Optional[str]
    uuid: str
    owner: Optional[str]
    organisation: Optional[str]
    fields: Optional[dict]

