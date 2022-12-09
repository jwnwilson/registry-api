from typing import List

from hex_lib.ports.db import DbAdapter
from hex_lib.ports.user import UserData

from app.domain import entity
from app.ports.entity import CreateEntityDTO, EntityDTO, QueryParam, UpdateEntityDTO
from app.ports.file import FileDTO


def list(
    query_param: QueryParam, db_adapter: DbAdapter, user: UserData
) -> List[EntityDTO]:
    return entity.list(query_param, db_adapter=db_adapter)


def read(
    uuid: str, entity_type: str, db_adapter: DbAdapter, user: UserData
) -> EntityDTO:
    return entity.read(uuid, entity_type, db_adapter=db_adapter)


def update(
    uuid: str,
    entity_type: str,
    entity_data: UpdateEntityDTO,
    db_adapter: DbAdapter,
    user: UserData,
) -> EntityDTO:
    return entity.update(
        uuid, entity_type, entity_data=entity_data, db_adapter=db_adapter
    )


def delete(uuid: str, entity_type: str, db_adapter: DbAdapter, user: UserData) -> None:
    return entity.delete(uuid, entity_type, db_adapter=db_adapter)


def create(
    entity_data: CreateEntityDTO, user: UserData, db_adapter: DbAdapter
) -> EntityDTO:
    return entity.create(entity_data, db_adapter=db_adapter)


def create_entities_from_file(
    entity_type: str, file: FileDTO, user: UserData, db_adapter: DbAdapter
) -> List[EntityDTO]:
    entities_dto: List[EntityDTO] = entity.parse_json(entity_type, file, db_adapter)
    return entity.create_entities(entities_dto, db_adapter=db_adapter)
