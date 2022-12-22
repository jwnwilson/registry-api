from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel

from .link import LinkFields


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
    uuid: str
    name: str
    data_type: DataEnum
    input_type: InputEnum
    default: Optional[str]
    description: Optional[str]
    choices: Optional[List[str]]
    required: bool = False

    class Config:
        use_enum_values = True


Fields = Dict[str, FieldAttr]


class EntityTypeDTO(BaseModel):
    name: str
    description: str
    uuid: str
    fields: Fields
    links: LinkFields
    metadata: Optional[Dict] = {}

    class Config:
        use_enum_values = True


class CreateEntityTypeDTO(BaseModel):
    name: str
    description: Optional[str] = ""
    fields: Optional[Fields] = {}
    links: Optional[LinkFields] = {}
    metadata: Optional[Dict] = {}

    class Config:
        use_enum_values = True


class UpdateEntityTypeDTO(BaseModel):
    name: str
    description: str
    fields: Fields
    links: LinkFields
    metadata: Dict

    class Config:
        use_enum_values = True
