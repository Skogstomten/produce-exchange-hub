from fastapi import Depends

from app.database.document_database import DocumentDatabase
from app.datastores.company_datastore import CompanyDatastore
from app.datastores.user_datastore import UserDatastore, get_user_datastore
from app.dependencies.document_database import get_document_database
from app.dependencies.log import AppLogger, AppLoggerInjector
from app.io.file_manager import FileManager, get_file_manager
from app.models.v1.database_models.address import Address
from app.models.v1.database_models.change import Change, ChangeType
from app.models.v1.database_models.user import User

logger_injector = AppLoggerInjector("AddressDatastore")


class AddressDatastore(CompanyDatastore):
    def __init__(
        self, db: DocumentDatabase, file_manager: FileManager, user_datastore: UserDatastore, logger: AppLogger
    ):
        super().__init__(db, file_manager, user_datastore, logger)

    def add_address(self, company_id: str, address: Address, authenticated_user: User) -> Address:
        address_dict = address.dict()
        update_context = self.db.update_context()
        update_context.push_to_list("addresses", address_dict)
        update_context.push_to_list(
            "changes",
            Change.create(f"addresses.[{address.id}]", ChangeType.add, authenticated_user.email, address_dict).dict()
        )
        self._companies.update_document(company_id, update_context)
        return address


def get_address_datastore(
    db: DocumentDatabase = Depends(get_document_database),
    file_manager: FileManager = Depends(get_file_manager),
    user_datastore: UserDatastore = Depends(get_user_datastore),
    logger: AppLogger = Depends(logger_injector),
) -> AddressDatastore:
    return AddressDatastore(db, file_manager, user_datastore, logger)
