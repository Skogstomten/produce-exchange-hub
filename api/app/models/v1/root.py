from pydantic import BaseModel, Field

from app.models.v1.database_models.user_database_model import UserDatabaseModel


class Root(BaseModel):
    current_user: str | None = Field(None)

    @classmethod
    def create(
            cls,
            user: UserDatabaseModel | None
    ) -> 'Root':
        user_email = None
        if user:
            user_email = user.email

        return cls(
            current_user=user_email
        )
    