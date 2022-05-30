from typing import TypeVar, Generic

from pydantic import BaseModel
from pydantic.generics import GenericModel
from fastapi import Request

from ....utils.query_string_parser import QueryStringParser

T = TypeVar('T', bound=BaseModel)


class OutputListModel(Generic[T], GenericModel):
    items: list[T]
    url: str
    number_of_items: int
    items_per_page: int
    page_number: int
    next_page: str

    @classmethod
    def create(cls, items: list[T], number_of_items: int, skip: int, take: int, request: Request):
        query = QueryStringParser(request.url.query)
        port = ""
        if request.url.port != 80:
            port = f":{request.url.port}"
        next_page_url = f"{request.url.scheme}://{request.url.hostname}{port}" \
                        f"{request.url.path}?skip={skip + take}&take={take}"

        for param in [
            query_parameter
            for query_parameter
            in query
            if query_parameter.param_name not in ('take', 'skip')
        ]:
            next_page_url += f"&{str(param)}"

        return cls(
            items=items,
            url=str(request.url),
            number_of_items=number_of_items,
            items_per_page=take,
            page_number=skip / take,
            next_page=next_page_url,
        )
