from typing import List

from hex_lib.ports.db import DbAdapter
from hex_lib.ports.user import UserData

from ..domain import entity
from ..ports.entity import EntityDTO, QueryParam


def list(query_param: QueryParam, db_adapter: DbAdapter, user: UserData) -> List[str]:
    """[summary]

    Args:
        html (str): [description]
        file_path (str): [description]

    Returns:
        [type]: [description]
    """
    entity_data: List[EntityDTO] = entity.list(
        query_param, user=user, db_adapter=db_adapter
    )
    return entity_data
