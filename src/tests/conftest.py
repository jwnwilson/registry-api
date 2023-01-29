import pytest
from fastapi.testclient import TestClient

from app.port.adapter.db import DbAdapter, Repositories
from app.port.domain.entity_type import EntityTypeDTO
from app.port.domain.entity import EntityDTO
from app.port.domain.link_type import LinkTypeDTO

@pytest.fixture
def client():
    from app.adapter.into.fastapi.main import app

    return TestClient(app)


@pytest.fixture(autouse=True)
def override_db():
    from app.adapter.into.fastapi.dependencies import get_db
    from app.adapter.into.fastapi.main import app

    from .overrides import override_get_db

    app.dependency_overrides[get_db] = override_get_db
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
def test_data(db: DbAdapter, repos: Repositories, test_user):
    db.db["linkType"].delete_many({})
    db.db["entityType"].delete_many({})
    db.db["entity"].delete_many({})

    data = {
        "linkType_1": {
            "uuid": "d187540d-fe9e-47e4-b738-95a09661fe05",
            "name": "related",
            "back_link": "related",
        },
        "linkType_2": {
            "uuid": "2e4127f1-1977-4ab0-989c-62fbfba66a25",
            "name": "related_to",
            "back_link": "related_from",
        },
        "linkType_3": {
            "uuid": "47aaba9c-bf74-493a-bd42-0d6dad80c4e3",
            "name": "related_from",
            "back_link": "related_from",
        },
        "productEntityType": {
            "name": "product",
            "description": "",
            "uuid": "e3105dbb-937e-43a3-bcc0-5f6500cb1f10",
            "fields": {
                "product_number": {
                    "uuid": "f6d7bdd9-f426-4515-b51a-5daad906e131",
                    "name": "product_number",
                    "input_type": "text",
                    "data_type": "string",
                    "description": "",
                    "default": "",
                }
            },
            "links": {
                "b8e6df9f-2b75-4f96-b955-70a216d170e5": {
                    "link_type": "related",
                    "entity_type": "organisation",
                }
            },
            "metadata": {},
        },
        "userEntityType": {
            "name": "user",
            "description": "",
            "uuid": "99ac59e7-74a7-4900-a482-d93441b3edd1",
            "fields": {
                "name": {
                    "uuid": "8742424e-46de-45e4-8d98-4a4d3ddb66b5",
                    "name": "name",
                    "input_type": "text",
                    "data_type": "string",
                    "description": "",
                    "default": "",
                }
            },
            "links": {
                "b8e6df9f-2b75-4f96-b955-70a216d170e5": {
                    "link_type": "related",
                    "entity_type": "organisation",
                }
            },
            "metadata": {},
        },
        "orgEntityType": {
            "name": "organisation",
            "description": "",
            "uuid": "b8e6df9f-2b75-4f96-b955-70a216d170e5",
            "fields": {
                "name": {
                    "name": "name",
                    "uuid": "2bb37c7d-3aa2-4d0d-ad9a-6b15149c1605",
                    "input_type": "text",
                    "data_type": "string",
                    "description": "",
                    "default": "",
                }
            },
            "links": {},
            "metadata": {},
        },
        "organisation_1": {
            "name": "test org",
            "description": "",
            "entity_type": "organisation",
            "uuid": "444f41fb-30af-4997-a993-54ba5d4466e8",
            "fields": {"name": "Test Org"},
            "links": {
                "2ddc873b-dbe9-4c89-944d-75b58ae33cca": {
                    "entity_type": "product",
                    "link_type": "related",
                }
            },
            "metadata": {},
        },
        "entity_1": {
            "name": "knife",
            "description": "",
            "entity_type": "product",
            "uuid": "2ddc873b-dbe9-4c89-944d-75b58ae33cca",
            "fields": {"product_number": "12345"},
            "links": {
                "444f41fb-30af-4997-a993-54ba5d4466e8": {
                    "entity_type": "organisation",
                    "link_type": "related",
                }
            },
            "metadata": {},
        },
        "entity_2": {
            "name": "spoon",
            "description": "",
            "entity_type": "product",
            "uuid": "259f80d6-5f1a-4d87-9440-bbbc155db294",
            "fields": {"product_number": "54321"},
            "links": {},
            "metadata": {},
        },
    }

    link_collection = db.db["linkType"]
    link_collection.insert_one(data["linkType_1"])
    link_collection.insert_one(data["linkType_2"])
    link_collection.insert_one(data["linkType_3"])

    entity_type_collection = db.db["entityType"]
    entity_type_collection.insert_one(data["productEntityType"])
    entity_type_collection.insert_one(data["userEntityType"])
    entity_type_collection.insert_one(data["orgEntityType"])

    entity_collection = db.db["entity"]
    entity_collection.insert_one(data["entity_1"])
    entity_collection.insert_one(data["entity_2"])
    entity_collection.insert_one(data["organisation_1"])

    return data
