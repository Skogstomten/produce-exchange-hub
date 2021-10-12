import pytz


class Company(object):
    def __init__(self, company_id: str, data: map):
        self._data = data
        self._id = company_id
        self._company_languages = data['content_languages_iso']
        from app.db import get_db
        self._db = get_db()

    def to_partial_json_response(self, user_language: str) -> map:
        timezone = pytz.timezone('Europe/Stockholm')
        created_date = self._data['created_date'].astimezone(timezone)
        return {
            'id': self._id,
            'content_language_iso': self._data['content_languages_iso'],
            'company_types': self._build_company_types_node(
                self._data['company_types'],
                user_language,
            ),
            'created_date': created_date.strftime('%Y-%m-%d %H:%M:%S.%f %z'),
            'name': self._get_item_by_lang_or_default(self._data['name'], user_language, ''),
            'status': self._build_status_node(self._data['status'], user_language),
        }

    def to_full_json_response(self, user_language: str) -> map:
        result = self.to_partial_json_response(user_language)
        result.update({
            'buys': self._build_buys_node(self._data['buys'], user_language)
        })
        return result

    def _build_status_node(self, status: str, language: str) -> str:
        statuses_localizations = self._db.get_localization('company_statuses').to_dict()
        if statuses_localizations is None:
            return status

        result = status
        if status in statuses_localizations:
            status_localizations = statuses_localizations[status]
            result = self._get_item_by_lang_or_default(status_localizations, language, status)

        return result

    def _build_company_types_node(self, company_types: list, language: str) -> list:
        company_types_localizations = self._db.get_localization('company_types').to_dict()
        result = []
        for company_type in company_types:
            company_type_localization_map = {}
            if company_type in company_types_localizations:
                company_type_localization_map = company_types_localizations[company_type]

            result.append(
                self._get_item_by_lang_or_default(company_type_localization_map,
                                                  language,
                                                  company_type)
            )

        return result

    def _build_buys_node(self, data: list, language: str) -> list:
        produce_types_localizations = self._db.get_localization('produce_types').to_dict()
        result = []
        for item in data:
            produce_type_key = item['produce_type']
            produce_type_localization_map = {}
            if produce_type_key is not None:
                if produce_type_key in produce_types_localizations:
                    produce_type_localization_map = produce_types_localizations[produce_type_key]

            temp = {
                'produce_type': self._get_item_by_lang_or_default(
                    produce_type_localization_map,
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

    def _get_item_by_lang_or_default(self, locale_map: map, user_language: str, default) -> str:
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
