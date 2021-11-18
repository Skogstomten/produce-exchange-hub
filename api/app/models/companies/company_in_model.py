from datetime import datetime
from typing import List, Dict

import pytz
from pydantic import BaseModel, Field

from .company_status import CompanyStatus


class CompanyInModel(BaseModel):
    name: Dict[str, str] = Field(...)
    company_types: List[str] = Field(...)
    content_languages_iso: List[str] = Field(..., min_items=1)

    def to_database_dict(self, status: CompanyStatus) -> dict:
        result = {
            'name': self.name,
            'status': status,
            'created_date': datetime.now(pytz.utc),
            'company_types': self.company_types,
            'content_languages_iso': [language_iso.upper() for language_iso in self.content_languages_iso],
        }
        return result
