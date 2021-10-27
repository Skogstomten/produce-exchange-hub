from typing import Optional

from pydantic import BaseModel, Field


class AddressInModel(BaseModel):
    address_type: Optional[str] = Field(None, description='')
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

    def to_database_dict(self) -> dict[str, str]:
        result = {
            'address_type': self.address_type,
            'addressee': self.addressee,
            'co_address': self.co_address,
            'street_address': self.street_address,
            'zip_code': self.zip_code,
            'city': self.city,
            'county': self.county,
            'country_iso': self.country_iso,
        }
        return result
