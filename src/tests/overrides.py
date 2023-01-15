from fastapi import Depends
from hex_lib.adapter.out.db import MongoDbAdapter
from hex_lib.port.db import DbAdapter
from hex_lib.port.user import UserData
from starlette.requests import Request

from app.adapter.into.fastapi.dependencies import get_current_user


def get_test_user():
    user_id = "01f2612b-e277-4ed5-91a3-254fc8c09325"
    return UserData(user_id=user_id, organisation_id=None)


def get_test_db_adapater(user_data: UserData):
    # connect to test db
    return MongoDbAdapter(config={"db_name": "test_db"}, user=user_data)


def override_get_db_adapater(
    user_data: UserData = Depends(get_current_user),
) -> DbAdapter:
    return get_test_db_adapater(user_data)


def override_get_current_user(request: Request) -> UserData:
    return get_test_user()
