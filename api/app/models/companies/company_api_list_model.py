from typing import List, Any, Dict
from datetime import datetime

from pydantic import BaseModel

from app.datastores.base_datastore import BaseDatastore, Localization
from app.dependencies.app_headers import AppHeaders
from app.utilities.datetime_utilities import format_datetime


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
    def create(company_id: str, data: dict, headers: AppHeaders, datastore: BaseDatastore) -> Dict:
        company_languages = data.get('content_languages_iso')
        result: Dict = {
            'id': company_id,
            'name': datastore.localize(data.get('name'), headers.language, company_languages),
            'company_types': data.get('company_types', []),
            'content_languages_iso': company_languages,
            'created_date': format_datetime(data.get('created_date'), headers.timezone),
            'status': datastore.localize_from_document(
                Localization.company_statuses,
                data.get('status'),
                headers.language,
                company_languages
            ),
        }
        return result
