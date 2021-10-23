from typing import Dict, List

from pydantic import BaseModel

from app.datastores.base_datastore import BaseDatastore, Localization


class ContactOutModel(BaseModel):
    contact_name: str
    contact_type: str
    value: str

    @staticmethod
    def create(
            data: dict,
            language: str,
            company_languages: List[str],
            datastore: BaseDatastore
    ) -> Dict:
        return {
            'contact_name': data.get('contact_name'),
            'contact_type': datastore.localize_from_document(
                Localization.contact_types,
                data.get('contact_type'),
                language,
                company_languages
            ),
            'value': data.get('value')
        }
