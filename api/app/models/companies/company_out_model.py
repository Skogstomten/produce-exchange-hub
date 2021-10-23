from typing import List, Dict

from .address_out_model import AddressOutModel
from .company_api_list_model import CompanyApiListModel
from .contact_out_model import ContactOutModel
from ...datastores.base_datastore import BaseDatastore


class CompanyOutModel(CompanyApiListModel):
    addresses: List[AddressOutModel] = []
    contacts: List[ContactOutModel] = []
    produces: List[ProducesOutModel] = []
    buys: List[BuysOutModel] = []

    @staticmethod
    def create(
            company_id: str,
            data: dict,
            language: str,
            datastore: BaseDatastore
    ) -> Dict:
        result = super(CompanyOutModel).create(company_id, data, language, datastore)
        company_languages = data.get('content_languages_iso')
        result.update({
            'addresses': [
                AddressOutModel.create(
                    address,
                    language,
                    company_languages,
                    datastore
                )
                for address
                in data.get('addresses', [])
            ],
            'contacts': [
                ContactOutModel.create(contact, language, company_languages, datastore)
                for contact
                in data.get('contacts', [])
            ],
            'produces': [
                ProducesOutModel.create(produce)
                for produce
                in data.get('produces', [])
            ],
            'buys': [
                BuysOutModel.create(buys)
                for buys
                in data.get('buys', [])
            ],
        })
        return result
