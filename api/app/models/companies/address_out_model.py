from typing import Dict, Optional, List

from pydantic import BaseModel, Field

from app.datastores.base_datastore import BaseDatastore, Localization
from app.dependencies.app_headers import AppHeaders


class AddressOutModel(BaseModel):
    address_type: Optional[str] = Field(None, description='')
    addressee: Optional[str] = Field(
        None,
        description='Name used over address. Company name will be used if this is not set'
    )
    co_address: Optional[str] = None
    street_address: str
    zip_code: str
    city: str
    county: str
    country_iso: str = Field(..., min_length=2, max_length=2)
    country: str

    @classmethod
    def create(
            cls,
            data: Dict[str, str],
            headers: AppHeaders,
            company_languages: List[str],
            datastore: BaseDatastore
    ):
        return cls(
            address_type=datastore.localize_from_document(
                Localization.address_types,
                data.get('address_type', None),
                headers.language,
                company_languages
            ),
            addressee=data.get('addressee', None),
            co_address=data.get('co_address', None),
            street_address=data.get('street_address'),
            zip_code=data.get('zip_code'),
            city=data.get('city'),
            county=data.get('county'),
            country_iso=data.get('country_iso'),
            country=datastore.localize_from_document(
                Localization.countries_iso_name,
                data.get('country_iso'),
                headers.language,
                company_languages
            )
        )
