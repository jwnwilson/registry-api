import os
from distutils.command import upload

from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from adapter.out.db import MongoDbAdapter
from hex_lib.ports.db import DbAdapter
from hex_lib.ports.user import UserData
from starlette.requests import Request

ENVIRONMENT = os.environ["ENVIRONMENT"]

security = HTTPBearer()


def get_current_user(
    request: Request, credentials: HTTPBasicCredentials = Depends(security)
) -> UserData:
    # attempt to get user id from authorizer logic
    user_id = (
        request.scope.get("aws.event", {})
        .get("requestContext", {})
        .get("authorizer", {})
        .get("user_id")
    )
    return UserData(user_id=user_id)


def get_db_adapater(user_data: UserData = Depends(get_current_user)) -> DbAdapter:
    table_name = f"registry_task_{ENVIRONMENT}"
    return MongoDbAdapter(
        config={"table": table_name},
        user=user_data,
        part_key_name="user_id",
        sort_key_name="task_id",
    )
