from typing import Dict, List

from pydantic import BaseModel

from app.datastores.base_datastore import BaseDatastore, Localization
from app.dependencies.app_headers import AppHeaders


class ContactOutModel(BaseModel):
    contact_name: str
    contact_type: str
    value: str

    @classmethod
    def create(cls, data: Dict, headers: AppHeaders, company_languages: List[str], datastore: BaseDatastore):
        return cls(
            contact_name=data.get('contact_name'),
            contact_type=datastore.localize_from_document(
                Localization.contact_types,
                data.get('contact_type'),
                headers.language,
                company_languages
            ),
            value=data.get('value')
        )
