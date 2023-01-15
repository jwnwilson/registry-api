
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Type, TypeVar
from pydantic import BaseModel
import logging

from app.port.adapter.db import ListParams
from app.port.adapter.db.repository import Repository
from app.port.domain.user import UserData
from ..exceptions import DuplicateRecord, RecordNotFound
if TYPE_CHECKING:
    from .adapter import DynamodbAdapter

ModelType = TypeVar("ModelType", bound=BaseModel)
ModelDTOType = TypeVar("ModelDTOType", bound=BaseModel)

logger = logging.getLogger(__name__)


class DynamodbRepository(Repository):
    model: Type[ModelType]
    model_dto: Type[ModelDTOType]

    def __init__(
        self,
        db: DynamodbAdapter
    ):
        self.db: DynamodbAdapter = db
        
    def read(self, table: str, record_id: str) -> dict:
        try:
            table_data: dict = self._get_table(table).get_item(
                Key={
                    self.part_key_name: self.user.user_id,
                    self.sort_key_name: record_id,
                }
            )["Item"]
            return table_data
        except KeyError:
            raise RecordNotFound("Record not found: {record_id} in table: {table}")

    def list(self, table: str, params: ListParams) -> List[dict]:
        table_data: List[dict] = self._get_table(table).scan(
            **self._build_query_params(params), Limit=params.limit
        )
        return table_data

    def create(self, table: str, record_data: dict) -> dict:
        record_data[self.part_key_name] = self.user.user_id
        table_data: dict = self._get_table(table).put_item(Item=record_data)
        return table_data

    def update(self, table: str, record_id: str, record_data: dict) -> dict:
        update_expression = "SET "
        expression_attr_values = {}
        expression_attr_names = {}
        update_expressions = []

        for key in record_data.keys():
            update_expressions.append(f"#{key} = :{key}")
            expression_attr_values[f":{key}"] = record_data[key]
            expression_attr_names[f"#{key}"] = key

        update_expression += ", ".join(update_expressions)

        table_data: dict = self._get_table(table).update_item(
            Key={self.part_key_name: self.user.user_id, self.sort_key_name: record_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attr_values,
            ExpressionAttributeNames=expression_attr_names,
        )
        return table_data
