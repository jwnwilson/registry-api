import os
from typing import List

from hex_lib.ports.db import DbAdapter, ListParams
from hex_lib.ports.user import UserData
from pymongo import MongoClient

URI = "mongodb://%s:%s@%s:27017/%s?retryWrites=true&w=majority" % (
    os.environ["MONGO_USER"],
    os.environ["MONGO_PASSWORD"],
    os.environ["MONGO_HOST"],
    os.environ["MONGO_DB_NAME"],
)
DB = os.environ["MONGO_DB_NAME"]
CLIENT = MongoClient(URI)


class MongoDbAdapter(DbAdapter):
    def __init__(self, config: dict, user: UserData, *args, **kwargs) -> None:
        self.config = config
        self.user = user
        self.client = CLIENT

    def list(self, table: str, params: ListParams) -> List[dict]:
        collection = self.client[DB][table]
        if params.filters:
            data = collection.find(params.filters)
        else:
            data = collection.find({})
        if params.limit:
            data = data.limit(params.limit)

        data = [x for x in data]
        return data

    def read(self, table: str, record_id: str) -> List[dict]:
        collection = self.client[DB][table]
        record = collection.find({'uuid': record_id})
        return next(record)

    def create(self, table: str, data: dict) -> dict:
        collection = self.client[DB][table]
        return collection.insert_one(data)