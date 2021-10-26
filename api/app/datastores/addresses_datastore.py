from typing import List

from fastapi import Depends
from google.cloud.firestore_v1 import Client

from app.datastores.companies_datastore import CompaniesDatastore
from app.dependencies.app_headers import AppHeaders
from app.dependencies.firestore import get_db_client
from app.models.companies.in_models.company_post_put_model import AddressPostPutModel
from app.models.companies.out_models.address_out_model import AddressOutModel


class AddressesDatastore(CompaniesDatastore):
    def __init__(self, db: Client):
        super(AddressesDatastore, self).__init__(db)

    def get_addresses(self, company_id: str, headers: AppHeaders) -> List[AddressOutModel]:
        company_ref, company_snapshot = self._get_company_ref_and_snapshot(company_id)
        data = company_snapshot.to_dict()
        addresses = data.get('addresses', [])
        company_languages = data.get('content_languages_iso')
        for address in addresses:
            yield AddressOutModel.create(address, headers, company_languages, self)

    def add_address(self, company_id: str, body: AddressPostPutModel, headers: AppHeaders):
        ref, snapshot = self._get_company_ref_and_snapshot(company_id)
        company_data = snapshot.to_dict()
        company_languages = company_data.get('content_languages_iso')
        addresses: list = company_data.get('addresses', [])
        addresses.append(body.to_database_dict(headers, company_languages, self))
        ref.update({
            'addresses': addresses
        })
        return self.get_addresses(company_id, headers)

    def update_addresses(self, company_id: str, addresses: List[AddressPostPutModel], headers: AppHeaders):
        ref, snapshot = self._get_company_ref_and_snapshot(company_id)
        company_languages = snapshot.to_dict().get('content_languages_iso')
        ref.update({
            'addresses': [address.to_database_dict(headers, company_languages, self) for address in addresses]
        })
        return self.get_addresses(company_id, headers)


def get_addresses_datastore(db: Client = Depends(get_db_client)) -> AddressesDatastore:
    return AddressesDatastore(db)
