from enum import Enum
from pickletools import int4
from typing import Optional

from pydantic import BaseModel


class FieldEnum(Enum):
    string = 'string'
    int = 'int'
    float = 'float'


FieldType = dict[str, FieldEnum]


class QueryParam(BaseModel):
    limit: Optional[int]
    filters: Optional[dict]


class EntityTypeDTO(BaseModel):
    name: str
    uuid: str
    owner: str
    organisation: Optional[str]
    fields: FieldType

    class Config:  
        use_enum_values = True


class CreateEntityTypeDTO(BaseModel):
    name: str
    fields: FieldType

    class Config:  
        use_enum_values = True


class UpdateEntityTypeDTO(BaseModel):
    uuid: str
    name: Optional[str]
    fields: Optional[FieldType]

    class Config:  
        use_enum_values = True

