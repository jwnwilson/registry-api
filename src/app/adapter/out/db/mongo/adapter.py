import contextlib
import logging
import os
from typing import Dict, List, Optional

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from app.port.adapter.db import DbAdapter, ListParams
from app.port.domain.user import UserData
from ..exceptions import DuplicateRecord, RecordNotFound

logger = logging.getLogger(__name__)


class MongoDbAdapter(DbAdapter):
    # Cache mongo clients for performance
    clients: Dict[str, MongoClient] = {}

    def __init__(self, config: dict, user: UserData, *args, **kwargs):
        self.config = config
        self.user = user
        self._configure_db()

    @contextlib.contextmanager
    def transaction(self):
        with self.client.start_session() as session:
            with session.start_transaction():
                yield

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
            self.client: MongoClient = MongoClient(uri)
            self.clients[db_client_key] = self.client
        else:
            self.client: MongoClient = self.clients[db_client_key]