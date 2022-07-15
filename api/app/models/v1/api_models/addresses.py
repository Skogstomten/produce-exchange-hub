from pydantic import BaseModel

from app.dependencies.document_database import get_new_document_id
from app.models.v1.database_models.address import Address
from app.models.v1.shared import CountryCode


class AddAddressModel(BaseModel):
    addressee: str | None
    co_address: str | None
    street_address: str | None
    city: str | None
    zip_code: str | None
    country_code: CountryCode | None

    def to_database_model(self) -> Address:
        return Address(id=get_new_document_id(), **self.dict())
