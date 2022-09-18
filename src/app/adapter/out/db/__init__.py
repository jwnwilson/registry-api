import os
from typing import List
import logging

from hex_lib.ports.db import DbAdapter, ListParams
from hex_lib.ports.user import UserData
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from .exceptions import DuplicateRecord, RecordNotFound


logger = logging.getLogger(__name__)


class MongoDbAdapter(DbAdapter):
    # Cache mongo clients for performance
    clients = {}

    def __init__(self, config: dict, user: UserData, *args, **kwargs) -> None:
        self.config = config
        self.user = user
        self.client = None
        self.db = None
        self._configure_db()

    def _configure_db(self):
        uri = "mongodb://%s:%s@%s:27017/%s?retryWrites=true&w=majority" % (
            self.config.get("user", os.environ["MONGO_USER"]),
            self.config.get("password", os.environ["MONGO_PASSWORD"]),
            self.config.get("host", os.environ["MONGO_HOST"]),
            self.config.get("db_name", os.environ["MONGO_DB_NAME"]),
        )
        self.db = self.config.get("db_name", os.environ["MONGO_DB_NAME"])

        # Cache mongo clients to avoid performance issues
        db_client_key = uri + self.db
        if not self.clients.get(db_client_key):
            self.client = MongoClient(uri)
            self.clients[db_client_key] = self.client
        else:
            self.client = self.clients[db_client_key]

    def list(self, table: str, params: ListParams) -> List[dict]:
        collection = self.client[self.db][table]
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
        collection = self.client[self.db][table]
        record = collection.find_one({"uuid": record_id})
        if not record:
            raise RecordNotFound(f"Record not found uuid: '{record_id}'")
        return record

    def create(self, table: str, record_data: dict) -> dict:
        collection = self.client[self.db][table]
        try:
            return collection.insert_one(record_data)
        except DuplicateKeyError:
            uuid = record_data.get("uuid")
            error = f"Duplicate record uuid: '{uuid}'"
            logger.info(error)
            raise DuplicateRecord(error)
    
    def delete(self, table: str, record_id: str):
        collection = self.client[self.db][table]
        collection.delete_one({"uuid": record_id})

    def update(self, table:str, record_id: str, record_data: dict) -> dict:
        collection = self.client[self.db][table]
        record = collection.find_one({"uuid": record_id})
        query = {
            "uuid": record_id
        }
        # Remove empty keys to avoid overwritting empty data
        record_data_with_values = dict((k, v) for k, v in record_data.items() if v)
        record.update(record_data_with_values)
        return collection.replace_one(query, record, upsert=True)
