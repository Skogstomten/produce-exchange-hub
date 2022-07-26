from fastapi import Depends

from app.database.abstract.document_database import BaseDatastore, DocumentDatabase, DatabaseCollection
from app.database.dependencies.document_database import get_document_database
from app.knowlege.models.db.product import Product
from app.shared.models.v1.shared import Language


class ProductDatastore(BaseDatastore):
    """Datastore handling product related things."""

    def __init__(self, db: DocumentDatabase):
        super().__init__(db)

    @property
    def _products(self) -> DatabaseCollection:
        return self.db.collection("products")

    def get_products(self, language: Language, name_search: str) -> list[Product]:
        """
        Get products according to filter.

        :param language: Langauge to search in.
        :param name_search: Used for prefix search.
        :return: list of Product
        """
        if language and name_search:
            product_docs = self._products.like(f"name.{language.value}", name_search).to_list()
        else:
            product_docs = self._products.get_all().to_list()

        for doc in product_docs:
            yield Product(**doc)

    def add_product(self, product_name: str, language: Language) -> Product:
        """
        Add new product.
        :param product_name: The product in the given localization.
        :param language: The language of the product name.
        :return: The newly added product.
        """
        product_doc = self._products.add({"name": {language.value: product_name.title()}})
        return Product(**product_doc)

    def update_product(self, product_id: str, product: Product) -> Product:
        """
        Update product.
        :param product_id: ID of product.
        :param product: The updated product model.
        :return: The updated product.
        """
        doc = self._products.by_id(product_id).replace(product.dict())
        return Product(**doc)


def get_product_datastore(db: DocumentDatabase = Depends(get_document_database)) -> ProductDatastore:
    return ProductDatastore(db)
