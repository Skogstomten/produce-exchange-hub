"""Contains PagingResponseModel class."""
from typing import TypeVar, Generic

from fastapi import Request
from pydantic import BaseModel
from pydantic.generics import GenericModel

from app.company.models.v1.paging_information import PagingInformation
from app.shared.utils.query_parameter import QueryParameter
from app.shared.utils.query_string_parser import QueryStringParser
from app.shared.utils.request_utils import get_current_request_url_with_additions

T = TypeVar("T", bound=BaseModel)


class PagingResponseModel(GenericModel, Generic[T]):
    """Generic response model for paging responses when listing items."""

    items: list[T]
    url: str
    count: int
    page_size: int
    page: int
    next_page_url: str
    previous_page_url: str | None

    @classmethod
    def create(cls, items: list[T], paging_information: PagingInformation, request: Request):
        """Creates a paging responses for the given data."""
        query = QueryStringParser(request.url.query)
        query.remove("page")

        next_page_url = get_current_request_url_with_additions(
            request,
            query_parameters=tuple(query) + (QueryParameter("page", paging_information.page + 1),),
            include_query=False,
        )

        previous_page_url: str | None = None
        if not paging_information.is_first_page:
            previous_page_number = paging_information.page - 1
            if previous_page_number < 1:
                previous_page_number = 1
            previous_page_url = get_current_request_url_with_additions(
                request,
                query_parameters=tuple(query) + (QueryParameter("page", previous_page_number),),
                include_query=False,
            )

        return cls(
            items=items,
            url=str(request.url),
            count=len(items),
            page_size=paging_information.page_size,
            page=paging_information.page,
            next_page_url=next_page_url,
            previous_page_url=previous_page_url,
        )
