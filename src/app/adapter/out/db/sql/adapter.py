import contextlib
import logging
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.ports.db import DbAdapaterException, DbAdapter

from .model import *
from .model.base import Base

logger = logging.getLogger(__name__)


class SessionNotInitialised(DbAdapaterException):
    pass


class SQLALchemyAdapter(DbAdapter):
    def __init__(
        self,
        database_uri: str,
        engine_args: Optional[dict] = None,
        session_args: Optional[dict] = None,
    ):
        self.database_uri = database_uri
        self.engine_args = engine_args or dict(
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=0,
            pool_recycle=10,
            pool_timeout=5,
            future=True,
        )
        self.session_args = session_args or dict(
            expire_on_commit=False, autoflush=False
        )
        self.engine = self.create_engine()
        self._session = None

    @property
    def session(self) -> Session:
        if not self._session:
            raise SessionNotInitialised
        return self._session

    def init_db(self):
        logger.info("Creating database tables from models")
        # Note: This can be sped up, clearing the tables is faster than dropping
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def create_engine(self):
        logger.debug("Setting up a new database engine.")
        return create_engine(self.database_uri, **self.engine_args)

    def session_maker(self):
        logger.debug("Setting up a new local session.")
        engine = self.session_args.get("bind")
        if not engine:
            engine = self.engine

        return sessionmaker(bind=engine, **self.session_args)

    @contextlib.contextmanager
    def transaction(self):
        Session = self.session_maker()
        with Session() as session:
            self._session = session
            yield session
            self._session = None

    @property
    def property(self) -> PropertyRepository:
        return PropertyRepositorySQL(self, Property, PropteryDTO)
