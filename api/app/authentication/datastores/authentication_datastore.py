from fastapi import Depends

from app.authentication.errors.invalid_username_or_password_error import InvalidUsernameOrPasswordError
from app.authentication.models.db.user import User
from app.database.abstract.document_database import BaseDatastore, DatabaseCollection, DocumentDatabase
from app.database.dependencies.document_database import get_document_database
from app.logging.log import AppLoggerInjector, AppLogger
from app.shared.cryptography import password_hasher as hasher

logger_injector = AppLoggerInjector("AuthenticationDatastore")


class AuthenticationDatastore(BaseDatastore):
    """Datastore for authentication related database access."""

    def __init__(self, db: DocumentDatabase, logger: AppLogger):
        super().__init__(db)
        self._logger = logger

    @property
    def _users(self) -> DatabaseCollection:
        return self.db.collection("users")

    def get_user(self, email: str) -> User | None:
        """
        Get user by email.
        :param email: EMail/UserName of user.
        :return: UserDatabaseModel or None if user was not found.
        """
        self._logger.debug(f"get_user(email={email})")
        doc = self._users.by_key("email", email)
        if doc is None:
            self._logger.debug(f"get_user(email={email}): doc is None")
            return None
        return User.create(doc)

    def authenticate_user(self, email: str, password: str) -> User:
        """
        Authenticate that provided username and password matches stored.
        :raise InvalidUsernameOrPasswordError: If user can't be found with
        email or if password is not correct.
        :param email: UserName.
        :param password: Password in clear text.
        :return: User, if credentials are correct.
        """
        self._logger.debug(f"authenticate_user(email={email}, password=****)")
        user = self.get_user(email)
        if user is None:
            raise InvalidUsernameOrPasswordError()
        if not hasher.is_correct_password(password, user.password_hash):
            raise InvalidUsernameOrPasswordError()
        return user


def get_authentication_datastore(
    db: DocumentDatabase = Depends(get_document_database),
    logger: AppLogger = Depends(logger_injector)
) -> AuthenticationDatastore:
    return AuthenticationDatastore(db, logger)
