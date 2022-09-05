from pydantic import BaseModel

from app.company.models.db.order import Order
from app.company.models.shared.enums import Currency
from app.shared.models.v1.shared import Language
from app.shared.utils.lang_utils import select_localized_text


class AddOrderModel(BaseModel):
    product_id: str
    description: dict[Language, str]
    price_per_unit: float | None
    unit_type: str | None
    currency: Currency | None


class OrderOutModel(BaseModel):
    id: str
    product_id: str
    product_name: str
    description: str
    price_per_unit: float | None
    unit_type: str | None
    currency: Currency | None

    @classmethod
    def from_db_model(
        cls, order: Order, product_name: str, language: Language, company_languages: list[Language]
    ) -> "OrderOutModel":
        return cls(
            id=order.id,
            product_id=order.product_id,
            product_name=product_name,
            description=select_localized_text(order.description, language, company_languages),
            price_per_unit=order.price_per_unit,
            unit_type=order.unit_type,
            currency=order.currency,
        )
