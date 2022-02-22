from pydantic import BaseModel, Field

from .user import UserInternal


class Root(BaseModel):
    current_user: str | None = Field(None)

    @classmethod
    def create(
            cls,
            user: UserInternal | None
    ) -> 'Root':
        user_email = None
        if user:
            user_email = user.email

        return cls(
            current_user=user_email
        )
    