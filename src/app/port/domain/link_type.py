from enum import Enum
from typing import Dict

from pydantic import BaseModel


# Type of link
class LinkTypeDTO(BaseModel):
    name: str
    uuid: str
    back_link: str


class CreateLinkTypeDTO(BaseModel):
    entity_type: str
    link_type: str


class UpdateLinkTypeDTO(BaseModel):
    entity_type: str
    link_type: str


# Links between entities
class LinkDTO(BaseModel):
    entity_type: str
    link_type: str


LinkFields = Dict[str, LinkDTO]
