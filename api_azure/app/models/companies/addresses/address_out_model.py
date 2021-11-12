from typing import Optional, Dict, List

from pydantic import BaseModel, Field

from app.datastores.base_datastore import BaseDatastore, Localization
from app.dependencies.app_headers import AppHeaders


class AddressOutModel(BaseModel):
    id: str = Field(...)
    address_type: Optional[str] = Field(None, description='')
    address_type_localized: Optional[str] = Field(None)
    addressee: Optional[str] = Field(
        None,
        description='Name used over address. Company name will be used if this is not set'
    )
    co_address: Optional[str] = Field(None)
    street_address: str = Field(...)
    zip_code: str = Field(...)
    city: str = Field(...)
    county: str = Field(...)
    country_iso: str = Field(..., min_length=2, max_length=2)
    country: str = Field(...)

    @classmethod
    def create(
            cls,
            address_id: str,
            data: Dict[str, str],
            headers: AppHeaders,
            company_languages: List[str],
            datastore: BaseDatastore
    ):
        address_type = data.get('address_type')
        return cls(
            id=address_id,
            address_type=address_type,
            address_type_localized=datastore.localize_from_document(
                Localization.address_types,
                address_type,
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
