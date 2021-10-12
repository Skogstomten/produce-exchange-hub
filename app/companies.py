from time import strftime

from flask import Blueprint, request

from app.db import get_db, DocumentDatabase

bp = Blueprint('companies', __name__, url_prefix='/companies')


@bp.route('/', methods=('GET',))
def producers():
    language = request.headers.get('language', 'SV')

    db = get_db()
    companies = db.list_companies()
    items = []

    for company in companies:
        raw_data = company.to_dict()
        company_languages: list = raw_data['content_languages_iso']

        item = {
            'addresses': raw_data['addresses'],
            'contacts': raw_data['contacts'],
            'content_language_iso': raw_data['content_languages_iso'],
            'company_types': _build_company_types_node(raw_data['company_types'], language, company_languages),
            'buys': _build_buys_node(raw_data['buys'], language, company_languages),
            'created_date': raw_data['created_date'].strftime('%Y-%m-%d %H:%M:%S.%f %z'),
        }
        items.append(item)

    response = {'items': items}
    return response


def _build_company_types_node(company_types: list, language: str, company_languages: list) -> list:
    db = get_db()
    company_types_localizations = db.get_localization('company_types').to_dict()
    result = []
    for company_type in company_types:
        company_type_localization_map = {}
        if company_type in company_types_localizations:
            company_type_localization_map = company_types_localizations[company_type]

        result.append(
            _get_item_by_lang_or_default(company_type_localization_map, language, company_languages, company_type)
        )

    return result


def _build_buys_node(data: list, language: str, company_languages: list) -> list:
    db = get_db()
    produce_types_localizations = db.get_localization('produce_types').to_dict()
    result = []
    for item in data:
        produce_type_key = item['produce_type']
        produce_type_localization_map = {}
        if produce_type_key is not None:
            if produce_type_key in produce_types_localizations:
                produce_type_localization_map = produce_types_localizations[produce_type_key]

        temp = {
            'produce_type': _get_item_by_lang_or_default(
                produce_type_localization_map,
                language,
                company_languages,
                produce_type_key
            ),
            'description': _get_item_by_lang_or_default(item['description'], language, company_languages, ''),
            'max_price': item['max_price'],
            'min_number_of_units': item['min_number_of_units'],
            'unit_type': item['unit_type'],
            'delivery_options': item['delivery_options'],
        }
        result.append(temp)

    return result


def _get_item_by_lang_or_default(locale_map: map, user_language: str, company_languages: list, default) -> str:
    result = None
    if user_language in locale_map:
        result = locale_map[user_language]

    if result is None:
        for company_language in company_languages:
            if company_language in locale_map:
                result = locale_map[company_language]
                break

    if result is None:
        result = default

    return result
