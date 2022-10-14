from pydantic import BaseModel


class Language(BaseModel):
    id: str
    ISO_code: str
    name: str
