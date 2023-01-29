from fastapi import Depends
from starlette.requests import Request

from app.adapter.into.fastapi.dependencies import get_current_user
from app.adapter.out.db import MongoDbAdapter
from app.port.adapter.db import DbAdapter
from app.domain.user import UserData


def get_test_user():
    user_id = "01f2612b-e277-4ed5-91a3-254fc8c09325"
    return UserData(user_id=user_id, organisation_id=None)


def get_test_db_adapater(user_data: UserData):
    # connect to test db
    return MongoDbAdapter(config={"db_name": "test_db"})


def override_get_db(
    user_data: UserData = Depends(get_current_user),
) -> DbAdapter:
    return get_test_db_adapater(user_data)


def override_get_current_user(request: Request) -> UserData:
    return get_test_user()
