"""Token and TokenData."""
from pydantic import BaseModel, Field


class Token(BaseModel):
    """Model for oauth2 token."""

    access_token: str
    token_type: str


class TokenRoleMap:
    """Map like role collection"""

    def __init__(self, roles: list[str]):
        self._roles = roles
        self._map = {}

        for role in roles:
            parts = role.split(":")
            role_name = parts[0]
            ref = parts[1] if len(parts) > 1 else None
            if role_name in self._map:
                self._map[role_name].append(ref)
            else:
                self._map[role_name] = [ref]

    def __getitem__(self, key) -> list[str]:
        return self._map.get(key, None)


class TokenData(BaseModel):
    """Model for data in deserialized token."""

    sub: str
    scopes: list[str] = Field([])
    verified: bool = Field(False)
    email: str | None
    given_name: str | None
    family_name: str | None
    roles: list[str] = Field([])

    def get_token_role_map(self) -> TokenRoleMap:
        """Get roles as a dict like map object."""
        return TokenRoleMap(self.roles)

    def has_superuser_role(self) -> bool:
        return any((role for role in self.roles if role == "superuser"))
