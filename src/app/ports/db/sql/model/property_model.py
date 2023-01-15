from typing import List

from pydantic import BaseModel

from ..repository import Repository


class PropteryDTO(BaseModel):
    street_name: str
    postal_code: str
    city: str
    county: str
    state_code: str
    country: str


class PropertyRepository(Repository):
    pass
