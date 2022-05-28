from pydantic import BaseModel

from ....database.document_database import Document


class ClaimDatabaseModel(BaseModel):
    claim_type: str

    @classmethod
    def from_doc(cls, doc: Document):
        return cls(
            id=doc.id,
            **doc.to_dict(),
        )
