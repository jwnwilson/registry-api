import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from app.adapter.into.fastapi.main import app

    return TestClient(app)
