"""Contains PagingResponseModel class."""
from typing import TypeVar, Generic

from fastapi import Request
from pydantic import BaseModel
from pydantic.generics import GenericModel

from app.shared.utils.query_parameter import QueryParameter
from app.shared.utils.query_string_parser import QueryStringParser
from app.shared.utils.request_utils import get_current_request_url_with_additions

T = TypeVar("T", bound=BaseModel)


class PagingResponseModel(GenericModel, Generic[T]):
    """Generic response model for paging responses when listing items."""

    items: list[T]
    url: str
    number_of_items: int
    items_per_page: int
    page_number: int
    next_page: str
    previous_page: str | None

    @classmethod
    def create(cls, items: list[T], skip: int, take: int, request: Request):
        """Creates a paging responses for the given data."""
        query = QueryStringParser(request.url.query)
        query.remove("take")
        query.remove("skip")

        next_page_url = get_current_request_url_with_additions(
            request,
            query_parameters=tuple(query)
            + (
                QueryParameter("take", take),
                QueryParameter("skip", skip + take),
            ),
            include_query=False,
        )

        previous_page_url: str | None = None
        if skip > 0:
            skip_previous_url: int = skip - take
            if skip_previous_url < 0:
                skip_previous_url = 0
            previous_page_url = get_current_request_url_with_additions(
                request,
                query_parameters=tuple(query)
                + (
                    QueryParameter("skip", skip_previous_url),
                    QueryParameter("take", take),
                ),
                include_query=False,
            )

        return cls(
            items=items,
            url=str(request.url),
            number_of_items=len(items),
            items_per_page=take,
            page_number=int(skip / take) + 1,
            next_page=next_page_url,
            previous_page=previous_page_url,
        )
