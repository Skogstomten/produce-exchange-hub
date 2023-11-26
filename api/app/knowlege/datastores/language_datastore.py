# from fastapi import Depends
#
# from app.database.abstract.document_database import BaseDatastore, DatabaseCollection, DocumentDatabase
# from app.database.dependencies.document_database import get_document_database
# from app.knowlege.models.db.country import Country
#
#
# class LanguageDatastore(BaseDatastore):
#     @property
#     def _languages(self) -> DatabaseCollection:
#         return self.db.collection("languages")
#
#     def get_languages(self) -> list[Country]:
#         return [Country(**doc) for doc in self._languages.get_all().to_list()]
#
#
# def get_language_datastore(db: DocumentDatabase = Depends(get_document_database)) -> LanguageDatastore:
#     return LanguageDatastore(db)
