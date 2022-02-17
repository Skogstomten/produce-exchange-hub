from typing import TypeVar, Generic, List

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T', bound=BaseModel)


class OutputList(GenericModel, Generic[T]):
    items: List[T]
