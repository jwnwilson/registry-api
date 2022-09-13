from typing import List

from domain import entity_type
from hex_lib.ports.db import DbAdapter
from hex_lib.ports.user import UserData
from ports.entity_type import EntityTypeDTO, QueryParam


def list(
    query_param: QueryParam, db_adapter: DbAdapter, user: UserData
) -> List[EntityTypeDTO]:
    """[summary]

    Args:
        html (str): [description]
        file_path (str): [description]

    Returns:
        [type]: [description]
    """
    return entity_type.list(query_param, user=user, db_adapter=db_adapter)


def create(
    entity_data: EntityTypeDTO, user: UserData, db_adapter: DbAdapter
) -> List[EntityTypeDTO]:
    """[summary]

    Args:
        html (str): [description]
        file_path (str): [description]

    Returns:
        [type]: [description]
    """
    return entity_type.create(entity_data, user=user, db_adapter=db_adapter)
