from app.domain.entity_type import EntityTypeDTO
from ..repository import MongoRepository


class EntityTypeRepository(MongoRepository):
    model_dto = EntityTypeDTO
    table = "entityType"

