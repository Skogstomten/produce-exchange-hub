from fastapi import Depends

from app.database.document_database import BaseDatastore, DocumentDatabase
from app.dependencies.document_database import get_document_database
from app.errors import DuplicateError
from app.models.v1.database_models.product import Product
from app.models.v1.shared import Language


class ProductDatastore(BaseDatastore):
    def __init__(self, db: DocumentDatabase):
        super().__init__(db)

    @property
    def _products(self):
        return self.db.collection("products")

    def add_product(self, product_name: str, language: Language) -> Product:
        if self._products.exists({"name": {language: "*"}}):
            raise DuplicateError(f"There's already a product with the product name '{product_name}'")
        product_doc = self._products.add({"name": {language.value: product_name}})
        return Product(**product_doc)


def get_product_datastore(db: DocumentDatabase = Depends(get_document_database)) -> ProductDatastore:
    return ProductDatastore(db)
