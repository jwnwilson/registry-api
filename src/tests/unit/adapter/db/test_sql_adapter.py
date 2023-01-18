import pytest

from app.adapter.out.db.sql import SessionNotInitialised


# def test_create_session(db_adapter):
#     with db_adapter.transaction() as session:
#         assert db_adapter.session is session

#     with pytest.raises(SessionNotInitialised):
#         assert db_adapter.session
