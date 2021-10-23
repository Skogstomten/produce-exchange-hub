from enum import Enum
from typing import List

from google.cloud.firestore_v1.client import Client


class Localization(Enum):
    company_statuses = 'company_statuses'
    address_types = 'address_types'
    countries_iso_name = 'countries_iso_name'
    contact_types = 'contact_types'
    produce_types = 'produce_types'
    unit_types = 'unit_types'
    period_types = 'period_types'


class BaseDatastore(object):
    db: Client

    def __init__(self, db: Client):
        self.db = db

    @staticmethod
    def localize(
            data: dict[str, str],
            language: str,
            company_languages: List[str],
            default: str = None
    ) -> str:
        if data is None:
            return default

        if language in data:
            return data.get(language)

        for language in company_languages:
            if language in data:
                return data.get(language)

        return default

    def localize_from_document(
            self,
            localization: Localization,
            key: str,
            language: str,
            company_languages: List[str]
    ) -> str | None:
        if key is None:
            return None

        snapshot = self.db.collection('localization').document(str(localization)).get()
        if snapshot.exists:
            data = snapshot.to_dict()
            if key in data:
                localizations = data.get(key)
                if language in localizations:
                    return localizations.get(language)

                for language in company_languages:
                    if language in localizations:
                        return localizations.get(language)

        return key
