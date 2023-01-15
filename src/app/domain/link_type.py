import logging
import uuid
from typing import List

from pydantic import ValidationError

from app.port.adapter.db import DbAdapter, ListParams
from app.port.domain.user import UserData
from app.port.domain.link_type import CreateLinkTypeDTO, LinkTypeDTO, UpdateLinkTypeDTO

TABLE = "linkType"

logger = logging.getLogger(__name__)


def list_link_type(query_param: ListParams, db_adapter: DbAdapter) -> List[LinkTypeDTO]:
    params = ListParams(limit=query_param.limit, filters=query_param.filters)
    data = db_adapter.list(TABLE, params)
    link_types = []
    for entity in data:
        try:
            link_types.append(LinkTypeDTO(**entity))
        except ValidationError as err:
            uuid = entity.get("uuid")
            logger.warn(f"Invalid record uuid: '{uuid}', error: {err}\n skipping...")

    return link_types


def read(uuid: str, db_adapter: DbAdapter) -> LinkTypeDTO:
    data = db_adapter.read(TABLE, uuid)
    return LinkTypeDTO(**data)


def update(
    uuid: str, entity_data: UpdateLinkTypeDTO, db_adapter: DbAdapter
) -> LinkTypeDTO:
    update_data = entity_data.dict()
    _id = db_adapter.update(table=TABLE, record_id=uuid, record_data=update_data)
    data = db_adapter.read(TABLE, uuid)
    return LinkTypeDTO(**data)


def delete(uuid: str, db_adapter: DbAdapter) -> None:
    db_adapter.delete(table=TABLE, record_id=uuid)
    return


def create(entity_data: CreateLinkTypeDTO, db_adapter: DbAdapter) -> LinkTypeDTO:
    create_data = entity_data.dict()
    entity_uuid = str(uuid.uuid4())
    create_data["uuid"] = entity_uuid
    _id = db_adapter.create(TABLE, record_data=create_data)
    data = db_adapter.read(TABLE, entity_uuid)
    return LinkTypeDTO(**data)
