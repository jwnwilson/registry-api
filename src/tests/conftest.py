import pytest
from fastapi.testclient import TestClient
from hex_lib.ports.db import DbAdapter
from hex_lib.ports.user import UserData


@pytest.fixture
def client():
    from app.adapter.into.fastapi.main import app

    return TestClient(app)


@pytest.fixture(autouse=True)
def override_db():
    from app.adapter.into.fastapi.dependencies import get_db_adapater
    from app.adapter.into.fastapi.main import app

    from .overrides import override_get_db_adapater

    app.dependency_overrides[get_db_adapater] = override_get_db_adapater
    yield
    app.dependency_overrides = {}


@pytest.fixture(autouse=True)
def override_user_data():
    from app.adapter.into.fastapi.dependencies import get_current_user
    from app.adapter.into.fastapi.main import app

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
        "productEntityType": {
            "name": "product",
            "uuid": "e3105dbb-937e-43a3-bcc0-5f6500cb1f10",
            "fields": {
                "product_number": {
                    "input_type": "text",
                    "data_type": "string",
                    "description": "",
                    "default": "",
                }
            },
            "links": {
                "b8e6df9f-2b75-4f96-b955-70a216d170e5": {
                    "direction": "bi_directional",
                    "entity_type": "organisation",
                }
            },
        },
        "userEntityType": {
            "name": "user",
            "uuid": "99ac59e7-74a7-4900-a482-d93441b3edd1",
            "fields": {
                "name": {
                    "input_type": "text",
                    "data_type": "string",
                    "description": "",
                    "default": "",
                }
            },
            "links": {
                "b8e6df9f-2b75-4f96-b955-70a216d170e5": {
                    "direction": "bi_directional",
                    "entity_type": "organisation",
                }
            },
        },
        "orgEntityType": {
            "name": "organisation",
            "uuid": "b8e6df9f-2b75-4f96-b955-70a216d170e5",
            "fields": {
                "name": {
                    "input_type": "text",
                    "data_type": "string",
                    "description": "",
                    "default": "",
                }
            },
            "links": None,
        },
        "entity": {
            "name": "knife",
            "entity_type": "product",
            "uuid": "2ddc873b-dbe9-4c89-944d-75b58ae33cca",
            "fields": {"product_number": "12345"},
            "links": {
                "b8e6df9f-2b75-4f96-b955-70a216d170e5": {
                    "direction": "bi_directional",
                    "entity_type": "organisation",
                }
            },
        },
    }

    db.create("entityType", data["productEntityType"])
    db.create("entityType", data["userEntityType"])
    db.create("entityType", data["orgEntityType"])
    db.create("entity", data["entity"])

    return data
