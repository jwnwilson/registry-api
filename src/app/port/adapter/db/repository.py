from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, Optional, TypeVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from .adapter import DbAdapter

ModelDTO = TypeVar("ModelDTO", bound=BaseModel)


class PaginatedData(BaseModel):
    results: Any
    total: int
    page_size: int
    page_number: int


class ListParams(BaseModel):
    limit: Optional[int]
    filters: Optional[dict]


class Repository(ABC):
    def __init__(self, db: DbAdapter):
        self.db = db

    def create(self, obj_in: ModelDTO) -> ModelDTO:
        raise NotImplementedError

    def read(self, id: Any) -> Optional[ModelDTO]:  # type: ignore
        raise NotImplementedError

    def read_multi(
        self, filters: Any = None, page_size: int = 100, page_number: int = 1
    ) -> PaginatedData:
        raise NotImplementedError

    def update(self, id: Any, obj_in: ModelDTO) -> ModelDTO:
        raise NotImplementedError

    def delete(self, id: Any) -> bool:
        raise NotImplementedError

    def get_offset(self, page_size, page_number):
        return (page_number - 1) * page_size

    def paginate(self, query, page_number, page_size):
        raise NotImplementedError
