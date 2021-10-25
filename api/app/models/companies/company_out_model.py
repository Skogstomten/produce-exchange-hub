from datetime import datetime
from typing import List

from pydantic import Field, BaseModel

from .address_out_model import AddressOutModel
from .buys_out_model import BuysOutModel
from .contact_out_model import ContactOutModel
from .produces_out_model import ProducesOutModel
from ...datastores.base_datastore import BaseDatastore, Localization
from ...dependencies.app_headers import AppHeaders
from ...utilities.datetime_utilities import format_datetime


class CompanyOutModel(BaseModel):
    id: str
    name: str
    company_types: List[str]
    content_languages_iso: List[str]
    created_date: datetime = Field(..., title='Created Date')
    status: str
    addresses: List[AddressOutModel] = []
    contacts: List[ContactOutModel] = []
    produces: List[ProducesOutModel] = []
    buys: List[BuysOutModel] = []

    @classmethod
    def create(
            cls,
            company_id: str = None,
            data: dict = None,
            headers: AppHeaders = None,
            datastore: BaseDatastore = None
    ):
        company_languages = data.get('content_languages_iso')
        return cls(
            id=company_id,
            name=datastore.localize(data.get('name'), headers.language, company_languages),
            company_types=data.get('company_types', []),
            content_languages_iso=company_languages,
            created_date=format_datetime(data.get('created_date'), headers.timezone),
            status=datastore.localize_from_document(
                Localization.company_statuses,
                data.get('status'),
                headers.language,
                company_languages
            ),
            addresses=[
                AddressOutModel.create(address, headers, company_languages, datastore)
                for address in data.get('addresses', [])
            ],
            contacts=[
                ContactOutModel.create(contact, headers, company_languages, datastore)
                for contact in data.get('contacts', [])
            ],
            produces=[
                ProducesOutModel.create(produce, headers, company_languages, datastore)
                for produce in data.get('produces', [])
            ],
            buys=[
                BuysOutModel.create(buys, headers, company_languages, datastore) for buys in data.get('buys', [])
            ]
        )
