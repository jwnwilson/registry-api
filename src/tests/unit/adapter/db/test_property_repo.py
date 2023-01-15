import pytest

from app.adapter.db.model.property_model import Property
from app.adapter.db.repository import SQLRepository
from app.ports.db import DbAdapter
from app.ports.db.model.property_model import PropteryDTO
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


def test_list_properties(db: DbAdapter, create_properties):
    properties = db.property.read_multi()

    assert len(properties["data"]) == 2
    assert properties["total"] == 2
    assert isinstance(properties["data"][0], PropteryDTO)
