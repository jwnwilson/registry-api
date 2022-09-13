import os
from typing import List
import logging

from hex_lib.ports.db import DbAdapter, ListParams
from hex_lib.ports.user import UserData
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from .exceptions import DuplicateRecord

URI = "mongodb://%s:%s@%s:27017/%s?retryWrites=true&w=majority" % (
    os.environ["MONGO_USER"],
    os.environ["MONGO_PASSWORD"],
    os.environ["MONGO_HOST"],
    os.environ["MONGO_DB_NAME"],
)
DB = os.environ["MONGO_DB_NAME"]
CLIENT = MongoClient(URI)


logger = logging.getLogger(__name__)


class MongoDbAdapter(DbAdapter):
    def __init__(self, config: dict, user: UserData, *args, **kwargs) -> None:
        self.config = config
        self.user = user
        self.client = CLIENT

    def list(self, table: str, params: ListParams) -> List[dict]:
        collection = self.client[DB][table]
        filters = {}
        if params.filters:
            filters.update(params.filters)
        if params.organisation:
            filters.update({
                "organisation": params.organisation
            })
        else:
            filters.update({
                "owner": self.user.user_id
            })
        if params.limit:
            data = data.limit(params.limit)

        data = collection.find(filters)
        data = [x for x in data]
        return data

    def read(self, table: str, record_id: str) -> List[dict]:
        collection = self.client[DB][table]
        record = collection.find({"uuid": record_id})
        return next(record)

    def create(self, table: str, data: dict) -> dict:
        collection = self.client[DB][table]
        try:
            return collection.insert_one(data)
        except DuplicateKeyError:
            uuid = data.get("uuid")
            error = f"Duplicate record uuid: '{uuid}'"
            logger.info(error)
            raise DuplicateRecord(error)
