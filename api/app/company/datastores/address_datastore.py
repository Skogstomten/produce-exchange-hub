from fastapi import Depends

from app.authentication.models.db.user import User
from app.company.models.v1.addresses import AddAddressModel
from app.database.abstract.document_database import DocumentDatabase
from app.database.dependencies.document_database import get_document_database
from app.company.datastores.company_datastore import CompanyDatastore
from app.company.models.db.address import Address
from app.logging.log import AppLogger, AppLoggerInjector
from app.shared.models.db.change import Change, ChangeType

logger_injector = AppLoggerInjector("AddressDatastore")


class AddressDatastore(CompanyDatastore):
    def __init__(self, db: DocumentDatabase, logger: AppLogger):
        super().__init__(db, logger)

    def add_address(self, company_id: str, model: AddAddressModel, authenticated_user: User) -> Address:
        address = Address.from_add_model(self.db.new_id(), model)
        address_dict = address.dict()
        update_context = self.db.update_context()
        update_context.push_to_list("addresses", address_dict)
        update_context.push_to_list(
            "changes",
            Change.create(
                self.db.new_id(), f"addresses.[{address.id}]", ChangeType.add, authenticated_user.email, address_dict
            ).dict(),
        )
        self._companies.update_document(company_id, update_context)
        return address


def get_address_datastore(
    db: DocumentDatabase = Depends(get_document_database),
    logger: AppLogger = Depends(logger_injector),
) -> AddressDatastore:
    return AddressDatastore(db, logger)
