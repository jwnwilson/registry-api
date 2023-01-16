from sqlalchemy import Column, Integer, String

from ..repository import SQLRepository
from .base import BaseSQLModel
from app.domain.entity_type import EntityTypeDTO


class EntityType(BaseSQLModel):
    pass


class EntityTypeSQLRepository(SQLRepository):
    model = EntityType
    model_dto = EntityTypeDTO

