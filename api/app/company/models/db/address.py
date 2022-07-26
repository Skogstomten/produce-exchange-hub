from pydantic import BaseModel

from app.company.models.shared.enums import CountryCode
from app.company.models.v1.addresses import AddAddressModel


class Address(BaseModel):
    id: str
    addressee: str | None
    co_address: str | None
    street_address: str | None
    city: str | None
    zip_code: str | None
    country_code: CountryCode | None

    @classmethod
    def from_add_model(cls, new_address_id: str, model: AddAddressModel) -> "Address":
        return cls(
            id=new_address_id,
            **model.dict(),
        )
