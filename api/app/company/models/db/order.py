from pydantic import BaseModel

from app.company.models.shared.enums import Currency
from app.shared.models.v1.shared import Language


class Order(BaseModel):
    id: str
    product_id: str
    description: dict[Language, str]
    price_per_unit: float | None
    unit_type: str | None
    currency: Currency | None

    @classmethod
    def create(
        cls,
        new_id: str,
        product_id: str,
        description: dict[Language, str],
        price_per_unit: float | None = None,
        unit_type: str | None = None,
        currency: Currency | None = None,
    ) -> "Order":
        return cls(
            id=new_id,
            product_id=product_id,
            description=description,
            price_per_unit=price_per_unit,
            unit_type=unit_type,
            currency=currency,
        )
