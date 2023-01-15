import contextlib
from abc import ABC

from .repository import Repository, Repositories

class DbAdapaterException(Exception):
    pass


class DbAdapter(ABC):
    _repositories = Repositories()

    @contextlib.contextmanager
    def transaction(self):
        raise NotImplementedError

    def init_db(self):
        raise NotImplementedError
    
    def init_repositories(self):
        raise NotImplementedError

    def register_repository(self, name: str, repository: Repository):
        self._repositories.register_repository(name, repository)
    
    def create_table(self, table: str, **kwargs):
        raise NotImplementedError

    @property
    def repositories(self):
        return self._repositories

