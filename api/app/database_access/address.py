class Address(object):
    address_type: str | None = None
    addressee: str | None = None
    co_address: str | None = None
    street_address: str
    zip_code: str
    city: str
    country_iso: str
    country: str
    county: str

    def __init__(self, address: dict[str, str]):
        self.address_type = address.get('address_type', None)
        self.addressee = address.get('addressee', None)
        self.co_address = address.get('co_address', None)
        self.street_address = address.get('street_address')
        self.zip_code = address.get('zip_code')
        self.city = address.get('city')
        self.country_iso = address.get('country_iso')
        self.country = address.get('country')
        self.county = address.get('county')

    def to_dict(self) -> dict:
        return {
            'address_type': self.address_type,
            'addressee': self.addressee,
            'co_address': self.co_address,
            'street_address': self.street_address,
            'zip_code': self.zip_code,
            'city': self.city,
            'country_iso': self.country_iso,
            'country': self.country,
            'county': self.county,
        }
