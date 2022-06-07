from typing import TypeVar, Generic

from fastapi import Request
from pydantic import BaseModel
from pydantic.generics import GenericModel

from app.utils.query.query_parameter import QueryParameter
from app.utils.query.query_string_parser import QueryStringParser
from app.utils.request_utils import get_current_request_url_with_additions

T = TypeVar('T', bound=BaseModel)


class OutputListModel(GenericModel, Generic[T]):
    items: list[T]
    url: str
    number_of_items: int
    items_per_page: int
    page_number: int
    next_page: str
    previous_page: str | None

    @classmethod
    def create(cls, items: list[T], skip: int, take: int, request: Request):
        query = QueryStringParser(request.url.query)
        query.remove('take')
        query.remove('skip')

        next_page_url = get_current_request_url_with_additions(
            request,
            query_parameters=tuple(query) + (
                QueryParameter('take', take),
                QueryParameter('skip', skip + take),
            ),
            include_query=False,
        )

        previous_page_url = None
        if skip > 0:
            skip -= take
            if skip < 0:
                skip = 0
            previous_page_url = get_current_request_url_with_additions(
                request,
                query_parameters=tuple(query) + (
                    QueryParameter('skip', skip),
                    QueryParameter('take', take),
                ),
                include_query=False,
            )

        return cls(
            items=items,
            url=str(request.url),
            number_of_items=len(items),
            items_per_page=take,
            page_number=skip / take,
            next_page=next_page_url,
            previous_page=previous_page_url,
        )
