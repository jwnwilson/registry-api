import logging
from typing import List

from adapter.into.fastapi.dependencies import (
    get_db_adapater,
    get_current_user
)
from fastapi import APIRouter, Depends, HTTPException
from use_case import entity

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/entity-type",
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def list_entity(
    db_adapter=Depends(get_db_adapater),
    user=Depends(get_current_user)
) -> List[dict]:
    # call create use case
    data: List[dict] = entity.list(
        db_adapter,
        user
    )
    return data
