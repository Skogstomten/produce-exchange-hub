from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.datastores.base_datastore import BaseDatastore, Localization
from app.dependencies.app_headers import AppHeaders
from app.utilities.datetime_utilities import format_datetime


class CompanyBriefOutModel(BaseModel):
    id: str
    name: str
    company_types: List[str]
    content_languages_iso: List[str]
    created_date: datetime = Field(..., title='Created Date')
    status: str

    @classmethod
    def create(cls, company_id: str, data: dict, headers: AppHeaders, datastore: BaseDatastore):
        company_languages = data.get('content_languages_iso')
        return cls(
            id=company_id,
            name=datastore.localize(data.get('name'), headers.language, company_languages),
            company_types=data.get('company_types', []),
            content_languages_iso=company_languages,
            created_date=format_datetime(data.get('created_date'), headers.timezone),
            status=datastore.localize_from_document(
                Localization.company_statuses,
                data.get('status'),
                headers.language,
                company_languages
            )
        )
