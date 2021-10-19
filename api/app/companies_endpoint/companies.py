from flask import Blueprint, request

from app.database_access.companies_datastore import CompaniesDatastore
from app.validation.validation import validate
from app.validation import schemas
from app.response_helpers import make_response

bp = Blueprint('companies', __name__, url_prefix='/companies')


@bp.route('/', methods=('GET',))
def list_companies():
    language = request.headers.get('language', 'SV')
    sort = request.args.get('sort', None)
    start = request.args.get('start', 0)
    take = request.args.get('take', None)
    datastore = CompaniesDatastore()
    companies = datastore.list_companies(sort, 'desc', start, take)
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


@bp.route('/', methods=('POST',))
@validate(schemas.companies_add_company_input_schema)
def add_company():
    language = request.headers.get('language', 'SV')
    user_id = request.headers.get('user_id', None)
    if user_id is None:
        return make_response({
            'error': 'missing user_id header'
        }, 400)
    datastore = CompaniesDatastore()
    company = datastore.add_company(request.json, user_id)
    return company.to_full_json_response(language)
