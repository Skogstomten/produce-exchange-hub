from pydantic import BaseModel
from typing import TypeVar, Generic, List

T = TypeVar('T')


class ApiListResponseModel(BaseModel, Generic[T]):
    items: List[T] = []

    @classmethod
    def create(cls, items: List[T]):
        return cls(items=items)
