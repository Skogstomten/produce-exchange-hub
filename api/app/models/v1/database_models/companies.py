from datetime import datetime

from pydantic import BaseModel

from ....database.document_database import Document


class CompanyDatabaseModel(BaseModel):
    id: str | None
    name: dict[str, str]
    status: str
    created_date: datetime | None
    company_types: list[str]
    content_languages_iso: list[str]
    activation_date: datetime | None
    description: dict[str, str]

    @classmethod
    def create_from_doc(cls, doc: Document):
        return cls(
            id=doc.id,
            **doc.to_dict()
        )
