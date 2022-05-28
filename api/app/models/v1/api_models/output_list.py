from typing import TypeVar, Generic, List

from pydantic import BaseModel
from pydantic.generics import GenericModel
from fastapi import Request

T = TypeVar('T', bound=BaseModel)


class OutputListModel(Generic[T], GenericModel):
    items: List[T]
    number_of_items: int
    offset: int | None
    size: int | None
    url: str

    @classmethod
    def create(cls, items: List[T], number_of_items: int, offset: int, size: int, request: Request):
        print(items)
        return cls(
            items=items,
            number_of_items=number_of_items,
            offset=offset,
            size=size,
            url=request.url,
        )
