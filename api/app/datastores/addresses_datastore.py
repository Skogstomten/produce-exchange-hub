from typing import List, Tuple, Iterable

from fastapi import Depends
from google.cloud.firestore_v1 import Client, DocumentReference, DocumentSnapshot

from app.datastores.companies_datastore import CompaniesDatastore
from app.dependencies.app_headers import AppHeaders
from app.dependencies.firestore import get_db_client
from app.errors.not_found_error import NotFoundError
from app.models.companies.addresses.address_in_model import AddressInModel
from app.models.companies.addresses.address_out_model import AddressOutModel


def _get_address_ref_and_snapshot(
        company_ref: DocumentReference,
        address_id: str,
        field_paths: Iterable[str] | None = None
) -> Tuple[DocumentReference, DocumentSnapshot]:
    ref = company_ref.collection('addresses').document(address_id)
    snapshot = ref.get(field_paths)
    if not snapshot.exists:
        raise NotFoundError(f"No address with id '{address_id}' was found")
    return ref, snapshot


class AddressesDatastore(CompaniesDatastore):
    def __init__(self, db: Client):
        super(AddressesDatastore, self).__init__(db)

    def get_addresses(self, company_id: str, headers: AppHeaders) -> List[AddressOutModel]:
        company_ref, company_snapshot = self._get_company_ref_and_snapshot(company_id, ('content_languages_iso',))
        data = company_snapshot.to_dict()
        company_languages = data.get('content_languages_iso')
        for address in company_ref.collection('addresses').get():
            yield AddressOutModel.create(address.id, address.to_dict(), headers, company_languages, self)

    def get_address(self, company_id: str, address_id: str, headers: AppHeaders) -> AddressOutModel:
        company_ref, company_snapshot = self._get_company_ref_and_snapshot(company_id, ('content_languages_iso',))
        address_ref, address_snapshot = _get_address_ref_and_snapshot(company_ref, address_id)
        company_languages = company_snapshot.to_dict().get('content_languages_iso')
        return AddressOutModel.create(address_id, address_snapshot.to_dict(), headers, company_languages, self)

    def add_address(self, company_id: str, body: AddressInModel, headers: AppHeaders) -> AddressOutModel:
        company_ref, company_snapshot = self._get_company_ref_and_snapshot(company_id)
        address_ref: DocumentReference = company_ref.collection('addresses').document()
        address_ref.create(body.to_database_dict())
        return self.get_address(company_id, address_ref.id, headers)

    def update_address(
            self,
            company_id: str,
            address_id: str,
            body: AddressInModel,
            headers: AppHeaders
    ) -> AddressOutModel:
        company_ref, company_snapshot = self._get_company_ref_and_snapshot(company_id)
        address_ref, address_snapshot = _get_address_ref_and_snapshot(company_ref, address_id)
        address_ref.update(body.to_database_dict())
        return self.get_address(company_id, address_id, headers)


def get_addresses_datastore(db: Client = Depends(get_db_client)) -> AddressesDatastore:
    return AddressesDatastore(db)
