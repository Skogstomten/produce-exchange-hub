from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str
    scopes: list[str] = Field([])
    verified: bool = Field(False)
    email: str | None
    given_name: str | None
    family_name: str | None
    roles: list[str] = Field([])
