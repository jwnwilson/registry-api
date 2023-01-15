import pytest

from tests.helpers.factories import property_factory  # type: ignore


@pytest.fixture
def create_properties(db, property_factory):
    properties = [
        property_factory(),
        property_factory(),
    ]
    db.session.add_all(properties)
    db.session.commit()
    return properties


def test_property_no_data(client):
    response = client.get("/api/v1/property/")
    assert response.status_code == 200, response.json()


def test_property_with_data(client, create_properties):
    response = client.get("/api/v1/property/")
    assert response.status_code == 200, response.json()
    assert response.json()["total"] == 2
    assert len(response.json()["data"]) == 2
