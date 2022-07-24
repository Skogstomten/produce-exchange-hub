from fastapi import Depends

from app.database.abstract.document_database import DocumentDatabase
from app.company.datastores.company_datastore import CompanyDatastore
from app.user.datastores.user_datastore import UserDatastore, get_user_datastore
from app.database.dependencies.document_database import get_document_database
from app.shared.dependencies.log import AppLogger, AppLoggerInjector
from app.shared.errors import NotFoundError, InvalidInputError
from app.user.models.v1.users import User
from app.shared.models.db.change import Change, ChangeType
from app.shared.models.v1.shared import RoleType

_logger_injector = AppLoggerInjector("CompanyUserDatastore")


class CompanyUserDatastore(CompanyDatastore):
    def __init__(self, db: DocumentDatabase, user_datastore: UserDatastore, logger: AppLogger):
        super().__init__(db, logger)
        self._user_datastore = user_datastore

    def add_user_to_company(self, company_id: str, role_name: str, user_id: str, authenticated_user: User) -> list[User]:
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
            raise InvalidInputError("Invalid role")

        self._user_datastore.add_role_to_user(authenticated_user, user_id, role_name, company_id)
        self._companies.push_to_list(
            company_id,
            "changes",
            Change.create(
                f"company.users.{user_id}", ChangeType.add, authenticated_user.email, f"{user_id}:{role_name}"
            ).dict(),
        )
        return self._user_datastore.get_company_users(company_id)


def get_company_user_datastore(
    db: DocumentDatabase = Depends(get_document_database),
    user_datastore: UserDatastore = Depends(get_user_datastore),
    logger: AppLogger = Depends(_logger_injector),
) -> CompanyUserDatastore:
    return CompanyUserDatastore(db, user_datastore, logger)
