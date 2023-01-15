from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, Optional, TypeVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from .adapter import DbAdapter

ModelDTOType = TypeVar("ModelDTOType", bound=BaseModel)


class ListParams(BaseModel):
    limit: Optional[int]
    filters: Optional[dict]


class Repositories(object):
    def __init__(self):
        self.repositories = {}
    
    def register_repository(self, name: str, repository: Repository):
        # assert name not in self.repositories, f"Repository '{name}' already registered"
        self.repositories[name] = repository
    
    def __getattribute__(self, name: str) -> Repository:
        repositories = object.__getattribute__(self, "repositories")
        if name in repositories:
            return repositories[name]
        else:
            return object.__getattribute__(self, name)


class Repository(ABC):
    def __init__(self, db: DbAdapter):
        self.db = db

    def create(self, obj_in: ModelDTOType) -> ModelDTOType:
        raise NotImplementedError

    def read(self, id: Any) -> Optional[ModelDTOType]:  # type: ignore
        raise NotImplementedError

    def read_multi(
        self, filters: Optional[ListParams] = None, page_size: int = 100, page_number: int = 1
    ) -> Any:
        raise NotImplementedError

    def update(self, id: Any, obj_in: ModelDTOType) -> ModelDTOType:
        raise NotImplementedError

    def delete(self, id: Any) -> bool:
        raise NotImplementedError

    def get_offset(self, page_size, page_number):
        return (page_number - 1) * page_size

    def paginate(self, query, page_number, page_size):
        raise NotImplementedError
