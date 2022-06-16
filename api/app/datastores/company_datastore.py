from datetime import datetime
from pytz import utc

from fastapi import Depends

from app.models.v1.shared import SortOrder, CompanyStatus
from app.models.v1.api_models.companies import CompanyCreateModel
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.models.v1.database_models.contact_database_model import (
    ContactDatabaseModel,
)
from app.models.v1.database_models.company_database_model import (
    CompanyDatabaseModel,
)
from app.database.document_database import DocumentDatabase, DatabaseCollection
from app.dependencies.document_database import get_document_database
from app.errors.not_found_error import NotFoundError
from .user_datastore import UserDatastore, get_user_datastore

IGNORE_ON_UPDATE: tuple = ("id", "created_date", "activation_date")


class CompanyDatastore(object):
    db: DocumentDatabase
    users: UserDatastore

    def __init__(self, db: DocumentDatabase, users: UserDatastore):
        self.db = db
        self.users = users

    @property
    def _companies(self) -> DatabaseCollection:
        return self.db.collection("companies")

    def get_companies(
        self,
        skip: int | None = None,
        take: int | None = None,
        sort_by: str | None = None,
        sort_order: SortOrder | None = None,
    ) -> list[CompanyDatabaseModel]:
        docs = self._companies.get_all()
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
        doc = self._companies.by_id(company_id)
        return CompanyDatabaseModel(**doc)

    def add_company(
        self,
        company: CompanyCreateModel,
        user: UserDatabaseModel,
    ) -> CompanyDatabaseModel:
        datum = company.dict()
        datum.update(
            {
                "status": CompanyStatus.created.value,
                "created_date": datetime.now(utc),
                "activation_date": None,
                "description": {},
                "contacts": [],
            }
        )
        doc = self._companies.add(datum)
        self.add_user_to_company(doc.id, "company_admin", user)
        return CompanyDatabaseModel(**doc)

    def update_company(
        self,
        company: CompanyDatabaseModel,
    ) -> CompanyDatabaseModel:
        doc = self._companies.by_id(company.id)
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
    ) -> ContactDatabaseModel:
        doc = self._companies.by_id(company_id)
        if doc is None:
            raise NotFoundError

        company = CompanyDatabaseModel(**doc)
        company.contacts.append(model)
        doc.replace(company.dict())
        return model

    def add_user_to_company(
        self, company_id: str, role_name: str, user: UserDatabaseModel
    ) -> list[UserDatabaseModel]:
        self.users.add_role_to_user(user.id, role_name, company_id)
        return self.users.get_company_users(company_id)


def get_company_datastore(
    db: DocumentDatabase = Depends(get_document_database),
    user_datastore: UserDatastore = Depends(get_user_datastore),
) -> CompanyDatastore:
    return CompanyDatastore(db, user_datastore)
