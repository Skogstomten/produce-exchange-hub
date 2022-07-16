from fastapi import Depends

from app.database.document_database import DocumentDatabase
from app.datastores.company_datastore import CompanyDatastore
from app.dependencies.document_database import get_document_database
from app.dependencies.log import AppLogger, AppLoggerInjector
from app.models.v1.database_models.address import Address
from app.models.v1.database_models.change import Change, ChangeType
from app.models.v1.database_models.user import User

logger_injector = AppLoggerInjector("AddressDatastore")


class AddressDatastore(CompanyDatastore):
    def __init__(self, db: DocumentDatabase, logger: AppLogger):
        super().__init__(db, logger)

    def add_address(self, company_id: str, address: Address, authenticated_user: User) -> Address:
        address_dict = address.dict()
        update_context = self.db.update_context()
        update_context.push_to_list("addresses", address_dict)
        update_context.push_to_list(
            "changes",
            Change.create(f"addresses.[{address.id}]", ChangeType.add, authenticated_user.email, address_dict).dict(),
        )
        self._companies.update_document(company_id, update_context)
        return address


def get_address_datastore(
    db: DocumentDatabase = Depends(get_document_database),
    logger: AppLogger = Depends(logger_injector),
) -> AddressDatastore:
    return AddressDatastore(db, logger)
