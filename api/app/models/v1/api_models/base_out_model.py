from pydantic import BaseModel

from .operation import Operation


class BaseOutModel(BaseModel):
    operations: list[Operation]
    url: str
