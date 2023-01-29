from abc import ABC
from enum import Enum
from typing import Any, Callable, List, Optional, Type, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.types import DecoratedCallable
from pydantic import BaseModel

from app.port.adapter.db import PaginatedData, Repositories, Repository
from ...out.db.exceptions import RecordNotFound


class CrudRouter(APIRouter):
    """
    Dynamically create Create Read Update and Delete methods for our repositories

    Lots of concepts and ideas stolen from this project:
    https://github.com/awtkns/fastapi-crudrouter

    Has the ability to be overriden with regular router functons e.g.

    router_v1 = CrudRouter(
        repo_dependency=get_repos,
        respository="quote",
        methods=["CREATE", "READ", "UPDATE", "DELETE"],
        response_schema=QuoteDTO,
        create_schema=CreateQuoteDTO,
        update_schema=UpdateQuoteDTO,
    )

    @router_v1.get("/")
    def override_read_multi():
        return "example"
    """

    response_schema: Type[BaseModel]
    create_schema: Type[BaseModel]
    update_schema: Type[BaseModel]

    def __init__(
        self,
        repo_dependency: Callable,
        respository: str,
        response_schema: Type[BaseModel],
        methods: List[str],
        create_schema: Type[BaseModel],
        update_schema: Type[BaseModel],
        prefix: Optional[str] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        paginate: Optional[int] = None,
        **kwargs: Any,
    ):
        self.repo_dependency: Callable = repo_dependency
        self.repository: str = respository
        self.methods = methods or ["READ"]

        self.response_schema: Type[BaseModel] = response_schema
        self.create_schema: Type[BaseModel] = create_schema
        self.update_schema: Type[BaseModel] = update_schema

        prefix = prefix or ""

        super().__init__(prefix=prefix, tags=tags, **kwargs)
        self._setup_routes()

    def _setup_routes(self):
        if "CREATE" in self.methods:
            assert self.create_schema
            self.add_api_route(
                "/",
                self._create(),
                methods=["POST"],
                response_model=self.response_schema,
            )
        if "READ" in self.methods:
            self.add_api_route(
                "/{id}",
                self._read(),
                methods=["GET"],
                response_model=self.response_schema,
            )

            self.add_api_route(
                "/",
                self._read_multi(),
                methods=["GET"],
                response_model=PaginatedData,
            )
        if "UPDATE" in self.methods:
            assert self.update_schema
            self.add_api_route(
                "/{id}",
                self._update(),
                methods=["PATCH"],
                response_model=self.response_schema,
            )
        if "DELETE" in self.methods:
            self.add_api_route(
                "/{id}",
                self._delete(),
                methods=["DELETE"],
            )

    @property
    def router(self):
        return self

    def _create(self) -> Callable:
        def create_record(
            obj_in: self.create_schema,  # type: ignore
            repos: Repositories = Depends(self.repo_dependency),
        ) -> self.response_schema:  # type: ignore
            try:
                repositry: Repository = getattr(repos, self.repository)
                result = repositry.create(obj_in)
            except RecordNotFound as e:
                raise HTTPException(status_code=404, detail=str(e))
            else:
                return result

        return create_record

    def _read(self) -> Callable:
        def read_record(
            id: str,
            repos: Repositories = Depends(self.repo_dependency),
        ) -> self.response_schema:  # type: ignore
            try:
                repositry: Repository = getattr(repos, self.repository)
                result = repositry.read(id)
            except RecordNotFound as e:
                raise HTTPException(status_code=404, detail=str(e))
            else:
                return result

        return read_record

    def _read_multi(self) -> Callable:
        def read_multiple_records(
            repos: Repositories = Depends(self.repo_dependency),
            page_size: int = 0,
            page_number: int = 1,
        ) -> PaginatedData:  # type: ignore
            repositry: Repository = getattr(repos, self.repository)
            return repositry.read_multi(filters={}, page_size=page_size, page_number=page_number)

        return read_multiple_records

    def _update(self) -> Callable:
        def update_record(
            id: str,
            obj_in: self.update_schema,  # type: ignore
            repos: Repositories = Depends(self.repo_dependency),
        ) -> self.response_schema:  # type: ignore
            try:
                repositry: Repository = getattr(repos, self.repository)
                result = repositry.update(id, obj_in)
            except RecordNotFound as e:
                raise HTTPException(status_code=404, detail=str(e))
            else:
                return result

        return update_record

    def _delete(self) -> Callable:
        def delete_record(
            id: str,
            repos: Repositories = Depends(self.repo_dependency),
        ):
            repositry: Repository = getattr(repos, self.repository)
            return repositry.delete(id)

        return delete_record

    def remove_api_route(self, path: str, methods: List[str]) -> None:
        """
        Used when overriding default routes above, will remove registered
        route to allow a new one to override it.
        """
        methods_ = set(methods)

        for route in self.routes:
            if (
                route.path == f"{self.prefix}{path}"  # type: ignore
                and route.methods == methods_  # type: ignore
            ):
                self.routes.remove(route)

    def get(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["GET"])
        return super().get(path, *args, **kwargs)

    def post(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["POST"])
        return super().post(path, *args, **kwargs)

    def put(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["PUT"])
        return super().put(path, *args, **kwargs)

    def delete(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["DELETE"])
        return super().delete(path, *args, **kwargs)
