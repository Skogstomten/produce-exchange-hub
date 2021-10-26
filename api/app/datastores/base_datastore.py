from enum import Enum
from typing import List, Dict

from google.cloud.firestore_v1.client import Client

from app.errors.not_found_error import NotFoundError


class Localization(Enum):
    company_statuses = 'company_statuses'
    address_types = 'address_types'
    countries_iso_name = 'countries_iso_name'
    contact_types = 'contact_types'
    produce_types = 'produce_types'
    unit_types = 'unit_types'
    period_types = 'period_types'
    delivery_options = 'delivery_options'


class BaseDatastore(object):
    db: Client

    def __init__(self, db: Client):
        self.db = db

    @staticmethod
    def localize(
            data: dict[str, str],
            language: str,
            company_languages: List[str],
            default: str | Dict = None
    ) -> str | Dict[str, str]:
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

        snapshot = self.db.collection('localization').document(localization.value).get()
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

    def get_user_ref(self, user_id: str):
        user_ref = self.db.collection('users').document(user_id)
        if not user_ref.get().exists:
            raise NotFoundError(f"User with id '{user_id}' is not found")

        return user_ref
