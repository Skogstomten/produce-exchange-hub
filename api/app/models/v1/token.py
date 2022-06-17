"""Token and TokenData."""
from pydantic import BaseModel, Field


class Token(BaseModel):
    """Model for oauth2 token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Model for data in deserialized token."""

    sub: str
    scopes: list[str] = Field([])
    verified: bool = Field(False)
    email: str | None
    given_name: str | None
    family_name: str | None
    roles: list[str] = Field([])
