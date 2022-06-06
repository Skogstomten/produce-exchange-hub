from fastapi import Depends

from app.models.v1.shared import SortOrder
from app.models.v1.users import UserInternal
from app.models.v1.database_models.contact_database_model import ContactDatabaseModel
from app.models.v1.database_models.companies import CompanyDatabaseModel
from app.database.document_database import DocumentDatabase
from app.dependencies.document_database import get_document_database
from app.errors.not_found_error import NotFoundError

IGNORE_ON_UPDATE: list[str] = ['id', 'created_date', 'activation_date']


class CompanyDatastore(object):
    db: DocumentDatabase

    def __init__(self, db: DocumentDatabase):
        self.db = db

    def get_companies(
            self,
            skip: int | None = None,
            take: int | None = None,
            sort_by: str | None = None,
            sort_order: SortOrder | None = None,
    ) -> list[CompanyDatabaseModel]:
        collection = self.db.collection('companies')
        docs = collection.get_all()
        if skip:
            docs = docs.skip(skip)
        if take:
            docs = docs.take(take)
        if sort_by:
            if sort_order:
                docs = docs.sort(sort_by, sort_order.value)

        result = []
        for doc in docs.to_list():
            result.append(CompanyDatabaseModel.create_from_doc(doc))

        return result
    
    def get_company(self, company_id: str) -> CompanyDatabaseModel:
        collection = self.db.collection('companies')
        doc = collection.by_id(company_id)
        return CompanyDatabaseModel.create_from_doc(doc)

    def add_company(
            self,
            company: CompanyDatabaseModel,
            user: UserInternal,
    ) -> CompanyDatabaseModel:
        collection = self.db.collection('companies')
        doc = collection.add(company.dict())
        return CompanyDatabaseModel.create_from_doc(doc)

    def update_company(
            self,
            company: CompanyDatabaseModel,
            user: UserInternal,
    ) -> CompanyDatabaseModel:
        collection = self.db.collection('companies')
        doc = collection.by_id(company.id)
        if doc is None:
            raise NotFoundError
        data = doc.to_dict()
        for key, value in company.dict().items():
            if key not in IGNORE_ON_UPDATE:
                data[key] = value
        doc = doc.replace(data)
        return CompanyDatabaseModel.create_from_doc(doc)

    def add_contact_to_company(
            self,
            company_id: str,
            model: ContactDatabaseModel,
            user: UserInternal,
    ) -> ContactDatabaseModel:
        collection = self.db.collection('companies')
        doc = collection.by_id(company_id)
        if doc is None:
            raise NotFoundError

        data = doc.to_dict()
        contacts = data.get('contacts') if 'contacts' in data else []
        contacts.append(model.dict())
        data['contacts'] = contacts
        doc.replace(data)
        return model


def get_company_datastore(
        db: DocumentDatabase = Depends(get_document_database)
) -> CompanyDatastore:
    return CompanyDatastore(db)
