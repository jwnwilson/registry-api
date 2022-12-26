import os

from fastapi import Depends
from fastapi.security import HTTPBearer
from hex_lib.adapter.out.db import MongoDbAdapter
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
    # Setup a DB transaction for the length of- the request
    db = MongoDbAdapter(config={}, user=user_data)
    with db.transaction_context_manager():
        yield db
