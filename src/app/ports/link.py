from enum import Enum
from typing import Dict

from pydantic import BaseModel


class LinkType(Enum):
    bi_directional = "bi_directional"
    related_to = "related_to"
    related_fom = "related_from"


class Link(BaseModel):
    direction: LinkType = LinkType.bi_directional
    entity_type: str

    class Config:
        use_enum_values = True


LinkFields = Dict[str, Link]
