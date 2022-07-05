"""
The company datastore.
For accessing and manipulating company related data.
"""
from datetime import datetime
from pytz import utc

from fastapi import Depends

from app.models.v1.shared import SortOrder, CompanyStatus, RoleType
from app.models.v1.api_models.companies import (
    CompanyCreateModel,
    CompanyUpdateModel,
)
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.models.v1.database_models.contact_database_model import (
    ContactDatabaseModel,
)
from app.models.v1.database_models.company_database_model import (
    CompanyDatabaseModel,
    ChangeDatabaseModel,
    ChangeType,
)
from app.database.document_database import DocumentDatabase, DatabaseCollection, transaction, BaseDatastore
from app.dependencies.document_database import get_document_database
from .user_datastore import UserDatastore, get_user_datastore
from ..dependencies.log import AppLoggerInjector, AppLogger
from ..errors import NotFoundError, InvalidInputError

logger_injector = AppLoggerInjector("company_datastore")


class CompanyDatastore(BaseDatastore):
    """The datastore class."""
    def __init__(self, db: DocumentDatabase, users: UserDatastore, logger: AppLogger):
        """
        Initializes the datastore with a reference to the document db.
        :param db: document db instance.
        :param users: users datastore for cross collection operations.
        """
        super().__init__(db)
        self.users = users
        self.logger = logger

    @property
    def _companies(self) -> DatabaseCollection:
        """
        Accessor for companies collection.
        :return: DatabaseCollection for companies.
        """
        return self.db.collection("companies")

    @property
    def _roles(self) -> DatabaseCollection:
        """Accessor for roles collection."""
        return self.db.collection("roles")

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
        self.logger.debug(
            f"CompanyDatastore.get_companies(skip={skip}, take={take}, sort_by={sort_by}, sort_order={sort_order})"
        )
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
        self.add_user_to_company(doc.id, "company_admin", user.id, user)
        return CompanyDatabaseModel(**doc)

    def update_company(
        self,
        company_id: str,
        company: CompanyUpdateModel,
    ) -> CompanyDatabaseModel:
        """
        Updates a company with given model.
        :raise NotFoundError: If company with id is not found.
        :param company_id: ID of company to update.
        :param company: The data to update.
        :return: CompanyDatabaseModel. The updated company.
        """
        doc = self._companies.by_id(company_id)
        if doc is None:
            raise NotFoundError(f"No company with id '{company_id}' was found.")
        for key, value in company.dict().items():
            doc[key] = value
        doc = doc.replace(doc)
        return CompanyDatabaseModel(**doc)

    def add_contact(
        self,
        company_id: str,
        model: ContactDatabaseModel,
    ) -> ContactDatabaseModel:
        """
        Add a new contact to the company.

        :param company_id: The id of the company to add the contact to.
        :param model: The contact model.

        :return: The added contact. ContactDatabaseModel.
        """
        self._companies.add_to_sub_collection(company_id, "contacts", model.dict())
        return model

    @transaction
    def update_contact(
        self,
        company_id: str,
        model: ContactDatabaseModel,
        authenticated_user: UserDatabaseModel,
    ) -> ContactDatabaseModel:
        """
        Updates contact on company.
        :param company_id: ID of company to update contact on.
        :param model: Database model object with updated contact data.
        :param authenticated_user: User object for authenticated user. For change logging.
        :return: Updated contact model.
        """
        company_doc = self._companies.by_id(company_id)
        if company_doc is None:
            raise NotFoundError(f"Company with id '{company_id}' not found.")

        company = CompanyDatabaseModel(**company_doc)
        contact = next((c for c in company.contacts if c.id == model.id), None)
        if contact is None:
            raise NotFoundError(f"Contact with id '{model.id}' not found on company '{company_id}'.")

        contact.type = model.type
        contact.value = model.value
        contact.description = model.description
        contact.changed_by = authenticated_user.email
        contact.changed_at = datetime.now(utc)

        change = ChangeDatabaseModel.create(
            f"contacts.{contact.id}", ChangeType.update, authenticated_user.id, authenticated_user.email
        )
        company.changes.append(change)

        company_doc.replace(company.dict())
        return contact

    def delete_contact(self, company_id: str, contact_id: str, user: UserDatabaseModel) -> None:
        """
        Delete a contact from company.

        :param company_id: ID of company to delete from.
        :param contact_id: ID of contact to be deleted.
        :param user: Authenticated user who's deleting.

        :return: None.

        :raises app.errors.NotFoundError: if company or contact does not exist.
        """
        company_doc = self._companies.by_id(company_id)
        if company_doc is None:
            raise NotFoundError(f"No company with id '{company_id}' was found.")

        company = CompanyDatabaseModel(**company_doc)
        contact = next((c for c in company.contacts if c.id == contact_id), None)
        if contact is None:
            raise NotFoundError(f"No contact with id '{contact_id}' was found.")

        company.changes.append(
            ChangeDatabaseModel.create(
                f"company.contacts.{contact_id}",
                ChangeType.delete,
                user.id,
                user.email,
            )
        )
        company.contacts.remove(contact)
        company_doc.replace(company.dict())

    def add_user_to_company(
        self, company_id: str, role_name: str, user_id: str, authenticated_user: UserDatabaseModel
    ) -> list[UserDatabaseModel]:
        """
        Adds user to company with role.

        :param company_id: ID of company to add user to.
        :param role_name: Name of role to give the user. Has to be role of type company_role.
            It is not allowed to give other roles to user through this method.
        :param user_id: ID of user to receive the role.
        :param authenticated_user: User performing operation.

        :return: List of users connected to company.

        :raise app.errors.NotFoundError: If company or user is not found.
        :raise app.errors.InvalidInputError: If provided role is not of type company_role.
        """
        if not self._companies.exists({"id": company_id}):
            raise NotFoundError(f"No company with id '{company_id}' was found.")

        if not self._roles.exists({"name": role_name, "type": RoleType.company_role}):
            raise InvalidInputError("Invalid role.")

        self.users.add_role_to_user(user_id, role_name, company_id)
        self._companies.add_to_sub_collection(
            company_id,
            "changes",
            ChangeDatabaseModel.create(
                f"company.users.{user_id}", ChangeType.add, authenticated_user.id, authenticated_user.email
            ).dict(),
        )
        return self.users.get_company_users(company_id)

    def activate_company(self, company_id: str) -> CompanyDatabaseModel:
        """Updates a companys status to active."""
        self._companies.patch_document(company_id, {"status": CompanyStatus.active})
        return self.get_company(company_id)


def get_company_datastore(
    db: DocumentDatabase = Depends(get_document_database),
    user_datastore: UserDatastore = Depends(get_user_datastore),
    logger: AppLogger = Depends(logger_injector),
) -> CompanyDatastore:
    """
    Dependency injection function to inject CompanyDatastore.
    :param db: Reference to document db.
    :param user_datastore: Reference to user datastore.
    :param logger: Class logger.
    :return: New instance of CompanyDatastore.
    """
    return CompanyDatastore(db, user_datastore, logger)
