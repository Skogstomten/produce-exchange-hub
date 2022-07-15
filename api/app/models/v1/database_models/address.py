from pydantic import BaseModel

from app.models.v1.shared import CountryCode


class Address(BaseModel):
    id: str
    addressee: str | None
    co_address: str | None
    street_address: str | None
    city: str | None
    zip_code: str | None
    country_code: CountryCode | None
