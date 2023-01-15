import contextlib
from abc import ABC
from typing import Optional

from pydantic import BaseModel


class ListParams(BaseModel):
    limit: Optional[int]
    filters: Optional[dict]


class DbAdapaterException(Exception):
    pass


class DbAdapter(ABC):
    @contextlib.contextmanager
    def transaction_context_manager(self):
        raise NotImplementedError

    def create(self, table: str, record_data: dict):
        raise NotImplementedError

    def list(self, table: str, params: ListParams):
        raise NotImplementedError

    def read(self, table: str, record_id: str):
        raise NotImplementedError

    def update(self, table: str, record_id: str, record_data: dict):
        raise NotImplementedError

    def delete(self, table: str, record_id: str):
        raise NotImplementedError

    def create_table(self, table: str, **kwargs):
        raise NotImplementedError
