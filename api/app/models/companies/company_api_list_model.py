from typing import List, Any, Dict
from datetime import datetime

from pydantic import BaseModel

from app.datastores.base_datastore import BaseDatastore, Localization


class CompanyApiListModel(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)

    id: str
    name: str
    company_types: List[str]
    content_languages_iso: List[str]
    created_date: datetime
    status: str

    @staticmethod
    def create(company_id: str, data: dict, language_iso: str, datastore: BaseDatastore) -> Dict:
        company_languages = data.get('content_languages_iso')
        result: Dict = {
            'id': company_id,
            'name': datastore.localize(data.get('name'), language_iso, company_languages),
            'company_types': data.get('company_types', []),
            'content_languages_iso': company_languages,
            'created_date': data.get('created_date'),
            'status': datastore.localize_from_document(
                Localization.company_statuses,
                data.get('status'),
                language_iso,
                company_languages
            ),
        }
        return result
