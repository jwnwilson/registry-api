from app.port.domain.entity import EntityDTO
from ..repository import MongoRepository


class EntityRepository(MongoRepository):
    model_dto = EntityDTO
    table = "entity"

