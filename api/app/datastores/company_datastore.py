from fastapi import Depends

from app.models.v1.shared import SortOrder
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.models.v1.database_models.contact_database_model import ContactDatabaseModel
from app.models.v1.database_models.company_database_model import CompanyDatabaseModel
from app.database.document_database import DocumentDatabase
from app.dependencies.document_database import get_document_database
from app.errors.not_found_error import NotFoundError
from .user_datastore import UserDatastore, get_user_datastore

IGNORE_ON_UPDATE: list[str] = ['id', 'created_date', 'activation_date']


class CompanyDatastore(object):
    db: DocumentDatabase
    users: UserDatastore

    def __init__(self, db: DocumentDatabase, users: UserDatastore):
        self.db = db
        self.users = users

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
            result.append(CompanyDatabaseModel(**doc))

        return result
    
    def get_company(self, company_id: str) -> CompanyDatabaseModel:
        collection = self.db.collection('companies')
        doc = collection.by_id(company_id)
        return CompanyDatabaseModel(**doc)

    def add_company(
            self,
            company: CompanyDatabaseModel,
            user: UserDatabaseModel,
    ) -> CompanyDatabaseModel:
        collection = self.db.collection('companies')
        doc = collection.add(company.dict())
        return CompanyDatabaseModel(**doc)

    def update_company(
            self,
            company: CompanyDatabaseModel,
            user: UserDatabaseModel,
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
        return CompanyDatabaseModel(**doc)

    def add_contact_to_company(
            self,
            company_id: str,
            model: ContactDatabaseModel,
            user: UserDatabaseModel,
    ) -> ContactDatabaseModel:
        collection = self.db.collection('companies')
        doc = collection.by_id(company_id)
        if doc is None:
            raise NotFoundError

        company = CompanyDatabaseModel(**doc)
        company.contacts.append(model)
        doc.replace(company.dict())
        return model

    def add_user_to_company(self, company_id: str, role_name: str, user: UserDatabaseModel) -> list[UserDatabaseModel]:
        self.users.add_role_to_user(user.id, role_name, company_id)
        return self.users.get_company_users(company_id)


def get_company_datastore(
        db: DocumentDatabase = Depends(get_document_database),
        user_datastore: UserDatastore = Depends(get_user_datastore),
) -> CompanyDatastore:
    return CompanyDatastore(db, user_datastore)
