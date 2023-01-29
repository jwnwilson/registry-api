from __future__ import annotations
import uuid
from typing import Dict, Optional, Type, TypeVar, Any, List, TYPE_CHECKING
from pydantic import BaseModel, ValidationError
import logging
from pymongo.errors import DuplicateKeyError

from app.port.adapter.db.repository import Repository, PaginatedData
from ..exceptions import DuplicateRecord, RecordNotFound
from .adapter import MongoDbAdapter

if TYPE_CHECKING:
    from .repositories import Repositories

ModelType = TypeVar("ModelType", bound=BaseModel)
ModelDTOType = TypeVar("ModelDTOType", bound=BaseModel)

logger = logging.getLogger(__name__)


class MongoRepository(Repository):
    model_dto: Type[ModelDTOType]
    table: str

    def __init__(self, db: MongoDbAdapter, repos: Repositories):
        self.db: MongoDbAdapter = db
        self.repos: Repositories = repos

    def get_offset(self, page_size: int, page_number: int):
        return (page_number - 1) * page_size

    def paginate(self, data: Any, page_number: int, page_size: int):
        if page_size > 0 and page_number >= 1:
            offset = self.get_offset(page_size, page_number)
            data = data.skip(offset).limit(page_size)

        return data

    def read_multi(self, filters: Dict, page_size: int = 100, page_number: int = 1) -> PaginatedData:
        collection = self.db.db[self.table]
        data = collection.find(filters)
        data = self.paginate(data, page_number=page_number, page_size=page_size)
        entities = []
        for entity in data:
            try:
                entities.append(self.model_dto(**entity))
            except ValidationError as err:
                uuid = entity.get("uuid")
                logger.warn(
                    f"Invalid record uuid: '{uuid}', error: {err}\n skipping..."
                )

        return PaginatedData(
            results=entities, total=len(entities), page_size=page_size, page_number=page_number
        )

    def read(self, record_id: str) -> model_dto:
        collection = self.db.db[self.table]
        record: Optional[dict] = collection.find_one({"uuid": record_id})
        if not record:
            raise RecordNotFound(f"Record not found uuid: '{record_id}'")
        return self.model_dto(**record)

    def create(self, record_data: model_dto) -> model_dto:
        collection = self.db.db[self.table]
        record_id = str(uuid.uuid4())
        mongo_data = {**record_data.dict(), **{"_id": record_id}}
        try:
            collection.insert_one(mongo_data)
            return self.read(record_id=record_id)
        except DuplicateKeyError:
            error = f"Duplicate record uuid: '{record_id}'"
            logger.info(error)
            raise DuplicateRecord(error)

    def create_multi(self, record_data: List[model_dto]) -> List[model_dto]:
        entity_dtos = []
        for entity in record_data:
            entity_dtos.append(self.create(entity))
        return entity_dtos

    def delete(self, record_id: str):
        collection = self.db.db[self.table]
        collection.delete_one({"uuid": record_id})

    def update(self, record_id: str, record_data: model_dto) -> model_dto:
        collection = self.db.db[self.table]
        record: Optional[dict] = collection.find_one({"uuid": record_id})
        if not record:
            raise RecordNotFound(f"Record not found uuid: '{record_id}'")

        query = {"uuid": record_id}
        record.update(record_data.dict())
        updated_record: dict = collection.replace_one(
            query, record, upsert=True
        ).raw_result
        return self.model_dto(**updated_record)
