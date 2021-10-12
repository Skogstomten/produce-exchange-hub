from flask import Blueprint, request

from app.db import get_db
from app.company import Company
from app.errors import NotFoundError
from app.response_helpers import not_found_response

bp = Blueprint('companies', __name__, url_prefix='/companies')


@bp.route('/', methods=('GET',))
def list_companies():
    language = request.headers.get('language', 'SV')
    db = get_db()
    companies = db.list_companies()
    items = []

    for item in companies:
        company = Company(item.id, item.to_dict())
        items.append(company.to_partial_json_response(language))

    response = {'items': items}
    return response


@bp.route('/<string:company_id>', methods=('GET',))
def get_company(company_id: str):
    language = request.headers.get('language', 'SV')
    db = get_db()

    try:
        company = db.get_company(company_id)
    except NotFoundError as err:
        return not_found_response(err)

    return company.to_full_json_response(language)
