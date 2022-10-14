from pydantic import BaseModel


class Country(BaseModel):
    id: str
    ISO_code: str
    name: str
