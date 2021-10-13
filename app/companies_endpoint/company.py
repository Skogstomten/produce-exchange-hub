from typing import Any

from flask import url_for

from app.datetime_helpers import format_date


class Company(object):
    def __init__(self, company_id: str, data: dict[str, str | list | Any]):
        self._data = data
        self._id = company_id
        self._company_languages = data['content_languages_iso']
        from app.db import get_db
        self._db = get_db()

    def to_partial_json_response(self, user_language: str) -> dict[str, str | list | Any]:
        return {
            'id': self._id,
            'content_languages_iso': self._data['content_languages_iso'],
            'company_types': self._build_company_types_node(
                self._data['company_types'],
                user_language,
            ),
            'created_date': format_date(
                self._data.get('created_date'),
                'Europe/Stockholm'
            ),
            'name': self._get_item_by_lang_or_default(self._data['name'], user_language, ''),
            'status': self._build_status_node(self._data['status'], user_language),
        }

    def to_full_json_response(self, user_language: str) -> dict[str, str | list | Any]:
        result = self.to_partial_json_response(user_language)
        result.update({
            'buys': self._build_buys_node(self._data['buys'], user_language),
            'addresses': self._data['addresses'],
            'contacts': self._data['contacts'],
            'produces': self._build_produces_node(self._data['produces'], user_language),
            'news_feed': url_for('company_news_feed.news_feed', company_id=self._id),
            'notifications': url_for('company_notifications.list_notifications', company_id=self._id)
        })
        return result

    def _build_produces_node(self, data: list[dict], user_language: str):
        period_types_localizations = self._db.get_localization('period_types')
        produce_types_localizations = self._db.get_localization('produce_types')
        unit_types_localizations = self._db.get_localization('unit_types')
        result = []
        for item in data:
            temp_item = {
                'delivery_options': self._build_delivery_options_node(item['delivery_options'], user_language),
                'description': self._get_item_by_lang_or_default(
                    item['description'],
                    user_language,
                    default=''
                ),
                'period_type': self._get_item_by_lang_or_default(
                    period_types_localizations.get(item['period_type'], {}),
                    user_language,
                    default=item['period_type']
                ),
                'price_per_unit': item['price_per_unit'],
                'produce_type': self._get_item_by_lang_or_default(
                    produce_types_localizations.get(item['produce_type'], {}),
                    user_language,
                    default=item['produce_type']
                ),
                'unit_type': self._get_item_by_lang_or_default(
                    unit_types_localizations.get(item['unit_type'], {}),
                    user_language,
                    default=item['unit_type']
                ),
                'units_per_period': item['units_per_period'],
            }
            result.append(temp_item)
        return result

    def _build_delivery_options_node(self, data: list[dict], user_language: str):
        delivery_options_localizations = self._db.get_localization('delivery_options')
        result = []
        for item in data:
            temp_item = {
                'delivery_option': self._get_item_by_lang_or_default(
                    delivery_options_localizations.get(item['delivery_option'], {}),
                    user_language,
                    item['delivery_option']
                ),
                'specifications': item['specifications'],
            }
            result.append(temp_item)
        return result

    def _build_status_node(self, status: str, language: str) -> str:
        statuses_localizations = self._db.get_localization('company_statuses')
        if statuses_localizations is None:
            return status

        result = status
        if status in statuses_localizations:
            result = self._get_item_by_lang_or_default(statuses_localizations.get(status, {}), language, status)

        return result

    def _build_company_types_node(self, company_types: list, language: str) -> list:
        company_types_localizations = self._db.get_localization('company_types')
        result = []
        for company_type in company_types:
            result.append(
                self._get_item_by_lang_or_default(company_types_localizations.get(company_type, {}),
                                                  language,
                                                  company_type)
            )

        return result

    def _build_buys_node(self, data: list, language: str) -> list:
        produce_types_localizations = self._db.get_localization('produce_types')
        result = []
        for item in data:
            produce_type_key = item['produce_type']
            temp = {
                'produce_type': self._get_item_by_lang_or_default(
                    produce_types_localizations.get(produce_type_key, {}),
                    language,
                    produce_type_key
                ),
                'description': self._get_item_by_lang_or_default(item['description'], language, ''),
                'max_price': item['max_price'],
                'min_number_of_units': item['min_number_of_units'],
                'unit_type': item['unit_type'],
                'delivery_options': item['delivery_options'],
            }
            result.append(temp)

        return result

    def _get_item_by_lang_or_default(self, locale_map: dict[str, str], user_language: str, default) -> str:
        if locale_map is None:
            return default

        result = None
        if user_language in locale_map:
            result = locale_map[user_language]

        if result is None:
            for company_language in self._company_languages:
                if company_language in locale_map:
                    result = locale_map[company_language]
                    break

        if result is None:
            result = default

        return result
