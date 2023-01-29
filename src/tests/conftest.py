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
            "name": "related",
            "back_link": "related",
        },
        "linkType_2": {
            "name": "related_to",
            "back_link": "related_from",
        },
        "linkType_3": {
            "name": "related_from",
            "back_link": "related_from",
        },
        "productEntityType": {
            "name": "product",
            "description": "",
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
            "fields": {
                "name": {
                    "name": "name",
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
            "fields": {"product_number": "54321"},
            "links": {},
            "metadata": {},
        },
    }

    repos.link_type.create(LinkTypeDTO(**data["linkType_1"]))
    repos.link_type.create(LinkTypeDTO(**data["linkType_2"]))
    repos.link_type.create(LinkTypeDTO(**data["linkType_3"]))
    repos.entity_type.create(EntityTypeDTO(**data["productEntityType"]))
    repos.entity_type.create(EntityTypeDTO(**data["userEntityType"]))
    repos.entity_type.create(EntityTypeDTO(**data["orgEntityType"]))
    repos.entity.create(EntityDTO(**data["entity_1"]))
    repos.entity.create(EntityDTO(**data["entity_2"]))
    repos.entity.create(EntityDTO(**data["organisation_1"]))

    return data
