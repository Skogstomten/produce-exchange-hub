from pydantic import BaseModel

from app.company.models.v1.addresses import AddAddressModel
from app.shared.models.v1.shared import CountryCode


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
