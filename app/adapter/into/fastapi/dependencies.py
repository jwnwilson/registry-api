import os
from distutils.command import upload

from adapter.out.db import MongoDbAdapter
from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from hex_lib.ports.db import DbAdapter
from hex_lib.ports.user import UserData
from starlette.requests import Request

ENVIRONMENT = os.environ["ENVIRONMENT"]

security = HTTPBearer()


def get_current_user(request: Request) -> UserData:
    # attempt to get user id from jwt token
    user_id = "01f2612b-e277-4ed5-91a3-254fc8c09325"
    return UserData(user_id=user_id, organisation_id=None)


def get_db_adapater(user_data: UserData = Depends(get_current_user)) -> DbAdapter:
    return MongoDbAdapter(config={}, user=user_data)
