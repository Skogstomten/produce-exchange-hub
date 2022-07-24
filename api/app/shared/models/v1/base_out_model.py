"""Base class model that other models can inherit from."""
from pydantic import BaseModel, Field

from app.shared.models.v1.operation import Operation


class BaseOutModel(BaseModel):
    """Base class model that other models can inherit from."""

    operations: list[Operation] = Field([])
    url: str = Field("")
