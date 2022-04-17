from fastapi import Depends

from ..database.document_database import DocumentDatabase
from ..models.company import CompanyPublicOutModel, CompanyUpdateModel, CompanyCreateModel
from ..dependencies.document_database import get_document_database


class CompanyDatastore(object):
    db: DocumentDatabase

    def __init__(self, db: DocumentDatabase):
        self.db = db

    def get_companies(
            self,
            skip: int | None = None,
            take: int | None = None,
            sort_by: str | None = None,
            sort_order: str | None = None,
    ) -> list[CompanyPublicOutModel]:
        collection = self.db.collection('companies')
        docs = collection.get_all()
        if skip:
            docs = docs.skip(skip)
        if take:
            docs = docs.take(take)
        if sort_by:
            if sort_order:
                docs = docs.sort(sort_by, sort_order)
        return docs.select_for_each(
            lambda doc: CompanyPublicOutModel(id=doc.id, **doc.to_dict())
        )
    
    def get_company(self, id: str) -> CompanyPublicOutModel:
        collection = self.db.collection('companies')
        doc = collection.by_id(id)
        return CompanyPublicOutModel(id=doc.id, **doc.to_dict())

    def add_company(
            self,
            company: CompanyCreateModel,
    ) -> CompanyPublicOutModel:
        collection = self.db.collection('companies')
        doc = collection.add(company.dict())
        return CompanyPublicOutModel(id=doc.id, **doc.to_dict())

    def update_company(
            self,
            company_id: str,
            company: CompanyUpdateModel
    ) -> CompanyPublicOutModel:
        collection = self.db.collection('companies')
        doc = collection.by_id(company_id)
        data = doc.to_dict()
        for key, value in company.dict().items():
            data[key] = value
        doc = doc.replace(data)
        return CompanyPublicOutModel(id=doc.id, **doc.to_dict())


def get_company_datastore(
        db: DocumentDatabase = Depends(get_document_database)
) -> CompanyDatastore:
    return CompanyDatastore(db)
