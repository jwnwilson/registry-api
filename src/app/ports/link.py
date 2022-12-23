from enum import Enum
from typing import Dict

from pydantic import BaseModel


class LinkType(Enum):
    name: str
    uuid: str


class Link(BaseModel):
    entity_type: str
    link_type: str

    class Config:
        use_enum_values = True


LinkFields = Dict[str, Link]
