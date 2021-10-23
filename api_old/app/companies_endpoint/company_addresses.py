from flask import Blueprint, request

from app.database_access.companies_datastore import CompaniesDatastore
from app.validation import schemas
from app.validation.validation import validate

bp = Blueprint('company_addresses', __name__, url_prefix='/companies/<string:company_id>/addresses')


@bp.route('/', methods=('GET',))
def list_addresses(company_id: str):
    language_iso = request.headers.get('language', 'SV')
    datastore = CompaniesDatastore()
    addresses = datastore.get_addresses(company_id, language_iso)
    items = []
    for address in addresses:
        items.append(address.to_dict())

    return {'items': items}


@bp.route('/', methods=('POST',))
@validate(schemas.addresses_add_address_schema)
def add_address(company_id: str):
    language_iso = request.headers.get('language', 'SV')
    datastore = CompaniesDatastore()
    address = datastore.add_address(company_id, request.json, language_iso)
    return address.to_dict()
