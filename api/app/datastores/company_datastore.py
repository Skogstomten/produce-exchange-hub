"""
The company datastore.
For accessing and manipulating company related data.
"""
from datetime import datetime

from bson import ObjectId
from fastapi import Depends
from pytz import utc

from app.database.document_database import DocumentDatabase, DatabaseCollection, transaction, BaseDatastore, Document
from app.dependencies.document_database import get_document_database
from app.models.v1.database_models.user import User
from app.models.v1.shared import SortOrder, CompanyStatus
from ..dependencies.log import AppLoggerInjector, AppLogger
from ..errors import NotFoundError
from ..models.v1.api_models.companies import CompanyCreateModel, CompanyUpdateModel
from ..models.v1.database_models.change import Change, ChangeType
from ..models.v1.database_models.company import CompanyDatabaseModel
from ..models.v1.database_models.contact import ContactDatabaseModel

logger_injector = AppLoggerInjector("company_datastore")


class CompanyDatastore(BaseDatastore):
    """The datastore class."""

    def __init__(self, db: DocumentDatabase, logger: AppLogger):
        super().__init__(db)
        self._logger = logger

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"CompanyDatastore(db={self.db}, logger={self._logger})"

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
        authenticated_user: User | None = None,
    ) -> list[CompanyDatabaseModel]:
        """
        Gets a list of companies.
        :param skip: number of companies to skip, for paging.
        :param take: number of companies to return, to limit response size.
        :param sort_by: field name to sort by.
        :param sort_order: asc or desc.
        :param authenticated_user: If any.
        :return: list of companies.
        """
        self._logger.debug(
            f"CompanyDatastore.get_companies(skip={skip}, take={take}, sort_by={sort_by}, sort_order={sort_order}, "
            f"authenticated_user={authenticated_user})"
        )

        filters = {}
        if authenticated_user is None:
            filters["status"] = CompanyStatus.active
        else:
            if not authenticated_user.is_superuser():
                company_admins = authenticated_user.get_roles("company_admin")
                if not company_admins:
                    filters["status"] = CompanyStatus.active
                else:
                    filters.update(
                        {
                            "$or": [
                                {"status": CompanyStatus.active},
                                *[{"_id": ObjectId(role.reference)} for role in company_admins],
                            ]
                        }
                    )

        self._logger.debug(f"Querying companies: filters={filters}")
        docs = self._companies.get(filters, CompanyDatabaseModel.brief())
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

        self._logger.debug(f"Result from get_companies={result}")

        return result

    def get_company(self, company_id: str, user: User | None) -> CompanyDatabaseModel:
        """
        Get a single company.
        :param company_id: ID of the company to get.
        :param user: Authenticated user.
        :return: Company database model object.
        """
        company_doc = self._get_company_doc(company_id)
        company = CompanyDatabaseModel(**company_doc)
        if company.status != CompanyStatus.active:
            if user.is_superuser():
                return company
            if user.get_role("company_admin").reference == company_id:
                return company
        else:
            return company
        raise NotFoundError(f"Company '{company_id}' not found")

    def add_company(
        self,
        company: CompanyCreateModel,
        user: User,
    ) -> CompanyDatabaseModel:
        """
        Add a new company to collection.
        Also adds the authenticated user as admin for the company.
        :param company: Model with data for the new company.
        :param user: The authenticated user.
        :return: The new company. CompanyDatabaseModel.
        """
        data = company.dict()
        data.update(
            {
                "status": CompanyStatus.created.value,
                "created_date": datetime.now(utc),
                "activation_date": None,
                "description": {},
                "contacts": [],
                "changes": [Change.create("init", ChangeType.add, user.email, data)],
            }
        )
        doc = self._companies.add(data)
        return CompanyDatabaseModel(**doc)

    def update_company(
        self,
        company_id: str,
        model: CompanyUpdateModel,
        authenticated_user: User,
    ) -> CompanyDatabaseModel:
        """
        Updates a company with given model.
        :raise NotFoundError: If company with id is not found.
        :param company_id: ID of company to update.
        :param model: The data to update.
        :param authenticated_user: User performing the update.
        :return: CompanyDatabaseModel. The updated company.
        """
        company_doc = self._get_company_doc(company_id)

        company = CompanyDatabaseModel(**company_doc)
        for key, value in model.__dict__.items():
            current_value = company.__dict__.get(key)
            if current_value != value:
                company.__dict__[key] = value
                company.changes.append(Change.create(key, ChangeType.update, authenticated_user.email, value))

        company_doc = company_doc.replace(company.dict())
        return CompanyDatabaseModel(**company_doc)

    @transaction
    def update_company_names(self, company_id: str, names: dict[str, str], user: User) -> CompanyDatabaseModel:
        update_context = self.db.update_context()
        update_context.set_values({"name": names})
        update_context.push_to_list("changes", Change.create("name", ChangeType.update, user.email, names).dict())
        self._companies.update_document(
            company_id,
            update_context,
        )
        return self.get_company(company_id, user)

    def update_company_descriptions(
        self, company_id: str, descriptions: dict[str, str], user: User
    ) -> CompanyDatabaseModel:
        update_context = self.db.update_context()
        update_context.set_values({"description": descriptions})
        update_context.push_to_list(
            "changes", Change.create("description", ChangeType.update, user.email, descriptions).dict()
        )
        self._companies.update_document(company_id, update_context)
        return self.get_company(company_id, user)

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
        self._companies.push_to_list(company_id, "contacts", model.dict())
        return model

    @transaction
    def update_contact(
        self,
        company_id: str,
        model: ContactDatabaseModel,
        authenticated_user: User,
    ) -> ContactDatabaseModel:
        """
        Updates contact on company.
        :param company_id: ID of company to update contact on.
        :param model: Database model object with updated contact data.
        :param authenticated_user: User object for authenticated user. For change logging.
        :return: Updated contact model.
        """
        company_doc = self._get_company_doc(company_id)
        company = CompanyDatabaseModel(**company_doc)
        contact = next((c for c in company.contacts if c.id == model.id), None)
        if contact is None:
            raise NotFoundError(f"Contact with id '{model.id}' not found on company '{company_id}'.")

        contact.type = model.type
        contact.value = model.value
        contact.description = model.description
        contact.changed_by = authenticated_user.email
        contact.changed_at = datetime.now(utc)

        change = Change.create(f"contacts.{contact.id}", ChangeType.update, authenticated_user.email, contact.dict())
        company.changes.append(change)

        company_doc.replace(company.dict())
        return contact

    def delete_contact(self, company_id: str, contact_id: str, user: User) -> None:
        """
        Delete a contact from company.

        :param company_id: ID of company to delete from.
        :param contact_id: ID of contact to be deleted.
        :param user: Authenticated user who's deleting.

        :return: None.

        :raises app.errors.NotFoundError: if company or contact does not exist.
        """
        company_doc = self._get_company_doc(company_id)
        company = CompanyDatabaseModel(**company_doc)
        contact = next((c for c in company.contacts if c.id == contact_id), None)
        if contact is None:
            raise NotFoundError(f"No contact with id '{contact_id}' was found.")

        company.changes.append(
            Change.create(
                f"company.contacts.{contact_id}",
                ChangeType.delete,
                user.email,
                None,
            )
        )
        company.contacts.remove(contact)
        company_doc.replace(company.dict())

    def activate_company(self, company_id: str, authenticated_user: User) -> CompanyDatabaseModel:
        """Updates a companys status to active."""
        return self._change_status(company_id, authenticated_user, CompanyStatus.active)

    def deactivate_company(self, company_id: str, authenticated_user: User) -> CompanyDatabaseModel:
        """Updates company status to 'deactivated'."""
        return self._change_status(company_id, authenticated_user, CompanyStatus.deactivated)

    def _get_company_doc(self, company_id: str) -> Document:
        company_doc = self._companies.by_id(company_id)
        if company_doc is None:
            raise NotFoundError(f"Company with id '{company_id}' not found")
        return company_doc

    def _change_status(self, company_id: str, authenticated_user: User, status: CompanyStatus) -> CompanyDatabaseModel:
        update_context = self.db.update_context()
        update_context.set_values({"status": status})
        update_context.push_to_list(
            "changes", Change.create("status", ChangeType.update, authenticated_user.email, status)
        )
        self._companies.update_document(company_id, update_context)
        return self.get_company(company_id, authenticated_user)


def get_company_datastore(
    db: DocumentDatabase = Depends(get_document_database),
    logger: AppLogger = Depends(logger_injector),
) -> CompanyDatastore:
    """
    Dependency injection function to inject CompanyDatastore.
    :param db: Reference to document db.
    :param logger: Class logger.
    :return: New instance of CompanyDatastore.
    """
    return CompanyDatastore(db, logger)
