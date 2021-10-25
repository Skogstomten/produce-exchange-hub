from typing import List, Dict

from .address_out_model import AddressOutModel
from .buys_out_model import BuysOutModel
from .company_api_list_model import CompanyApiListModel
from .contact_out_model import ContactOutModel
from .produces_out_model import ProducesOutModel
from ...datastores.base_datastore import BaseDatastore
from ...dependencies.app_headers import AppHeaders


class CompanyOutModel(CompanyApiListModel):
    addresses: List[AddressOutModel] = []
    contacts: List[ContactOutModel] = []
    produces: List[ProducesOutModel] = []
    buys: List[BuysOutModel] = []

    @staticmethod
    def create(
            company_id: str,
            data: dict,
            headers: AppHeaders,
            datastore: BaseDatastore
    ) -> Dict:
        result = CompanyApiListModel.create(company_id, data, headers, datastore)
        company_languages = data.get('content_languages_iso')
        result.update({
            'addresses': [
                AddressOutModel.create(
                    address,
                    headers.language,
                    company_languages,
                    datastore
                )
                for address
                in data.get('addresses', [])
            ],
            'contacts': [
                ContactOutModel.create(contact, headers, company_languages, datastore)
                for contact
                in data.get('contacts', [])
            ],
            'produces': [
                ProducesOutModel.create(produce, headers, company_languages, datastore)
                for produce
                in data.get('produces', [])
            ],
            'buys': [
                BuysOutModel.create(buys, headers, company_languages, datastore)
                for buys
                in data.get('buys', [])
            ],
        })
        return result
