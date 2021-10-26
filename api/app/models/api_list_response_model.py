from pydantic import BaseModel
from typing import TypeVar, Generic, List

T = TypeVar('T')


class ApiListResponseModel(BaseModel, Generic[T]):
    def __init__(self, items: List[T] = None, **data):
        super(ApiListResponseModel, self).__init__(items=items, **data)

    items: List[T] = []
