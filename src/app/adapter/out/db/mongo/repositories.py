from app.port.adapter.db import Repositories
from .adapter import MongoDbAdapter
from .repository import MongoRepository
from .model import EntityRepository, EntityRepository, LinkTypeRepository


class MongoRepositories(Repositories):
    def __init__(self, db: MongoDbAdapter) -> None:
        self.db: MongoDbAdapter = db
    
    @property
    def entity_type(self) -> MongoRepository:
        return EntityRepository(self.db)
    
    @property
    def entity(self) -> MongoRepository:
        return EntityRepository(self.db)
    
    @property
    def link_type(self) -> MongoRepository:
        return LinkTypeRepository(self.db)