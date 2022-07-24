from pydantic import BaseModel

from app.models.v1.database_models.product import Product
from app.models.v1.shared import Language
from app.utils.lang_utils import select_localized_text


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
