from pydantic import BaseModel

from app.shared.models.v1.shared import Language, Currency, IntervalType


class Order(BaseModel):
    id: str
    product_id: str
    description: dict[Language, str]
    price: float | None
    currency: Currency | None
    quantity: int | None
    recurring: bool
    interval: int | None
    interval_type: IntervalType | None
