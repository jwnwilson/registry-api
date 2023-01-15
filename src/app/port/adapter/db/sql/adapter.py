import contextlib
from abc import ABC

from .model.property_model import PropertyRepository


class DbAdapaterException(Exception):
    pass


class DbAdapter(ABC):
    @contextlib.contextmanager
    def transaction(self):
        raise NotImplementedError

    def init_db(self):
        raise NotImplementedError

    @property
    def property(self) -> PropertyRepository:
        raise NotImplementedError
