import pytest
from fastapi.testclient import TestClient
from hex_lib.ports.user import UserData
from hex_lib.ports.db import DbAdapter


@pytest.fixture
def client():
    from app.adapter.into.fastapi.main import app

    return TestClient(app)


@pytest.fixture(autouse=True)
def override_db():
    from app.adapter.into.fastapi.main import app
    from app.adapter.into.fastapi.dependencies import get_db_adapater
    from .overrides import override_get_db_adapater

    app.dependency_overrides[get_db_adapater] = override_get_db_adapater
    yield
    app.dependency_overrides = {}


@pytest.fixture(autouse=True)
def override_user_data():
    from app.adapter.into.fastapi.main import app
    from app.adapter.into.fastapi.dependencies import get_current_user
    from .overrides import override_get_current_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    app.dependency_overrides = {}


@pytest.fixture()
def test_user():
    from .overrides import get_test_user
    return get_test_user()


@pytest.fixture()
def db(test_user):
    from .overrides import get_test_db_adapater
    return get_test_db_adapater(test_user)


@pytest.fixture
def test_data(db, test_user):
    db.client[db.db]["entityType"].delete_many({})
    db.client[db.db]["entity"].delete_many({})

    data = {
        "entityType": {
            "name": "product",
            "uuid": "e3105dbb-937e-43a3-bcc0-5f6500cb1f10",
            "owner": test_user.user_id,
            "organisation": test_user.organisation_id,
            "fields": {
                "product_number": {
                    "input_type": "text",
                    "data_type": "string",
                    "description": "",
                    "default": ""
                }
            }
        },
        "entity": {
            "name": "knife",
            "entity_type": "product",
            "uuid": "2ddc873b-dbe9-4c89-944d-75b58ae33cca",
            "owner": test_user.user_id,
            "organisation": test_user.organisation_id,
            "fields": {
                "product_number": "12345"
            },
            "links": []
        }
    }

    db.create("entityType", data["entityType"])
    db.create("entity", data["entity"])

    return data
