from pydantic import BaseModel


def get_ref(role: str):
    parts = role.split(":")
    if len(parts) > 1:
        return parts[1]
    return None


class User(BaseModel):
    """Authenticated User."""

    id: str
    password_hash: str
    email: str
    verified: bool
    firstname: str
    lastname: str
    roles: list[str]

    @classmethod
    def create(cls, doc):
        roles = []
        for role in doc.get("roles", []):
            value = role.get("role_name")
            ref = role.get("reference", None)
            if ref:
                value += f":{ref}"
            roles.append(value)
        return cls(
            id=doc.get("id"),
            password_hash=doc.get("password_hash"),
            email=doc.get("email"),
            verified=doc.get("verified"),
            firstname=doc.get("firstname"),
            lastname=doc.get("lastname"),
            roles=roles,
        )

    def is_superuser(self) -> bool:
        return any(role for role in self.roles if role == "superuser")

    def get_roles(self, role_name: str) -> list[str]:
        return [role for role in self.roles if role.split(":")[0] == role_name]

    def has_role(self, role_name: str, ref: str | None) -> bool:
        for role in self.get_roles(role_name):
            if ref:
                if ref == get_ref(role):
                    return True
            else:
                return True
        return False
