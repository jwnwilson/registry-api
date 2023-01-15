from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Type, TypeVar
from pydantic import BaseModel
import logging
from pymongo.errors import DuplicateKeyError

from app.port.adapter.db import ListParams
from app.port.adapter.db.repository import Repository
from app.port.domain.user import UserData
from ..exceptions import DuplicateRecord, RecordNotFound
if TYPE_CHECKING:
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

    def list(self, table: str, params: ListParams) -> List[model_dto]:
        collection = self.db.client[self.db][table]
        filters = {}
        if params.filters:
            filters.update(params.filters)

        data = collection.find(filters)
        if params.limit:
            data = data.limit(params.limit)
        list_data: List[dict] = [x for x in data]

        return list_data

    def read(self, table: str, record_id: str) -> model_dto:
        collection = self.db.client[self.db][table]
        record: Optional[dict] = collection.find_one({"uuid": record_id})
        if not record:
            raise RecordNotFound(f"Record not found uuid: '{record_id}'")
        return record

    def create(self, table: str, record_data: dict) -> model_dto:
        collection = self.db.client[self.db][table]
        mongo_data = {**record_data, **{"_id": record_data["uuid"]}}
        try:
            collection.insert_one(mongo_data)
            record: dict = self.read(table, record_id=record_data["uuid"])
            return record
        except DuplicateKeyError:
            uuid = record_data.get("uuid")
            error = f"Duplicate record uuid: '{uuid}'"
            logger.info(error)
            raise DuplicateRecord(error)

    def delete(self, table: str, record_id: str):
        collection = self.db.client[self.db][table]
        collection.delete_one({"uuid": record_id})

    def update(self, table: str, record_id: str, record_data: dict) -> model_dto:
        collection = self.db.client[self.db][table]
        record: Optional[dict] = collection.find_one({"uuid": record_id})
        if not record:
            raise RecordNotFound(f"Record not found uuid: '{record_id}'")

        query = {"uuid": record_id}
        record.update(record_data)
        updated_record: dict = collection.replace_one(
            query, record, upsert=True
        ).raw_result
        return updated_record
