from datetime import datetime
from typing import List, Dict, Optional

from pydantic import BaseModel, Field

from ...database.document_database import Document
from ...datastores.base_datastore import BaseDatastore, Localization, localize
from ...dependencies.app_headers import AppHeaders
from ...utilities.datetime_utilities import format_datetime


class CompanyOutModel(BaseModel):
    id: str = Field(...)
    name: Dict[str, str] = Field(...)
    name_localized: str = Field(None)
    description: Optional[Dict[str, str]] = Field({})
    description_localized: str = Field(None)
    status: str = Field(...)
    status_localized: str = Field(...)
    created_date: datetime = Field(...)
    activation_date: Optional[datetime] = Field(None)
    company_types: List[str] = Field(...)
    company_types_localized: Optional[List[str]] = Field(None)
    content_languages_iso: List[str] = Field(..., min_items=1)
    picture_url: Optional[str] = Field(None)

    @classmethod
    def create(
            cls,
            data: Document,
            headers: AppHeaders,
            datastore: BaseDatastore
    ):
        name = data.get(Dict[str, str], 'name')
        description = data.get(Dict, 'description', {})
        company_languages = data.get(List[str], 'content_languages_iso')
        status = data.get(str, 'status')
        company_types: List[str] = data.get(List[str], 'company_types')
        return cls(
            id=data.id,
            name=name,
            name_localized=localize(name, headers.language, company_languages),
            status=status,
            status_localized=datastore.localize_from_document(
                Localization.company_statuses,
                status,
                headers.language,
                company_languages
            ),
            created_date=format_datetime(data.get(datetime, 'created_date'), headers.timezone),
            activation_date=format_datetime(data.get(datetime, 'activation_date'), headers.timezone),
            company_types=company_types,
            company_types_localized=[
                datastore.localize_from_document(
                    Localization.company_types,
                    company_type,
                    headers.language,
                    company_languages
                )
                for company_type in company_types
            ],
            content_languages_iso=company_languages,
            picture_url=data.get(str, 'picture_url', None),
            description=description,
            description_localized=localize(description, headers.language, company_languages)
        )
