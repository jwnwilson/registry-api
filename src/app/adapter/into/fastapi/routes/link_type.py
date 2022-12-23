import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi_pagination import Page, paginate
from fastapi_pagination.bases import AbstractPage
from hex_lib.adapter.out.db.exceptions import DuplicateRecord
from hex_lib.ports.db import ListParams

from app.adapter.into.fastapi.dependencies import get_current_user, get_db_adapater
from app.domain import link_type
from app.domain.exceptions import EntityValidationError
from app.ports.link_type import (
    LinkTypeDTO,
    CreateLinkTypeDTO,
    UpdateLinkTypeDTO
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/link-type",
    dependencies=[],
    responses={404: {"description": "Not found"}},
    redirect_slashes=True,
)


@router.get("/", tags=["Link Type"], response_model=Page[LinkTypeDTO])
def list_links(
    filters: Optional[str] = None,
    limit: Optional[int] = None,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user),
) -> AbstractPage[LinkTypeDTO]:
    query_param = ListParams(filters=filters, limit=limit)
    data: List[LinkTypeDTO] = link_type.list(query_param=query_param, db_adapter=db_adapter)
    return paginate(data)


@router.get("/{uuid}/", tags=["Link Type"])
def get_link(
    uuid: str,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user),
) -> LinkTypeDTO:
    data: LinkTypeDTO = link_type.read(
        uuid=uuid, db_adapter=db_adapter
    )
    return data


@router.post("/", tags=["Link Type"])
def create_entity(
    link_data: CreateLinkTypeDTO,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user),
) -> LinkTypeDTO:
    try:
        data: LinkTypeDTO = link_type.create(link_data=link_data, db_adapter=db_adapter)
    except (DuplicateRecord, EntityValidationError) as err:
        raise HTTPException(400, str(err))
    return data


@router.patch("/{uuid}/", tags=["Link Type"])
def update_entity(
    uuid: str,
    entity_data: UpdateLinkTypeDTO,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user),
) -> LinkTypeDTO:
    try:
        data: LinkTypeDTO = link_type.update(
            uuid=uuid,
            link_data=entity_data,
            db_adapter=db_adapter,
        )
    except (DuplicateRecord, EntityValidationError) as err:
        raise HTTPException(400, str(err))
    return data


@router.delete("/{uuid}/", tags=["Link Type"], status_code=201)
def delete_entity(
    entity_type: str,
    uuid: str,
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user),
) -> None:
    link_type.delete(uuid=uuid, db_adapter=db_adapter)
    return
