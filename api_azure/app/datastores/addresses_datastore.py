from typing import List, NoReturn

from fastapi import Depends
from azure.cosmos import DatabaseProxy

from .companies_datastore import CompaniesDatastore
from ..dependencies.app_headers import AppHeaders
from ..dependencies.cosmos_db import get_database_proxy
from ..models.companies.addresses.address_in_model import AddressInModel
from ..models.companies.addresses.address_out_model import AddressOutModel


class AddressesDatastore(CompaniesDatastore):
    def __init__(self, db: DatabaseProxy):
        super(AddressesDatastore, self).__init__(db)

    def get_addresses(self, company_id: str, headers: AppHeaders) -> List[AddressOutModel]:
        # company_ref, company_snapshot = self._get_ref_and_snapshot(company_id, ('content_languages_iso',))
        # data = company_snapshot.to_dict()
        # company_languages = data.get('content_languages_iso')
        # for address in company_ref.collection('addresses').get():
        #     yield AddressOutModel.create(address.id, address.to_dict(), headers, company_languages, self)
        return []

    def get_address(self, company_id: str, address_id: str, headers: AppHeaders) -> AddressOutModel:
        # company_ref, company_snapshot = self._get_ref_and_snapshot(company_id, ('content_languages_iso',))
        # address_ref, address_snapshot = self._get_ref_and_snapshot(
        #     address_id,
        #     parent_doc_ref=company_ref,
        #     sub_collection_name='addresses'
        # )
        # company_languages = company_snapshot.to_dict().get('content_languages_iso')
        # return AddressOutModel.create(address_id, address_snapshot.to_dict(), headers, company_languages, self)
        pass

    def add_address(self, company_id: str, body: AddressInModel, headers: AppHeaders) -> AddressOutModel:
        # company_ref, company_snapshot = self._get_ref_and_snapshot(company_id)
        # address_ref: DocumentReference = company_ref.collection('addresses').document()
        # address_ref.create(body.to_database_dict())
        # return self.get_address(company_id, address_ref.id, headers)
        pass

    def update_address(
            self,
            company_id: str,
            address_id: str,
            body: AddressInModel,
            headers: AppHeaders
    ) -> AddressOutModel:
        # company_ref, company_snapshot = self._get_ref_and_snapshot(company_id)
        # address_ref, address_snapshot = self._get_ref_and_snapshot(
        #     address_id,
        #     parent_doc_ref=company_ref,
        #     sub_collection_name='addresses'
        # )
        # address_ref.update(body.to_database_dict())
        # return self.get_address(company_id, address_id, headers)
        pass

    def delete_address(self, company_id: str, address_id: str) -> NoReturn:
        # self._get_ref_and_snapshot(
        #     address_id,
        #     parent_doc_ref=self._get_ref_and_snapshot(company_id)[0],
        #     sub_collection_name='addresses'
        # )[0].delete()
        pass


def get_addresses_datastore(db: DatabaseProxy = Depends(get_database_proxy)) -> AddressesDatastore:
    return AddressesDatastore(db)
