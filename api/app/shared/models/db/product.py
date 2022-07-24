from pydantic import BaseModel

from app.shared.models.v1.shared import Language


class Product(BaseModel):
    id: str
    name: dict[Language, str]
