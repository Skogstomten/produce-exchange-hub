from datetime import datetime
from enum import Enum
from typing import List, Optional

import pytz
from pydantic import BaseModel, Field

from app.datastores.base_datastore import BaseDatastore, Localization
from app.dependencies.app_headers import AppHeaders


class CompanyStatus(Enum):
    unactivated = 'unactivated'


class AddressPostPutModel(BaseModel):
    address_type: Optional[str] = Field(None)
    addressee: Optional[str] = Field(None, description='Company name will be used if this is empty')
    co_address: Optional[str] = Field(None)
    street_address: str
    zip_code: str
    city: str
    country_iso: str
    county: str

    def to_database_dict(
            self,
            headers: AppHeaders,
            company_languages: List[str],
            datastore: BaseDatastore
    ) -> dict[str, str]:
        result = {
            'address_type': datastore.localize_from_document(
                Localization.address_types,
                self.address_type,
                headers.language,
                company_languages
            ),
            'addressee': self.addressee,
            'co_address': self.co_address,
            'street_address': self.street_address,
            'zip_code': self.zip_code,
            'city': self.city,
            'country_iso': self.country_iso,
            'county': self.county,
        }
        return result


class CompanyNamePostPutModel(BaseModel):
    language_iso: str = Field(..., min_length=2, max_length=2)
    name: str


class CompanyPostPutModel(BaseModel):
    name: List[CompanyNamePostPutModel] = Field(..., min_items=1)
    content_languages_iso: List[str] = Field(..., min_items=1)
    company_types: Optional[List[str]] = Field([])
    addresses: Optional[List[AddressPostPutModel]] = Field([])

    def to_database_dict(self, headers: AppHeaders, datastore: BaseDatastore) -> dict[str, list[dict] | dict | str]:
        result: dict[str, list[dict] | dict | str] = {
            'addresses': [],
            'authorized_users': [],
            'buys': [],
            'company_types': self.company_types,
            'contacts': [],
            'content_languages_iso': self.content_languages_iso,
            'created_date': datetime.now(pytz.utc),
            'name': {},
            'produces': [],
            'status': CompanyStatus.unactivated.value,
        }
        for address in self.addresses:
            result['addresses'].append(address.to_database_dict(headers, self.content_languages_iso, datastore))

        result['authorized_users'].append({
            'roles': ['admin'],
            'user': datastore.get_user_ref(headers.user_id),
        })

        for name in self.name:
            result['name'][name.language_iso] = name.name

        return result
