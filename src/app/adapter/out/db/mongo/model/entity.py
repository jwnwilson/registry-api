import uuid
from typing import List

from app.domain.entity import EntityDTO, validate_fields, update_entity_links, create_links
from ..repository import MongoRepository


class EntityRepository(MongoRepository):
    model_dto = EntityDTO
    table = "entity"

    def create(self, record_data: EntityDTO) -> EntityDTO:
        validate_fields(
            record_data,
            self.repos
        )
        create_data = record_data.dict()
        create_data["uuid"] = str(uuid.uuid4())
        create_links(record_data, self.repos)

        return super().create(record_data)

    def update(self, record_id: str, record_data: model_dto) -> model_dto:
        validate_fields(
            record_data,
            self.repos
        )
        current_entity: EntityDTO = self.read(record_id)
        # Update current entity with new data
        updated_entity = EntityDTO(**{**current_entity.dict(), **record_data.dict()})

        update_entity_links(current_entity, updated_entity, self.repos)
        return super().update(record_id, updated_entity)