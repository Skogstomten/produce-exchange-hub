from datetime import datetime
from typing import List, Dict
from uuid import uuid4

import pytz
from pydantic import BaseModel, Field

from .company_status import CompanyStatus
from ...utilities.datetime_utilities import format_datetime


class CompanyInModel(BaseModel):
    name: Dict[str, str] = Field(...)
    company_types: List[str] = Field(...)
    content_languages_iso: List[str] = Field(..., min_items=1)

    def to_database_dict(self, status: CompanyStatus) -> dict:
        result = {
            'id': str(uuid4()),
            'name': self.name,
            'status': status.value,
            'created_date': format_datetime(datetime.now(pytz.utc), 'utc'),
            'company_types': self.company_types,
            'content_languages_iso': [language_iso.upper() for language_iso in self.content_languages_iso],
        }
        return result
