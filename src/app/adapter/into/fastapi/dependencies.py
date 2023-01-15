import os

from fastapi import Depends
from fastapi.security import HTTPBearer
from starlette.requests import Request

from ...out.db.mongo import MongoDbAdapter
from app.port.adapter.db import DbAdapter
from app.port.domain.user import UserData

ENVIRONMENT = os.environ["ENVIRONMENT"]

security = HTTPBearer()


def get_current_user(request: Request) -> UserData:
    # attempt to get user id from jwt token
    user_id = "01f2612b-e277-4ed5-91a3-254fc8c09325"
    return UserData(user_id=user_id, organisation_id=None)


def get_db(user_data: UserData = Depends(get_current_user)) -> DbAdapter:
    # Setup a DB transaction for the length of- the request
    db = MongoDbAdapter(config={}, user=user_data)
    with db.transaction():
        yield db


# def get_db() -> Generator[DbAdapter, None, None]:
#     adapter = SQLALchemyAdapter(DB_URL)
#     with adapter.transaction():
#         yield adapter
