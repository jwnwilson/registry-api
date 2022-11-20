from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class DataEnum(Enum):
    string = 'string'
    number = 'number'
    url = 'url'
    enum = 'enum'


class InputEnum(Enum):
    text = 'text'
    text_area = 'textArea'
    select = 'select'
    checkbox = 'checkbox'
    radio = 'radio'


class FieldAttr(BaseModel):
    data_type: DataEnum
    input_type: InputEnum
    default: Optional[str]
    description: Optional[str]
    choices: Optional[List[str]]
    required: bool = False

    class Config:  
        use_enum_values = True


FieldType = dict[str, FieldAttr]


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
    name: Optional[str]
    fields: Optional[FieldType]
    owner: Optional[str]
    organisation: Optional[str]

    class Config:  
        use_enum_values = True

