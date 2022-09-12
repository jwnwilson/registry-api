from typing import List
from pydantic import BaseModel


class Entity(BaseModel):
    name: str
    uuid: str
    owner: str
    fields: dict
    links: List[str]
