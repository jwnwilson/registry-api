
from __future__ import annotations
from typing import List, Optional, Type, TypeVar
from pydantic import BaseModel, ValidationError
import logging
from pymongo.errors import DuplicateKeyError

from app.port.adapter.db.repository import Repository, ListParams
from app.port.domain.user import UserData
from ..exceptions import DuplicateRecord, RecordNotFound
from .adapter import MongoDbAdapter

ModelType = TypeVar("ModelType", bound=BaseModel)
ModelDTOType = TypeVar("ModelDTOType", bound=BaseModel)

logger = logging.getLogger(__name__)


class MongoRepository(Repository):
    model_dto: Type[ModelDTOType]
    table: str

    def __init__(
        self,
        db: MongoDbAdapter
    ):
        self.db: MongoDbAdapter = db

    def list(self, params: ListParams) -> List[model_dto]:
        collection = self.db.db[self.table]
        filters = {}
        if params.filters:
            filters.update(params.filters)

        data = collection.find(filters)
        if params.limit:
            data = data.limit(params.limit)
        list_data: List[dict] = [self.model_dto(**x) for x in data]
        entities = []

        for entity in data:
            try:
                entities.append(self.model_dto(**entity))
            except ValidationError as err:
                uuid = entity.get("uuid")
                logger.warn(f"Invalid record uuid: '{uuid}', error: {err}\n skipping...")

        return list_data

    def read(self, record_id: str) -> model_dto:
        collection = self.db.db[self.table]
        record: Optional[dict] = collection.find_one({"uuid": record_id})
        if not record:
            raise RecordNotFound(f"Record not found uuid: '{record_id}'")
        return self.model_dto(**record)

    def create(self, record_data: dict) -> model_dto:
        collection = self.db.db[self.table]
        mongo_data = {**record_data, **{"_id": record_data["uuid"]}}
        try:
            collection.insert_one(mongo_data)
            return self.read(record_id=record_data["uuid"])
        except DuplicateKeyError:
            uuid = record_data.get("uuid")
            error = f"Duplicate record uuid: '{uuid}'"
            logger.info(error)
            raise DuplicateRecord(error)

    def delete(self, record_id: str):
        collection = self.db.db[self.table]
        collection.delete_one({"uuid": record_id})

    def update(self, record_id: str, record_data: dict) -> model_dto:
        collection = self.db.db[self.table]
        record: Optional[dict] = collection.find_one({"uuid": record_id})
        if not record:
            raise RecordNotFound(f"Record not found uuid: '{record_id}'")

        query = {"uuid": record_id}
        record.update(record_data)
        updated_record: dict = collection.replace_one(
            query, record, upsert=True
        ).raw_result
        return self.model_dto(**updated_record)
