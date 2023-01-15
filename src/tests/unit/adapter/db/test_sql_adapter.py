import pytest

from app.adapter.db.adapter import SessionNotInitialised
from app.ports.db.model.property_model import PropertyRepository


def test_create_session(db_adapter):
    with db_adapter.transaction() as session:
        assert db_adapter.session is session
        assert isinstance(db_adapter.property, PropertyRepository)
        assert db_adapter.property.db.session is session
    with pytest.raises(SessionNotInitialised):
        assert db_adapter.session
