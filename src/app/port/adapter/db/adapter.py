import contextlib
from abc import ABC


class DbAdapaterException(Exception):
    pass


class DbAdapter(ABC):

    @contextlib.contextmanager
    def transaction(self):
        raise NotImplementedError

    def init_db(self):
        raise NotImplementedError
    
    def create_table(self, table: str, **kwargs):
        raise NotImplementedError

