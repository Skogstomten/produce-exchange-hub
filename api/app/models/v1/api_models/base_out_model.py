from pydantic import BaseModel, Field

from .operation import Operation


class BaseOutModel(BaseModel):
    operations: list[Operation] = Field([])
    url: str = Field('')
