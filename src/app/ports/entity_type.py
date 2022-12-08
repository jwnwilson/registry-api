from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel

from .link import Link


class DataEnum(Enum):
    string = "string"
    number = "number"
    url = "url"
    enum = "enum"


class InputEnum(Enum):
    text = "text"
    text_area = "textArea"
    select = "select"
    checkbox = "checkbox"
    radio = "radio"


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
    fields: FieldType
    links: Optional[Dict[str, Link]]

    class Config:
        use_enum_values = True


class CreateEntityTypeDTO(BaseModel):
    name: str
    fields: FieldType
    links: Optional[Dict[str, Link]]

    class Config:
        use_enum_values = True


class UpdateEntityTypeDTO(BaseModel):
    name: Optional[str]
    fields: Optional[FieldType]
    links: Optional[Dict[str, Link]]

    class Config:
        use_enum_values = True
