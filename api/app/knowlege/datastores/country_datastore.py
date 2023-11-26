# from fastapi import Depends
#
# from app.database.abstract.document_database import BaseDatastore, DocumentDatabase, DatabaseCollection
# from app.database.dependencies.document_database import get_document_database
# from app.knowlege.models.db.country import Country
#
#
# class CountryDatastore(BaseDatastore):
#     @property
#     def _countries(self) -> DatabaseCollection:
#         return self.db.collection("countries")
#
#     def get_countries(self) -> list[Country]:
#         docs = self._countries.get_all().to_list()
#         return [Country(**doc) for doc in docs]
#
#
# def get_country_datastore(db: DocumentDatabase = Depends(get_document_database)) -> CountryDatastore:
#     return CountryDatastore(db)
