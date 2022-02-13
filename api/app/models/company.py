from datetime import datetime

from pydantic import BaseModel


class CompanyPublic(BaseModel):
    id: str
    name: dict[str, str]
    status: str
    created_date: datetime
    company_types: list[str]
    content_languages_iso: list[str]
    activation_date: datetime | None
