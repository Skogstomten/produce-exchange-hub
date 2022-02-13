from fastapi import Depends

from ..database.document_database import DocumentDatabase
from ..models.company import CompanyPublic
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
    ) -> list[CompanyPublic]:
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
            lambda doc: CompanyPublic(id=doc.id, **doc.dict())
        )


def get_company_datastore(
        db: DocumentDatabase = Depends(get_document_database)
) -> CompanyDatastore:
    return CompanyDatastore(db)
