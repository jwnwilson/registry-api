from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Query

from app.ports.db.repository import Repository

from .exception import RecordNotFound
from .model.base import BaseSQLModel

if TYPE_CHECKING:
    from .adapter import SQLALchemyAdapter

ModelType = TypeVar("ModelType", bound=BaseSQLModel)
ModelDTOType = TypeVar("ModelDTOType", bound=BaseModel)


class SQLRepository(Repository):
    def __init__(
        self,
        db: SQLALchemyAdapter,
        model: Type[ModelType],
        model_dto: Type[ModelDTOType],
    ):
        self.db: SQLALchemyAdapter = db
        self.model: Type[ModelType] = model
        self.model_dto: Type[ModelDTOType] = model_dto

    def create(self, obj_in: ModelDTOType) -> ModelDTOType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        self.db.session.add(db_obj)
        self.db.session.flush()
        return self.model_dto(**db_obj.__dict__)  # type: ignore

    def read(self, id: Any) -> Optional[ModelDTOType]:  # type: ignore
        entity = self.db.session.query(self.model).filter(self.model.id == id).first()
        if not entity:
            raise RecordNotFound(
                f"Model: {self.model.__class__}, Record: {id}, not found"
            )
        return self.model_dto(**entity.__dict__)  # type: ignore

    def read_multi(
        self, filters: Any = None, page_size: int = 100, page_number: int = 1
    ) -> Any:
        entities = self.db.session.query(self.model)
        if filters:
            entities = entities.filter(**filters)
        total = entities.count()
        results = self.paginate(entities, page_number, page_size)
        results = [self.model_dto(**item.__dict__) for item in results]
        return {
            "data": results,
            "total": total,
            "page": page_number,
            "page_number": page_number,
        }

    def update(self, id: Any, obj_in: ModelDTOType) -> ModelDTOType:
        entity = self.db.session.query(self.model).filter(self.model.id == id).first()
        for key in obj_in.dict():
            setattr(entity, key, getattr(obj_in, key))
        self.db.session.add(entity)
        self.db.session.flush()
        return self.model_dto(**entity.__dict__)  # type: ignore

    def delete(self, id: Any) -> bool:
        self.db.session.query(self.model).filter(self.model.id == id).delete()
        return True

    def get_offset(self, page_size: int, page_number: int):
        return (page_number - 1) * page_size

    def paginate(self, query: Query, page_number: int, page_size: int):
        if page_size > 0 and page_number >= 1:
            offset = self.get_offset(page_size, page_number)
            query = query.offset(offset).limit(page_size)

        return query
