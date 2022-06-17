"""
The company datastore.
For accessing and manipulating company related data.
"""
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


class CompanyDatastore:
    """The datastore class."""

    db: DocumentDatabase
    users: UserDatastore

    def __init__(self, db: DocumentDatabase, users: UserDatastore):
        """
        Initializes the datastore with a reference to the document db.
        :param db: document db instance.
        :param users: users datastore for cross collection operations.
        """
        self.db = db
        self.users = users

    @property
    def _companies(self) -> DatabaseCollection:
        """
        Accessor for companies collection.
        :return: DatabaseCollection for companies.
        """
        return self.db.collection("companies")

    def get_companies(
        self,
        skip: int | None = None,
        take: int | None = None,
        sort_by: str | None = None,
        sort_order: SortOrder | None = None,
    ) -> list[CompanyDatabaseModel]:
        """
        Gets a list of companies.
        :param skip: number of companies to skip, for paging.
        :param take: number of companies to return, to limit response size.
        :param sort_by: field name to sort by.
        :param sort_order: asc or desc.
        :return: list of companies.
        """
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
        """
        Get a single company.
        :param company_id: id of the company to get.
        :return: company database model object.
        """
        doc = self._companies.by_id(company_id)
        return CompanyDatabaseModel(**doc)

    def add_company(
        self,
        company: CompanyCreateModel,
        user: UserDatabaseModel,
    ) -> CompanyDatabaseModel:
        """
        Add a new company to collection.
        Also adds the authenticated user as admin for the company.
        :param company: Model with data for the new company.
        :param user: The authenticated user.
        :return: The new company. CompanyDatabaseModel.
        """
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
        """
        Updates a company with given model.
        :raise NotFoundError: If company with id is not found.
        :param company: The data to update.
        :return: CompanyDatabaseModel. The updated company.
        """
        doc = self._companies.by_id(company.id)
        if doc is None:
            raise NotFoundError(
                f"No company with id '{company.id}' was found."
            )
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
        """
        Add a new contact to the company.
        :raise NotFoundError: If company with given id is not found.
        :param company_id: The id of the company to add the contact to.
        :param model: The contact model.
        :return: The added contact. ContactDatabaseModel.
        """
        doc = self._companies.by_id(company_id)
        if doc is None:
            raise NotFoundError(
                f"No company with id '{company_id}' was found."
            )

        company = CompanyDatabaseModel(**doc)
        company.contacts.append(model)
        doc.replace(company.dict())
        return model

    def add_user_to_company(
        self, company_id: str, role_name: str, user: UserDatabaseModel
    ) -> list[UserDatabaseModel]:
        """
        Adds user to company with role.

        TODO: This method is wrong. See issue:
        https://github.com/Skogstomten/produce-exchange-hub/issues/30
        https://github.com/Skogstomten/produce-exchange-hub/issues/31

        :param company_id: ID of company to add user to.
        :param role_name: Name of role to give the user.
        :param user: The user.
        :return:
        """
        self.users.add_role_to_user(user.id, role_name, company_id)
        return self.users.get_company_users(company_id)


def get_company_datastore(
    db: DocumentDatabase = Depends(get_document_database),
    user_datastore: UserDatastore = Depends(get_user_datastore),
) -> CompanyDatastore:
    """
    Dependency injection function to inject CompanyDatastore.
    :param db: Reference to document db.
    :param user_datastore: Reference to user datastore.
    :return: New instance of CompanyDatastore.
    """
    return CompanyDatastore(db, user_datastore)
