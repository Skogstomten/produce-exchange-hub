from flask import Blueprint, request

from app.database_access.companies_datastore import CompaniesDatastore

bp = Blueprint('companies', __name__, url_prefix='/companies')


@bp.route('/', methods=('GET',))
def list_companies():
    language = request.headers.get('language', 'SV')
    datastore = CompaniesDatastore()
    companies = datastore.list_companies()
    items = []

    for item in companies:
        items.append(item.to_partial_json_response(language))

    response = {'items': items}
    return response


@bp.route('/<string:company_id>', methods=('GET',))
def get_company(company_id: str):
    language = request.headers.get('language', 'SV')
    datastore = CompaniesDatastore()
    company = datastore.get_company(company_id)
    return company.to_full_json_response(language)
