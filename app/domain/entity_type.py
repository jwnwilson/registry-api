from pydantic import BaseModel


class EntityType(BaseModel):
    name: str
    uuid: str
    owner: str
    fields: dict