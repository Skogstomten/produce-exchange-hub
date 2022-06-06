from pydantic import BaseModel

from app.database.document_database import Document


class RoleDatabaseModel(BaseModel):
    id: str
    name: str
    type: str
    description: str | None

    @classmethod
    def from_doc(cls, doc: Document):
        cls(
            id=doc.id,
            **doc.to_dict()
        )
