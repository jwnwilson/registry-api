from .adapter import DbAdapter
from .repository import Repository


class Repositories(object):
    def __init__(self, db: DbAdapter):
        self.db = db

    @property
    def entity_type(self) -> Repository:
        raise NotImplementedError
    
    @property
    def entity(self) -> Repository:
        raise NotImplementedError
    
    @property
    def link_type(self) -> Repository:
        raise NotImplementedError