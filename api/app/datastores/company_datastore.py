"""
The company datastore.
For accessing and manipulating company related data.
"""
from datetime import datetime

from bson import ObjectId
from fastapi import Depends, UploadFile
from pytz import utc

from app.database.document_database import DocumentDatabase, DatabaseCollection, transaction, BaseDatastore, Document
from app.dependencies.document_database import get_document_database
from app.models.v1.api_models.companies import (
    CompanyCreateModel,
    CompanyUpdateModel,
)
from app.models.v1.database_models.company_database_model import (
    CompanyDatabaseModel,
    ChangeDatabaseModel,
    ChangeType,
)
from app.models.v1.database_models.contact_database_model import (
    ContactDatabaseModel,
)
from app.models.v1.database_models.user_database_model import UserDatabaseModel
from app.models.v1.shared import SortOrder, CompanyStatus, RoleType
from .user_datastore import UserDatastore, get_user_datastore
from ..dependencies.log import AppLoggerInjector, AppLogger
from ..errors import NotFoundError, InvalidInputError
from ..io.file_manager import FileManager, get_file_manager

logger_injector = AppLoggerInjector("company_datastore")


class CompanyDatastore(BaseDatastore):
    """The datastore class."""

    def __init__(self, db: DocumentDatabase, file_manager: FileManager, users: UserDatastore, logger: AppLogger):
        super().__init__(db)
        self._file_manager = file_manager
        self._users = users
        self._logger = logger

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"CompanyDatastore(db={self.db}, users={self._users}, logger={self._logger})"

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
        authenticated_user: UserDatabaseModel | None = None,
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
        docs = self._companies.get(filters)
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

    def get_company(self, company_id: str, user: UserDatabaseModel | None) -> CompanyDatabaseModel:
        """
        Get a single company.
        :param company_id: id of the company to get.
        :param user: Authenticated user.
        :return: company database model object.
        """
        company_doc = self._get_company_doc(company_id)
        return CompanyDatabaseModel(**company_doc)

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
        model: CompanyUpdateModel,
        authenticated_user: UserDatabaseModel,
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
            current_value = company.__dict__.get(key, None)
            if current_value != value:
                company.__dict__[key] = value
                company.changes.append(
                    ChangeDatabaseModel.create(key, ChangeType.update, authenticated_user.id, authenticated_user.email)
                )

        company_doc = company_doc.replace(company.dict())
        return CompanyDatabaseModel(**company_doc)

    @transaction
    def update_company_names(
        self, company_id: str, names: dict[str, str], user: UserDatabaseModel
    ) -> CompanyDatabaseModel:
        self._companies.update_document(
            company_id,
            {
                "$set": {"name": names},
                "$push": {"changes": ChangeDatabaseModel.create("name", ChangeType.update, user.id, user.email).dict()},
            },
        )
        return self.get_company(company_id, user)

    def update_company_descriptions(
        self, company_id: str, descriptions: dict[str, str], user: UserDatabaseModel
    ) -> CompanyDatabaseModel:
        self._companies.update_document(
            company_id,
            {
                "$set": {"description": descriptions},
                "$push": {
                    "changes": ChangeDatabaseModel.create("description", ChangeType.update, user.id, user.email).dict()
                },
            },
        )
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
        company_doc = self._get_company_doc(company_id)
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

        self._users.add_role_to_user(user_id, role_name, company_id)
        self._companies.add_to_sub_collection(
            company_id,
            "changes",
            ChangeDatabaseModel.create(
                f"company.users.{user_id}", ChangeType.add, authenticated_user.id, authenticated_user.email
            ).dict(),
        )
        return self._users.get_company_users(company_id)

    def activate_company(self, company_id: str, authenticated_user: UserDatabaseModel) -> CompanyDatabaseModel:
        """Updates a companys status to active."""
        self._companies.patch_document(company_id, {"status": CompanyStatus.active})
        return self.get_company(company_id, authenticated_user)

    async def save_profile_picture(self, company_id: str, file: UploadFile, user: UserDatabaseModel) -> str:
        """
        Saves profile picture for company.
        If a profile picture already exists for company, it will be overwritten.
        URL of file will be stored on company in DB.
        :param company_id: ID of company to save picture for.
        :param file: Image bytes.
        :param user: Authenticated user.
        :return: URL for new file.
        :raise NotFoundError: If company was not found.
        """
        company = CompanyDatabaseModel(**self._get_company_doc(company_id))
        file_url = await self._file_manager.save_profile_picture(company.id, file)
        company.profile_picture_url = file_url
        company.changes.append(ChangeDatabaseModel.create("profile_picture_url", ChangeType.update, user.id, user.email))
        return file_url

    def _get_company_doc(self, company_id: str) -> Document:
        company_doc = self._companies.by_id(company_id)
        if company_doc is None:
            raise NotFoundError(f"Company with id '{company_id}' not found")
        return company_doc


def get_company_datastore(
    db: DocumentDatabase = Depends(get_document_database),
    file_manager: FileManager = Depends(get_file_manager),
    user_datastore: UserDatastore = Depends(get_user_datastore),
    logger: AppLogger = Depends(logger_injector),
) -> CompanyDatastore:
    """
    Dependency injection function to inject CompanyDatastore.
    :param db: Reference to document db.
    :param file_manager: app.io.file_manager.FileManager.
    :param user_datastore: Reference to user datastore.
    :param logger: Class logger.
    :return: New instance of CompanyDatastore.
    """
    return CompanyDatastore(db, file_manager, user_datastore, logger)
