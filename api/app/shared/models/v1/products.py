from pydantic import BaseModel

from app.shared.models.db.product import Product
from app.shared.models.v1.shared import Language
from app.shared.utils.lang_utils import select_localized_text


class AddProductModel(BaseModel):
    name: str


class ProductOutModel(BaseModel):
    id: str
    name: str

    @classmethod
    def from_db_model(cls, product: Product, language: Language) -> "ProductOutModel":
        return cls(id=product.id, name=select_localized_text(product.name, language, []))


class ProductUpdateModel(BaseModel):
    name: dict[Language, str]

    def to_db_model(self, product_id: str) -> Product:
        return Product(id=product_id, name={language: value.title() for language, value in self.name.items()})
