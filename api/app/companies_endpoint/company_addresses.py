from flask import Blueprint

from app.database_access.companies_datastore import CompaniesDatastore

bp = Blueprint('company_addresses', __name__, url_prefix='/companies/<string:company_id>/addresses')


@bp.route('/', methods=('GET',))
def list_addresses(company_id: str):
    datastore = CompaniesDatastore()
    addresses = datastore.get_addresses(company_id)
    items = []
    for address in addresses:
        items.append(address.to_dict())

    return {'items': items}
