import os
from collections.abc import Generator

# Silence SQLALchemy deprecation warning until we can upgrade
os.environ["SQLALCHEMY_SILENCE_UBER_WARNING"] = "1"

import pytest
from fastapi.testclient import TestClient

from app.adapter.out.db import MongoDbAdapter, MongoRepositories
from app.port.adapter.db import DbAdapter, Repositories

# Create local file db
SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"


@pytest.fixture
def db_adapter() -> DbAdapter:
    """
    Return db adapter without DB session
    """
    return MongoDbAdapter(
        config={"db_name": "test_db"}
    )


@pytest.fixture
def db(db_adapter: DbAdapter) -> Generator[DbAdapter, None, None]:
    """
    Return db adapter with initialised DB & DB session.
    """
    # Create tables
    db_adapter.init_db()
    # Create DB session
    with db_adapter.transaction() as session:
        yield MongoRepositories(db_adapter)


@pytest.fixture
def repos(db_adapter: DbAdapter) -> Generator[Repositories, None, None]:
    """
    Return db adapter with initialised DB & DB session.
    """
    # Create tables
    db_adapter.init_db()
    # Create DB session
    with db_adapter.transaction() as session:
        yield MongoRepositories(db_adapter)


@pytest.fixture
def client(db):
    from app.adapter.into.fastapi import app
    from app.adapter.into.fastapi.dependencies import get_db

    def get_db_override():
        yield db

    app.dependency_overrides[get_db] = get_db_override
    return TestClient(app)
