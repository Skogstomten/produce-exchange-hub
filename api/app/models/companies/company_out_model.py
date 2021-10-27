from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel, Field

from app.datastores.base_datastore import BaseDatastore, Localization
from app.dependencies.app_headers import AppHeaders
from app.utilities.datetime_utilities import format_datetime


class CompanyOutModel(BaseModel):
    id: str = Field(...)
    name: Dict[str, str] = Field(...)
    name_localized: str = Field(None)
    status: str = Field(...)
    status_localized: str = Field(...)
    created_date: datetime = Field(...)
    company_types: List[str] = Field(...)
    content_languages_iso: List[str] = Field(..., min_items=1)

    @classmethod
    def create(
            cls,
            company_id: str,
            data: Dict[str, str | Dict[str, str] | datetime | List[str]],
            headers: AppHeaders,
            datastore: BaseDatastore
    ):
        name = data.get('name')
        company_languages = data.get('content_languages_iso')
        status = data.get('status')
        return cls(
            id=company_id,
            name=name,
            name_localized=datastore.localize(name, headers.language, company_languages),
            status=status,
            status_localized=datastore.localize_from_document(
                Localization.company_statuses,
                status,
                headers.language,
                company_languages
            ),
            created_date=format_datetime(data.get('created_date'), headers.timezone),
            company_types=data.get('company_types'),
            content_languages_iso=company_languages
        )
