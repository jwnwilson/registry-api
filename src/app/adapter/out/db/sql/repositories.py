from app.port.adapter.db import Repositories
from .adapter import SQLALchemyAdapter


class SQLRepositories(Repositories):
    def __init__(self, db: SQLALchemyAdapter) -> None:
        self.db: SQLALchemyAdapter = db