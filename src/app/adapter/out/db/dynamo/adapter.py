from enum import Enum
from functools import reduce
from operator import and_
from typing import Any, Dict, List

import boto3
from boto3.dynamodb.conditions import Attr
from pydantic import BaseModel

from app.port.adapter.db import DbAdapter
from app.port.adapter.db.repository import ListParams
from app.port.domain.user import UserData
from ..exceptions import RecordNotFound


class KeyType(Enum):
    HASH = "HASH"
    RANGE = "RANGE"


class AttributeType(Enum):
    string = "S"
    number = "N"
    binary = "B"


class KeySchema(BaseModel):
    name: str
    type: KeyType


class AttributeDefinitions(BaseModel):
    name: str
    type: AttributeType


class TableDefinition(BaseModel):
    key_schema: List[KeySchema]
    attribute_definitions: List[AttributeDefinitions]


class DynamodbAdapter(DbAdapter):
    def __init__(
        self, config: dict, user: UserData, part_key_name: str, sort_key_name: str
    ):
        # Get the service resource.
        self.client = boto3.resource("dynamodb")
        self.config = config
        self.part_key_name = part_key_name
        self.sort_key_name = sort_key_name
        self.user = user

    def _get_table(self, table):
        return self.client.Table(table)

    def _build_query_params(self, params: ListParams):
        query_params = {}
        filters: Dict[str, Any] = {}
        if params.filters:
            filters = {**filters, **params.filters}
        if filters:
            query_params["FilterExpression"] = self._add_expressions(filters)

        return query_params

    def _add_expressions(self, filters: dict):
        if filters:
            conditions = []
            for key, value in filters.items():
                if isinstance(value, str):
                    conditions.append(Attr(key).eq(value))
                if isinstance(value, list):
                    conditions.append(Attr(key).is_in([v for v in value]))
            return reduce(and_, conditions)

    def create_table(self, table: str, **kwargs):
        table_definition: TableDefinition = kwargs.pop("table_definition")
        key_schema = [
            {"AttributeName": key.name, "KeyType": key.type.value}
            for key in table_definition.key_schema
        ]
        attribute_definitions = [
            {"AttributeName": attr.name, "AttributeType": attr.type.value}
            for attr in table_definition.attribute_definitions
        ]
        if "BillingMode" not in kwargs:
            kwargs["BillingMode"] = "PAY_PER_REQUEST"

        table = self.client.create_table(
            TableName=table,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            **kwargs,
        )

        # Wait until the table exists.
        table.wait_until_exists()  # type: ignore

        return table
